def evaluate_cognitive_state(model: dict):
    """
    Evaluate the cognitive state represented by Human Model V2.

    Ownership:
        engines/tandil/cognition

    Input:
        Human Model V2 contract.

    Output:
        Advisory cognitive decision.

    This engine does not execute actions and does not own governance.
    """

    strengths = model.get("strengths", [])
    weaknesses = model.get("weaknesses", [])
    identity_state = model.get("identity_state", "BUILDING")
    growth_direction = model.get("growth_direction", "UNKNOWN")

    if weaknesses:
        risk = "MEDIUM"
        decision = "GUIDED_IMPROVEMENT"
        actions = ["learning_loop"]
    elif identity_state == "STABLE":
        risk = "LOW"
        decision = "NORMAL_EVOLUTION"
        actions = ["continue_monitoring"]
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
