"""
2FUN Universal Value Infrastructure (UVI)
Universal Value Source Registry
"""

from typing import Any, Dict


class ValueSourceRegistry:
    """
    Registry مرکزی منابع ارزش UVI.

    این کلاس فقط مسئول ثبت و شناسایی Sourceهاست.
    منطق محاسبه ارزش نباید داخل Registry قرار بگیرد.
    """

    def __init__(self):
        self._sources: Dict[str, Any] = {}

    def register(self, source: str, adapter: Any) -> None:
        if not source:
            raise ValueError("source is required")

        if source in self._sources:
            raise ValueError(f"source already registered: {source}")

        self._sources[source] = adapter

    def unregister(self, source: str) -> None:
        self._sources.pop(source, None)

    def get(self, source: str) -> Any:
        return self._sources.get(source)

    def require(self, source: str) -> Any:
        adapter = self.get(source)

        if adapter is None:
            raise KeyError(f"source not registered: {source}")

        return adapter

    def has(self, source: str) -> bool:
        return source in self._sources

    def sources(self) -> list[str]:
        return sorted(self._sources.keys())

    def count(self) -> int:
        return len(self._sources)
