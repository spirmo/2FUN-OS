"""
2FUN / TANDIL
Concept Application / Coordinator

Application layer for Concept use-cases.

Responsibilities:
- Coordinate Concept domain engines.
- Coordinate Governance.
- Coordinate persistence.
- Keep domain rules outside the application layer.

This class does NOT:
- define Concept rules
- calculate completeness itself
- decide lifecycle transitions itself
- generate Concept identity itself
"""

from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal

from platform_core.runtime.runtime_context import get_event_bus


from .models import Concept
from .validation import ConceptValidationEngine
from .completeness import refresh_completeness
from .lifecycle import (
    submit_for_review,
    approve,
    reject,
    reopen,
    publish,
    archive,
)
from .identity import (
    assign_initial_identity,
    create_revision,
)
from .history import ConceptHistory

from db.repositories.concept_version_repository import (
    ConceptVersionRepository,
)


class ConceptApplication:
    """
    Concept Application / Coordinator.

    Coordinates domain engines and persistence without
    duplicating their business rules.
    """

    def __init__(
        self,
        *,
        repository: Optional[ConceptVersionRepository] = None,
        validator: Optional[ConceptValidationEngine] = None,
        history: Optional[ConceptHistory] = None,
    ):
        self.repository = repository or ConceptVersionRepository()
        self.validator = validator or ConceptValidationEngine()
        self.history = history or ConceptHistory()

    # ======================================================
    # VALIDATION / COMPLETENESS
    # ======================================================

    def refresh(self, concept: Concept) -> dict:
        """
        Refresh system-managed completeness and return
        the canonical validation result.
        """

        completeness = refresh_completeness(concept)
        validation = self.validator.validate(concept)

        return {
            "completeness": completeness,
            "validation": validation,
        }

    # ======================================================
    # ITEM COMPLETION
    # ======================================================

    def complete_item(
        self,
        concept: Concept,
        *,
        item_key: str,
        value,
        user_id: str,
        difficulty: Optional[str] = None,
        base_value: Decimal = Decimal("10"),
    ) -> dict:
        """
        Complete one visible Concept item.

        ConceptApplication coordinates the operation.
        Business rules remain in the Concept domain engines.
        Value calculation is delegated to UVI.
        """

        item = concept.get_item(item_key)

        if item is None:
            return {
                "success": False,
                "reason": "ITEM_NOT_FOUND",
                "item_key": item_key,
            }

        if not concept.has_valid_item_key(item_key):
            return {
                "success": False,
                "reason": "INVALID_ITEM_KEY",
                "item_key": item_key,
            }

        if concept.is_system_item(item_key):
            return {
                "success": False,
                "reason": "SYSTEM_ITEM_NOT_EDITABLE",
                "item_key": item_key,
            }

        if item.value is not None:
            return {
                "success": False,
                "reason": "ITEM_ALREADY_COMPLETED",
                "item_key": item_key,
            }

        timestamp = datetime.now(timezone.utc).isoformat()

        previous_value = item.value

        item.value = value
        item.completed_by = str(user_id)
        item.completed_at = timestamp
        item.status = "APPROVED"

        completeness = refresh_completeness(concept)

        self.history.record_item_completion(
            concept_code=concept.concept_code,
            version=concept.system.version,
            user_id=str(user_id),
            item_key=item_key,
            new_value=value,
            completeness=completeness,
            base_score=item.base_score,
            difficulty_bonus=0,
            multiplier=1.0,
            earned_score=0,
        )

        event_bus = get_event_bus()

        event_result = event_bus.emit(
            "KNOWLEDGE",
            "FIELD_COMPLETED",
            "concept",
            {
                "user_id": str(user_id),
                "concept_id": concept.system.database_id,
                "concept_code": concept.concept_code,
                "item_key": item_key,
                "base_value": str(base_value),
                "difficulty": difficulty,
                "currency": "XP",
            },
        )

        return {
            "success": True,
            "item_key": item_key,
            "previous_value": previous_value,
            "value": value,
            "completed_by": str(user_id),
            "completed_at": timestamp,
            "completeness": completeness,
            "event": event_result,
        }

    # ======================================================
    # ITEM COMPLETION
    # ======================================================
