"""
2FUN Universal Value Infrastructure (UVI)

Knowledge → UVI Adapter
"""

from decimal import Decimal
from dataclasses import dataclass
from typing import Optional

from ...core.value_request import ValueRequest
from ...core.value_engine import ValueResult
from ...pipeline.value_pipeline import ValuePipeline


@dataclass(frozen=True)
class KnowledgeValueRequest:
    """
    قرارداد داخلی/سازگاری Knowledge.
    """

    user_id: str
    event_id: str
    field_key: str
    difficulty: Optional[str] = None
    base_value: Decimal = Decimal("0")
    currency: str = "XP"
    metadata: Optional[dict] = None


class KnowledgeValueAdapter:
    """
    Adapter بین Knowledge Engine و UVI.

    Knowledge:
        - Ledger را مدیریت نمی‌کند
        - Transaction را مدیریت نمی‌کند
        - محاسبه نهایی مستقل انجام نمی‌دهد

    فقط Knowledge event را به ValueRequest عمومی UVI تبدیل می‌کند.
    """

    SOURCE = "KNOWLEDGE"

    def build_request(
        self,
        *,
        user_id: str,
        event_id: str,
        field_key: str,
        base_value: Decimal,
        difficulty: Optional[str] = None,
        currency: str = "XP",
        metadata: Optional[dict] = None,
    ) -> ValueRequest:

        return ValueRequest(
            user_id=user_id,
            event_id=event_id,
            source=self.SOURCE,
            action="FIELD_COMPLETED",
            item_key=field_key,
            base_value=Decimal(base_value),
            difficulty=difficulty,
            currency=currency,
            metadata={
                **(metadata or {}),
                "source": self.SOURCE,
                "field_key": field_key,
                "difficulty": difficulty,
            },
        )

    def calculate(
        self,
        pipeline: ValuePipeline,
        request: ValueRequest,
        *,
        multiplier: Decimal = Decimal("1"),
    ) -> ValueResult:
        """
        ارسال ValueRequest به UVI Pipeline.
        """

        if not isinstance(request, ValueRequest):
            raise TypeError(
                "request must be a ValueRequest"
            )

        if request.source != self.SOURCE:
            raise ValueError(
                f"Invalid source for Knowledge adapter: "
                f"{request.source}"
            )

        return pipeline.calculate(
            request,
            multiplier=multiplier,
        )
