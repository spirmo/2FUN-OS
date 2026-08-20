"""
2FUN / TANDIL
Concept Engine Validation

Single validation authority for Concept structure.

Completeness calculations are delegated to the
Concept Completeness Engine.
"""

from typing import Dict

from .contract import (
    MANDATORY_ITEMS,
    OPTIONAL_ITEMS,
    SYSTEM_ITEMS,
)

from .completeness import (
    completed_item_count,
    missing_mandatory_items,
    calculate_completion_percentage,
    has_all_mandatory_items,
    is_complete as completeness_is_complete,
    get_completeness_state,
)


class ConceptValidationEngine:
    """
    Validates Concept structure against the locked Concept Contract.

    Rules:
    - 11 mandatory items are required for submission.
    - 25 optional items may be completed progressively.
    - 11 system items are never user-entered.
    - Completeness is calculated by the Completeness Engine.
    """

    def validate_item_key(self, item_key: str) -> bool:
        return (
            item_key in MANDATORY_ITEMS
            or item_key in OPTIONAL_ITEMS
            or item_key in SYSTEM_ITEMS
        )

    def is_system_item(self, item_key: str) -> bool:
        return item_key in SYSTEM_ITEMS

    def is_mandatory(self, item_key: str) -> bool:
        return item_key in MANDATORY_ITEMS

    def is_optional(self, item_key: str) -> bool:
        return item_key in OPTIONAL_ITEMS

    def missing_mandatory_items(self, concept) -> list[str]:
        return missing_mandatory_items(concept)

    def completed_visible_items(self, concept) -> int:
        return completed_item_count(concept)

    def completeness(self, concept) -> int:
        return calculate_completion_percentage(concept)

    def has_all_mandatory(self, concept) -> bool:
        return has_all_mandatory_items(concept)

    def is_complete(self, concept) -> bool:
        return completeness_is_complete(concept)

    def state_for(self, concept) -> str:
        return get_completeness_state(concept)

    def validate(self, concept) -> Dict[str, object]:
        missing = self.missing_mandatory_items(concept)
        completed = self.completed_visible_items(concept)
        total = len(MANDATORY_ITEMS) + len(OPTIONAL_ITEMS)
        percentage = self.completeness(concept)

        errors = []

        if missing:
            errors.append("MANDATORY_ITEMS_INCOMPLETE")

        return {
            "valid": len(missing) == 0,
            "errors": errors,
            "missing_required_items": missing,
            "completed_visible_items": completed,
            "total_visible_items": total,
            "completeness": percentage,
            "state": self.state_for(concept),
        }


# Backward-compatible alias
ValidationEngine = ConceptValidationEngine
