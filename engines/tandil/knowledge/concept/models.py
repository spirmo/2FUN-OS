"""
2FUN / TANDIL
Concept Engine Models

Internal domain models for the Concept Engine.
Database persistence is handled separately.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .contract import (
    CONCEPT_ENGINE_VERSION,
    ITEM_STATUSES,
    CONCEPT_STATES,
    MANDATORY_ITEMS,
    OPTIONAL_ITEMS,
    SYSTEM_ITEMS,
)


# ==========================================================
# CONCEPT ITEM
# ==========================================================

@dataclass
class ConceptItem:
    """
    A single visible Concept item.

    Each item has:
    - a fixed contract key
    - a value
    - required/optional classification
    - status
    - score
    - completion metadata
    """

    item_key: str
    value: Any = None

    is_required: bool = False

    status: str = "NOT_STARTED"

    base_score: int = 0
    earned_score: int = 0

    completed_by: Optional[str] = None
    completed_at: Optional[str] = None

    validation_note: Optional[str] = None


# ==========================================================
# CONCEPT SYSTEM METADATA
# ==========================================================

@dataclass
class ConceptSystemMetadata:
    """
    Internal system-managed Concept metadata.

    These fields are never entered manually by the user.
    """

    node_id: Optional[str] = None
    concept_code: Optional[str] = None
    database_id: Optional[int] = None
    topic_id: Optional[int] = None

    creator: Optional[str] = None
    created_at: Optional[str] = None

    status: str = "OPEN_FOR_COMPLETION"

    completeness: int = 0

    history: List[Dict[str, Any]] = field(default_factory=list)

    version: str = CONCEPT_ENGINE_VERSION

    snapshot_reference: Optional[str] = None


# ==========================================================
# CONCEPT
# ==========================================================

@dataclass
class Concept:
    """
    Core Concept domain entity.

    Concept is an independent architectural entity.
    """

    # Permanent identity
    concept_code: Optional[str] = None

    # Visible items
    items: Dict[str, ConceptItem] = field(default_factory=dict)

    # System metadata
    system: ConceptSystemMetadata = field(
        default_factory=ConceptSystemMetadata
    )

    # ======================================================
    # CONTRACT VALIDATION
    # ======================================================

    def has_valid_item_key(self, item_key: str) -> bool:
        return (
            item_key in MANDATORY_ITEMS
            or item_key in OPTIONAL_ITEMS
        )

    def is_system_item(self, item_key: str) -> bool:
        return item_key in SYSTEM_ITEMS

    # ======================================================
    # ITEM ACCESS
    # ======================================================

    def get_item(self, item_key: str) -> Optional[ConceptItem]:
        return self.items.get(item_key)

    def set_item(self, item: ConceptItem) -> None:
        if not self.has_valid_item_key(item.item_key):
            raise ValueError(
                f"Invalid Concept item: {item.item_key}"
            )

        self.items[item.item_key] = item

    # ======================================================
    # STATUS
    # ======================================================

    @property
    def status(self) -> str:
        return self.system.status

    @status.setter
    def status(self, value: str) -> None:
        if value not in CONCEPT_STATES:
            raise ValueError(
                f"Invalid Concept state: {value}"
            )

        self.system.status = value

    # ======================================================
    # COMPLETENESS
    # ======================================================

    @property
    def completeness(self) -> int:
        return self.system.completeness

    @completeness.setter
    def completeness(self, value: int) -> None:
        if not 0 <= value <= 100:
            raise ValueError(
                "Completeness must be between 0 and 100."
            )

        self.system.completeness = value

    # ======================================================
    # IDENTITY
    # ======================================================

    def has_permanent_identity(self) -> bool:
        return bool(self.concept_code)

    # ======================================================
    # CONTRACT COUNTS
    # ======================================================

    @staticmethod
    def mandatory_count() -> int:
        return len(MANDATORY_ITEMS)

    @staticmethod
    def optional_count() -> int:
        return len(OPTIONAL_ITEMS)

    @staticmethod
    def system_count() -> int:
        return len(SYSTEM_ITEMS)

    @staticmethod
    def visible_item_count() -> int:
        return len(MANDATORY_ITEMS) + len(OPTIONAL_ITEMS)


# ==========================================================
# ITEM STATUS SNAPSHOT
# ==========================================================

@dataclass
class ItemStatusSnapshot:
    """
    Immutable-style representation of an item's status change.
    """

    item_key: str
    previous_status: str
    new_status: str

    changed_by: Optional[str] = None
    changed_at: Optional[str] = None

    reason: Optional[str] = None


# ==========================================================
# ITEM SCORE SNAPSHOT
# ==========================================================

@dataclass
class ItemScoreSnapshot:
    """
    Score information for one Concept item.
    """

    item_key: str

    base_score: int = 0
    multiplier: float = 1.0
    earned_score: int = 0

    awarded_to: Optional[str] = None
    awarded_at: Optional[str] = None


# ==========================================================
# VALIDATION RESULT
# ==========================================================

@dataclass
class ConceptValidationResult:
    """
    Standard result returned by Concept validation.
    """

    valid: bool

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    missing_required_items: List[str] = field(
        default_factory=list
    )

    completeness: int = 0


# ==========================================================
# LIFECYCLE RESULT
# ==========================================================

@dataclass
class ConceptLifecycleResult:
    """
    Standard result returned by lifecycle operations.
    """

    success: bool

    previous_state: Optional[str] = None
    current_state: Optional[str] = None

    concept_code: Optional[str] = None

    reason: Optional[str] = None
