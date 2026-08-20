"""
2FUN Universal Value Infrastructure (UVI)
Value Ledger
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List


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
    """
    دفتر کل مرکزی UVI.

    Ledger تنها محل ثبت immutable رویدادهای ارزش است.
    """

    def __init__(self):
        self._entries: List[LedgerEntry] = []
        self._transaction_ids = set()

    def record(
        self,
        *,
        transaction_id: str,
        event_id: str,
        user_id: str,
        amount: Decimal,
        currency: str,
        transaction_type: str,
        metadata: dict | None = None,
    ) -> LedgerEntry:

        if transaction_id in self._transaction_ids:
            raise ValueError(
                f"Duplicate transaction: {transaction_id}"
            )

        if amount < 0:
            raise ValueError("Ledger amount cannot be negative")

        entry = LedgerEntry(
            transaction_id=transaction_id,
            event_id=event_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )

        self._entries.append(entry)
        self._transaction_ids.add(transaction_id)

        return entry

    def all_entries(self) -> List[LedgerEntry]:
        return list(self._entries)

    def user_entries(self, user_id: str) -> List[LedgerEntry]:
        return [
            entry
            for entry in self._entries
            if entry.user_id == user_id
        ]

    def balance(
        self,
        user_id: str,
        currency: str,
    ) -> Decimal:

        total = Decimal("0")

        for entry in self._entries:
            if (
                entry.user_id == user_id
                and entry.currency == currency
            ):
                if entry.transaction_type in {
                    "CREDIT",
                    "REWARD",
                    "EARN",
                    "CONVERSION_IN",
                }:
                    total += entry.amount

                elif entry.transaction_type in {
                    "DEBIT",
                    "SPEND",
                    "CONVERSION_OUT",
                }:
                    total -= entry.amount

        return total
