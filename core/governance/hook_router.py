# =========================
# GOVERNANCE HOOK ROUTER
# =========================

from core.governance.hooks import (
    on_xp_change,
    on_violation,
    on_activity,
)

class GovernanceHookRouter:
    """
    Maps EventBus events → governance hooks
    """

    def __init__(self):
        self.routes = {
            "XP_GAIN": self._xp_gain,
            "VIOLATION": self._violation,
            "ACTIVITY": self._activity,
        }

    # =========================
    # PUBLIC DISPATCH
    # =========================

    def dispatch(self, event: dict):
        event_type = event.get("event_type")

        # 🔥 DEBUG
        print("[ROUTER RECEIVED]", event_type)
        print("[ROUTER EVENT]", event)

        handler = self.routes.get(event_type)

        if not handler:
            print(f"[HOOK ROUTER] No handler for {event_type}")
            return

        try:
            handler(event)
        except Exception as e:
            print(f"[HOOK ROUTER ERROR] {e}")

    # =========================
    # ROUTES
    # =========================

    def _xp_gain(self, event):
        user_id = event["value"].get("user_id")
        xp = event["value"].get("xp", 0)
        on_xp_change(user_id, xp)

    def _violation(self, event):
        user_id = event["value"].get("user_id")
        severity = event["value"].get("severity", 1)
        on_violation(user_id, severity)

    def _activity(self, event):
        user_id = event["value"].get("user_id")
        on_activity(user_id)
