"""
2FUN / TANDIL
Governance Validation Adapter

Concept Engine owns the Concept Contract.
Governance consumes its validation result.
"""

from engines.tandil.knowledge.concept.validation import (
    ConceptValidationEngine,
)
from engines.tandil.knowledge.concept.models import (
    Concept,
    ConceptItem,
)
from engines.tandil.knowledge.concept.contract import MANDATORY_ITEMS


class ValidationEngine:

    def __init__(self):
        self.concept_validator = ConceptValidationEngine()

    def _dict_to_concept(self, data: dict) -> Concept:
        """
        Temporary compatibility adapter.

        Governance currently receives Concept data as dict.
        Convert it to the canonical Concept domain model.
        """

        concept = Concept()

        for key, value in data.items():

            if concept.has_valid_item_key(key):

                concept.set_item(
                    ConceptItem(
                        item_key=key,
                        value=value,
                        is_required=key in MANDATORY_ITEMS,
                    )
                )

        return concept

    def validate_concept(self, concept) -> dict:

        # Canonical Concept model
        if isinstance(concept, Concept):
            canonical = concept

        # Legacy Governance dict input
        elif isinstance(concept, dict):
            canonical = self._dict_to_concept(concept)

        else:
            return {
                "valid": False,
                "errors": [
                    "INVALID_CONCEPT_TYPE"
                ],
                "missing_required_items": [],
                "completeness": 0,
                "state": "OPEN_FOR_COMPLETION",
                "completed_visible_items": 0,
                "total_visible_items": 36,
            }

        result = self.concept_validator.validate(canonical)

        return {
            "valid": result["valid"],
            "errors": result["errors"],
            "missing_required_items": result[
                "missing_required_items"
            ],
            "completeness": result[
                "completeness"
            ],
            "state": result["state"],
            "completed_visible_items": result[
                "completed_visible_items"
            ],
            "total_visible_items": result[
                "total_visible_items"
            ],
        }
