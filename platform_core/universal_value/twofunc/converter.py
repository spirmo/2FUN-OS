"""2FUNC conversion engine.

Converts between POINT, SHIR, SIGMA_SHIR and 2FUNC
while preserving exact remainder values.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple

from .units import POINT, DRIKA, SHIR, SIGMA_SHIR, TWOFUNC, DRIK
from .conversion import (
    POINTS_PER_DRIKA,
    POINTS_PER_SHIR,
    POINTS_PER_SIGMA_SHIR,
    POINTS_PER_2FUNC,
    POINTS_PER_DRIK,
)


@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    target_unit: str
    source_amount: Decimal
    target_amount: Decimal
    remainder_amount: Decimal


class TwoFuncConverter:
    """Exact converter for the internal 2FUNC value hierarchy."""

    _POINTS_PER_UNIT = {
        POINT: Decimal("1"),
        DRIKA: POINTS_PER_DRIKA,
        SHIR: POINTS_PER_SHIR,
        SIGMA_SHIR: POINTS_PER_SIGMA_SHIR,
        TWOFUNC: POINTS_PER_2FUNC,
        DRIK: POINTS_PER_DRIK,
    }

    def convert(
        self,
        amount: Decimal,
        source_unit: str,
        target_unit: str,
    ) -> ConversionResult:
        amount = Decimal(amount)

        if amount < 0:
            raise ValueError("amount must be non-negative")

        if source_unit not in self._POINTS_PER_UNIT:
            raise ValueError(f"unsupported source unit: {source_unit}")

        if target_unit not in self._POINTS_PER_UNIT:
            raise ValueError(f"unsupported target unit: {target_unit}")

        source_in_points = amount * self._POINTS_PER_UNIT[source_unit]
        target_points = self._POINTS_PER_UNIT[target_unit]

        target_amount = source_in_points // target_points
        remainder_points = source_in_points - (
            target_amount * target_points
        )

        remainder_amount = (
            remainder_points / self._POINTS_PER_UNIT[source_unit]
        )

        return ConversionResult(
            source_unit=source_unit,
            target_unit=target_unit,
            source_amount=amount,
            target_amount=target_amount,
            remainder_amount=remainder_amount,
        )
