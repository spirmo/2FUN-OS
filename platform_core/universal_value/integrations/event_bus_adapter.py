"""
2FUN Universal Value Infrastructure (UVI)

EventBus → UVI Pipeline → Transaction → Ledger
"""

from decimal import Decimal
from typing import Any, Mapping, Optional

from ..core.value_request import ValueRequest
from ..pipeline.value_pipeline import ValuePipeline
from ..core.contracts import ValueEvent
from ..ledger.value_ledger import ValueLedger
from ..transactions.transaction_manager import TransactionManager


class UVIEventBusAdapter:

    def __init__(
        self,
        pipeline: ValuePipeline,
        *,
        ledger: Optional[ValueLedger] = None,
        transaction_manager: Optional[TransactionManager] = None,
        enabled: bool = True,
    ):
        self.pipeline = pipeline
        self.enabled = enabled

        self.ledger = ledger or ValueLedger()

        self.transaction_manager = (
            transaction_manager
            or TransactionManager(self.ledger)
        )

    def supports(self, event: Mapping[str, Any]) -> bool:
        if not self.enabled:
            return False

        return bool(
            event.get("event_type")
            and event.get("source")
            and event.get("value") is not None
        )

    def build_request(
        self,
        event: Mapping[str, Any],
    ) -> ValueRequest:

        value = event.get("value") or {}

        if not isinstance(value, Mapping):
            value = {"value": value}

        user_id = (
            value.get("user_id")
            or event.get("user_id")
            or event.get("target")
        )

        event_id = str(event.get("event_id"))
        source = str(event.get("source"))
        action = str(event.get("event_type"))

        item_key: Optional[str] = (
            value.get("item_key")
            or value.get("field_key")
        )

        base_value = Decimal(
            str(
                value.get(
                    "base_value",
                    value.get(
                        "xp",
                        value.get(
                            "reward",
                            value.get("value", 0),
                        ),
                    ),
                )
            )
        )

        difficulty = value.get("difficulty")

        currency = str(
            value.get("currency", "XP")
        )

        metadata = dict(value)
        metadata["uvi_source_event_type"] = action

        return ValueRequest(
            user_id=str(user_id),
            event_id=event_id,
            source=source,
            action=action,
            item_key=item_key,
            base_value=base_value,
            difficulty=difficulty,
            currency=currency,
            metadata=metadata,
        )

    def process(
        self,
        event: Mapping[str, Any],
        *,
        multiplier: Decimal = Decimal("1"),
        transaction_type: str = "REWARD",
    ):

        if not self.supports(event):
            return None

        request = self.build_request(event)

        result = self.pipeline.calculate(
            request,
            multiplier=multiplier,
        )

        value_event = ValueEvent(
            event_id=request.event_id,
            user_id=request.user_id,
            source=request.source,
            action=request.action,
            base_value=result.final_value,
            currency=result.currency,
            metadata=dict(request.metadata),
        )

        transaction = self.transaction_manager.create_transaction(
            event=value_event,
            amount=result.final_value,
            transaction_type=transaction_type,
            metadata={
                **dict(request.metadata),
                "field_key": request.item_key,
                "uvi_final_value": str(result.final_value),
            },
        )

        return result, transaction
