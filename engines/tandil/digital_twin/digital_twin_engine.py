def build_digital_twin(model: dict):
    """
    Digital Twin V2

    Input:
        Human Model V2

    Output:
        Living digital representation of the user.

    Ownership:
        engines/tandil/digital_twin

    The Digital Twin is an independent subsystem.
    It does not execute decisions or own governance.
    Human Evolution is intentionally not invoked here.
    """

    trait_profile = model.get("trait_profile", {})
    strengths = model.get("strengths", [])
    weaknesses = model.get("weaknesses", [])
    identity_state = model.get("identity_state", "BUILDING")

    traits = [
        {
            "code": code,
            **data,
        }
        for code, data in trait_profile.items()
    ]

    dominant_traits = sorted(
        traits,
        key=lambda item: item.get("count", 1),
        reverse=True,
    )[:5]

    dominant_traits = [
        trait["code"]
        for trait in dominant_traits
    ]

    if len(strengths) >= 3:
        twin_identity_state = "STABLE_IDENTITY"
    elif len(strengths) >= 1:
        twin_identity_state = "GROWING_IDENTITY"
    else:
        twin_identity_state = "UNDEFINED_IDENTITY"

    total_traits = len(traits)

    if total_traits < 3:
        growth_stage = "EARLY_DEVELOPMENT"
    elif total_traits < 10:
        growth_stage = "DEVELOPING"
    else:
        growth_stage = "ADVANCED"

    if len(weaknesses) >= len(strengths):
        risk_level = "HIGH"
    elif weaknesses:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    recommended_nodes = []

    node_mapping = {
        "PERSISTENCE": "IE002",
        "SELF_AWARENESS": "IE003",
    }

    for trait_code in dominant_traits:
        node = node_mapping.get(trait_code)

        if node and node not in recommended_nodes:
            recommended_nodes.append(node)

    if not recommended_nodes:
        recommended_nodes.append("IE001")

    return {
        "user_id": model.get("user_id"),
        "identity_state": twin_identity_state,
        "human_model_identity_state": identity_state,
        "growth_stage": growth_stage,
        "dominant_traits": dominant_traits,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "risk_level": risk_level,
        "recommended_nodes": recommended_nodes,
        "twin_version": "2.0",
    }
