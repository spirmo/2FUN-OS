from .founder_explainability import FounderExplainability

class FounderDashboard:

    def __init__(self, store, engine):
        self.store = store
        self.engine = engine
        self.explainability = FounderExplainability(self.store)

    # =========================
    # GET STATE
    # =========================
    def _get_state(self, e):
        if e.get("decision", {}).get("status") == "approved_by_founder":
            return "APPROVED"

        if e.get("decision", {}).get("status") == "vetoed_by_founder":
            return "REJECTED"

        if e.get("approval", {}).get("status") == "PENDING_FOUNDER_APPROVAL":
            return "PENDING"

        if e.get("founder_state", {}).get("state") == "WAITING_FOR_CONDITION":
            return "WAITING"

        return "UNKNOWN"
    # =========================
    # ALL EVENTS
    # =========================
    def get_all_events(self):
        all_events = self.store.list_all()

        return {
            "pending": [
                e for e in all_events
                if self._get_state(e) == "PENDING"
            ],
            "approved": [
                e for e in all_events
                if self._get_state(e) == "APPROVED"
            ],
            "rejected": [
                e for e in all_events
                if self._get_state(e) == "REJECTED"
            ],
            "waiting": [
                e for e in all_events
                if self._get_state(e) == "WAITING"
            ],
        }
    # =========================
    # LIVE STATE ENGINE
    # =========================
    def set_state(self, event_id, state, color):
        event = self._find_event(event_id)
        if not event:
            return {"status": "NOT_FOUND"}
        # مهم: sync به store
        self.store.add(event)
        return event
    # =========================
    # FOUNDER ACTIONS LAYER
    # =========================

    def approve(self, event_id):
        result = self.engine.approve(event_id)
        return result


    def veto(self, event_id):
        result = self.engine.veto(event_id)
        return result


    def wait(self, event_id):
        event = self._find_event(event_id)
        if not event:
            return None

            event["founder_state"] = {
            "state": "WAITING_FOR_CONDITION",
            "color": "YELLOW"
        }

        return event

    def rollback(self, event_id):
        event = self._find_event(event_id)
        if event:
            event["founder_state"] = {
                "state": "ROLLBACK",
                "color": "RED"
            }
        return event

    # =========================
    # ACTIONS
    # =========================

    def _find_event(self, event_id):
        all_events = self.store.list_all()
        for e in all_events:
            if e.get("event_id") == event_id:
                return e
        return None

    # =========================
    # UI VIEW (IMPORTANT)
    # =========================
    def get_ui_view(self):

        events = self.get_all_events()

        return {
            "pending": self._attach_color(events["pending"]),
            "approved": self._attach_color(events["approved"]),
            "rejected": self._attach_color(events["rejected"]),
            "waiting": self._attach_color(events["waiting"]),
        }

    # =========================
    # COLOR MAPPER
    # =========================
    def _attach_color(self, events):
        result = []

        for e in events:
            rule = e.get("rule", {})
            ui = rule.get("ui_state", {})

            founder_state = e.get("founder_state", {})
            e["veto_reason"] = (
                e.get("veto", {}).get("reason")
            )

            e["veto_explanation"] = (
                e.get("veto", {}).get("explanation")
            )

            e["explainability"] = (
                e.get("veto", {}).get("explanation_layer")             )

            if founder_state.get("color"):
                e["color"] = founder_state["color"]
            else:
                e["color"] = ui.get("color", "BLUE")

                e["mode"] = ui.get("mode", "AUTO")

            result.append(e)

        return result
