import time


class AdaptiveEngine:

    def __init__(self):

        self.learning_data = {}

    def learn(self, event):

        source = event.get("source")

        if source not in self.learning_data:

            self.learning_data[source] = {
                "events": 0,
                "trust_growth": 0,
                "risk_reduction": 0,
                "adaptation_level": 1,
            }

        profile = self.learning_data[source]

        profile["events"] += 1

        risk = event.get("risk", {}).get("risk_level", "medium")

        if risk == "low":

            profile["trust_growth"] += 5
            profile["risk_reduction"] += 2

        elif risk == "high":

            profile["trust_growth"] -= 3
            profile["risk_reduction"] -= 5

        # Adaptive evolution
        if profile["events"] >= 5:

            profile["adaptation_level"] += 1

        result = {
            "source": source,
            "events": profile["events"],
            "trust_growth": profile["trust_growth"],
            "risk_reduction": profile["risk_reduction"],
            "adaptation_level": profile["adaptation_level"],
            "timestamp": time.time(),
        }

        return result
