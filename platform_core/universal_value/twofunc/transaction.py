"""2FUNC transaction bridge to the existing UVI transaction layer."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Optional
from uuid import uuid4

from platform_core.universal_value.core.contracts import ValueEvent
from platform_core.universal_value.transactions.transaction_manager import (
    TransactionManager,
)

from .units import POINT, SHIR, SIGMA_SHIR, TWOFUNC


@dataclass(frozen=True)
class TwoFuncTransaction:
    """Internal representation of a 2FUNC value transaction."""

    transaction_id: str
    user_id: str
    unit: str
    amount: Decimal
    transaction_type: str
    timestamp: str
    metadata: dict


class TwoFuncTransactionBridge:
    """Bridge 2FUNC transactions into the existing UVI transaction manager."""

    SUPPORTED_UNITS = {
        POINT,
        SHIR,
        SIGMA_SHIR,
        TWOFUNC,
    }

    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager

    def record(
        self,
        *,
        user_id: str,
        amount: Decimal,
        unit: str,
        transaction_type: str = "EARN",
        metadata: Optional[dict[str, Any]] = None,
        event_id: Optional[str] = None,
    ) -> TwoFuncTransaction:

        amount = Decimal(amount)

        if not user_id:
            raise ValueError("user_id must not be empty")

        if amount < 0:
            raise ValueError("amount must be non-negative")

        if unit not in self.SUPPORTED_UNITS:
            raise ValueError(f"unsupported 2FUNC unit: {unit}")

        transaction_id = str(uuid4())
        event_id = event_id or str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        event = ValueEvent(
            event_id=event_id,
            user_id=user_id,
            source="2FUNC",
            action=transaction_type,
            base_value=amount,
            currency=unit,
            metadata={
                "twofunc_unit": unit,
                "twofunc_transaction_id": transaction_id,
                **(metadata or {}),
            },
        )

        transaction = self.transaction_manager.create_transaction(
            event=event,
            amount=amount,
            transaction_type=transaction_type,
            metadata={
                "twofunc_unit": unit,
                "twofunc_transaction_id": transaction_id,
                "timestamp": timestamp,
                **(metadata or {}),
            },
        )

        return TwoFuncTransaction(
            transaction_id=transaction.transaction_id,
            user_id=user_id,
            unit=unit,
            amount=amount,
            transaction_type=transaction_type,
            timestamp=timestamp,
            metadata=dict(transaction.metadata or {}),
        )
