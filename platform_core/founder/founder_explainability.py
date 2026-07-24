import time


class FounderExplainability:

    def __init__(self, store):
        self.store = store

    # =========================
    # MAIN ENTRY
    # =========================
    def build_report(self, event_id):

        event = self._find(event_id)
        if not event:
            return {"status": "NOT_FOUND"}

        decision = event.get("decision", {})
        veto = event.get("veto", {})
        rule = event.get("rule", {})

        report = {
            "event_id": event_id,

            # =====================
            # ORIGINAL VETO REASON
            # =====================
            "original_veto": {
                "reason": veto.get("reason"),
                "explanation": veto.get("explanation"),
                "timestamp": veto.get("timestamp")
            },

            # =====================
            # CURRENT SYSTEM STATE
            # =====================
            "current_state": {
                "status": event.get("status"),
                "risk": event.get("governance", {}).get("risk_score"),
                "trust": event.get("governance", {}).get("trust_score"),
                "mode": event.get("rule", {}).get("mode")
            },

            # =====================
            # CHANGE DETECTION
            # =====================
            "changes_since_veto": self._detect_changes(event),

            # =====================
            # REACTIVATION SIGNAL
            # =====================
            "reactivation_signal": self._can_reactivate(event),

            # =====================
            # FINAL EXPLANATION
            # =====================
            "summary": self._build_summary(event)
        }

        return report

    # =========================
    # CHANGE DETECTOR
    # =========================
    def _detect_changes(self, event):

        changes = []

        # risk improvement
        risk = event.get("governance", {}).get("risk_score", 100)
        if risk < 50:
            changes.append("risk_reduced")

        # trust improvement
        trust = event.get("governance", {}).get("trust_score", 0)
        if trust > 50:
            changes.append("trust_improved")

        # rule relaxation
        if event.get("rule", {}).get("mode") == "AUTO":
            changes.append("rule_relaxed")

        return changes

    # =========================
    # REACTIVATION RULE
    # =========================
    def _can_reactivate(self, event):

        veto = event.get("veto", {})
        changes = self._detect_changes(event)

        # شرط ساده ولی واقعی
        if not veto:
            return False

        if len(changes) >= 2:
            return True

        return False

    # =========================
    # HUMAN READABLE SUMMARY
    # =========================
    def _build_summary(self, event):

        veto = event.get("veto", {})
        changes = self._detect_changes(event)

        if not veto:
            return "No veto history found."

        summary = f"""
This event was previously vetoed.

Reason:
{veto.get('reason')}

Explanation:
{veto.get('explanation')}

System now detects the following improvements:
- {', '.join(changes) if changes else 'no significant improvements'}

Reactivation eligibility:
{'YES' if self._can_reactivate(event) else 'NO'}
        """

        return summary

    # =========================
    # FIND EVENT
    # =========================
    def _find(self, event_id):

        events = self.store.list_all()

        for e in events:
            if e.get("event_id") == event_id:
                return e

        return None
