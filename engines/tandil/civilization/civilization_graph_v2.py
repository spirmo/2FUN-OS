from modules.profile.profile_aggregator import aggregate_user_profile
from engines.tandil.evolution.human_evolution_engine import (
    build_evolution_model,
)
from engines.tandil.life_book.life_narrative_engine import (
    generate_life_narrative_v3,
)


def score_traits(profile):
    traits = profile["traits"]
    return min(len(traits) / 10, 1.0)


def score_evolution(evo):
    return evo.get("stability_index", 0.0)


def score_narrative(narrative):
    text = narrative.get("story", "")
    return min(len(text) / 500, 1.0)


def build_civilization_graph_v2(
    user_id: int,
    human_model: dict | None = None,
):
    profile = aggregate_user_profile(user_id)

    if human_model is None:
        from db.services.human_model_v2_engine import build_human_model_v2

        human_model = build_human_model_v2(user_id)

    evo = build_evolution_model(human_model)
    narrative = generate_life_narrative_v3(user_id)

    trait_score = score_traits(profile)
    evolution_score = score_evolution(evo)
    narrative_score = score_narrative(narrative)

    knowledge_score = len(profile.get("strengths", [])) / 10
    knowledge_score = min(knowledge_score, 1.0)

    total_score = (
        trait_score * 0.3
        + knowledge_score * 0.2
        + evolution_score * 0.3
        + narrative_score * 0.2
    )

    rank = int(total_score * 100)

    return {
        "user_id": user_id,
        "scores": {
            "trait_strength": trait_score,
            "knowledge_depth": knowledge_score,
            "evolution_stability": evolution_score,
            "narrative_coherence": narrative_score,
            "total": total_score,
        },
        "rank": rank,
        "percentile": total_score * 100,
        "peer_group": "GLOBAL_V1",
    }
