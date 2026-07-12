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
    required = [
        "Concept Code",
        "Domain",
        "Status",
        "Persian Title",
    ]

    optional = [
        "Canonical Title",
        "Definition",
        "Evidence",
        "Sources",
        "Questions",
        "Missions",
        "Snapshot",
    ]

    total = len(required) + len(optional)
    score = 0

    for field in required:
        if metadata.get(field):
            score += 1

    for field in optional:
        value = metadata.get(field)
        if value and value != "Pending":
            score += 1

    return int((score / total) * 100)


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
        node.metadata.get("Persian Title"),
    ]

    return all(required)
