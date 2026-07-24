class DecisionRouter:
    def decide(
        self,
        classification,
        policy_result,
        enforcement_result,
        governance_result,
        event_rule,
    ):
        if event_rule.get("mode") == "FOUNDER_REQUIRED":

            return {
                "status": "pending_founder_approval",
                "action": "HOLD",
                "reason": "FOUNDER_REQUIRED_RULE",
            }
        """
        Central decision point for event execution
        """

        # 1. HARD BLOCKS FIRST
        if enforcement_result.get("status") == "BLOCKED":
            return {
                "action": "STOP",
                "reason": "ENFORCEMENT_BLOCK",
                "status": "blocked",
            }

        if governance_result.get("recommendation") == "BLOCK":
            return {"action": "STOP", "reason": "GOVERNANCE_BLOCK", "status": "blocked"}

        # 2. Founder required path
        if classification.get("mode") == "FOUNDER_REQUIRED":
            return {
                "action": "HOLD",
                "reason": "FOUNDER_APPROVAL",
                "status": "pending_founder",
            }

        # 3. AUTO path
        return {"action": "CONTINUE", "reason": "AUTO_APPROVED", "status": "approved"}
