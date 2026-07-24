import time


class PolicyDraftEngine:

    def __init__(self):

        self.drafts = []

    # -----------------------------------
    # Generate Policy Draft
    # تولید پیش‌نویس سیاست
    # -----------------------------------

    def generate(self, event):

        risk = event.get("risk", {})

        behavior = event.get("behavior", {})

        conflict = event.get("conflict", {})

        target = event.get("target")

        value = event.get("value")

        risk_level = risk.get("risk_level", "low")

        suggestion = None

        # -----------------------------------
        # SECURITY MODE CHANGES
        # تغییرات امنیتی
        # -----------------------------------

        if target == "security_mode":

            suggestion = {
                "rule_type": "security_policy",
                "suggestion": f"review_security_mode_{value}",
                "reason": (f"Security mode changed to {value}"),
                "priority": "HIGH",
            }

        # -----------------------------------
        # HIGH RISK DETECTED
        # ریسک بالا
        # -----------------------------------

        elif risk_level == "high":

            suggestion = {
                "rule_type": "security_policy",
                "suggestion": "increase_validation_level",
                "reason": "High risk activity detected",
                "priority": "HIGH",
            }

        # -----------------------------------
        # MACHINE GOVERNANCE EXPANSION
        # افزایش کنترل ماشینی
        # -----------------------------------

        elif conflict.get("decision") == "MACHINE_APPROVED":

            suggestion = {
                "rule_type": "governance_policy",
                "suggestion": "require_human_review",
                "reason": "Machine decisions increasing",
                "priority": "MEDIUM",
            }

        # -----------------------------------
        # AGGRESSIVE BEHAVIOR
        # رفتار پرریسک
        # -----------------------------------

        elif behavior.get("risk_tendency", 0) > 5:

            suggestion = {
                "rule_type": "behavior_policy",
                "suggestion": "monitor_behavior_pattern",
                "reason": ("Aggressive behavior tendency detected"),
                "priority": "MEDIUM",
            }

        # -----------------------------------
        # NO DRAFT
        # بدون پیش‌نویس
        # -----------------------------------

        if not suggestion:

            return {"status": "NO_DRAFT", "message": "No policy suggestion generated"}

        # -----------------------------------
        # CREATE DRAFT
        # ساخت پیش‌نویس
        # -----------------------------------

        draft = {
            "id": len(self.drafts) + 1,
            "timestamp": time.time(),
            "status": "DRAFT",
            "event_source": event.get("source"),
            "event_type": event.get("event_type"),
            "target": target,
            "value": value,
            "proposal": suggestion,
        }

        self.drafts.append(draft)

        # -----------------------------------
        # RETURN
        # خروجی
        # -----------------------------------

        return {"status": "DRAFT_CREATED", "draft": draft}
