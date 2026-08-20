"""
UVI Core Contracts
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class ValueEvent:
    """
    قرارداد عمومی تمام رویدادهای ارزش‌زا در 2FUN.
    """

    event_id: str
    user_id: str
    source: str
    action: str
    base_value: Decimal
    currency: str = "XP"
    metadata: Optional[dict] = None


@dataclass(frozen=True)
class ValueTransaction:
    """
    قرارداد عمومی تراکنش ارزش.
    """

    transaction_id: str
    event_id: str
    user_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    metadata: Optional[dict] = None
