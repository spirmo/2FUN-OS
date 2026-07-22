class GovernanceEngine:

    def evaluate(self, event, policy_result, memory_result):

        risk_score = memory_result.get("risk_score", 0)
        trust_score = memory_result.get("trust_score", 100)

        recommendation = "APPROVE"
        severity = "low"
        confidence = 0.95
        requires_founder_review = False
        explanation = "System stable"

        # POLICY BLOCK
        if policy_result.get("status") == "BLOCKED":

            recommendation = "BLOCK"
            severity = "critical"
            confidence = 0.99
            requires_founder_review = True
            explanation = "Policy engine blocked this action"

        # HIGH RISK
        elif risk_score >= 70:

            recommendation = "REVIEW"
            severity = "high"
            confidence = 0.85
            requires_founder_review = True
            explanation = "High risk score detected"

        # LOW TRUST
        elif trust_score < 40:

            recommendation = "REVIEW"
            severity = "medium"
            confidence = 0.80
            requires_founder_review = True
            explanation = "Trust score too low"

        # AI RESTRICTION
        elif event.get("source") == "AI":

            recommendation = "REVIEW"
            severity = "high"
            confidence = 0.90
            requires_founder_review = True
            explanation = "AI-originated governance event"

        return {
            "recommendation": recommendation,
            "severity": severity,
            "confidence": confidence,
            "requires_founder_review": requires_founder_review,
            "explanation": explanation,
            "risk_score": risk_score,
            "trust_score": trust_score,
        }
