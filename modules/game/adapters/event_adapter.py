"""
Game Event Adapter

Boundary between the Game module and the 2FUN-OS EventBus.

The Game module does not create or own EventBus.
It only emits official Game events through RuntimeAdapter.
"""

from modules.game.adapters.runtime_adapter import RuntimeAdapter


class GameEventAdapter:
    """Emit official Game events through the OS-owned EventBus."""

    SOURCE = "game"

    def __init__(self):
        self.runtime = RuntimeAdapter()

    @property
    def event_bus(self):
        return self.runtime.event_bus

    def emit_user_activity(
        self,
        user_id: int,
        action: str,
        timestamp=None,
    ):
        value = {
            "user_id": user_id,
            "action": action,
        }

        if timestamp is not None:
            value["timestamp"] = timestamp

        return self.event_bus.emit(
            source=self.SOURCE,
            event_type="USER_ACTIVITY",
            target="identity/governance",
            value=value,
        )

    def emit_mission_completed(
        self,
        user_id: int,
        mission_id,
        reward,
    ):
        return self.event_bus.emit(
            source=self.SOURCE,
            event_type="MISSION_COMPLETED",
            target="economy/knowledge",
            value={
                "user_id": user_id,
                "mission_id": mission_id,
                "reward": reward,
            },
        )

    def emit_points_earned(
        self,
        user_id: int,
        amount,
        reason: str,
    ):
        return self.event_bus.emit(
            source=self.SOURCE,
            event_type="POINTS_EARNED",
            target="economy/profile",
            value={
                "user_id": user_id,
                "amount": amount,
                "reason": reason,
            },
        )
