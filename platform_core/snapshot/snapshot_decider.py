# core_engine/snapshot/snapshot_decider.py

import time


class SnapshotDecider:

    def __init__(self):
        self.last_snapshot_time = 0
        self.event_counter = 0

    def should_snapshot(self, event: dict) -> dict:

        self.event_counter += 1
        reason = []


        # ==================================
        # TARGO MILESTONE (ALWAYS SNAPSHOT)
        # ==================================

        if event.get("event_type", "").startswith("TARGO_"):
            return {
                "take_snapshot": True,
                "reason": "targo_milestone"
            }

        # 1. policy block
        if event.get("policy", {}).get("status") == "BLOCKED":
            return {"take_snapshot": True, "reason": "policy_block"}

        # 2. risk check
        risk = event.get("risk", {})
        if risk.get("risk_level") == "high":
            return {"take_snapshot": True, "reason": "high_risk"}

        # 3. governance jump
        gov = event.get("governance", {})
        if gov.get("governance_score", 0) > 120:
            reason.append("high_governance_change")

        # 4. event threshold
        if self.event_counter % 5 == 0:
            reason.append("event_threshold")

        # 5. time fallback
        if time.time() - self.last_snapshot_time > 30:
            reason.append("time_based")

        if reason:
            return {"take_snapshot": True, "reason": reason}

        return {"take_snapshot": False, "reason": "no_trigger"}
