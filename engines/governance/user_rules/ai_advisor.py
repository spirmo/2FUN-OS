class AIAdvisor:
    """Advisory-only analysis; never makes the governance decision."""

    def analyze_user(self, user_data):
        reputation = user_data.get("reputation", 0)
        violations = user_data.get("violations", 0)

        suggestions = []

        if reputation < 30:
            suggestions.append("low_reputation_warning")

        if violations >= 3:
            suggestions.append("high_risk_user")

        if reputation > 80 and violations == 0:
            suggestions.append("trusted_user")

        return {
            "ai_suggestions": suggestions,
            "advisory_only": True,
        }
