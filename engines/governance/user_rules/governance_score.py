class GovernanceScore:
    """Legacy user-governance score contract preserved exactly."""

    def calculate(self, user_data):
        score = user_data.get("score", 0)
        reputation = user_data.get("reputation", 0)
        violations = user_data.get("violations", 0)

        governance_score = (score * 0.4) + (reputation * 0.5) - (violations * 20)

        if governance_score < 0:
            governance_score = 0

        if governance_score >= 2000:
            risk_level = "low"
        elif governance_score >= 1000:
            risk_level = "medium"
        else:
            risk_level = "high"

        if reputation >= 80:
            trust_level = "high"
        elif reputation >= 50:
            trust_level = "medium"
        else:
            trust_level = "low"

        return {
            "governance_score": governance_score,
            "risk_level": risk_level,
            "trust_level": trust_level,
        }
