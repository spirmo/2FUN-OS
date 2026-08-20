from decimal import Decimal

from ..pipeline.value_policy import ValuePolicy
from ..core.value_request import ValueRequest


class KnowledgeDifficultyPolicy(ValuePolicy):
    """
    Difficulty Policy برای Knowledge Field Reward.

    Base Value + Difficulty Bonus = Policy Value

    این Policy فقط محاسبه ارزش را انجام می‌دهد.
    Ledger / Transaction / Engine در اینجا مدیریت نمی‌شوند.
    """

    name = "DIFFICULTY_BONUS"

    DIFFICULTY_VALUES = {
        "EASY": Decimal("25"),
        "MEDIUM": Decimal("30"),
        "HARD": Decimal("35"),
    }

    def apply(
        self,
        request: ValueRequest,
        value: Decimal,
    ) -> Decimal:
        difficulty_value = self.DIFFICULTY_VALUES.get(
            (request.difficulty or "").upper(),
            Decimal("0"),
        )

        return Decimal(value) + difficulty_value
