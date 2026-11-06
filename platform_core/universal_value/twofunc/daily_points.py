"""Read validated daily POINT earnings from the central UVI ledger."""
import json
import sqlite3
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from db.database import DB_PATH


def validated_daily_points(
    user_id: str,
    operational_date: date,
    db_path: str | Path | None = None,
    connection=None,
) -> Decimal:
    """Return validated POINT earnings for one UTC day; fail closed."""
    if not user_id:
        raise ValueError("user_id is required")

    path = str(Path(db_path) if db_path is not None else DB_PATH)
    start = datetime.combine(
        operational_date, time.min, tzinfo=timezone.utc
    ).isoformat()
    end = datetime.combine(
        operational_date + timedelta(days=1), time.min, tzinfo=timezone.utc
    ).isoformat()

    if connection is not None:
        rows = connection.execute(
            """
            SELECT transaction_id, amount, metadata_json
            FROM uvi_ledger_entries
            WHERE user_id = ?
              AND currency = 'POINT'
              AND transaction_type = 'EARN'
              AND timestamp >= ?
              AND timestamp < ?
            ORDER BY timestamp, transaction_id
            """,
            (str(user_id), start, end),
        ).fetchall()
    else:
        with sqlite3.connect(path, timeout=30) as read_connection:
            rows = read_connection.execute(
                """
                SELECT transaction_id, amount, metadata_json
                FROM uvi_ledger_entries
                WHERE user_id = ?
                  AND currency = 'POINT'
                  AND transaction_type = 'EARN'
                  AND timestamp >= ?
                  AND timestamp < ?
                ORDER BY timestamp, transaction_id
                """,
                (str(user_id), start, end),
            ).fetchall()

    total = Decimal("0")
    seen = set()

    for transaction_id, amount, metadata_json in rows:
        if transaction_id in seen:
            continue
        seen.add(transaction_id)

        metadata = json.loads(metadata_json or "{}")
        if metadata.get("value_flow") != "POINT_TO_2FUNC":
            continue
        if metadata.get("activity_validated") is not True:
            continue
        if metadata.get("fraud_invalidated") is True:
            continue

        value = Decimal(amount)
        if not value.is_finite() or value < 0:
            raise ValueError("Invalid POINT amount in UVI ledger")
        total += value

    return total
