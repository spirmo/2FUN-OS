"""
TANDIL Cognitive Decision Engine

Cognition is advisory only.
It does not execute actions and does not own governance.
"""


def evaluate_cognitive_state(model: dict):
    """
    Evaluate cognitive state using the available Human Model contract.

    Legacy-compatible inputs:
        self_model.avg_score
        self_model.trend

    Human Model V2 inputs:
        strengths
        weaknesses
        identity_state
        growth_direction
    """

    self_model = model.get("self_model", {})
    has_legacy_cognitive_input = (
        "avg_score" in self_model or "trend" in self_model
    )

    if has_legacy_cognitive_input:
        avg_score = self_model.get("avg_score", 0)
        trend = self_model.get("trend", "UNKNOWN")

        if avg_score < 4 and trend == "DECLINING":
            risk = "HIGH"
            decision = "INTERVENTION_REQUIRED"
            actions = [
                "learning_loop",
                "drift_monitoring",
            ]
        elif avg_score < 6:
            risk = "MEDIUM"
            decision = "GUIDED_IMPROVEMENT"
            actions = [
                "learning_loop",
            ]
        else:
            risk = "LOW"
            decision = "NORMAL_EVOLUTION"
            actions = [
                "continue_monitoring",
            ]

        return {
            "decision": decision,
            "risk": risk,
            "actions": actions,
            "state": model.get("personality_state"),
            "growth": model.get("growth_direction"),
        }

    strengths = model.get("strengths", [])
    weaknesses = model.get("weaknesses", [])
    identity_state = model.get("identity_state", "BUILDING")
    growth_direction = model.get("growth_direction", "UNKNOWN")

    if weaknesses:
        risk = "MEDIUM"
        decision = "GUIDED_IMPROVEMENT"
        actions = ["learning_loop"]
    else:
        risk = "LOW"
        decision = "NORMAL_EVOLUTION"
        actions = ["continue_monitoring"]

    return {
        "decision": decision,
        "risk": risk,
        "actions": actions,
        "identity_state": identity_state,
        "growth_direction": growth_direction,
        "strength_count": len(strengths),
        "weakness_count": len(weaknesses),
    }
