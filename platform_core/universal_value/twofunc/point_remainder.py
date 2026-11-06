"""Atomic daily POINT carry-over and Drika calculation."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import sqlite3
from decimal import Decimal

from db.database import engine


POINTS_PER_DRIKA = Decimal("4")


@dataclass(frozen=True)
class DailyPointResult:
    user_id: str
    operational_date: date
    daily_points: Decimal
    carry_in_points: Decimal
    drika_amount: Decimal
    remainder_points: Decimal


class PointRemainderStore:
    """Persist daily POINT remainder and idempotent daily results in 2fun.db."""

    def initialize(self) -> None:
        with engine.begin() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_point_remainders (
                    user_id TEXT NOT NULL,
                    operational_date TEXT NOT NULL,
                    remainder_points TEXT NOT NULL,
                    updated_at_utc TEXT NOT NULL,
                    PRIMARY KEY (user_id, operational_date),
                    CHECK (
                        CAST(remainder_points AS NUMERIC) >= 0
                        AND CAST(remainder_points AS NUMERIC) < 4
                    )
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_point_settlements (
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
                )
                """
            )

    def process_day(
        self,
        *,
        user_id: str,
        operational_date: date,
        daily_points: Decimal,
        connection=None,
    ) -> DailyPointResult:
        """Process fresh daily POINT once; never add carry-over to lifetime score."""
        if not user_id:
            raise ValueError("user_id must not be empty")

        daily_points = Decimal(daily_points)
        if not daily_points.is_finite() or daily_points < 0:
            raise ValueError("daily_points must be a finite non-negative Decimal")

        current_date = operational_date.isoformat()
        previous_date = (operational_date - timedelta(days=1)).isoformat()

        owns_connection = connection is None
        if owns_connection:
            connection = sqlite3.connect(str(engine.url.database), timeout=30)
            connection.execute("PRAGMA busy_timeout = 30000")

        try:
            if owns_connection:
                connection.execute("BEGIN IMMEDIATE")

            # A supplied connection is managed by the caller's transaction.
            existing = connection.execute(
                """
                SELECT daily_points, carry_in_points, drika_amount,
                       remainder_points
                FROM daily_point_settlements
                WHERE user_id = ? AND operational_date = ?
                """,
                (user_id, current_date),
            ).fetchone()

            if existing:
                if Decimal(existing[0]) != daily_points:
                    raise ValueError(
                        "day already processed with different daily_points"
                    )

                result = DailyPointResult(
                    user_id=user_id,
                    operational_date=operational_date,
                    daily_points=Decimal(existing[0]),
                    carry_in_points=Decimal(existing[1]),
                    drika_amount=Decimal(existing[2]),
                    remainder_points=Decimal(existing[3]),
                )

                if owns_connection:
                    connection.commit()

                return result

            previous = connection.execute(
                """
                SELECT remainder_points
                FROM daily_point_remainders
                WHERE user_id = ? AND operational_date < ?
                ORDER BY operational_date DESC
                LIMIT 1
                """,
                (user_id, current_date),
            ).fetchone()

            carry_in = Decimal(previous[0]) if previous else Decimal("0")
            combined = daily_points + carry_in
            drika_amount = combined // POINTS_PER_DRIKA
            remainder = combined - drika_amount * POINTS_PER_DRIKA
            timestamp = datetime.now(timezone.utc).isoformat()

            connection.execute(
                """
                INSERT INTO daily_point_settlements (
                    user_id, operational_date, daily_points,
                    carry_in_points, drika_amount, remainder_points,
                    created_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    current_date,
                    str(daily_points),
                    str(carry_in),
                    str(drika_amount),
                    str(remainder),
                    timestamp,
                ),
            )

            connection.execute(
                """
                INSERT INTO daily_point_remainders (
                    user_id, operational_date, remainder_points,
                    updated_at_utc
                ) VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, operational_date) DO UPDATE SET
                    remainder_points = excluded.remainder_points,
                    updated_at_utc = excluded.updated_at_utc
                """,
                (user_id, current_date, str(remainder), timestamp),
            )

            if owns_connection:
                connection.commit()

            return DailyPointResult(
                user_id=user_id,
                operational_date=operational_date,
                daily_points=daily_points,
                carry_in_points=carry_in,
                drika_amount=drika_amount,
                remainder_points=remainder,
            )
        except Exception:
            if owns_connection:
                connection.rollback()
            raise
        finally:
            if owns_connection:
                connection.close()
