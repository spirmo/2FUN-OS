"""
2FUN Universal Value Infrastructure (UVI)
Value Conversion Engine
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN


@dataclass(frozen=True)
class ConversionResult:
    source_currency: str
    target_currency: str
    source_amount: Decimal
    target_amount: Decimal
    rate: Decimal
    remainder: Decimal


class ConversionEngine:
    """
    هسته عمومی تبدیل واحدهای ارزش در UVI.

    قوانین اقتصادی واقعی بعداً از طریق Policy تعریف می‌شوند.
    """

    def convert(
        self,
        *,
        amount: Decimal,
        source_currency: str,
        target_currency: str,
        rate: Decimal,
        precision: int = 18,
    ) -> ConversionResult:

        if amount < 0:
            raise ValueError("Conversion amount cannot be negative")

        if rate <= 0:
            raise ValueError("Conversion rate must be positive")

        if not source_currency:
            raise ValueError("Source currency is required")

        if not target_currency:
            raise ValueError("Target currency is required")

        raw_target = amount * rate

        quantizer = Decimal("1").scaleb(-precision)
        target_amount = raw_target.quantize(
            quantizer,
            rounding=ROUND_DOWN,
        )

        remainder = amount - (
            target_amount / rate
        )

        return ConversionResult(
            source_currency=source_currency,
            target_currency=target_currency,
            source_amount=amount,
            target_amount=target_amount,
            rate=rate,
            remainder=remainder,
        )
