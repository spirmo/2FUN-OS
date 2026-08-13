import json
from pathlib import Path
from threading import Lock
from typing import Any


class DiagnosticStorage:
    def __init__(self, storage_path: str | None = None):
        if storage_path:
            self.path = Path(storage_path)
        else:
            self.path = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "diagnostic"
                / "crashes.jsonl"
            )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def save(self, event: dict[str, Any]) -> None:
        record = {
            "received_at": __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat(),
            "event": event,
        }

        line = json.dumps(
            record,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        with self._lock:
            with self.path.open("a", encoding="utf-8") as file:
                file.write(line + "\n")
                file.flush()
