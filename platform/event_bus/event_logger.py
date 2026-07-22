import json
import os
import time

from datetime import datetime
from pathlib import Path

from TANDIL_GOVERNANCE.core_engine.snapshot_manager import SnapshotManager


class EventLogger:

    def __init__(self):

        base_dir = Path(__file__).resolve().parents[1]

        self.log_file = base_dir / "logs" / "event_stream.jsonl"

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        self.snapshot = SnapshotManager()

    def log(self, source, event_type, target, value):

        event = {
            "timestamp": time.time(),
            "datetime": str(datetime.now()),
            "source": source,
            "event_type": event_type,
            "target": target,
            "value": value,
        }

        with open(self.log_file, "a", encoding="utf-8") as f:

            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        # sync runtime state
        self.snapshot.update(target, value)

        return event
