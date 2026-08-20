"""
2FUN Universal Value Infrastructure (UVI)

Universal Value Gateway

Event / Source
      ↓
Source Validation
      ↓
Adapter
      ↓
ValueRequest
      ↓
ValuePipeline
      ↓
UniversalValueEngine
"""

from decimal import Decimal
from typing import Any

from .value_request import ValueRequest
from .value_engine import ValueResult
from ..registry.source_registry import ValueSourceRegistry
from ..pipeline.value_pipeline import ValuePipeline


class UniversalValueGateway:

    def __init__(
        self,
        registry: ValueSourceRegistry,
        pipeline: ValuePipeline,
    ):
        self.registry = registry
        self.pipeline = pipeline

    def validate_source(self, source: str) -> None:

        if not source:
            raise ValueError(
                "source is required"
            )

        if not self.registry.has(source):
            raise KeyError(
                f"UVI source not registered: {source}"
            )

    def resolve(self, source: str) -> Any:

        self.validate_source(source)

        return self.registry.require(source)

    def process(
        self,
        request: ValueRequest,
        *,
        multiplier: Decimal = Decimal("1"),
    ) -> ValueResult:

        if not isinstance(request, ValueRequest):
            raise TypeError(
                "request must be a ValueRequest"
            )

        adapter = self.resolve(
            request.source
        )

        if not hasattr(
            adapter,
            "calculate",
        ):
            raise TypeError(
                f"UVI adapter for source "
                f"{request.source} "
                f"has no calculate()"
            )

        return adapter.calculate(
            self.pipeline,
            request,
            multiplier=multiplier,
        )
