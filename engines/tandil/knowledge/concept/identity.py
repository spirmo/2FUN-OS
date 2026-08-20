"""
2FUN / TANDIL
Concept Engine — Identity

Responsible for:
- Permanent Concept Code
- Concept Version
- Identity preservation across revisions
"""

import re

CONCEPT_CODE_PREFIX = "C"
CONCEPT_CODE_WIDTH = 6


def format_concept_code(number: int) -> str:
    """Create the permanent public Concept Code."""

    if not isinstance(number, int) or number <= 0:
        raise ValueError("Concept code number must be a positive integer.")

    return f"{CONCEPT_CODE_PREFIX}{number:0{CONCEPT_CODE_WIDTH}d}"


def is_valid_concept_code(code: str) -> bool:
    """Validate a Concept Code."""

    if not isinstance(code, str):
        return False

    pattern = rf"^{CONCEPT_CODE_PREFIX}\d{{{CONCEPT_CODE_WIDTH}}}$"
    return bool(re.fullmatch(pattern, code))


def initial_version() -> str:
    """Return the first approved Concept version."""

    return "1.0"


def next_version(current_version: str) -> str:
    """
    Generate the next Concept version.

    Examples:
        1.0 -> 1.1
        1.1 -> 1.2
        1.9 -> 1.10
    """

    if not isinstance(current_version, str):
        raise ValueError("Invalid Concept version.")

    parts = current_version.split(".")

    if len(parts) != 2:
        raise ValueError("Concept version must have format MAJOR.MINOR.")

    try:
        major = int(parts[0])
        minor = int(parts[1])
    except ValueError as exc:
        raise ValueError("Invalid Concept version.") from exc

    if major < 0 or minor < 0:
        raise ValueError("Concept version numbers cannot be negative.")

    return f"{major}.{minor + 1}"


def assign_initial_identity(concept, code: str) -> None:
    """
    Assign the permanent Concept Code after approval.

    This operation must never overwrite an existing identity.
    """

    if not is_valid_concept_code(code):
        raise ValueError(f"Invalid Concept Code: {code}")

    if concept.concept_code is not None:
        raise ValueError("Concept already has a permanent identity.")

    concept.concept_code = code
    concept.system.concept_code = code
    concept.system.version = initial_version()


def preserve_identity(concept, code: str) -> None:
    """
    Verify that a revision still belongs to the same Concept.
    """

    if concept.concept_code != code:
        raise ValueError(
            "Concept identity mismatch. "
            "A Concept Code cannot change during revision."
        )

    if concept.system.concept_code != code:
        raise ValueError(
            "System Concept Code does not match permanent identity."
        )


def create_revision(concept) -> str:
    """
    Create the next version of an already identified Concept.
    """

    if not concept.has_permanent_identity():
        raise ValueError(
            "Cannot create a revision before permanent Concept identity."
        )

    current = concept.system.version
    new_version = next_version(current)

    concept.system.version = new_version

    return new_version
