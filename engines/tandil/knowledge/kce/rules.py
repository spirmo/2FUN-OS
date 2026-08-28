VALID_TRANSITIONS = {
    "NEW": ["DRAFT"],
    "DRAFT": ["NEED_COMPLETION", "UNDER_REVIEW"],
    "NEED_COMPLETION": ["UNDER_REVIEW"],
    "UNDER_REVIEW": ["APPROVED"],
    "APPROVED": ["PUBLISHED"],
    "PUBLISHED": ["ARCHIVED"],
    "ARCHIVED": [],
}

def calculate_completeness(metadata: dict) -> int:
    """
    Concept completeness based on 36 approved items.
    """

    approved_items = 0

    for key, value in metadata.items():
        if value and value != "Pending":
            approved_items += 1

    return approved_items


def get_completion_status(completeness: int) -> str:
    if completeness < 11:
        return "INVALID"

    if completeness < 36:
        return "NEED_COMPLETION"

    return "COMPLETE"


def can_transition(current_state: str, next_state: str) -> bool:
    """
    Check whether a state transition is allowed.
    """
    return next_state in VALID_TRANSITIONS.get(current_state, [])


def minimum_validation(node) -> bool:
    """
    KD-001 Minimum Validation
    """

    required = [
        node.node_id,
        node.domain,
        node.status,
        node.metadata.get("persian_title"),
    ]

    return all(required)
