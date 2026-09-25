"""
Game Runtime Adapter

Bridge between the Game module and the 2FUN-OS Runtime Context.

The Game module does not create or own Runtime or EventBus.
Runtime Context remains the single infrastructure authority.
"""

from platform_core.runtime.runtime_context import get_event_bus


class RuntimeAdapter:
    """Adapter boundary for connecting Game to the OS Runtime."""

    @property
    def event_bus(self):
        """Return the EventBus owned by the 2FUN-OS Runtime Context."""
        return get_event_bus()
