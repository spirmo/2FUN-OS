"""
2FUN / TANDIL
Concept Engine — History

Append-only Concept lifecycle history.

History records:
- item completion
- item changes
- user participation
- reward information
- submission
- approval / rejection
- version creation
- Knowledge Engine delivery
- completion milestones
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


HISTORY_VERSION = "1.0"


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ConceptHistoryEvent:
    """
    Immutable representation of one Concept history event.
    """

    event_type: str
    concept_code: Optional[str] = None
    version: Optional[str] = None

    user_id: Optional[str] = None
    item_key: Optional[str] = None

    previous_value: Any = None
    new_value: Any = None

    previous_status: Optional[str] = None
    new_status: Optional[str] = None

    completeness: Optional[int] = None

    base_score: int = 0
    difficulty_bonus: int = 0
    multiplier: float = 1.0
    earned_score: int = 0

    approved_by: Optional[str] = None
    reason: Optional[str] = None

    timestamp: str = ""
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the event."""

        return asdict(self)


class ConceptHistory:
    """
    Append-only history container.

    Existing events are never modified or deleted.
    """

    def __init__(self, events: Optional[List[Dict[str, Any]]] = None):
        self._events: List[Dict[str, Any]] = list(events or [])

    @property
    def events(self) -> List[Dict[str, Any]]:
        """
        Return a copy of the history.
        """

        return list(self._events)

    @property
    def count(self) -> int:
        return len(self._events)

    def append(
        self,
        event_type: str,
        *,
        concept_code: Optional[str] = None,
        version: Optional[str] = None,
        user_id: Optional[str] = None,
        item_key: Optional[str] = None,
        previous_value: Any = None,
        new_value: Any = None,
        previous_status: Optional[str] = None,
        new_status: Optional[str] = None,
        completeness: Optional[int] = None,
        base_score: int = 0,
        difficulty_bonus: int = 0,
        multiplier: float = 1.0,
        earned_score: int = 0,
        approved_by: Optional[str] = None,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> ConceptHistoryEvent:
        """
        Append one immutable event.
        """

        if not event_type or not str(event_type).strip():
            raise ValueError("event_type is required.")

        if completeness is not None:
            if not 0 <= completeness <= 100:
                raise ValueError(
                    "completeness must be between 0 and 100."
                )

        event = ConceptHistoryEvent(
            event_type=event_type,
            concept_code=concept_code,
            version=version,
            user_id=user_id,
            item_key=item_key,
            previous_value=previous_value,
            new_value=new_value,
            previous_status=previous_status,
            new_status=new_status,
            completeness=completeness,
            base_score=base_score,
            difficulty_bonus=difficulty_bonus,
            multiplier=multiplier,
            earned_score=earned_score,
            approved_by=approved_by,
            reason=reason,
            timestamp=timestamp or utc_now(),
            metadata=dict(metadata) if metadata else None,
        )

        self._events.append(event.to_dict())

        return event

    def record_item_completion(
        self,
        *,
        concept_code: Optional[str],
        version: Optional[str],
        user_id: str,
        item_key: str,
        new_value: Any,
        completeness: int,
        base_score: int,
        difficulty_bonus: int,
        multiplier: float,
        earned_score: int,
    ) -> ConceptHistoryEvent:
        """Record a user's completion of a Concept item."""

        return self.append(
            "ITEM_COMPLETED",
            concept_code=concept_code,
            version=version,
            user_id=user_id,
            item_key=item_key,
            new_value=new_value,
            completeness=completeness,
            base_score=base_score,
            difficulty_bonus=difficulty_bonus,
            multiplier=multiplier,
            earned_score=earned_score,
        )

    def record_item_update(
        self,
        *,
        concept_code: Optional[str],
        version: Optional[str],
        user_id: str,
        item_key: str,
        previous_value: Any,
        new_value: Any,
        completeness: int,
    ) -> ConceptHistoryEvent:
        """Record a change to an existing item."""

        return self.append(
            "ITEM_UPDATED",
            concept_code=concept_code,
            version=version,
            user_id=user_id,
            item_key=item_key,
            previous_value=previous_value,
            new_value=new_value,
            completeness=completeness,
        )

    def record_submission(
        self,
        *,
        concept_code: Optional[str],
        version: Optional[str],
        user_id: str,
        completeness: int,
    ) -> ConceptHistoryEvent:
        """Record submission to the approval queue."""

        return self.append(
            "SUBMITTED_FOR_APPROVAL",
            concept_code=concept_code,
            version=version,
            user_id=user_id,
            completeness=completeness,
        )

    def record_approval(
        self,
        *,
        concept_code: str,
        version: str,
        approved_by: str,
        completeness: int,
    ) -> ConceptHistoryEvent:
        """Record Founder/System approval."""

        return self.append(
            "APPROVED",
            concept_code=concept_code,
            version=version,
            completeness=completeness,
            approved_by=approved_by,
            new_status="APPROVED",
        )

    def record_rejection(
        self,
        *,
        concept_code: Optional[str],
        version: Optional[str],
        approved_by: str,
        completeness: int,
        reason: str,
    ) -> ConceptHistoryEvent:
        """Record rejection."""

        return self.append(
            "REJECTED",
            concept_code=concept_code,
            version=version,
            completeness=completeness,
            approved_by=approved_by,
            new_status="REJECTED",
            reason=reason,
        )

    def record_version_created(
        self,
        *,
        concept_code: str,
        previous_version: str,
        new_version: str,
        completeness: int,
    ) -> ConceptHistoryEvent:
        """Record creation of a new approved Concept revision."""

        return self.append(
            "VERSION_CREATED",
            concept_code=concept_code,
            version=new_version,
            completeness=completeness,
            metadata={
                "previous_version": previous_version,
                "new_version": new_version,
            },
        )

    def record_knowledge_delivery(
        self,
        *,
        concept_code: str,
        version: str,
        completeness: int,
    ) -> ConceptHistoryEvent:
        """Record delivery of an approved Concept version to Knowledge Engine."""

        return self.append(
            "KNOWLEDGE_ENGINE_DELIVERY",
            concept_code=concept_code,
            version=version,
            completeness=completeness,
        )

    def record_completion(
        self,
        *,
        concept_code: str,
        version: str,
    ) -> ConceptHistoryEvent:
        """Record the moment Concept reaches 36/36."""

        return self.append(
            "CONCEPT_COMPLETED",
            concept_code=concept_code,
            version=version,
            completeness=100,
            new_status="COMPLETE",
        )

    def filter_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Return events of one type."""

        return [
            event
            for event in self._events
            if event["event_type"] == event_type
        ]

    def filter_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Return all events created by one user."""

        return [
            event
            for event in self._events
            if event["user_id"] == user_id
        ]

    def filter_by_item(self, item_key: str) -> List[Dict[str, Any]]:
        """Return all events related to one item."""

        return [
            event
            for event in self._events
            if event["item_key"] == item_key
        ]

    def last_event(self) -> Optional[Dict[str, Any]]:
        """Return the latest event."""

        if not self._events:
            return None

        return self._events[-1]

    def to_list(self) -> List[Dict[str, Any]]:
        """Return a serializable copy."""

        return [dict(event) for event in self._events]
