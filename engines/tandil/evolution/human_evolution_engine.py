def analyze_trait_trends(traits):
    if not traits:
        return []

    return sorted(
        traits,
        key=lambda x: x.get("count", 1),
        reverse=True,
    )


def build_evolution_model(model: dict):
    """
    Human Evolution Engine V1

    Input:
        Human Model V2

    Output:
        Evolution signals.

    Ownership:
        engines/tandil/evolution

    This engine analyzes human change.
    It does not guide the user and does not make decisions.
    """

    trait_profile = model.get("trait_profile", {})
    strengths = model.get("strengths", [])
    weaknesses = model.get("weaknesses", [])

    traits = [
        {
            "code": code,
            **data,
        }
        for code, data in trait_profile.items()
    ]

    trait_trend = analyze_trait_trends(traits)

    dominant_traits = [
        trait.get("code") or trait.get("title")
        for trait in trait_trend[:5]
    ]

    emerging_traits = []
    declining_traits = []

    for trait in traits:
        count = trait.get("count", 1)
        name = trait.get("code") or trait.get("title")

        if count >= 3:
            emerging_traits.append(name)

        if count == 1:
            declining_traits.append(name)

    total = len(traits)

    if total == 0:
        stability = 0.0
    else:
        stability = min(
            1.0,
            len(strengths) / (total + 1),
        )

    if len(weaknesses) > len(strengths):
        behavior_shift = "UNSTABLE"
    elif len(strengths) > len(weaknesses):
        behavior_shift = "IMPROVING"
    else:
        behavior_shift = "STABLE"

    risk_signals = []

    if stability < 0.3:
        risk_signals.append("LOW_STABILITY")

    if len(weaknesses) > 2:
        risk_signals.append("MULTIPLE_WEAKNESSES")

    return {
        "user_id": model.get("user_id"),
        "dominant_traits": dominant_traits,
        "emerging_traits": emerging_traits,
        "declining_traits": declining_traits,
        "behavior_shift": behavior_shift,
        "risk_signals": risk_signals,
        "stability_index": stability,
        "timeline_depth": model.get("timeline_depth", 0),
        "evolution_state": "ANALYZED_V1",
    }


def estimate_trajectory(behavior_shift, stability_index):
    if behavior_shift == "IMPROVING" and stability_index > 0.6:
        return "UPWARD"

    if behavior_shift == "UNSTABLE":
        return "FLUCTUATING"

    return "STABLE"
