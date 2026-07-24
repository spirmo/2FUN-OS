class RiskAnalyzer:

    def analyze(self, event):

        risk = "low"

        if event["source"] == "MACHINE":
            risk = "medium"

        if event["event_type"] == "delete":
            risk = "high"

        return {"risk_level": risk}
