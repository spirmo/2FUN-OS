from typing import Dict, List, Tuple

# ==========================================================
# KNOWLEDGE INJECTION VALIDATOR (MVP v1.1)
# ==========================================================

MINIMUM_FIELDS = [
    "node_id",
    "persian_title",
    "category",
    "creator",
    "created_at",
]

OPTIONAL_FIELDS = [
    "canonical_meaning",
    "definition",
    "source",
    "translations",
    "other_languages",
    "related_concepts",
    "questions",
    "missions",
    "tags",
    "difficulty",
    "notes",
]


def _has_value(value) -> bool:
    """Returns True if a field contains meaningful data."""
    if value is None:
        return False

    if isinstance(value, str):
        return value.strip() != ""

    if isinstance(value, (list, dict)):
        return len(value) > 0

    return True


def calculate_completeness(data: Dict) -> int:
    """
    Calculates node completeness percentage.
    """

    total = len(MINIMUM_FIELDS) + len(OPTIONAL_FIELDS)
    completed = 0

    for field in MINIMUM_FIELDS:
        if _has_value(data.get(field)):
            completed += 1

    for field in OPTIONAL_FIELDS:
        if _has_value(data.get(field)):
            completed += 1

    return round((completed / total) * 100)


def validate_node(data: Dict) -> Tuple[bool, List[str], Dict]:
    """
    Returns:
        valid
        errors
        metadata
    """

    errors = []

    for field in MINIMUM_FIELDS:
        if not _has_value(data.get(field)):
            errors.append(f"Missing required field: {field}")

    completeness = calculate_completeness(data)

    if errors:
        status = "NEED_COMPLETION"
    else:
        status = data.get("status", "DRAFT")

    metadata = {
        "status": status,
        "completeness": completeness,
    }

    return len(errors) == 0, errors, metadata
