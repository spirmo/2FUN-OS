from typing import Dict, Any, List, Optional


REQUIRED_FIELDS = [
    "source",
    "event_type",
    "target",
    "value",
    "event_id",
    "trace_path",
]


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures every event is structurally safe across the pipeline.
    """

    normalized = dict(event)

    # Required fields safety
    normalized.setdefault("source", "unknown")
    normalized.setdefault("event_type", "UNKNOWN")
    normalized.setdefault("target", "unknown")
    normalized.setdefault("value", {})
    normalized.setdefault("event_id", None)

    # Critical invariants
    normalized.setdefault("trace_path", [])
    normalized.setdefault("audit", None)

    return normalized


def validate_event(event: Dict[str, Any]) -> Dict[str, Any]:
    missing = [f for f in REQUIRED_FIELDS if f not in event]

    if missing:
        return {
            "valid": False,
            "reason": "MISSING_REQUIRED_FIELDS",
            "missing": missing,
        }

    return {
        "valid": True,
        "reason": "OK",
        "missing": [],
    }
