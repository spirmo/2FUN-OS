"""Persistent central value ledger for the 2FUN UVI."""

import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import List

from db.database import DB_PATH
from platform_core.universal_value.unit_contract import (
    POINT, canonicalize_unit,
)


@dataclass(frozen=True)
class LedgerEntry:
    transaction_id: str
    event_id: str
    user_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    timestamp: str
    metadata: dict


class ValueLedger:
    """دفتر کل مرکزی پایدار UVI روی پایگاه داده اصلی اکوسیستم."""

    def __init__(self, db_path=None):
        self.db_path = str(Path(db_path) if db_path is not None else DB_PATH)

    def _connect(self):
        connection = sqlite3.connect(self.db_path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    @staticmethod
    def _to_entry(row):
        return LedgerEntry(
            transaction_id=row["transaction_id"],
            event_id=row["event_id"],
            user_id=row["user_id"],
            amount=Decimal(row["amount"]),
            currency=canonicalize_unit(row["currency"]),
            transaction_type=row["transaction_type"],
            timestamp=row["timestamp"],
            metadata=json.loads(row["metadata_json"]),
        )

    def record(
        self, *, transaction_id: str, event_id: str, user_id: str,
        amount: Decimal, currency: str, transaction_type: str,
        metadata: dict | None = None,
    ) -> LedgerEntry:
        currency = canonicalize_unit(currency)
        amount = Decimal(amount)
        if not amount.is_finite() or amount < 0:
            raise ValueError("Ledger amount must be finite and non-negative")

        timestamp = datetime.now(timezone.utc).isoformat()
        saved_metadata = dict(metadata or {})
        metadata_json = json.dumps(
            saved_metadata, ensure_ascii=False, separators=(",", ":")
        )

        try:
            with closing(self._connect()) as connection:
                with connection:
                    connection.execute("""
                        INSERT INTO uvi_ledger_entries (
                            transaction_id, event_id, user_id, amount,
                            currency, transaction_type, timestamp,
                            metadata_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        transaction_id, event_id, user_id, str(amount),
                        currency, transaction_type, timestamp, metadata_json,
                    ))
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Duplicate transaction: {transaction_id}"
            ) from exc

        return LedgerEntry(
            transaction_id=transaction_id,
            event_id=event_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            timestamp=timestamp,
            metadata=saved_metadata,
        )

    def record_batch(self, entries: list[dict]) -> List[LedgerEntry]:
        """ثبت اتمی چند ورودی؛ شکست یک ورودی، کل دسته را لغو می‌کند."""
        prepared = []
        seen_ids = set()

        for item in entries:
            amount = Decimal(item["amount"])
            currency = canonicalize_unit(item["currency"])
            transaction_id = item["transaction_id"]

            if not amount.is_finite() or amount < 0:
                raise ValueError(
                    "Ledger amount must be finite and non-negative"
                )
            if transaction_id in seen_ids:
                raise ValueError(
                    f"Duplicate transaction in batch: {transaction_id}"
                )
            seen_ids.add(transaction_id)

            timestamp = datetime.now(timezone.utc).isoformat()
            metadata = dict(item.get("metadata") or {})
            prepared.append({
                "transaction_id": transaction_id,
                "event_id": item["event_id"],
                "user_id": item["user_id"],
                "amount": amount,
                "currency": currency,
                "transaction_type": item["transaction_type"],
                "timestamp": timestamp,
                "metadata": metadata,
                "metadata_json": json.dumps(
                    metadata, ensure_ascii=False, separators=(",", ":")
                ),
            })

        if not prepared:
            return []

        try:
            with closing(self._connect()) as connection:
                with connection:
                    for item in prepared:
                        connection.execute("""
                            INSERT INTO uvi_ledger_entries (
                                transaction_id, event_id, user_id, amount,
                                currency, transaction_type, timestamp,
                                metadata_json
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            item["transaction_id"], item["event_id"],
                            item["user_id"], str(item["amount"]),
                            item["currency"], item["transaction_type"],
                            item["timestamp"], item["metadata_json"],
                        ))
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "Batch rejected: duplicate transaction or event constraint"
            ) from exc

        return [
            LedgerEntry(
                transaction_id=item["transaction_id"],
                event_id=item["event_id"],
                user_id=item["user_id"],
                amount=item["amount"],
                currency=item["currency"],
                transaction_type=item["transaction_type"],
                timestamp=item["timestamp"],
                metadata=item["metadata"],
            )
            for item in prepared
        ]


    def execute_transfer(
        self, *, operation_id: str, source_user_id: str,
        destination_user_id: str, amount: Decimal, currency: str,
        metadata: dict | None = None,
    ) -> dict:
        """Atomically debit and credit; persist idempotency by operation ID."""
        currency = canonicalize_unit(currency)
        amount = Decimal(amount)
        if currency == POINT:
            raise ValueError("POINT is an activity unit and cannot be transferred")
        if not operation_id or not source_user_id or not destination_user_id:
            raise ValueError("Operation and account IDs are required")
        if source_user_id == destination_user_id:
            raise ValueError("Source and destination must differ")
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Transfer amount must be finite and positive")

        debit_id = f"{operation_id}:debit"
        credit_id = f"{operation_id}:credit"
        now = datetime.now(timezone.utc).isoformat()
        saved_metadata = dict(metadata or {})
        credits = {"CREDIT", "REWARD", "EARN", "CONVERSION_IN"}
        debits = {"DEBIT", "SPEND", "CONVERSION_OUT"}

        with closing(self._connect()) as connection:
            try:
                connection.execute("BEGIN IMMEDIATE")

                previous = connection.execute(
                    "SELECT * FROM uvi_transfer_operations WHERE operation_id = ?",
                    (operation_id,),
                ).fetchone()

                if previous is not None:
                    same_request = (
                        previous["source_user_id"] == source_user_id
                        and previous["destination_user_id"] == destination_user_id
                        and Decimal(previous["amount"]) == amount
                        and previous["currency"] == currency
                    )
                    if not same_request:
                        raise ValueError("Operation ID reused with different transfer details")
                    connection.commit()
                    return {
                        "operation_id": operation_id,
                        "debit_transaction_id": previous["debit_transaction_id"],
                        "credit_transaction_id": previous["credit_transaction_id"],
                        "replayed": True,
                    }

                rows = connection.execute(
                    """SELECT amount, transaction_type
                       FROM uvi_ledger_entries
                       WHERE user_id = ? AND currency = ?""",
                    (source_user_id, currency),
                ).fetchall()

                balance = Decimal("0")
                for row in rows:
                    value = Decimal(row["amount"])
                    if row["transaction_type"] in credits:
                        balance += value
                    elif row["transaction_type"] in debits:
                        balance -= value

                if amount > balance:
                    raise ValueError("Insufficient UVI balance")

                for tx_id, side, user_id, tx_type in (
                    (debit_id, "SOURCE", source_user_id, "DEBIT"),
                    (credit_id, "DESTINATION", destination_user_id, "CREDIT"),
                ):
                    tx_metadata = {
                        **saved_metadata,
                        "transfer_id": operation_id,
                        "side": side,
                    }
                    connection.execute(
                        """INSERT INTO uvi_ledger_entries (
                            transaction_id, event_id, user_id, amount,
                            currency, transaction_type, timestamp, metadata_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            tx_id, f"{operation_id}:{side.lower()}", user_id,
                            str(amount), currency, tx_type, now,
                            json.dumps(tx_metadata, ensure_ascii=False,
                                       separators=(",", ":")),
                        ),
                    )

                connection.execute(
                    """INSERT INTO uvi_transfer_operations (
                        operation_id, source_user_id, destination_user_id,
                        amount, currency, debit_transaction_id,
                        credit_transaction_id, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        operation_id, source_user_id, destination_user_id,
                        str(amount), currency, debit_id, credit_id, now,
                    ),
                )
                connection.commit()
                return {
                    "operation_id": operation_id,
                    "debit_transaction_id": debit_id,
                    "credit_transaction_id": credit_id,
                    "replayed": False,
                }
            except Exception:
                if connection.in_transaction:
                    connection.rollback()
                raise

    def all_entries(self) -> List[LedgerEntry]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM uvi_ledger_entries ORDER BY rowid"
            ).fetchall()
        return [self._to_entry(row) for row in rows]

    def user_entries(self, user_id: str) -> List[LedgerEntry]:
        with closing(self._connect()) as connection:
            rows = connection.execute("""
                SELECT * FROM uvi_ledger_entries
                WHERE user_id = ? ORDER BY rowid
            """, (user_id,)).fetchall()
        return [self._to_entry(row) for row in rows]

    def balance(self, user_id: str, currency: str) -> Decimal:
        # POINT records activity history; it is not an asset balance.
        currency = canonicalize_unit(currency)
        if currency == POINT:
            return Decimal("0")

        credits = {"CREDIT", "REWARD", "EARN", "CONVERSION_IN"}
        debits = {"DEBIT", "SPEND", "CONVERSION_OUT"}
        total = Decimal("0")

        for entry in self.user_entries(user_id):
            if entry.currency != currency:
                continue
            if entry.transaction_type in credits:
                total += entry.amount
            elif entry.transaction_type in debits:
                total -= entry.amount

        return total
