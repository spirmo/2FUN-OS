"""2FUNC value service."""

from dataclasses import dataclass
from decimal import Decimal

from .balance import TwoFuncBalance
from .units import POINT, SHIR, SIGMA_SHIR, TWOFUNC
from .transaction import TwoFuncTransaction, TwoFuncTransactionBridge


@dataclass(frozen=True)
class TwoFuncValueResult:
    """Calculated 2FUNC value representation."""

    user_id: str
    source_unit: str
    source_amount: Decimal
    func: Decimal
    sigma_shir: Decimal
    shir: Decimal
    point: Decimal
    transaction: TwoFuncTransaction


class TwoFuncValueService:
    """Calculate and record 2FUNC internal value."""

    def __init__(self, transaction_bridge: TwoFuncTransactionBridge):
        self.balance = TwoFuncBalance()
        self.transaction_bridge = transaction_bridge

    @property
    def ledger(self):
        """Return the existing UVI ledger."""
        return self.transaction_bridge.transaction_manager.ledger

    def earn_points(
        self,
        *,
        user_id: str,
        points: Decimal,
        metadata: dict | None = None,
    ) -> TwoFuncValueResult:

        points = Decimal(points)

        if points < 0:
            raise ValueError("points must be non-negative")

        representation = self.balance.from_points(points)

        transaction = self.transaction_bridge.record(
            user_id=user_id,
            amount=points,
            unit=POINT,
            transaction_type="EARN",
            metadata={
                "value_flow": "POINT_TO_2FUNC",
                **(metadata or {}),
            },
        )

        return TwoFuncValueResult(
            user_id=user_id,
            source_unit=POINT,
            source_amount=points,
            func=representation[TWOFUNC],
            sigma_shir=representation[SIGMA_SHIR],
            shir=representation[SHIR],
            point=representation[POINT],
            transaction=transaction,
        )

    def spend_points(self, *args, **kwargs):
        raise ValueError(
            "POINT is an activity unit and cannot be spent as a value asset"
        )
