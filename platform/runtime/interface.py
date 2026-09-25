"""2FUN-OS Runtime interface boundary."""

from abc import ABC, abstractmethod


class RuntimeInterface(ABC):
    """Single runtime authority contract for the 2FUN ecosystem."""

    @property
    @abstractmethod
    def event_bus(self):
        """Return the EventBus owned by this Runtime."""
        raise NotImplementedError

    @abstractmethod
    def initialize(self):
        """Initialize runtime-owned services and dependencies."""
        raise NotImplementedError

    @abstractmethod
    def start(self):
        """Start the runtime lifecycle."""
        raise NotImplementedError

    @abstractmethod
    def shutdown(self):
        """Shutdown the runtime lifecycle."""
        raise NotImplementedError
