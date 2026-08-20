"""
UVI Exceptions
"""


class UVIError(Exception):
    """Base UVI exception."""


class InvalidValueEvent(UVIError):
    """Invalid value event."""


class InvalidTransaction(UVIError):
    """Invalid value transaction."""


class DuplicateEvent(UVIError):
    """Duplicate value event."""


class ConversionError(UVIError):
    """Value conversion failure."""
