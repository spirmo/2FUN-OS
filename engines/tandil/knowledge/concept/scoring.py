"""
2FUN / TANDIL
Concept Engine
Scoring System

Rules:
- Every item has 10 base points.
- Optional items receive +25 / +30 / +35 research difficulty points.
- Community participation starts after the 11 mandatory items exist.
- The user's participation multiplier is locked on first entry.
- A user earns points only for items completed by that user.
"""

from typing import Dict, Optional

from .contract import (
    MANDATORY_ITEMS,
    OPTIONAL_ITEMS,
)


# ==========================================================
# BASE SCORE
# ==========================================================

BASE_ITEM_SCORE = 10


# ==========================================================
# OPTIONAL DIFFICULTY BONUS
# ==========================================================

OPTIONAL_DIFFICULTY_BONUS = {
    "LOW": 25,
    "MEDIUM": 30,
    "HIGH": 35,
}


# ==========================================================
# PARTICIPATION MULTIPLIERS
# ==========================================================

PARTICIPATION_MULTIPLIERS = {
    "BASE": 1,
    "30_39": 2,
    "40_49": 3,
    "50_59": 4,
    "60_69": 5,
    "70_79": 6,
    "80_89": 7,
    "90_100": 8,
}


# ==========================================================
# ITEM SCORE
# ==========================================================

def get_item_base_score(
    item_key: str,
    difficulty: Optional[str] = None,
) -> int:

    if item_key in MANDATORY_ITEMS:
        return BASE_ITEM_SCORE

    if item_key in OPTIONAL_ITEMS:

        if difficulty is None:
            raise ValueError(
                "Optional item requires difficulty."
            )

        if difficulty not in OPTIONAL_DIFFICULTY_BONUS:
            raise ValueError(
                f"Invalid difficulty: {difficulty}"
            )

        return (
            BASE_ITEM_SCORE
            + OPTIONAL_DIFFICULTY_BONUS[difficulty]
        )

    raise ValueError(
        f"Unknown Concept item: {item_key}"
    )


# ==========================================================
# COMPLETION PERCENTAGE
# ==========================================================

def calculate_completion_percentage(
    completed_items: int,
    total_items: int = 36,
) -> float:

    if total_items <= 0:
        raise ValueError(
            "total_items must be greater than zero."
        )

    if completed_items < 0:
        raise ValueError(
            "completed_items cannot be negative."
        )

    if completed_items > total_items:
        raise ValueError(
            "completed_items cannot exceed total_items."
        )

    return (
        completed_items / total_items
    ) * 100


# ==========================================================
# PARTICIPATION MULTIPLIER
# ==========================================================

def get_participation_multiplier(
    completed_items: int,
    total_items: int = 36,
) -> int:
    """
    Determine the participation multiplier.

    Concept Engine v1.0

    Rules:
    - 11 mandatory items = x1
    - 12-14 items = x2
    - 15-17 items = x3
    - 18-21 items = x4
    - 22-25 items = x5
    - 26-28 items = x6
    - 29-32 items = x7
    - 33-36 items = x8

    The multiplier is determined at the user's
    first participation and then locked.
    """

    if total_items != 36:
        raise ValueError(
            "Concept Engine v1.0 requires exactly 36 visible items."
        )

    if completed_items < 0:
        raise ValueError(
            "completed_items cannot be negative."
        )

    if completed_items > total_items:
        raise ValueError(
            "completed_items cannot exceed total_items."
        )

    # Community participation is unavailable
    # before all 11 mandatory items are complete.
    if completed_items < 11:
        raise ValueError(
            "Community participation is not available "
            "before all 11 mandatory items are completed."
        )

    # Special mandatory-complete stage.
    if completed_items == 11:
        return PARTICIPATION_MULTIPLIERS["BASE"]

    if 12 <= completed_items <= 14:
        return PARTICIPATION_MULTIPLIERS["30_39"]

    if 15 <= completed_items <= 17:
        return PARTICIPATION_MULTIPLIERS["40_49"]

    if 18 <= completed_items <= 21:
        return PARTICIPATION_MULTIPLIERS["50_59"]

    if 22 <= completed_items <= 25:
        return PARTICIPATION_MULTIPLIERS["60_69"]

    if 26 <= completed_items <= 28:
        return PARTICIPATION_MULTIPLIERS["70_79"]

    if 29 <= completed_items <= 32:
        return PARTICIPATION_MULTIPLIERS["80_89"]

    return PARTICIPATION_MULTIPLIERS["90_100"]


# ==========================================================
# USER PARTICIPATION LOCK
# ==========================================================

def lock_user_multiplier(
    user_id: str,
    concept_id: int,
    completed_items: int,
    existing_locks: Optional[Dict[str, int]] = None,
) -> int:

    if not user_id:
        raise ValueError(
            "user_id is required."
        )

    if concept_id is None:
        raise ValueError(
            "concept_id is required."
        )

    if existing_locks is None:
        existing_locks = {}

    lock_key = f"{user_id}:{concept_id}"

    # Existing lock never changes
    if lock_key in existing_locks:
        return existing_locks[lock_key]

    # First participation
    multiplier = get_participation_multiplier(
        completed_items
    )

    existing_locks[lock_key] = multiplier

    return multiplier


# ==========================================================
# EARNED SCORE
# ==========================================================

def calculate_earned_score(
    item_key: str,
    difficulty: Optional[str],
    multiplier: int,
) -> int:

    if multiplier < 1:
        raise ValueError(
            "Multiplier must be at least 1."
        )

    item_score = get_item_base_score(
        item_key,
        difficulty,
    )

    return item_score * multiplier


# ==========================================================
# USER ITEM REWARD
# ==========================================================

def calculate_user_item_reward(
    item_key: str,
    difficulty: Optional[str],
    completed_by_user: bool,
    multiplier: int,
) -> int:
    """
    User receives points only for an item
    completed by that same user.
    """

    if not completed_by_user:
        return 0

    return calculate_earned_score(
        item_key,
        difficulty,
        multiplier,
    )
