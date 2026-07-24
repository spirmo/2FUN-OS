import json
import hashlib
from typing import Dict, Any


class AuditHashSpec:
    """
    SINGLE SOURCE OF TRUTH for audit hash generation.

    Rules:
    - deterministic
    - version-aware (but backward compatible)
    - no scattered hash logic anywhere else
    """

    # =========================
    # PUBLIC API
    # =========================
    @staticmethod
    def generate(event: Dict[str, Any], previous_hash: str = "GENESIS") -> str:
        """
        Main hashing function used across entire system.
        """

        normalized = AuditHashSpec._normalize(event, previous_hash)

        encoded = json.dumps(
            normalized,
            sort_keys=True,
            default=str,
            separators=(",", ":")
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    # =========================
    # CANONICAL EVENT 
    # =========================
    def canonical_event(event: dict) -> dict:
        return {
            "source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
    }
    # =========================
    # NORMALIZATION LAYER
    # =========================
    @staticmethod
    def _normalize(event: Dict[str, Any], previous_hash: str) -> Dict[str, Any]:
        """
        Ensures deterministic structure across ALL versions.
        """

        # Detect version safely
        version = AuditHashSpec._detect_version(event)

        base = {
            "source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
            "previous_hash": previous_hash,
            "version": version,
        }

        # v2 enhancements (optional, but deterministic)
        if version == "v2":
            base["timestamp"] = event.get("timestamp", 0)

        return base

    # =========================
    # VERSION DETECTOR
    # =========================
    @staticmethod
    def _detect_version(event: Dict[str, Any]) -> str:
        """
        Rules:
        - if timestamp exists → v2
        - else → v1 (legacy)
        """

        if "timestamp" in event:
            return "v2"

        return "v1"

    # =========================
    # VALIDATION MODE
    # =========================
    @staticmethod
    def verify_chain(records: list) -> Dict[str, Any]:
        """
        Optional chain verification using SAME spec.
        """

        previous_hash = "GENESIS"

        for i, record in enumerate(records):
            expected = AuditHashSpec.generate(record, previous_hash)
            actual = record.get("hash")

            if actual != expected:
                return {
                    "valid": False,
                    "reason": "HASH_MISMATCH",
                    "index": i,
                    "expected": expected,
                    "actual": actual,
                }

            if record.get("previous_hash") != previous_hash:
                return {
                    "valid": False,
                    "reason": "CHAIN_BROKEN",
                    "index": i,
                    "expected_previous": previous_hash,
                    "actual_previous": record.get("previous_hash"),
                }

            previous_hash = actual

        return {
            "valid": True,
            "reason": "CHAIN_OK",
            "total": len(records),
        }
