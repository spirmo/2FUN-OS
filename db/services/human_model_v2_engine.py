from collections import defaultdict

from sqlalchemy import text

from db.database import SessionLocal

from core.profile.profile_aggregator import (
    aggregate_user_profile
)


def build_human_model_v2(user_id: int):

    profile = aggregate_user_profile(user_id)

    traits = profile["traits"]

    strengths = []
    weaknesses = []

    dominant_domains = []

    trait_profile = {}

    for t in traits:

        code = t["code"]

        trait_profile[code] = {
            "count": t["count"],
            "confidence": t["confidence"]
        }

        if t["confidence"] >= 0.7:
            strengths.append(code)
        else:
            weaknesses.append(code)

    identity_state = "BUILDING"

    if len(strengths) >= 5:
        identity_state = "FORMING"

    if len(strengths) >= 10:
        identity_state = "STABLE"

    growth_direction = "UNKNOWN"

    model = {

        "user_id": user_id,

        "trait_profile": trait_profile,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "dominant_domains": dominant_domains,

        "identity_state": identity_state,

        "growth_direction": growth_direction,

        "model_version": "2.0"
    }

    return model
