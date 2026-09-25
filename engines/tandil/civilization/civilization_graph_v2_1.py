from modules.profile.profile_aggregator import aggregate_user_profile

from .population_simulator import (
    build_population,
    get_trait_distribution,
)


def compute_trait_score(
    user_traits,
    distribution,
    total_population,
):
    score = 0

    for trait in user_traits:
        freq = distribution.get(trait, 1)
        rarity_weight = 1 / freq
        score += rarity_weight

    return score / max(len(user_traits), 1)


def build_civilization_graph_v2_1(user_id: int):
    profile = aggregate_user_profile(user_id)

    population = build_population(100)
    distribution = get_trait_distribution(population)

    user_traits = profile["traits"]

    trait_codes = [
        trait["code"]
        for trait in user_traits
    ]

    trait_score = compute_trait_score(
        trait_codes,
        distribution,
        len(population),
    )

    percentile = min(
        trait_score * 100,
        100,
    )

    rank = int(
        (1 - trait_score) * 100
    )

    return {
        "user_id": user_id,
        "trait_score": trait_score,
        "percentile": percentile,
        "rank": rank,
        "population_size": len(population),
        "distribution": distribution,
        "version": "2.1",
    }
