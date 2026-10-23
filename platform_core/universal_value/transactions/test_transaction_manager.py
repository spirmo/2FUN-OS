import sqlite3
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from platform_core.universal_value.core.contracts import ValueEvent
from platform_core.universal_value.ledger.value_ledger import ValueLedger
from platform_core.universal_value.transactions.transaction_manager import (
    TransactionManager,
)


class TransactionManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "uvi_transactions_test.sqlite3"

        with sqlite3.connect(self.db_path) as connection:
            connection.executescript("""
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

                CREATE INDEX ix_uvi_ledger_event_id
                ON uvi_ledger_entries (event_id);
            """)

        self.ledger = ValueLedger(db_path=self.db_path)
        self.manager = TransactionManager(self.ledger)

    def tearDown(self):
        self.temp_dir.cleanup()

    @staticmethod
    def make_event(event_id, user_id="USER-1", currency="Drika"):
        return ValueEvent(
            event_id=event_id,
            user_id=user_id,
            source="test",
            action="test_action",
            base_value=Decimal("1"),
            currency=currency,
        )

    def ledger_count(self):
        with sqlite3.connect(self.db_path) as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM uvi_ledger_entries"
            ).fetchone()[0]

    def test_batch_creates_and_persists_all_transactions(self):
        transactions = self.manager.create_transactions_batch([
            {
                "event": self.make_event("event-001"),
                "amount": "2.5",
            },
            {
                "event": self.make_event("event-002", "USER-2"),
                "amount": "4",
                "transaction_type": "REWARD",
                "metadata": {"source": "test"},
            },
        ])

        self.assertEqual(len(transactions), 2)
        self.assertEqual(self.ledger_count(), 2)
        self.assertEqual(transactions[0].amount, Decimal("2.5"))
        self.assertEqual(transactions[1].amount, Decimal("4"))
        self.assertEqual(transactions[1].metadata, {"source": "test"})

    def test_invalid_amount_rejects_batch_before_any_write(self):
        with self.assertRaises(ValueError):
            self.manager.create_transactions_batch([
                {
                    "event": self.make_event("event-valid"),
                    "amount": "2",
                },
                {
                    "event": self.make_event("event-invalid"),
                    "amount": "NaN",
                },
            ])

        self.assertEqual(self.ledger_count(), 0)

    def test_sqlite_failure_rolls_back_entire_batch(self):
        self.assertEqual(self.ledger_count(), 0)

        with self.assertRaisesRegex(ValueError, "Batch rejected"):
            self.manager.create_transactions_batch([
                {
                    "event": self.make_event("event-first"),
                    "amount": "2",
                },
                {
                    "event": self.make_event(
                        "event-second",
                        user_id="USER-2",
                        currency=None,
                    ),
                    "amount": "3",
                },
            ])

        self.assertEqual(self.ledger_count(), 0)


if __name__ == "__main__":
    unittest.main()
