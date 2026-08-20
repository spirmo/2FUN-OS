"""
2FUN Universal Value Infrastructure (UVI)
Universal Value Request Contract
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class ValueRequest:
    """
    قرارداد عمومی درخواست محاسبه ارزش در UVI.

    این قرارداد باید بتواند تمام منابع ارزش‌زای اکوسیستم 2FUN
    را بدون وابستگی به منطق داخلی آنها دریافت کند.
    """

    user_id: str
    event_id: str

    # منبع ارزش در UVI:
    # KNOWLEDGE / GAME / IDENTITY / ECONOMY / GOVERNANCE / ...
    source: str

    # نوع اقدام:
    # FIELD_COMPLETED / PURCHASE / SALE / CHALLENGE / ...
    action: str

    # شناسه دقیق مورد یا عملیات
    item_key: Optional[str] = None

    # مقدار پایه قبل از سیاست‌ها و ضرایب
    base_value: Decimal = Decimal("0")

    # سطح دشواری در صورت وجود
    difficulty: Optional[str] = None

    # واحد ارزش
    currency: str = "XP"

    # اطلاعات تکمیلی رویداد
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id is required")

        if not self.event_id:
            raise ValueError("event_id is required")

        if not self.source:
            raise ValueError("source is required")

        if not self.action:
            raise ValueError("action is required")

        if self.base_value < 0:
            raise ValueError("base_value cannot be negative")

        if not self.currency:
            raise ValueError("currency is required")
