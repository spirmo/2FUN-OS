"""
2FUN / TANDIL
Concept Engine — Completeness Engine

Architecture:
- 11 Mandatory Items
- 25 Optional Items
- 36 Visible Items

Rules:
- A Concept with all 11 mandatory items completed is eligible for submission.
- 11/36 through 35/36 = INCOMPLETE
- 36/36 = COMPLETE
- Completeness is based on the 36 visible Concept items.
"""

from .contract import (
    MANDATORY_ITEMS,
    OPTIONAL_ITEMS,
)
from .models import Concept


TOTAL_VISIBLE_ITEMS = len(MANDATORY_ITEMS) + len(OPTIONAL_ITEMS)
MANDATORY_COUNT = len(MANDATORY_ITEMS)


def is_item_completed(concept: Concept, item_key: str) -> bool:
    """
    Return True only when the requested item exists and
    contains a non-empty value.
    """

    item = concept.get_item(item_key)

    if item is None:
        return False

    if item.value is None:
        return False

    if isinstance(item.value, str):
        return bool(item.value.strip())

    if isinstance(item.value, (list, tuple, dict, set)):
        return len(item.value) > 0

    return True


def completed_item_count(concept: Concept) -> int:
    """
    Count completed visible Concept items.

    Only the 36 contract-defined visible items are counted.
    """

    count = 0

    for item_key in MANDATORY_ITEMS:
        if is_item_completed(concept, item_key):
            count += 1

    for item_key in OPTIONAL_ITEMS:
        if is_item_completed(concept, item_key):
            count += 1

    return count


def completed_mandatory_count(concept: Concept) -> int:
    """
    Count completed mandatory items.
    """

    return sum(
        1
        for item_key in MANDATORY_ITEMS
        if is_item_completed(concept, item_key)
    )


def missing_mandatory_items(concept: Concept) -> list[str]:
    """
    Return mandatory items that are still incomplete.
    """

    return [
        item_key
        for item_key in MANDATORY_ITEMS
        if not is_item_completed(concept, item_key)
    ]


def calculate_completion_percentage(concept: Concept) -> int:
    """
    Calculate Concept completeness from 0 to 100.

    Formula:
        completed visible items / 36 * 100

    The result is rounded down to an integer percentage.
    """

    completed = completed_item_count(concept)

    return int((completed / TOTAL_VISIBLE_ITEMS) * 100)


def has_all_mandatory_items(concept: Concept) -> bool:
    """
    A Concept becomes eligible for submission only when
    all 11 mandatory items are completed.
    """

    return completed_mandatory_count(concept) == MANDATORY_COUNT


def can_submit(concept: Concept) -> bool:
    """
    Determine whether the Concept is eligible for submission
    to the Approval process.
    """

    return has_all_mandatory_items(concept)


def is_incomplete(concept: Concept) -> bool:
    """
    A Concept is incomplete when:
        mandatory items are complete
        AND
        total visible items are less than 36.
    """

    completed = completed_item_count(concept)

    return (
        has_all_mandatory_items(concept)
        and completed < TOTAL_VISIBLE_ITEMS
    )


def is_complete(concept: Concept) -> bool:
    """
    A Concept is complete only when all 36 visible items
    have been completed.
    """

    return completed_item_count(concept) == TOTAL_VISIBLE_ITEMS


def get_completeness_state(concept: Concept) -> str:
    """
    Return the normalized completeness state.
    """

    completed = completed_item_count(concept)

    if completed < MANDATORY_COUNT:
        return "NOT_SUBMITTABLE"

    if completed < TOTAL_VISIBLE_ITEMS:
        return "INCOMPLETE"

    return "COMPLETE"


def refresh_completeness(concept: Concept) -> int:
    """
    Calculate and update the Concept's system completeness.

    Returns the new percentage.
    """

    completed = completed_item_count(concept)

    concept.completeness = completed

    return completed


def get_completeness_report(concept: Concept) -> dict:
    """
    Return a complete diagnostic report for the Concept.
    """

    completed = completed_item_count(concept)
    mandatory_completed = completed_mandatory_count(concept)
    percentage = calculate_completion_percentage(concept)

    return {
        "completed_items": completed,
        "total_visible_items": TOTAL_VISIBLE_ITEMS,
        "mandatory_completed": mandatory_completed,
        "mandatory_total": MANDATORY_COUNT,
        "percentage": percentage,
        "state": get_completeness_state(concept),
        "can_submit": can_submit(concept),
        "is_incomplete": is_incomplete(concept),
        "is_complete": is_complete(concept),
        "missing_mandatory_items": missing_mandatory_items(concept),
    }
