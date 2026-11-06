import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app.settlement import routes


class DailySettlementIntentIdempotencyTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "settlement_test.db"

        with sqlite3.connect(self.db_path) as con:
            con.executescript("""
                CREATE TABLE daily_settlement_intents (
                    settlement_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    status TEXT NOT NULL,
                    trigger_reason TEXT NOT NULL,
                    operation_id TEXT NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    UNIQUE(user_id, operational_date)
                );

                CREATE TABLE daily_settlement_choices (
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    PRIMARY KEY(user_id, operational_date)
                );
            """)

        def connect_test_db():
            con = sqlite3.connect(self.db_path, timeout=5)
            con.row_factory = sqlite3.Row
            return con

        self.connect_patch = patch.object(
            routes, "connect_db", side_effect=connect_test_db
        )
        self.connect_patch.start()
        self.addCleanup(self.connect_patch.stop)

        self.user = SimpleNamespace(id="test-user-001")
        self.fixed_now = datetime(
            2026, 10, 24, 12, 0, tzinfo=timezone.utc
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_repeated_request_reuses_intent_without_reprocessing_points(self):
        point_result = SimpleNamespace(
            daily_points=Decimal("5"),
            carry_in_points=Decimal("1"),
            drika_amount=Decimal("1"),
            remainder_points=Decimal("2"),
        )

        with (
            patch.object(routes, "utc_now", return_value=self.fixed_now),
            patch.object(
                routes,
                "validated_daily_points",
                return_value=Decimal("5"),
            ),
            patch.object(
                routes.PointRemainderStore,
                "process_day",
                return_value=point_result,
            ) as process_day,
        ):
            first = routes.create_previous_day_intent(user=self.user)
            second = routes.create_previous_day_intent(user=self.user)

        self.assertEqual(first["status"], "created")
        self.assertEqual(second["status"], "existing")
        self.assertEqual(
            first["settlement"]["settlement_id"],
            second["settlement"]["settlement_id"],
        )
        self.assertEqual(process_day.call_count, 1)

        with sqlite3.connect(self.db_path) as con:
            count = con.execute(
                "SELECT COUNT(*) FROM daily_settlement_intents"
            ).fetchone()[0]

        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
