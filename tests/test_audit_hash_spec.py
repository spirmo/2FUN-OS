import unittest

from platform_core.audit.audit_hash_spec import AuditHashSpec


class TestAuditHashSpec(unittest.TestCase):

    def setUp(self):
        self.event_v1 = {
            "source": "audit-test",
            "event_type": "RECORD_CREATED",
            "target": "sample",
            "value": "10",
        }
        self.event_v2 = {
            **self.event_v1,
            "timestamp": 1735689600,
        }

    def _build_legacy_chain(self, events):
        records = []
        previous_hash = AuditHashSpec.GENESIS

        for event in events:
            digest = AuditHashSpec.generate(event, previous_hash)
            records.append({
                **event,
                "previous_hash": previous_hash,
                "hash": digest,
            })
            previous_hash = digest

        return records

    def _build_universal_chain(self, operations):
        records = []
        previous_hash = AuditHashSpec.GENESIS

        for operation in operations:
            digest = AuditHashSpec.generate_universal(
                operation, previous_hash
            )
            records.append({
                **operation,
                "previous_hash": previous_hash,
                "hash": digest,
            })
            previous_hash = digest

        return records

    def test_v1_golden_hash(self):
        self.assertEqual(
            AuditHashSpec.generate(self.event_v1),
            "c6c4c9c1d13446e3e13eebe983d265a01c4a1ce35270a177057b79ff2cd13c1b",
        )

    def test_v2_golden_hash(self):
        self.assertEqual(
            AuditHashSpec.generate(self.event_v2),
            "affd324bababc9f45b43d1b667465d349415ceee0f8aec6f562d2024b8c1d3a1",
        )

    def test_timestamp_presence_selects_v2(self):
        self.assertEqual(
            AuditHashSpec._detect_version(self.event_v1), "v1"
        )
        self.assertEqual(
            AuditHashSpec._detect_version(self.event_v2), "v2"
        )

    def test_v1_and_v2_normalization(self):
        self.assertEqual(
            AuditHashSpec._normalize(self.event_v1, "GENESIS"),
            {
                "source": "audit-test",
                "event_type": "RECORD_CREATED",
                "target": "sample",
                "value": "10",
                "previous_hash": "GENESIS",
                "version": "v1",
            },
        )

        self.assertEqual(
            AuditHashSpec._normalize(self.event_v2, "GENESIS"),
            {
                "source": "audit-test",
                "event_type": "RECORD_CREATED",
                "target": "sample",
                "value": "10",
                "previous_hash": "GENESIS",
                "version": "v2",
                "timestamp": 1735689600,
            },
        )

    def test_canonical_event_preserves_legacy_fields(self):
        self.assertEqual(
            AuditHashSpec.canonical_event(self.event_v2),
            {
                "source": "audit-test",
                "event_type": "RECORD_CREATED",
                "target": "sample",
                "value": "10",
            },
        )

    def test_legacy_chain_accepts_v1_and_v2(self):
        records = self._build_legacy_chain([
            self.event_v1,
            self.event_v2,
        ])

        result = AuditHashSpec.verify_chain(records)

        self.assertEqual(
            result,
            {"valid": True, "reason": "CHAIN_OK", "total": 2},
        )

    def test_legacy_chain_detects_hash_tampering(self):
        records = self._build_legacy_chain([self.event_v1])
        records[0]["value"] = "999"

        result = AuditHashSpec.verify_chain(records)

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "HASH_MISMATCH")
        self.assertEqual(result["index"], 0)

    def test_legacy_chain_detects_previous_hash_tampering(self):
        records = self._build_legacy_chain([self.event_v1])
        records[0]["previous_hash"] = "TAMPERED"

        result = AuditHashSpec.verify_chain(records)

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "CHAIN_BROKEN")
        self.assertEqual(result["index"], 0)

    def test_universal_canonical_operation(self):
        operation = {
            "operation_id": "op-001",
            "operation_type": "VALUE_RECORDED",
            "timestamp": 1735689600,
            "source": "audit-test",
            "actor": "user-1",
            "origin": "unit-test",
            "target": "account-1",
            "payload": {"amount": "10"},
            "value": "10",
        }

        self.assertEqual(
            AuditHashSpec.canonical_operation(operation, "GENESIS"),
            {
                "integrity_version": "v3",
                "operation_id": "op-001",
                "operation_type": "VALUE_RECORDED",
                "timestamp": 1735689600,
                "source": "audit-test",
                "actor": "user-1",
                "origin": "unit-test",
                "target": "account-1",
                "payload": {"amount": "10"},
                "value": "10",
                "previous_hash": "GENESIS",
            },
        )

    def test_universal_chain_accepts_valid_records(self):
        operation = {
            "operation_id": "op-001",
            "operation_type": "VALUE_RECORDED",
            "timestamp": 1735689600,
            "source": "audit-test",
            "actor": "user-1",
            "origin": "unit-test",
            "target": "account-1",
            "payload": {"amount": "10"},
            "value": "10",
        }

        records = self._build_universal_chain([operation])
        result = AuditHashSpec.verify_universal_chain(records)

        self.assertEqual(
            result,
            {"valid": True, "reason": "CHAIN_OK", "total": 1},
        )

    def test_universal_chain_detects_payload_tampering(self):
        operation = {
            "operation_id": "op-001",
            "operation_type": "VALUE_RECORDED",
            "timestamp": 1735689600,
            "source": "audit-test",
            "actor": "user-1",
            "origin": "unit-test",
            "target": "account-1",
            "payload": {"amount": "10"},
            "value": "10",
        }

        records = self._build_universal_chain([operation])
        records[0]["payload"]["amount"] = "999"

        result = AuditHashSpec.verify_universal_chain(records)

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "HASH_MISMATCH")
        self.assertEqual(result["index"], 0)

    def test_universal_chain_detects_previous_hash_tampering(self):
        operation = {
            "operation_id": "op-001",
            "operation_type": "VALUE_RECORDED",
            "timestamp": 1735689600,
            "source": "audit-test",
            "actor": "user-1",
            "origin": "unit-test",
            "target": "account-1",
            "payload": {"amount": "10"},
            "value": "10",
        }

        records = self._build_universal_chain([operation])
        records[0]["previous_hash"] = "TAMPERED"

        result = AuditHashSpec.verify_universal_chain(records)

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "CHAIN_BROKEN")
        self.assertEqual(result["index"], 0)

    def test_empty_chains_remain_valid(self):
        self.assertEqual(
            AuditHashSpec.verify_chain([]),
            {"valid": True, "reason": "CHAIN_OK", "total": 0},
        )
        self.assertEqual(
            AuditHashSpec.verify_universal_chain([]),
            {"valid": True, "reason": "CHAIN_OK", "total": 0},
        )


if __name__ == "__main__":
    unittest.main()
