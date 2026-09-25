import json
from pathlib import Path


class ReplayEngine:
    """
    Rebuild runtime state from the central 2FUN-OS audit chain.

    Legacy functionality migrated from:
    FREEZE_RUNTIME_V1/replay_engine.py

    The legacy replay reader expected the old audit-chain location.
    This implementation uses the canonical 2FUN-OS audit chain.
    """

    def __init__(self, audit_path=None):
        self.audit_path = Path(
            audit_path or "platform_core/logs/audit_chain.jsonl"
        )

    def load_events(self):
        if not self.audit_path.exists():
            return []

        events = []

        with open(self.audit_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                try:
                    record = json.loads(line)
                    events.append(record)
                except Exception as exc:
                    print(f"[REPLAY ERROR] {exc}")

        return events

    @staticmethod
    def _event(record):
        return record.get("event", record)

    def rebuild_governance_state(self):
        events = self.load_events()
        governance_map = {}

        for record in events:
            event = self._event(record)
            source = event.get("source", "UNKNOWN")

            gov = event.get("governance", {})
            policy = event.get("policy", {})
            enforcement = event.get("enforcement", {})

            if source not in governance_map:
                governance_map[source] = {
                    "total_decisions": 0,
                    "approvals": 0,
                    "blocks": 0,
                    "risk_accumulated": 0,
                }

            governance_map[source]["total_decisions"] += 1

            if policy.get("status") == "APPROVED":
                governance_map[source]["approvals"] += 1

            if enforcement.get("status") == "BLOCKED":
                governance_map[source]["blocks"] += 1

            governance_map[source]["risk_accumulated"] += gov.get(
                "risk_score", 0
            )

        return governance_map

    def rebuild_full_state(self):
        events = self.load_events()

        state = {
            "memory": {},
            "governance": {},
            "identity": {},
            "behavior": {},
        }

        for record in events:
            event = self._event(record)
            source = event.get("source", "UNKNOWN")

            mem = event.get("memory", {})
            gov = event.get("governance", {})
            identity = event.get("identity", {})
            behavior = event.get("behavior", {})

            if source not in state["memory"]:
                state["memory"][source] = {
                    "events": 0,
                    "trust": 0,
                    "risk": 0,
                }

            state["memory"][source]["events"] += 1
            state["memory"][source]["trust"] = mem.get(
                "trust_score",
                state["memory"][source]["trust"],
            )
            state["memory"][source]["risk"] = mem.get(
                "risk_score",
                state["memory"][source]["risk"],
            )

            state["governance"][source] = gov
            state["identity"][source] = identity
            state["behavior"][source] = behavior

        return state

    def rebuild_memory_state(self):
        events = self.load_events()
        users = {}

        for record in events:
            event = self._event(record)
            source = event.get("source", "UNKNOWN")
            memory = event.get("memory") or {}

            if source not in users:
                users[source] = {
                    "events": 0,
                    "trust_score": 0,
                    "risk_score": 0,
                }

            users[source]["events"] = memory.get(
                "events",
                users[source]["events"],
            )
            users[source]["trust_score"] = memory.get(
                "trust_score",
                users[source]["trust_score"],
            )
            users[source]["risk_score"] = memory.get(
                "risk_score",
                users[source]["risk_score"],
            )

        return users
