import json
import time


class PolicyRegistry:

    def __init__(self, path=None):
        self.path = (
            path
            or "platform_core/policy_registry/policy_registry.json"
        )

        self.rules = self.load()

        self.active_policies = []
        self.draft_policies = []
        self.history = []

    # ==========================
    # LOAD RULES
    # ==========================
    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)["rules"]

    # ==========================
    # GET ACTIVE RULE
    # ==========================
    def get_active(self, target: str):
        return self.find_rule(target)

    # ==========================
    # FIND RULE
    # ==========================
    def find_rule(self, target):

        for rule in self.rules:

            if rule["target"] == target or rule["target"] == "*":

                ui_state = self._build_ui_state(rule)

                rule_copy = dict(rule)
                rule_copy["ui_state"] = ui_state

                return rule_copy

        return {
            "id": "DEFAULT",
            "target": "*",
            "mode": "AUTO",
            "veto_allowed": True,
            "risk_level": "low",
            "ui_state": {
                "mode": "AUTO",
                "color": "BLUE",
                "founder_editable": False,
                "founder_notify": False,
            },
        }

    # ==========================
    # UI STATE BUILDER
    # ==========================
    def _build_ui_state(self, rule):

        mode = rule.get("mode", "AUTO")

        if mode == "AUTO":
            return {
                "mode": mode,
                "color": "BLUE",
                "founder_editable": False,
                "founder_notify": False,
            }

        if mode == "FOUNDER_REQUIRED":
            return {
                "mode": mode,
                "color": "ORANGE",
                "founder_editable": True,
                "founder_notify": True,
            }

        if mode == "OBSERVABLE":
            return {
                "mode": mode,
                "color": "YELLOW",
                "founder_editable": True,
                "founder_notify": True,
            }

        return {
            "mode": mode,
            "color": "BLUE",
            "founder_editable": False,
            "founder_notify": False,
        }

    # ==========================
    # REGISTER DRAFT
    # ==========================
    def register_draft(self, draft):

        self.draft_policies.append(draft)

        return {
            "status": "REGISTERED",
            "type": "DRAFT",
            "draft_id": draft.get("id"),
        }

    # ==========================
    # ACTIVATE POLICY
    # ==========================
    def activate(self, approved_policy):

        if not approved_policy:
            return {
                "status": "ERROR",
                "reason": "EMPTY_POLICY",
            }

        if approved_policy.get("status") != "APPROVED":
            return {
                "status": "REJECTED",
                "reason": "POLICY_NOT_APPROVED",
            }

        policy = {
            "id": approved_policy.get("id"),
            "rule": approved_policy.get(
                "policy",
                approved_policy,
            ),
            "status": "ACTIVE",
            "activated_at": time.time(),
        }

        self.active_policies.append(policy)

        self.history.append(
            {
                "action": "ACTIVATED",
                "policy_id": policy["id"],
            }
        )

        return policy
