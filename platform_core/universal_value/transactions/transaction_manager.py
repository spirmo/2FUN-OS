"""
2FUN Universal Value Infrastructure (UVI)
Transaction Manager
"""

from decimal import Decimal
from uuid import uuid4

from ..core.contracts import ValueEvent, ValueTransaction
from ..ledger.value_ledger import ValueLedger


class TransactionManager:
    """
    مدیریت چرخه ثبت تراکنش‌های ارزش در UVI.
    """

    def __init__(self, ledger: ValueLedger):
        self.ledger = ledger

    def create_transaction(
        self,
        event: ValueEvent,
        amount: Decimal,
        transaction_type: str = "EARN",
        metadata: dict | None = None,
    ) -> ValueTransaction:

        if amount < 0:
            raise ValueError("Transaction amount cannot be negative")

        transaction = ValueTransaction(
            transaction_id=str(uuid4()),
            event_id=event.event_id,
            user_id=event.user_id,
            amount=amount,
            currency=event.currency,
            transaction_type=transaction_type,
            metadata=metadata or {},
        )

        self.ledger.record(
            transaction_id=transaction.transaction_id,
            event_id=transaction.event_id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_type=transaction.transaction_type,
            metadata=transaction.metadata,
        )

        return transaction

    def create_transactions_batch(
        self, items: list[dict],
    ) -> list[ValueTransaction]:
        """ساخت و ثبت چند تراکنش UVI در یک عملیات اتمی."""
        transactions = []
        ledger_entries = []

        for item in items:
            event = item["event"]
            amount = Decimal(item["amount"])
            if not amount.is_finite() or amount < 0:
                raise ValueError(
                    "Transaction amount must be finite and non-negative"
                )

            transaction_type = item.get("transaction_type", "EARN")
            metadata = dict(item.get("metadata") or {})
            transaction_id = str(uuid4())

            transaction = ValueTransaction(
                transaction_id=transaction_id,
                event_id=event.event_id,
                user_id=event.user_id,
                amount=amount,
                currency=event.currency,
                transaction_type=transaction_type,
                metadata=metadata,
            )
            transactions.append(transaction)
            ledger_entries.append({
                "transaction_id": transaction_id,
                "event_id": event.event_id,
                "user_id": event.user_id,
                "amount": amount,
                "currency": event.currency,
                "transaction_type": transaction_type,
                "metadata": metadata,
            })

        # یک فراخوانی؛ اگر یکی از ورودی‌ها رد شود، هیچ‌کدام ثبت نمی‌شوند.
        self.ledger.record_batch(ledger_entries)
        return transactions
