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
    submit_for_review as lifecycle_submit_for_review,
    approve as lifecycle_approve,
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
from db.repositories.completion_queue_repository import (
    CompletionQueueRepository,
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
        completion_repository: Optional[CompletionQueueRepository] = None,
        validator: Optional[ConceptValidationEngine] = None,
        history: Optional[ConceptHistory] = None,
    ):
        self.repository = (
            repository or ConceptVersionRepository()
        )
        self.completion_repository = (
            completion_repository or CompletionQueueRepository()
        )
        self.validator = (
            validator or ConceptValidationEngine()
        )
        self.history = history or ConceptHistory()

    # ======================================================
    # VALIDATION / COMPLETENESS
    # ======================================================

    def refresh(self, concept: Concept) -> dict:
        """
        Refresh system-managed completeness and return
        the canonical validation result.

        IMPORTANT:
        completeness is the number of completed visible
        Concept items, not a percentage.
        """

        completeness = refresh_completeness(concept)

        # --------------------------------------------------
        # Current Concept state sync
        # --------------------------------------------------
        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=completeness,
            )

        # --------------------------------------------------
        # Completion Queue sync
        # --------------------------------------------------
        if completeness >= 36:
            self.completion_repository.mark_completed(
                concept.system.database_id
            )

        validation = self.validator.validate(concept)

        return {
            "completeness": completeness,
            "validation": validation,
        }

    # ======================================================
    # SUBMISSION FOR REVIEW
    # ======================================================

    def submit_for_review(
        self,
        concept: Concept,
        *,
        user_id: str,
        creator_user_code: Optional[str] = None,
        source_mobile_id: Optional[str] = None,
    ) -> dict:
        """
        Submit a Concept to the canonical review lifecycle.

        Application layer only coordinates:
        validation, lifecycle, history and persistence.
        """

        # --------------------------------------------------
        # Refresh canonical completeness / validation
        # --------------------------------------------------
        validation_result = self.refresh(concept)

        # --------------------------------------------------
        # Lifecycle guard + transition
        # --------------------------------------------------
        lifecycle_result = lifecycle_submit_for_review(
            concept
        )

        if not lifecycle_result["success"]:
            return {
                "success": False,
                "reason": lifecycle_result["reason"],
                "validation": validation_result,
                "lifecycle": lifecycle_result,
            }

        # --------------------------------------------------
        # History
        # --------------------------------------------------
        self.history.record_submission(
            concept_code=concept.concept_code,
            version=concept.system.version,
            user_id=str(user_id),
            completeness=concept.completeness,
        )

        # --------------------------------------------------
        # Persistence — canonical v2 approval queue
        # --------------------------------------------------
        approval_id = self.repository.create_approval_submission(
            concept_id=concept.system.database_id,
            concept_code=concept.concept_code,
            version=concept.system.version,
            creator_user_code=creator_user_code,
            source_mobile_id=source_mobile_id,
            payload={
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "completeness": concept.completeness,
                "status": concept.status,
                "items": {
                    key: item.value
                    for key, item in concept.items.items()
                },
            },
        )

        # --------------------------------------------------
        # EventBus
        # --------------------------------------------------
        event_bus = get_event_bus()

        event_result = event_bus.emit(
            "KNOWLEDGE",
            "CONCEPT_SUBMITTED",
            "concept",
            {
                "user_id": str(user_id),
                "concept_id": concept.system.database_id,
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "completeness": concept.completeness,
                "approval_id": approval_id,
            },
        )

        return {
            "success": True,
            "concept_id": concept.system.database_id,
            "concept_code": concept.concept_code,
            "version": concept.system.version,
            "status": concept.status,
            "completeness": concept.completeness,
            "approval_id": approval_id,
            "validation": validation_result,
            "lifecycle": lifecycle_result,
            "event": event_result,
        }

    # ======================================================
    # APPROVAL
    # ======================================================

    def approve_submission(
        self,
        *,
        approval_id: int,
        approved_by: str,
    ) -> dict:
        """
        Approve a pending Concept submission.

        The pending submission is restored from the canonical
        approval queue. Permanent database identity is created
        only during approval.
        """

        # --------------------------------------------------
        # Load canonical pending submission
        # --------------------------------------------------
        submission = self.repository.get_approval_submission(
            approval_id
        )

        if not submission:
            return {
                "success": False,
                "reason": "APPROVAL_SUBMISSION_NOT_FOUND",
            }

        if submission["status"] != "SUBMITTED":
            return {
                "success": False,
                "reason": "APPROVAL_SUBMISSION_ALREADY_REVIEWED",
                "status": submission["status"],
            }

        import json

        payload = json.loads(submission["payload"])

        # --------------------------------------------------
        # Restore Concept from canonical queue snapshot
        # --------------------------------------------------
        concept = Concept()

        for key, value in payload.get("items", {}).items():
            if concept.has_valid_item_key(key):
                concept.set_item(
                    __import__(
                        "engines.tandil.knowledge.concept.models",
                        fromlist=["ConceptItem"],
                    ).ConceptItem(
                        item_key=key,
                        value=value,
                    )
                )

        concept.system.version = submission["version"]

        concept.system.status = payload.get(
            "status",
            "PENDING_REVIEW",
        )

        concept.system.completeness = payload.get(
            "completeness",
            0,
        )

        # --------------------------------------------------
        # Lifecycle transition
        # --------------------------------------------------
        lifecycle_result = lifecycle_approve(concept)

        if not lifecycle_result["success"]:
            return {
                "success": False,
                "reason": lifecycle_result["reason"],
                "lifecycle": lifecycle_result,
            }

        # --------------------------------------------------
        # Create permanent Concept identity at approval
        # --------------------------------------------------
        concept_code = self.repository.allocate_next_concept_code()

        assign_initial_identity(
            concept,
            concept_code,
        )

        concept_id = self.repository.create_concept(
            creator=submission["creator_user_code"],
            concept_code=concept.concept_code,
            version=concept.system.version,
            status=concept.status,
            completeness=concept.completeness,
        )

        concept.system.database_id = concept_id

        # --------------------------------------------------
        # Persist approved version
        # --------------------------------------------------
        version_id = self.repository.create_version(
            concept_id=concept_id,
            concept_code=concept.concept_code,
            version=concept.system.version,
            payload=payload,
            completeness=concept.completeness,
            status="PENDING_REVIEW",
            created_by=str(approved_by),
        )

        # --------------------------------------------------
        # Mark canonical version as approved
        # --------------------------------------------------
        version_result = self.repository.approve_version(
            concept_code=concept.concept_code,
            version=concept.system.version,
            approved_by=str(approved_by),
        )

        if not version_result:
            return {
                "success": False,
                "reason": "CONCEPT_VERSION_APPROVAL_FAILED",
                "concept_id": concept_id,
                "version_id": version_id,
            }

        # --------------------------------------------------
        # Mark queue as approved
        # --------------------------------------------------
        queue_result = (
            self.repository.approve_approval_submission(
                approval_id=approval_id,
                approved_by=str(approved_by),
                concept_id=concept_id,
            )
        )

        if not queue_result:
            return {
                "success": False,
                "reason": "APPROVAL_QUEUE_UPDATE_FAILED",
                "concept_id": concept_id,
                "version_id": version_id,
            }

        # --------------------------------------------------
        # History
        # --------------------------------------------------
        self.history.record_approval(
            concept_code=concept.concept_code,
            version=concept.system.version,
            approved_by=str(approved_by),
            completeness=concept.completeness,
        )

        # --------------------------------------------------
        # Persistent History
        # --------------------------------------------------
        self.repository.add_history(
            concept_id=concept_id,
            concept_code=concept.concept_code,
            version=concept.system.version,
            actor=str(approved_by),
            event_type="APPROVED",
            from_state="PENDING_REVIEW",
            to_state="APPROVED",
            details={
                "approval_id": approval_id,
                "completeness": concept.completeness,
            },
        )

        # --------------------------------------------------
        # EventBus
        # --------------------------------------------------
        event_bus = get_event_bus()

        event_result = event_bus.emit(
            "KNOWLEDGE",
            "CONCEPT_APPROVED",
            "concept",
            {
                "concept_id": concept_id,
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "approved_by": str(approved_by),
                "approval_id": approval_id,
                "completeness": concept.completeness,
            },
        )

        return {
            "success": True,
            "concept_id": concept_id,
            "concept_code": concept.concept_code,
            "version": concept.system.version,
            "status": concept.status,
            "completeness": concept.completeness,
            "approval_id": approval_id,
            "version_id": version_id,
            "approved_by": str(approved_by),
            "lifecycle": lifecycle_result,
            "event": event_result,
        }

    # ======================================================
    # REJECTION
    # ======================================================

    def reject_submission(
        self,
        concept: Concept,
        *,
        approval_id: int,
        rejected_by: str,
        rejection_reason: str,
    ) -> dict:
        """
        Reject a Concept through the canonical application flow.

        Coordinates:
        - lifecycle rejection
        - approval queue persistence
        - Concept history
        - EventBus
        """

        # --------------------------------------------------
        # Validate rejection reason
        # --------------------------------------------------
        if not rejection_reason or not str(
            rejection_reason
        ).strip():
            return {
                "success": False,
                "reason": "REJECTION_REASON_REQUIRED",
            }

        # --------------------------------------------------
        # Lifecycle transition
        # --------------------------------------------------
        lifecycle_result = reject(
            concept,
            reason=str(rejection_reason),
        )

        if not lifecycle_result["success"]:
            return {
                "success": False,
                "reason": lifecycle_result["reason"],
                "lifecycle": lifecycle_result,
            }

        # --------------------------------------------------
        # Approval queue
        # --------------------------------------------------
        queue_result = (
            self.repository.reject_approval_submission(
                approval_id=approval_id,
                rejected_by=str(rejected_by),
                rejection_reason=str(rejection_reason),
            )
        )

        if not queue_result:
            return {
                "success": False,
                "reason": (
                    "APPROVAL_SUBMISSION_NOT_FOUND_OR_"
                    "ALREADY_REVIEWED"
                ),
                "lifecycle": lifecycle_result,
            }

        # --------------------------------------------------
        # Canonical version persistence
        #
        # New Concepts do not have a permanent Concept Version
        # yet. Their first Version is created only at approval.
        #
        # Therefore:
        # - New submission: Approval Queue is the persistence
        #   authority for rejection.
        # - Existing Concept: reject its existing Version.
        # --------------------------------------------------

        version_result = True

        if concept.system.database_id is not None:
            version_result = self.repository.reject_version(
                concept_code=concept.concept_code,
                version=concept.system.version,
                rejected_by=str(rejected_by),
                rejection_reason=str(rejection_reason),
            )

            if not version_result:
                return {
                    "success": False,
                    "reason": "CONCEPT_VERSION_REJECTION_FAILED",
                    "lifecycle": lifecycle_result,
                }

        # --------------------------------------------------
        # Current Concept state
        # --------------------------------------------------
        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=concept.completeness,
            )

        # --------------------------------------------------
        # History
        # --------------------------------------------------
        self.history.record_rejection(
            concept_code=concept.concept_code,
            version=concept.system.version,
            approved_by=str(rejected_by),
            completeness=concept.completeness,
            reason=str(rejection_reason),
        )

        # --------------------------------------------------
        # EventBus
        # --------------------------------------------------
        event_bus = get_event_bus()

        event_result = event_bus.emit(
            "KNOWLEDGE",
            "CONCEPT_REJECTED",
            "concept",
            {
                "concept_id": concept.system.database_id,
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "rejected_by": str(rejected_by),
                "rejection_reason": str(rejection_reason),
                "approval_id": approval_id,
                "completeness": concept.completeness,
            },
        )

        return {
            "success": True,
            "concept_id": concept.system.database_id,
            "concept_code": concept.concept_code,
            "version": concept.system.version,
            "status": concept.status,
            "completeness": concept.completeness,
            "approval_id": approval_id,
            "rejected_by": str(rejected_by),
            "rejection_reason": str(rejection_reason),
            "lifecycle": lifecycle_result,
            "event": event_result,
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

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        previous_value = item.value

        item.value = value
        item.completed_by = str(user_id)
        item.completed_at = timestamp
        item.status = "APPROVED"

        # --------------------------------------------------
        # Canonical completeness = completed item count
        # --------------------------------------------------
        completeness = refresh_completeness(concept)

        # --------------------------------------------------
        # Persist current Concept state
        # --------------------------------------------------
        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=completeness,
            )

        # --------------------------------------------------
        # Completion Queue
        # --------------------------------------------------
        if completeness >= 36:
            self.completion_repository.mark_completed(
                concept.system.database_id
            )

        # --------------------------------------------------
        # History
        # --------------------------------------------------
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

        # --------------------------------------------------
        # EventBus
        # --------------------------------------------------
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
                "completeness": completeness,
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
    # LIFECYCLE HELPERS
    # ======================================================

    def reopen(
        self,
        concept: Concept,
        *,
        reason: Optional[str] = None,
    ) -> dict:
        """
        Reopen a rejected Concept.
        """

        result = reopen(concept)

        if not result["success"]:
            return result

        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=concept.completeness,
            )

        return result

    def publish(
        self,
        concept: Concept,
        *,
        reason: Optional[str] = None,
    ) -> dict:
        """
        Publish an approved Concept.

        Lifecycle remains the single authority for
        publication guards.
        """

        result = publish(
        concept,
        )

        if not result["success"]:
            return result

        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=concept.completeness,
            )

        event_bus = get_event_bus()

        event_bus.emit(
            source="KNOWLEDGE",
            event_type="CONCEPT_PUBLISHED",
            target="knowledge",
            value={
                "concept_id": concept.system.database_id,
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "completeness": concept.completeness,
            },
        )

        return result

    def archive(
        self,
        concept: Concept,
        *,
        reason: Optional[str] = None,
    ) -> dict:
        """
        Archive a published Concept.
        """

        result = archive(
            concept,
            reason=reason,
        )

        if not result["success"]:
            return result

        if concept.system.database_id is not None:
            self.repository.update_current_state(
                concept_id=concept.system.database_id,
                version=concept.system.version,
                status=concept.status,
                completeness=concept.completeness,
            )

        return result

    # ======================================================
    # IDENTITY HELPERS
    # ======================================================

    def assign_identity(
        self,
        concept: Concept,
        *,
        creator: Optional[str] = None,
    ) -> dict:
        """
        Assign initial Concept identity through the identity
        domain engine.
        """

        result = assign_initial_identity(
            concept,
            creator=creator,
        )

        return result

    def create_revision(
        self,
        concept: Concept,
    ) -> dict:
        """
        Create a new Concept revision through the identity
        domain engine.
        """

        return create_revision(concept)
