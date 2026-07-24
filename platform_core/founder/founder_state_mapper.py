class FounderStateMapper:

    def map(self, event, decision, rule):

        # =========================
        # BLOCKED
        # =========================
        if decision.get("status") == "blocked":
            return {
                "state": "REJECTED",
                "color": "RED"
            }

        # =========================
        # PENDING FOUNDER
        # =========================
        if decision.get("status") == "pending_founder_approval":
            mode = rule.get("mode")

            if mode == "FOUNDER_REQUIRED":
                return {
                    "state": "PENDING",
                    "color": "ORANGE"
                }

            if mode == "OBSERVABLE":
                return {
                    "state": "OBSERVED",
                    "color": "YELLOW"
                }

        # =========================
        # AUTO EXECUTED
        # =========================
        if decision.get("status") == "approved":
            return {
                "state": "AUTO_EXECUTED",
                "color": "BLUE"
            }

        # =========================
        # DEFAULT
        # =========================
        return {
            "state": "UNKNOWN",
            "color": "GRAY"
        }
