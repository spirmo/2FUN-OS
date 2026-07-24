import json
from pathlib import Path
from .audit_hash_spec import AuditHashSpec


class AuditChainVerifier:
    def __init__(self):
        self.audit_file = Path(
            "/data/data/com.termux/files/home/2FUN_GAME/"
            "TANDIL_GOVERNANCE/core_engine/logs/audit_chain.jsonl"
        )

    # =========================
    # VERIFY CHAIN
    # =========================
    def verify(self):
        if not self.audit_file.exists():
            return {
                "valid": False,
                "reason": "AUDIT_FILE_NOT_FOUND"
            }

        with open(self.audit_file, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]

        if not lines:
            return {
                "valid": True,
                "reason": "EMPTY_CHAIN"
            }

        previous_hash = "GENESIS"
        broken_index = None

        for i, record in enumerate(lines):
            expected_hash = AuditHashSpec.generate(
                record["event"],
                previous_hash
            )
            actual_hash = record.get("hash")

            if actual_hash != expected_hash:
                broken_index = i
                return {
                    "valid": False,
                    "reason": "HASH_MISMATCH",
                    "index": i,
                    "expected": expected_hash,
                    "actual": actual_hash
                }

            if record.get("previous_hash") != previous_hash:
                return {
                    "valid": False,
                    "reason": "CHAIN_BROKEN",
                    "index": i,
                    "expected_previous": previous_hash,
                    "actual_previous": record.get("previous_hash")
                }

            previous_hash = actual_hash

        return {
            "valid": True,
            "reason": "CHAIN_OK",
            "total_records": len(lines)
        }

