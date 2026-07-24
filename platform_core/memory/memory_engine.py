import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

MEMORY_PATH = BASE_DIR / "memory_state.json"


class MemoryEngine:

    def __init__(self):
        self.path = MEMORY_PATH

        self._buffer = []

        if not self.path.exists():
            self._initialize()

    # -----------------------------------
    # Initialize Memory
    # -----------------------------------

    def _initialize(self):

        base_memory = {
            "users": {},
            "system": {
                "total_events": 0,
                "last_event": None,
                "created_at": time.time(),
            },
        }

        self._save(base_memory)

    # -----------------------------------
    # SANITIZE (FIXED)
    # -----------------------------------

    def sanitize(self, data):

        return data

    # -----------------------------------
    # Load
    # -----------------------------------

    def load(self):

        with open(self.path, "r", encoding="utf-8") as f:

            return json.load(f)

    # -----------------------------------
    # Save
    # -----------------------------------

    def _save(self, data):

        with open(self.path, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=2, ensure_ascii=False)

    # -----------------------------------
    # Record Event
    # -----------------------------------

    def record_event(self, event):

        # prevent circular / complex objects
        event = self.sanitize(event)

        memory = self.load()

        source = event.get("source", "UNKNOWN")

        if source not in memory["users"]:

            memory["users"][source] = {
                "events": 0,
                "trust_score": 50,
                "risk_score": 50,
                "history": [],
            }

        user_memory = memory["users"][source]

        user_memory["events"] += 1

        # history
        user_memory["history"].append(
            {
                "timestamp": time.time(),
                "event_type": event.get("event_type"),
                "target": event.get("target"),
                "value": event.get("value"),
            }
        )

        # trust update
        governance = event.get("governance", {})

        trust_level = governance.get("trust_level")

        if trust_level == "high":

            user_memory["trust_score"] += 5

        elif trust_level == "medium":

            user_memory["trust_score"] += 1

        else:

            user_memory["trust_score"] -= 5

        # risk update
        risk_level = governance.get("risk_level")

        if risk_level == "high":

            user_memory["risk_score"] += 10

        elif risk_level == "medium":

            user_memory["risk_score"] += 5

        else:

            user_memory["risk_score"] -= 2

        # system stats
        memory["system"]["total_events"] += 1

        memory["system"]["last_event"] = {
            "source": source,
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
        }

        # save
        self._buffer.append(memory)

        if len(self._buffer) >= 50:
            self._flush()

        return {
            "status": "memory_updated",
            "source": source,
            "events": user_memory["events"],
            "trust_score": user_memory["trust_score"],
            "risk_score": user_memory["risk_score"],
        }

    def _flush(self):
        memory = self._buffer[-1]
        with open(self.path, "w") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        self._buffer.clear()
