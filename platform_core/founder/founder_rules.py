class FounderRules:
    """
    Determines when an event requires founder approval
    """

    def evaluate(self, event, policy_result, memory_result, governance_result):
        risk_score = governance_result.get("risk_score", 0)
        value = event.get("value")
        if isinstance(value, dict):
            severity = value.get("severity", 0)
        else:
            severity = 0
        event_type = event.get("event_type")

        # =========================
        # RULE 1: High Risk Score
        # =========================
        if risk_score >= 60:
            return {
                "status": "pending_founder_approval",
                "reason": "high_risk_score"
            }

        # =========================
        # RULE 2: VIOLATION EVENTS
        # =========================
        if event_type == "VIOLATION" and severity >= 5:
            return {
                "status": "pending_founder_approval",
                "reason": "violation_severity_trigger"
            }

        # =========================
        # RULE 3: XP ANOMALY
        # =========================
        if event_type == "XP_GAIN":
            xp = event.get("value", {}).get("xp", 0)
            if xp > 1000:
                return {
                    "status": "pending_founder_approval",
                    "reason": "xp_anomaly"
                }

        return {
            "status": "approved"
        }
