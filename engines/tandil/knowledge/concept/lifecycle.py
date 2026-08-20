"""
2FUN / TANDIL
Concept Engine — Lifecycle

Single authority for Concept lifecycle state transitions.

Lifecycle:

OPEN_FOR_COMPLETION
        ↓
PENDING_REVIEW
        ↓
APPROVED
        ↓
PUBLISHED
        ↓
ARCHIVED

Rejection:

PENDING_REVIEW
        ↓
REJECTED
        ↓
OPEN_FOR_COMPLETION

Lifecycle does not generate Concept Codes.
Concept identity remains the responsibility of identity.py.
"""

from typing import Optional

from .contract import CONCEPT_STATES
from .completeness import (
    has_all_mandatory_items,
    is_complete as completeness_is_complete,
)


# ==========================================================
# LIFECYCLE TRANSITIONS
# ==========================================================

VALID_LIFECYCLE_TRANSITIONS = {
    "OPEN_FOR_COMPLETION": (
        "PENDING_REVIEW",
    ),

    "PENDING_REVIEW": (
        "APPROVED",
        "REJECTED",
    ),

    "APPROVED": (
        "PUBLISHED",
    ),

    "PUBLISHED": (
        "ARCHIVED",
    ),

    "REJECTED": (
        "OPEN_FOR_COMPLETION",
    ),

    "ARCHIVED": (),
}


# ==========================================================
# STATE VALIDATION
# ==========================================================

def is_valid_state(state: str) -> bool:
    """Return True when state belongs to the locked Concept Contract."""

    return state in CONCEPT_STATES


def can_transition(
    current_state: str,
    next_state: str,
) -> bool:
    """Check whether a lifecycle transition is structurally allowed."""

    if not is_valid_state(current_state):
        return False

    if not is_valid_state(next_state):
        return False

    return next_state in VALID_LIFECYCLE_TRANSITIONS.get(
        current_state,
        (),
    )


# ==========================================================
# TRANSITION GUARDS
# ==========================================================

def can_submit_for_review(concept) -> bool:
    """
    A Concept can enter review only when all 11 mandatory
    visible items are complete.
    """

    return has_all_mandatory_items(concept)


def can_publish(concept) -> bool:
    """
    A Concept can be published only when all 36 visible
    items are complete.
    """

    return completeness_is_complete(concept)


# ==========================================================
# LIFECYCLE TRANSITION
# ==========================================================

def transition(
    concept,
    next_state: str,
    *,
    reason: Optional[str] = None,
) -> dict:
    """
    Perform one validated Concept lifecycle transition.

    The Concept object is updated only after all transition
    guards pass.
    """

    current_state = concept.status

    # ------------------------------------------------------
    # Validate requested state
    # ------------------------------------------------------

    if not is_valid_state(next_state):
        return {
            "success": False,
            "reason": "INVALID_NEXT_STATE",
            "previous_state": current_state,
            "current_state": current_state,
            "requested_state": next_state,
        }

    # ------------------------------------------------------
    # Validate structural transition
    # ------------------------------------------------------

    if not can_transition(current_state, next_state):
        return {
            "success": False,
            "reason": "INVALID_TRANSITION",
            "previous_state": current_state,
            "current_state": current_state,
            "requested_state": next_state,
        }

    # ------------------------------------------------------
    # Submission guard
    # ------------------------------------------------------

    if next_state == "PENDING_REVIEW":
        if not can_submit_for_review(concept):
            return {
                "success": False,
                "reason": "MANDATORY_ITEMS_INCOMPLETE",
                "previous_state": current_state,
                "current_state": current_state,
                "requested_state": next_state,
            }

    # ------------------------------------------------------
    # Publication guard
    # ------------------------------------------------------

    if next_state == "PUBLISHED":
        if not can_publish(concept):
            return {
                "success": False,
                "reason": "CONCEPT_NOT_COMPLETE",
                "previous_state": current_state,
                "current_state": current_state,
                "requested_state": next_state,
            }

    # ------------------------------------------------------
    # Apply transition
    # ------------------------------------------------------

    concept.status = next_state

    return {
        "success": True,
        "previous_state": current_state,
        "current_state": next_state,
        "requested_state": next_state,
        "reason": reason,
    }


# ==========================================================
# CONVENIENCE OPERATIONS
# ==========================================================

def submit_for_review(concept) -> dict:
    """Move Concept from OPEN_FOR_COMPLETION to PENDING_REVIEW."""

    return transition(
        concept,
        "PENDING_REVIEW",
    )


def approve(concept, reason: Optional[str] = None) -> dict:
    """Move Concept from PENDING_REVIEW to APPROVED."""

    return transition(
        concept,
        "APPROVED",
        reason=reason,
    )


def reject(
    concept,
    reason: Optional[str] = None,
) -> dict:
    """Move Concept from PENDING_REVIEW to REJECTED."""

    return transition(
        concept,
        "REJECTED",
        reason=reason,
    )


def reopen(concept) -> dict:
    """Return a rejected Concept to OPEN_FOR_COMPLETION."""

    return transition(
        concept,
        "OPEN_FOR_COMPLETION",
    )


def publish(concept) -> dict:
    """Move a fully completed approved Concept to PUBLISHED."""

    return transition(
        concept,
        "PUBLISHED",
    )


def archive(concept) -> dict:
    """Archive a published Concept."""

    return transition(
        concept,
        "ARCHIVED",
    )
