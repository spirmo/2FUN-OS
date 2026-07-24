

from platform_core.snapshot_manager import SnapshotManager
from platform_core.snapshot.snapshot_decider import SnapshotDecider


class SnapshotListener:

    def __init__(self):
        self.snapshot_manager = SnapshotManager()
        self.snapshot_decider = SnapshotDecider()

    def handle(self, event, state):
        print("[SNAPSHOT LISTENER] RECEIVED:", event.get("event_type"))

        decision = self.snapshot_decider.should_snapshot(event)

        if not decision["take_snapshot"]:
            return {
                "status": "skipped",
                "reason": decision.get("reason")
            }

        payload = {
            "event": event,
            "decision": decision,
            "state": state,
        }

        self.snapshot_manager.save(payload)

        return {
            "status": "snapshot_saved",
            "reason": decision.get("reason")
        }
