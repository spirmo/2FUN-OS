from TANDIL_GOVERNANCE.core_engine.snapshot_manager import SnapshotManager


class SnapshotHandler:
    def __init__(self):
        self.snapshot = SnapshotManager()

    def handle(self, event):
        # فقط event هایی که state را تغییر می‌دهند
        if event["event_type"] in ["update", "snapshot"]:
            self.snapshot.update(event["target"], event["value"])
