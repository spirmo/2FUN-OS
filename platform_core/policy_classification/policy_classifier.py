class PolicyClassifier:

    def classify(self, event, policy_result, memory_result, governance_result=None):

        risk = 0
        flags = []

        if policy_result.get("status") == "BLOCKED":
            return {
                "mode": "FOUNDER_REQUIRED",
                "reason": "policy_blocked",
                "risk_score": 100,
                "flags": ["policy_block"],
            }

        if event.get("event_type") in ["update", "delete", "override"]:
            risk += 30
            flags.append("sensitive_operation")

        if memory_result.get("risk_score", 0) > 70:
            risk += 30
            flags.append("high_memory_risk")

        if governance_result and governance_result.get("risk_score", 0) > 60:
            risk += 40
            flags.append("governance_risk")

        if risk >= 60:
            return {
                "mode": "FOUNDER_REQUIRED",
                "risk_score": risk,
                "flags": flags,
                "reason": "risk_threshold_exceeded",
            }

        return {
            "mode": "AUTO",
            "risk_score": risk,
            "flags": flags,
            "reason": "low_risk",
        }
