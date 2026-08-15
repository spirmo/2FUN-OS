import time


class SnapshotDecider:

    TIME_FALLBACK = 7200

    def __init__(self):
        self.last_snapshot_time = 0
        self.event_counter = 0

    def should_snapshot(self, event: dict) -> dict:

        self.event_counter += 1

        reason = []

        # ==================================
        # TARGO MILESTONE
        # ==================================
        if event.get("event_type", "").startswith("TARGO_"):
            return {
                "take_snapshot": True,
                "reason": "targo_milestone",
            }

        # ==================================
        # POLICY BLOCK
        # ==================================
        if event.get("policy", {}).get("status") == "BLOCKED":
            return {
                "take_snapshot": True,
                "reason": "policy_block",
            }

        # ==================================
        # HIGH RISK
        # ==================================
        risk = event.get("risk", {})

        if risk.get("risk_level") == "high":
            return {
                "take_snapshot": True,
                "reason": "high_risk",
            }

        # ==================================
        # GOVERNANCE CHANGE
        # ==================================
        gov = event.get("governance", {})

        if gov.get("governance_score", 0) > 120:
            reason.append("high_governance_change")

        # ==================================
        # EVENT THRESHOLD
        # ==================================
        if self.event_counter % 5 == 0:
            reason.append("event_threshold")

        # ==================================
        # TIME FALLBACK
        # ==================================
        if time.time() - self.last_snapshot_time > self.TIME_FALLBACK:
            reason.append("time_based")

        if reason:
            return {
                "take_snapshot": True,
                "reason": reason,
            }

        return {
            "take_snapshot": False,
            "reason": "no_trigger",
        }
