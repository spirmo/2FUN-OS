import json
import time


from pathlib import Path
from .audit_hash_spec import AuditHashSpec


class AuditEngine:
    def __init__(self):
        self.audit_file = Path(
            "/data/data/com.termux/files/home/2FUN_GAME/"
            "TANDIL_GOVERNANCE/core_engine/logs/audit_chain.jsonl"
        )
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------------
    # Record Audit
    # -----------------------------------

    def record(self, event):
        previous_hash = self._get_last_hash()
        safe_event = {
            "source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
        }
        audit_entry = {
            "timestamp": time.time(),
            "event": safe_event,
            "previous_hash": previous_hash,
        }
        audit_entry["hash"] = AuditHashSpec.generate(             safe_event,
            previous_hash
        )
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
        return {
            "status": "audit_recorded",
            "hash": audit_entry["hash"],
            "previous_hash": previous_hash,
        }
    # -----------------------------------
    # Get Last Hash
    # -----------------------------------

    def _get_last_hash(self):
        if not self.audit_file.exists():
            return "GENESIS"
        with open(self.audit_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            return "GENESIS"
        last = json.loads(lines[-1])
        return last.get("hash", "GENESIS")
