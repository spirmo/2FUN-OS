import time

from .founder_explainability import FounderExplainability



class FounderEngine:

    def __init__(self, founder_store):
        self.store = founder_store
        self.explainability = FounderExplainability(self.store)


    # =========================
    # QUEUE ACCESS
    # =========================

    def pending(self):
        return self.store.list()

    def list_approved(self):
        return self.store.list_approved()

    def list_rejected(self):
        return self.store.list_rejected()

    def list_waiting(self):
        return self.store.list_waiting()

    # =========================
    # APPROVE FLOW
    # =========================

    def approve(self, event_id):

        queue = self.store.list_all()

        for event in queue:
            if event["event_id"] == event_id:

                # DB STATUS (canonical)
                self.store.update_status(event_id, "APPROVED")

                # decision metadata
                event["decision"] = {
                    "status": "APPROVED",
                    "action": "EXECUTE"
                }

                # UI state
                event["founder_state"] = {
                    "state": "APPROVED_BY_FOUNDER",
                    "color": "GREEN"
                }
                event["approval_explanation"] = self.explainability.build_report(event_id)


                self.store.update_event(event)
                return event

        return {"status": "NOT_FOUND"}

    # =========================
    # VETO FLOW (FIXED)
    # =========================

    def veto(self, event_id, reason=None, explanation=None):

        queue = self.store.list_all()

        for event in queue:
            if event["event_id"] == event_id:

                # ❗ enforce required reason/explanation
                if not reason or not explanation:
                    return {
                        "status": "INVALID_VETO",
                        "error": "reason and explanation are required"
                    }

                # DB STATUS (canonical)
                self.store.update_status(event_id, "VETOED")

                # decision metadata (full trace)
                event["decision"] = {
                    "status": "VETOED",
                    "action": "BLOCK",
                    "reason": reason,
                    "explanation": explanation,
                    "timestamp": time.time()
                }

                # UI state
                event["founder_state"] = {
                    "state": "VETOED",
                    "color": "RED"
                }

                # veto log (for future re-evaluation engine)
                event["veto"] = {
                    "status": "VETOED",
                    "reason": reason,
                    "explanation": explanation,
                    "timestamp": time.time(),
                    "reactivation_signal": False
                }

                # اول ذخیره شود
                self.store.update_event(event)

                # بعد Explainability روی نسخه ذخیره شده ساخته شود
                event["veto"]["explanation_layer"] = (
                    self.explainability.build_report(event_id)
                )

                # دوباره ذخیره شود
                self.store.update_event(event)

                return event

        return {"status": "NOT_FOUND"}
