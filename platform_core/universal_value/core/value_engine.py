"""
2FUN Universal Value Infrastructure (UVI)
Core Value Engine
"""

from dataclasses import dataclass
from decimal import Decimal

from .value_request import ValueRequest


@dataclass(frozen=True)
class ValueResult:
    """
    نتیجه محاسبه یک رویداد ارزش.
    """

    user_id: str
    event_id: str
    source: str
    base_value: Decimal
    multiplier: Decimal
    final_value: Decimal
    currency: str


class UniversalValueEngine:
    """
    هسته مرکزی محاسبه ارزش در اکوسیستم 2FUN.

    تمام Sourceها از طریق قرارداد ValueRequest
    می‌توانند وارد این موتور شوند.
    """

    def calculate_request(
        self,
        request: ValueRequest,
        *,
        multiplier: Decimal = Decimal("1"),
    ) -> ValueResult:

        if not isinstance(request, ValueRequest):
            raise TypeError("request must be a ValueRequest")

        return self.calculate(
            user_id=request.user_id,
            event_id=request.event_id,
            source=request.source,
            base_value=request.base_value,
            multiplier=multiplier,
            currency=request.currency,
        )

    def calculate(
        self,
        *,
        user_id: str,
        event_id: str,
        source: str,
        base_value: Decimal,
        multiplier: Decimal = Decimal("1"),
        currency: str = "XP",
    ) -> ValueResult:

        base_value = Decimal(base_value)
        multiplier = Decimal(multiplier)

        if base_value < 0:
            raise ValueError("base_value cannot be negative")

        if multiplier < 0:
            raise ValueError("multiplier cannot be negative")

        final_value = base_value * multiplier

        return ValueResult(
            user_id=user_id,
            event_id=event_id,
            source=source,
            base_value=base_value,
            multiplier=multiplier,
            final_value=final_value,
            currency=currency,
        )
