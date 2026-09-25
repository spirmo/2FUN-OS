import json
from pathlib import Path
from .audit_hash_spec import AuditHashSpec

class AuditChainEvolutionLayer:
    """
    Supports multiple audit hash generations:
    - LEGACY: without timestamp
    - NEW: with timestamp
    """

    def __init__(self):
        self.audit_file = Path(
            Path(__file__).resolve().parent.parent / "logs" / "audit_chain.jsonl"
        )

    # =========================
    # LEGACY HASH (v1)
    # =========================
    def _legacy_hash(self, record, previous_hash):
        event = record.get("event", record)
        safe_data = {
            "source": event["source"],
            "event_type": event["event_type"],
            "target": event["target"],
            "value": event["value"],
        }
        return AuditHashSpec.generate(
            safe_data,
            previous_hash
        )

    # =========================
    # NEW HASH (v2)
    # =========================
    def _new_hash(self, record, previous_hash):
        event = record.get("event", record)
        safe_data = {
            "source": event["source"],
            "event_type": event["event_type"],
            "target": event["target"],
            "value": event["value"],
        }

        if "timestamp" in event:
            safe_data["timestamp"] = event["timestamp"]

        return AuditHashSpec.generate(
            safe_data,
            previous_hash
        )

    # =========================
    # DETECT VERSION
    # =========================
    def _detect_version(self, record):
        event = record.get("event", record)
        if "timestamp" in event:
            return "v2"
        return "v1"

    # =========================
    # VERIFY CHAIN
    # =========================
    def verify(self):
        if not self.audit_file.exists():
            return {"valid": False, "reason": "AUDIT_FILE_NOT_FOUND"}

        with open(self.audit_file, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]

        if not lines:
            return {"valid": True, "reason": "EMPTY_CHAIN"}

        previous_hash = "GENESIS"

        for i, record in enumerate(lines):

            version = self._detect_version(record)

            if version == "v1":
                expected_hash = self._legacy_hash(record, previous_hash)
            else:
                expected_hash = self._new_hash(record, previous_hash)

            actual_hash = record.get("hash")

            if actual_hash != expected_hash:
                return {
                    "valid": False,
                    "reason": "HASH_MISMATCH",
                    "index": i,
                    "version": version,
                    "expected": expected_hash,
                    "actual": actual_hash,
                }

            if record.get("previous_hash") != previous_hash:
                return {
                    "valid": False,
                    "reason": "CHAIN_BROKEN",
                    "index": i,
                    "expected_previous": previous_hash,
                    "actual_previous": record.get("previous_hash"),
                }

            previous_hash = actual_hash

        return {
            "valid": True,
            "reason": "CHAIN_OK",
            "total_records": len(lines),
        }
