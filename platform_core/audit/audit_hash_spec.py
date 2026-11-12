import hashlib
import json
from typing import Any, Dict


class AuditHashSpec:
    """
    Central integrity hash specification.

    Legacy audit hashing (v1/v2) remains backward compatible.
    Universal integrity hashing is introduced as v3.

    Rules:
    - deterministic
    - canonical representation
    - version-aware
    - backward compatible
    - no scattered hash logic
    """

    HASH_ALGORITHM = "SHA-256"
    GENESIS = "GENESIS"
    UNIVERSAL_VERSION = "v3"

    # =========================
    # PUBLIC API
    # =========================
    @staticmethod
    def generate(
        event: Dict[str, Any],
        previous_hash: str = GENESIS,
    ) -> str:
        """
        Legacy-compatible hash generation.

        Existing Audit consumers continue to use v1/v2 behavior.
        Universal operations should use generate_universal().
        """
        normalized = AuditHashSpec._normalize(
            event,
            previous_hash,
        )

        encoded = json.dumps(
            normalized,
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def generate_universal(
        operation: Dict[str, Any],
        previous_hash: str = GENESIS,
    ) -> str:
        """
        Generate a universal integrity hash.

        This is the v3 contract for operations across the ecosystem.
        """
        normalized = AuditHashSpec.canonical_operation(
            operation,
            previous_hash,
        )

        encoded = json.dumps(
            normalized,
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    # =========================
    # LEGACY CANONICAL EVENT
    # =========================
    @staticmethod
    def canonical_event(event: dict) -> dict:
        """
        Preserve the existing Audit canonical representation.
        """
        return {
            "source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
        }

    # =========================
    # UNIVERSAL CANONICAL OPERATION
    # =========================
    @staticmethod
    def canonical_operation(
        operation: Dict[str, Any],
        previous_hash: str = GENESIS,
    ) -> Dict[str, Any]:
        """
        Canonical representation for EV-0020 Universal Integrity.

        Fields are intentionally explicit so that every participating
        module hashes the same semantic structure.
        """
        return {
            "integrity_version": AuditHashSpec.UNIVERSAL_VERSION,
            "operation_id": operation.get("operation_id"),
            "operation_type": operation.get("operation_type"),
            "timestamp": operation.get("timestamp"),
            "source": operation.get("source"),
            "actor": operation.get("actor"),
            "origin": operation.get("origin"),
            "target": operation.get("target"),
            "payload": operation.get("payload"),
            "value": operation.get("value"),
            "previous_hash": previous_hash,
        }

    # =========================
    # NORMALIZATION LAYER
    # =========================
    @staticmethod
    def _normalize(
        event: Dict[str, Any],
        previous_hash: str,
    ) -> Dict[str, Any]:
        """
        Existing v1/v2 normalization.

        Do not change this structure: current Audit consumers depend
        on its deterministic behavior.
        """

        version = AuditHashSpec._detect_version(event)

        base = {
            "source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": event.get("target"),
            "value": event.get("value"),
            "previous_hash": previous_hash,
            "version": version,
        }

        if version == "v2":
            base["timestamp"] = event.get("timestamp", 0)

        return base

    # =========================
    # VERSION DETECTOR
    # =========================
    @staticmethod
    def _detect_version(event: Dict[str, Any]) -> str:
        """
        Existing Audit version rules.

        - timestamp exists -> v2
        - otherwise -> v1
        """

        if "timestamp" in event:
            return "v2"

        return "v1"

    # =========================
    # CHAIN VERIFICATION
    # =========================
    @staticmethod
    def verify_chain(records: list) -> Dict[str, Any]:
        """
        Existing Audit chain verification.

        Preserved for backward compatibility.
        """

        previous_hash = AuditHashSpec.GENESIS

        for i, record in enumerate(records):
            expected = AuditHashSpec.generate(
                record,
                previous_hash,
            )

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

    # =========================
    # UNIVERSAL CHAIN VERIFICATION
    # =========================
    @staticmethod
    def verify_universal_chain(records: list) -> Dict[str, Any]:
        """
        Verify an EV-0020 universal integrity chain.
        """

        previous_hash = AuditHashSpec.GENESIS

        for i, record in enumerate(records):
            expected = AuditHashSpec.generate_universal(
                record,
                previous_hash,
            )

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
