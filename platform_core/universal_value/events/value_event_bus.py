"""
2FUN Universal Value Infrastructure (UVI)
Value Event Bus
"""

from typing import Callable, Dict, List

from ..core.contracts import ValueEvent


class ValueEventBus:

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(
        self,
        event_type: str,
        handler: Callable,
    ) -> None:

        self._handlers.setdefault(
            event_type,
            [],
        ).append(handler)

    def publish(
        self,
        event_type: str,
        event: ValueEvent,
    ) -> None:

        for handler in self._handlers.get(
            event_type,
            [],
        ):
            handler(event)
