import sqlite3
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from platform_core.universal_value.ledger.value_ledger import ValueLedger


class ValueLedgerTransferTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "uvi_transfer_test.sqlite3"

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

                CREATE TABLE uvi_transfer_operations (
                    operation_id TEXT PRIMARY KEY,
                    source_user_id TEXT NOT NULL,
                    destination_user_id TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    debit_transaction_id TEXT NOT NULL UNIQUE,
                    credit_transaction_id TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                );
            """)

        self.ledger = ValueLedger(db_path=self.db_path)
        self.ledger.record(
            transaction_id="seed-001",
            event_id="seed-event-001",
            user_id="ALICE",
            amount=Decimal("10"),
            currency="Drika",
            transaction_type="CREDIT",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_transfer_is_atomic_and_balances_are_correct(self):
        result = self.ledger.execute_transfer(
            operation_id="transfer-001",
            source_user_id="ALICE",
            destination_user_id="BOB",
            amount=Decimal("3"),
            currency="Drika",
        )

        self.assertFalse(result["replayed"])
        self.assertEqual(self.ledger.balance("ALICE", "Drika"), Decimal("7"))
        self.assertEqual(self.ledger.balance("BOB", "Drika"), Decimal("3"))

        with sqlite3.connect(self.db_path) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM uvi_ledger_entries"
            ).fetchone()[0]
        self.assertEqual(count, 3)

    def test_replay_after_restart_does_not_duplicate_transfer(self):
        first = self.ledger.execute_transfer(
            operation_id="transfer-restart-001",
            source_user_id="ALICE",
            destination_user_id="BOB",
            amount=Decimal("3"),
            currency="Drika",
        )

        restarted_ledger = ValueLedger(db_path=self.db_path)
        second = restarted_ledger.execute_transfer(
            operation_id="transfer-restart-001",
            source_user_id="ALICE",
            destination_user_id="BOB",
            amount=Decimal("3"),
            currency="Drika",
        )

        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(
            first["debit_transaction_id"], second["debit_transaction_id"]
        )
        self.assertEqual(
            first["credit_transaction_id"], second["credit_transaction_id"]
        )
        self.assertEqual(
            restarted_ledger.balance("ALICE", "Drika"), Decimal("7")
        )
        self.assertEqual(
            restarted_ledger.balance("BOB", "Drika"), Decimal("3")
        )

        with sqlite3.connect(self.db_path) as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM uvi_ledger_entries"
            ).fetchone()[0]
        self.assertEqual(count, 3)

    def test_reusing_operation_id_with_different_details_is_rejected(self):
        self.ledger.execute_transfer(
            operation_id="transfer-conflict-001",
            source_user_id="ALICE",
            destination_user_id="BOB",
            amount=Decimal("3"),
            currency="Drika",
        )

        with self.assertRaisesRegex(ValueError, "different transfer details"):
            self.ledger.execute_transfer(
                operation_id="transfer-conflict-001",
                source_user_id="ALICE",
                destination_user_id="BOB",
                amount=Decimal("4"),
                currency="Drika",
            )

        self.assertEqual(self.ledger.balance("ALICE", "Drika"), Decimal("7"))
        self.assertEqual(self.ledger.balance("BOB", "Drika"), Decimal("3"))


if __name__ == "__main__":
    unittest.main()
