"""Canonical value-unit identifiers for 2FUN."""

POINT = "POINT"
LEGACY_XP = "XP"
XP = POINT  # Compatibility alias: 1 XP = 1 POINT


def canonicalize_unit(unit: str) -> str:
    """Map the legacy XP label to canonical POINT."""
    return POINT if unit == LEGACY_XP else unit


DRIKA = "Drika"
SHIR = "SHIR"
SIGMA_SHIR = "SIGMA_SHIR"
TWOFUNC = "2FUNC"
DRIK = "Drik"
