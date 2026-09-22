"""
2FUN / توفان
TANDIL Life Book Engine

Functional migration of the Legacy 2FUN GAME Life Book v2.
"""

from modules.profile.profile_aggregator import aggregate_user_profile
from engines.tandil.digital_twin.digital_twin_engine import build_digital_twin
from engines.tandil.evolution.human_evolution_engine import build_evolution_model


def build_identity_chapter(profile: dict, twin: dict) -> dict:
    traits = [
        trait.get("title")
        or trait.get("fa")
        or trait.get("code")
        for trait in profile.get("traits", [])
    ]

    return {
        "title": "هویت",
        "content": {
            "identity_state": twin.get("identity_state"),
            "dominant_traits": traits,
        },
    }


def build_strengths_chapter(profile: dict) -> dict:
    return {
        "title": "نقاط قوت",
        "content": profile.get("strengths", []),
    }


def build_weaknesses_chapter(profile: dict) -> dict:
    return {
        "title": "نقاط قابل بهبود",
        "content": profile.get("weaknesses", []),
    }


def build_timeline_chapter(profile: dict) -> dict:
    events = []

    for event in profile.get("timeline", []):
        events.append(
            {
                "event_type": event.get("event_type"),
                "title": event.get("title"),
                "timestamp": event.get("timestamp"),
            }
        )

    return {
        "title": "خط زمانی زندگی",
        "content": events,
    }


def build_evolution_chapter(evolution: dict) -> dict:
    signals = evolution.get("signals")

    if not signals:
        signals = {
            "behavior_shift": evolution.get("behavior_shift", "STABLE"),
            "emerging_traits": evolution.get("emerging_traits", []),
            "declining_traits": evolution.get("declining_traits", []),
        }

    return {
        "title": "تحول شخصی",
        "content": {
            "trajectory": evolution.get("trajectory", "STABLE"),
            "stability_index": evolution.get("stability_index", 0),
            "signals": signals,
        },
    }


def build_summary_chapter(
    profile: dict,
    twin: dict,
) -> dict:
    return {
        "title": "جمع‌بندی",
        "content": {
            "traits_count": len(profile.get("traits", [])),
            "timeline_depth": len(profile.get("timeline", [])),
            "risk_level": twin.get("risk_level"),
            "growth_stage": twin.get("growth_stage"),
        },
    }


def _build_human_model_v2(profile: dict) -> dict:
    """
    Adapt the canonical Profile Aggregator contract to the
    Human Model V2 contract consumed by TANDIL Twin/Evolution.
    """
    trait_profile = {
        trait.get("code"): {
            "count": trait.get("count", 0),
            "confidence": trait.get("confidence", 0.0),
        }
        for trait in profile.get("traits", [])
        if trait.get("code")
    }

    return {
        "user_id": profile.get("user_id"),
        "trait_profile": trait_profile,
        "traits": profile.get("traits", []),
        "strengths": profile.get("strengths", []),
        "weaknesses": profile.get("weaknesses", []),
        "identity_state": profile.get("identity", {}).get(
            "status", "BUILDING"
        ),
        "growth_direction": profile.get(
            "growth_direction", "UNKNOWN"
        ),
        "timeline": profile.get("timeline", []),
    }


def generate_life_book_v2(user_id: int) -> dict:
    profile = aggregate_user_profile(user_id)
    human_model = _build_human_model_v2(profile)

    twin = build_digital_twin(human_model)
    evolution = build_evolution_model(human_model)

    return {
        "user_id": user_id,
        "book_version": "2.0",
        "chapters": [
            build_identity_chapter(profile, twin),
            build_strengths_chapter(profile),
            build_weaknesses_chapter(profile),
            build_timeline_chapter(profile),
            build_evolution_chapter(evolution),
            build_summary_chapter(profile, twin),
        ],
    }


__all__ = [
    "build_identity_chapter",
    "build_strengths_chapter",
    "build_weaknesses_chapter",
    "build_timeline_chapter",
    "build_evolution_chapter",
    "build_summary_chapter",
    "generate_life_book_v2",
]
