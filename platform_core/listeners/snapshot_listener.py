import time

from platform_core.snapshot_manager import SnapshotManager
from platform_core.snapshot.snapshot_decider import SnapshotDecider


class SnapshotListener:

    def __init__(self):
        self.snapshot_manager = SnapshotManager()
        self.snapshot_decider = SnapshotDecider()
        self.snapshot_decider.last_snapshot_time = (
            self.snapshot_manager.get_last_snapshot_time()
        )

    def handle(self, event, state):

        print(
            "[SNAPSHOT LISTENER] RECEIVED:",
            event.get("event_type"),
        )

        decision = self.snapshot_decider.should_snapshot(event)

        if not decision["take_snapshot"]:
            return {
                "status": "skipped",
                "reason": decision.get("reason"),
            }

        payload = {
            "_snapshot_meta": {
                "created_at": time.time(),
                "event_type": event.get("event_type"),
                "event_id": event.get("event_id"),
                "trigger_reason": decision.get("reason"),
            },
            "event": event,
            "decision": decision,
            "state": state,
        }

        self.snapshot_manager.save(payload)

        self.snapshot_decider.last_snapshot_time = time.time()

        return {
            "status": "snapshot_saved",
            "reason": decision.get("reason"),
        }
