import random


BASE_TRAITS = [
    "PERSISTENCE",
    "RESPONSIBILITY",
    "SELF_AWARENESS",
]


def generate_fake_user(user_id: str):
    trait_count = random.randint(1, 3)
    traits = random.sample(
        BASE_TRAITS,
        trait_count,
    )

    return {
        "user_id": user_id,
        "traits": traits,
    }


def build_population(size: int = 100):
    population = []

    for i in range(size):
        population.append(
            generate_fake_user(f"sim_{i}")
        )

    return population


def get_trait_distribution(population):
    distribution = {}

    for user in population:
        for trait in user["traits"]:
            distribution[trait] = distribution.get(trait, 0) + 1

    return distribution
