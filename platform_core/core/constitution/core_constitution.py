import time


class CoreConstitution:

    def __init__(self):

        self.core_rules = {
            # -------------------------------------------------
            # SYSTEM PROTECTION
            # -------------------------------------------------
            "CORE_RULES_IMMUTABLE": True,
            "FOUNDER_AUTHORITY_LOCKED": True,
            "AI_CANNOT_OVERRIDE_FOUNDER": True,
            "AI_CANNOT_DELETE_CORE": True,
            "AI_CANNOT_MODIFY_CONSTITUTION": True,
            # -------------------------------------------------
            # GOVERNANCE
            # -------------------------------------------------
            "FOUNDER_SUPREMACY": True,
            "HUMAN_REVIEW_REQUIRED": True,
            "MULTI_LAYER_VALIDATION": True,
            # -------------------------------------------------
            # SECURITY
            # -------------------------------------------------
            "EMERGENCY_LOCKDOWN_ENABLED": True,
            "AUTO_RISK_MONITORING": True,
            "AUDIT_TRAIL_REQUIRED": True,
            # -------------------------------------------------
            # SYSTEM STATE
            # -------------------------------------------------
            "CREATED_AT": time.time(),
            "STATUS": "ACTIVE",
        }

    # -------------------------------------------------
    # GET RULE
    # -------------------------------------------------

    def get_rule(self, key):

        return self.core_rules.get(key)

    # -------------------------------------------------
    # VALIDATE ACTION
    # -------------------------------------------------

    def validate_action(self, source, action, target):

        # AI restriction
        if source == "AI_AGENT":

            if target == "core_rules":
                return {"status": "BLOCKED", "reason": "AI_CANNOT_ACCESS_CORE_RULES"}

            if target == "constitution":
                return {"status": "BLOCKED", "reason": "AI_CANNOT_MODIFY_CONSTITUTION"}

        # Founder protected areas
        protected_targets = [
            "core_rules",
            "constitution",
            "founder_authority",
        ]

        if target in protected_targets:

            if source != "FOUNDER":

                return {"status": "BLOCKED", "reason": "FOUNDER_ONLY_AREA"}

        return {"status": "APPROVED"}

    # -------------------------------------------------
    # SYSTEM STATUS
    # -------------------------------------------------

    def status(self):

        return {
            "constitution": "ACTIVE",
            "rules": len(self.core_rules),
            "founder_protection": True,
            "ai_restrictions": True,
        }
