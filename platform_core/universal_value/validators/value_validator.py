"""
2FUN Universal Value Infrastructure (UVI)
Value Validator
"""

from decimal import Decimal

from ..core.contracts import ValueEvent, ValueTransaction


class ValueValidator:

    def validate_event(self, event: ValueEvent) -> None:

        if not event.event_id:
            raise ValueError("event_id is required")

        if not event.user_id:
            raise ValueError("user_id is required")

        if not event.source:
            raise ValueError("source is required")

        if not event.action:
            raise ValueError("action is required")

        if event.base_value < Decimal("0"):
            raise ValueError(
                "event base_value cannot be negative"
            )

        if not event.currency:
            raise ValueError("currency is required")

    def validate_transaction(
        self,
        transaction: ValueTransaction,
    ) -> None:

        if not transaction.transaction_id:
            raise ValueError("transaction_id is required")

        if not transaction.event_id:
            raise ValueError("event_id is required")

        if not transaction.user_id:
            raise ValueError("user_id is required")

        if transaction.amount < Decimal("0"):
            raise ValueError(
                "transaction amount cannot be negative"
            )

        if not transaction.currency:
            raise ValueError("currency is required")

        if not transaction.transaction_type:
            raise ValueError(
                "transaction_type is required"
            )
