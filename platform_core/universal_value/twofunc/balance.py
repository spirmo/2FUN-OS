"""2FUNC balance calculations."""

from decimal import Decimal

from .units import POINT, DRIKA, SHIR, SIGMA_SHIR, TWOFUNC, DRIK
from .converter import TwoFuncConverter
from .conversion import (
    POINTS_PER_DRIKA,
    POINTS_PER_SHIR,
    POINTS_PER_SIGMA_SHIR,
    POINTS_PER_2FUNC,
    POINTS_PER_DRIK,
)


class TwoFuncBalance:
    """Calculate balances across the 2FUNC value hierarchy."""

    def __init__(self):
        self.converter = TwoFuncConverter()

    def to_points(self, amount: Decimal, unit: str) -> Decimal:
        """Convert any 2FUNC unit to its exact POINT equivalent."""

        amount = Decimal(amount)

        if amount < 0:
            raise ValueError("amount must be non-negative")

        points_per_unit = {
            POINT: Decimal("1"),
            DRIKA: POINTS_PER_DRIKA,
            SHIR: POINTS_PER_SHIR,
            SIGMA_SHIR: POINTS_PER_SIGMA_SHIR,
            TWOFUNC: POINTS_PER_2FUNC,
            DRIK: POINTS_PER_DRIK,
        }

        if unit not in points_per_unit:
            raise ValueError(f"unsupported unit: {unit}")

        return amount * points_per_unit[unit]

    def from_points(
        self,
        points: Decimal,
    ) -> dict[str, Decimal]:
        """Represent POINT value across the complete hierarchy."""

        points = Decimal(points)

        if points < 0:
            raise ValueError("points must be non-negative")

        drik = points // POINTS_PER_DRIK
        remainder = points - drik * POINTS_PER_DRIK

        twofunc = remainder // POINTS_PER_2FUNC
        remainder -= twofunc * POINTS_PER_2FUNC

        sigma_shir = remainder // POINTS_PER_SIGMA_SHIR
        remainder -= sigma_shir * POINTS_PER_SIGMA_SHIR

        shir = remainder // POINTS_PER_SHIR
        remainder -= shir * POINTS_PER_SHIR

        drika = remainder // POINTS_PER_DRIKA

        return {
            POINT: points,
            DRIK: drik,
            TWOFUNC: twofunc,
            SIGMA_SHIR: sigma_shir,
            SHIR: shir,
            DRIKA: drika,
        }
