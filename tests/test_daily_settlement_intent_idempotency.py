import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.settlement import routes
from financial_core.settlement.daily_service import DailySettlementService
from platform_core.universal_value.ledger.value_ledger import ValueLedger


class DailySettlementIntentIdempotencyTests(unittest.TestCase):
    def test_route_delegates_intent_creation_to_finance_service(self):
        user = SimpleNamespace(id="test-user-001")
        fixed_now = datetime(2026, 10, 24, 12, 0, tzinfo=timezone.utc)

        expected = {
            "status": "created",
            "settlement": {
                "user_id": "test-user-001",
                "operational_date": "2026-10-23",
                "status": "PENDING",
            },
        }
        service = SimpleNamespace(
            create_previous_day_intent=Mock(return_value=expected)
        )

        with patch.object(routes, "utc_now", return_value=fixed_now):
            result = routes.create_previous_day_intent(
                user=user,
                service=service,
            )

        self.assertEqual(result, expected)
        service.create_previous_day_intent.assert_called_once_with(
            user_id="test-user-001",
            now=fixed_now,
        )

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "api_test.db")
        self.user = SimpleNamespace(id="test-user-001")
        self.fixed_now = datetime(
            2026, 11, 7, 12, 0, tzinfo=timezone.utc
        )

        self._create_schema()

        self.ledger = ValueLedger(db_path=self.db_path)
        self.service = DailySettlementService(
            self._connect,
            self.ledger,
        )

        self.original_overrides = app.dependency_overrides.copy()
        app.dependency_overrides[routes.get_current_user] = (
            lambda: self.user
        )
        app.dependency_overrides[
            routes.get_daily_settlement_service
        ] = lambda: self.service

        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.original_overrides)
        self.temp_dir.cleanup()

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=30)

    def _create_schema(self):
        with closing(sqlite3.connect(self.db_path)) as con, con:
            con.executescript("""
                CREATE TABLE uvi_ledger_entries (
                    transaction_id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata_json TEXT NOT NULL DEFAULT '{}'
                );

                CREATE TABLE daily_settlement_choices (
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    selected_at_utc TEXT NOT NULL,
                    PRIMARY KEY (user_id, operational_date)
                );

                CREATE TABLE daily_settlement_intents (
                    settlement_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    status TEXT NOT NULL,
                    trigger_reason TEXT NOT NULL,
                    operation_id TEXT NOT NULL UNIQUE,
                    created_at_utc TEXT NOT NULL,
                    finalized_at_utc TEXT,
                    source_amount TEXT,
                    source_unit TEXT,
                    destination_amount TEXT,
                    reference_price TEXT,
                    current_price TEXT,
                    uvi_transaction_id TEXT,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    UNIQUE (user_id, operational_date)
                );

                CREATE TABLE daily_point_remainders (
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    remainder_points TEXT NOT NULL,
                    updated_at_utc TEXT NOT NULL,
                    PRIMARY KEY (user_id, operational_date),
                    CHECK (
                        CAST(remainder_points AS NUMERIC) >= 0
                        AND CAST(remainder_points AS NUMERIC) < 4
                    )
                );

                CREATE TABLE daily_point_settlements (
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    daily_points TEXT NOT NULL,
                    carry_in_points TEXT NOT NULL,
                    drika_amount TEXT NOT NULL,
                    remainder_points TEXT NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    PRIMARY KEY (user_id, operational_date),
                    CHECK (CAST(daily_points AS NUMERIC) >= 0),
                    CHECK (
                        CAST(carry_in_points AS NUMERIC) >= 0
                        AND CAST(carry_in_points AS NUMERIC) < 4
                    ),
                    CHECK (CAST(drika_amount AS NUMERIC) >= 0),
                    CHECK (
                        CAST(remainder_points AS NUMERIC) >= 0
                        AND CAST(remainder_points AS NUMERIC) < 4
                    )
                );
            """)

            metadata = {
                "value_flow": "POINT_TO_2FUNC",
                "activity_validated": True,
                "fraud_invalidated": False,
            }
            con.execute("""
                INSERT INTO uvi_ledger_entries (
                    transaction_id, event_id, user_id, amount,
                    currency, transaction_type, timestamp, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "test-point-transaction",
                "test-point-event",
                "test-user-001",
                "5.5",
                "POINT",
                "EARN",
                "2026-11-06T12:00:00+00:00",
                json.dumps(metadata),
            ))

    def test_http_repeated_request_uses_finance_and_creates_one_intent(self):
        with patch.object(
            routes, "utc_now", return_value=self.fixed_now
        ):
            first = self.client.post("/settlement/daily/intent")
            second = self.client.post("/settlement/daily/intent")

        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 200, second.text)

        first_data = first.json()
        second_data = second.json()

        self.assertEqual(first_data["status"], "created")
        self.assertEqual(second_data["status"], "existing")
        self.assertEqual(
            first_data["settlement"]["settlement_id"],
            second_data["settlement"]["settlement_id"],
        )

        metadata = json.loads(
            first_data["settlement"]["metadata_json"]
        )
        self.assertEqual(metadata["daily_points"], "5.5")
        self.assertEqual(metadata["drika_amount"], "1")
        self.assertEqual(metadata["remainder_points"], "1.5")

        with closing(sqlite3.connect(self.db_path)) as con, con:
            intent_count = con.execute(
                "SELECT COUNT(*) FROM daily_settlement_intents"
            ).fetchone()[0]
            settlement_count = con.execute(
                "SELECT COUNT(*) FROM daily_point_settlements"
            ).fetchone()[0]
            remainder_count = con.execute(
                "SELECT COUNT(*) FROM daily_point_remainders"
            ).fetchone()[0]

        self.assertEqual(intent_count, 1)
        self.assertEqual(settlement_count, 1)
        self.assertEqual(remainder_count, 1)


if __name__ == "__main__":
    unittest.main()
