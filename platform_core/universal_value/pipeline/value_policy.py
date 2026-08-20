"""
2FUN Universal Value Infrastructure (UVI)
Unified Value Policy Contract
"""

from abc import ABC, abstractmethod
from decimal import Decimal

from ..core.value_request import ValueRequest


class ValuePolicy(ABC):
    """
    قرارداد واحد تمام Policyهای محاسبه ارزش در UVI.

    Policy فقط مسئول تغییر مقدار ارزش است.
    Policy نباید:
    - Ledger را مدیریت کند
    - Transaction ایجاد کند
    - Event منتشر کند
    - محاسبه نهایی Engine را انجام دهد
    """

    name = "BASE_POLICY"

    @abstractmethod
    def apply(
        self,
        request: ValueRequest,
        value: Decimal,
    ) -> Decimal:
        """
        مقدار فعلی ارزش را دریافت و مقدار جدید را برمی‌گرداند.
        """
        raise NotImplementedError
