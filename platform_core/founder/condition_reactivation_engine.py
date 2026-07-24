from .founder_explainability import FounderExplainability

class ConditionReactivationEngine:

    def __init__(self, store):
        self.store = store
        self.explainability = FounderExplainability(self.store)

    def scan(self):
        events = self.store.list_all()
        for e in events:
            if e.get("status") == "WAITING_FOR_CONDITION":
                report = self.explainability.build_report(e["event_id"])
                if report["reactivation_signal"]:
                    self._reactivate(e, report)

    def _condition_passed(self, event):
        # فعلاً تستی
        return True

    def _reactivate(self, event, report):

        event["status"] = "PENDING"

        event["founder_state"] = {
            "state": "PENDING",
            "color": "ORANGE",
            "reactivation_reason": report["original_veto"],
            "reactivation_changes": report["changes_since_veto"]
        }

        self.store.update_event(event)
