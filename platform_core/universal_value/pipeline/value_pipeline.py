"""
2FUN Universal Value Infrastructure (UVI)
Value Calculation Pipeline
"""

from decimal import Decimal
from typing import Iterable

from ..core.value_request import ValueRequest
from ..core.value_engine import UniversalValueEngine, ValueResult
from .value_policy import ValuePolicy


class ValuePipeline:
    """
    Pipeline مرکزی محاسبه ارزش.

    ترتیب:

        Request
           ↓
        Base Value
           ↓
        Policy 1
           ↓
        Policy 2
           ↓
        ...
           ↓
        UniversalValueEngine
           ↓
        ValueResult

    Pipeline مسئول Ledger یا Transaction نیست.
    """

    def __init__(
        self,
        engine: UniversalValueEngine | None = None,
        policies: Iterable[ValuePolicy] | None = None,
    ):
        self.engine = engine or UniversalValueEngine()
        self._policies: list[ValuePolicy] = list(policies or [])

    def add_policy(self, policy: ValuePolicy) -> None:
        if not isinstance(policy, ValuePolicy):
            raise TypeError("policy must implement ValuePolicy")

        self._policies.append(policy)

    def policies(self) -> list[str]:
        return [policy.name for policy in self._policies]

    def calculate(
        self,
        request: ValueRequest,
        *,
        multiplier: Decimal = Decimal("1"),
    ) -> ValueResult:

        if not isinstance(request, ValueRequest):
            raise TypeError("request must be a ValueRequest")

        value = Decimal(request.base_value)

        for policy in self._policies:
            value = Decimal(policy.apply(request, value))

            if value < 0:
                value = Decimal("0")

        return self.engine.calculate_request(
            request.__class__(
                user_id=request.user_id,
                event_id=request.event_id,
                source=request.source,
                action=request.action,
                item_key=request.item_key,
                base_value=value,
                difficulty=request.difficulty,
                currency=request.currency,
                metadata=dict(request.metadata),
            ),
            multiplier=multiplier,
        )
