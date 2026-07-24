import time


class GovernanceScore:

    def __init__(self):

        self.source_weights = {"HUMAN": 90, "MACHINE": 70}

        self.event_weights = {
            "update": 10,
            "snapshot": 5,
            "override": -15,
            "hack": -100,
        }

    def calculate(self, event):

        source = event.get("source")
        event_type = event.get("event_type")

        base_score = self.source_weights.get(source, 0)

        event_score = self.event_weights.get(event_type, 0)

        governance_score = base_score + event_score

        # -------------------------
        # Trust Level
        # -------------------------

        if governance_score >= 90:
            trust = "high"

        elif governance_score >= 60:
            trust = "medium"

        else:
            trust = "low"

        # -------------------------
        # Risk Level
        # -------------------------

        if governance_score >= 80:
            risk = "low"

        elif governance_score >= 50:
            risk = "medium"

        else:
            risk = "high"

        # -------------------------
        # Reputation
        # -------------------------

        reputation = governance_score * 1.5

        # -------------------------
        # Stability
        # -------------------------

        stability = max(0, governance_score - 20)

        return {
            "timestamp": time.time(),
            "governance_score": governance_score,
            "trust_level": trust,
            "risk_level": risk,
            "reputation": reputation,
            "stability": stability,
        }
