"""
2FUN / TANDIL
Concept Engine
Item Status System
"""

from .contract import ITEM_STATUSES


# ==========================================================
# ITEM STATUS CONSTANTS
# ==========================================================

NOT_STARTED = "NOT_STARTED"
PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"


# ==========================================================
# STATUS PRESENTATION
# ==========================================================

STATUS_PRESENTATION = {
    NOT_STARTED: {
        "color": "WHITE",
        "icon": "DEFAULT",
    },
    PENDING: {
        "color": "YELLOW",
        "icon": "PENDING",
    },
    APPROVED: {
        "color": "GREEN",
        "icon": "CHECK",
    },
    REJECTED: {
        "color": "RED",
        "icon": "REJECT",
    },
}


# ==========================================================
# VALIDATION
# ==========================================================

def is_valid_status(status: str) -> bool:
    return status in ITEM_STATUSES


# ==========================================================
# STATUS PRESENTATION
# ==========================================================

def get_status_presentation(status: str) -> dict:
    if not is_valid_status(status):
        raise ValueError(
            f"Invalid item status: {status}"
        )

    return dict(STATUS_PRESENTATION[status])


# ==========================================================
# STATUS TRANSITIONS
# ==========================================================

VALID_STATUS_TRANSITIONS = {
    NOT_STARTED: (
        PENDING,
    ),

    PENDING: (
        APPROVED,
        REJECTED,
    ),

    REJECTED: (
        PENDING,
    ),

    APPROVED: (),
}


def can_transition(
    current_status: str,
    next_status: str,
) -> bool:

    if not is_valid_status(current_status):
        return False

    if not is_valid_status(next_status):
        return False

    return next_status in VALID_STATUS_TRANSITIONS.get(
        current_status,
        (),
    )


# ==========================================================
# STATUS CHANGE
# ==========================================================

def transition_status(
    current_status: str,
    next_status: str,
) -> dict:

    if not is_valid_status(current_status):
        return {
            "success": False,
            "reason": "INVALID_CURRENT_STATUS",
            "current": current_status,
            "requested": next_status,
        }

    if not is_valid_status(next_status):
        return {
            "success": False,
            "reason": "INVALID_NEXT_STATUS",
            "current": current_status,
            "requested": next_status,
        }

    if not can_transition(
        current_status,
        next_status,
    ):
        return {
            "success": False,
            "reason": "INVALID_TRANSITION",
            "current": current_status,
            "requested": next_status,
        }

    return {
        "success": True,
        "previous": current_status,
        "current": next_status,
        "presentation": get_status_presentation(
            next_status
        ),
    }
