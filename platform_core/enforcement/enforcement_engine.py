class EnforcementEngine:

    def __init__(self, policy_registry):
        self.policy_registry = policy_registry

    def enforce(self, event):

        policy = self.policy_registry.get_active(event["target"])

        if policy is None:
            return {"status": "ALLOWED", "reason": "NO_ACTIVE_POLICY"}

        rule = policy

        # BLOCK EVENT
        if rule.get("block_event_type") == event.get("event_type"):

            return {
                "status": "BLOCKED",
                "reason": "Event type blocked by active policy",
                "policy_id": policy.get("id"),
            }

        # FORCE SECURITY MODE
        if rule.get("force_security_mode") == "HARDENED":

            event["value"] = "HARDENED"

        # DEFAULT ALLOW
        return {"status": "ALLOWED"}
