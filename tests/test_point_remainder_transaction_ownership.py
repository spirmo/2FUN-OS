import sqlite3
import unittest
from datetime import date
from decimal import Decimal

from platform_core.universal_value.twofunc.point_remainder import (
    PointRemainderStore,
)


class PointRemainderTransactionOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.executescript("""
            CREATE TABLE daily_point_remainders (
                user_id TEXT NOT NULL,
                operational_date TEXT NOT NULL,
                remainder_points TEXT NOT NULL,
                updated_at_utc TEXT NOT NULL,
                PRIMARY KEY (user_id, operational_date)
            );

            CREATE TABLE daily_point_settlements (
                user_id TEXT NOT NULL,
                operational_date TEXT NOT NULL,
                daily_points TEXT NOT NULL,
                carry_in_points TEXT NOT NULL,
                drika_amount TEXT NOT NULL,
                remainder_points TEXT NOT NULL,
                created_at_utc TEXT NOT NULL,
                PRIMARY KEY (user_id, operational_date)
            );
        """)
        self.store = PointRemainderStore()
        self.day = date(2026, 11, 5)

    def tearDown(self):
        self.connection.close()

    def test_new_day_keeps_caller_transaction_open_and_rollbackable(self):
        self.connection.execute("BEGIN")
        result = self.store.process_day(
            user_id="user-1",
            operational_date=self.day,
            daily_points=Decimal("5"),
            connection=self.connection,
        )

        self.assertEqual(result.drika_amount, Decimal("1"))
        self.assertEqual(result.remainder_points, Decimal("1"))
        self.assertTrue(self.connection.in_transaction)

        count_before_rollback = self.connection.execute(
            "SELECT COUNT(*) FROM daily_point_settlements"
        ).fetchone()[0]
        self.assertEqual(count_before_rollback, 1)

        self.connection.rollback()
        count_after_rollback = self.connection.execute(
            "SELECT COUNT(*) FROM daily_point_settlements"
        ).fetchone()[0]
        self.assertEqual(count_after_rollback, 0)

    def test_existing_day_keeps_caller_transaction_open(self):
        self.connection.execute("""
            INSERT INTO daily_point_settlements VALUES
            ('user-1', '2026-11-05', '5', '1', '1', '2', 'test')
        """)
        self.connection.commit()
        self.connection.execute("BEGIN")

        result = self.store.process_day(
            user_id="user-1",
            operational_date=self.day,
            daily_points=Decimal("5"),
            connection=self.connection,
        )

        self.assertEqual(result.daily_points, Decimal("5"))
        self.assertEqual(result.carry_in_points, Decimal("1"))
        self.assertEqual(result.drika_amount, Decimal("1"))
        self.assertEqual(result.remainder_points, Decimal("2"))
        self.assertTrue(self.connection.in_transaction)


if __name__ == "__main__":
    unittest.main()
