import random


TRAIT_WEIGHTS = {
    "PERSISTENCE": 0.6,
    "RESPONSIBILITY": 0.3,
    "SELF_AWARENESS": 0.1,
}


def weighted_choice(trait_weights):
    traits = list(trait_weights.keys())
    weights = list(trait_weights.values())

    return random.choices(
        traits,
        weights=weights,
        k=1,
    )[0]


def generate_realistic_user(user_id: str):
    trait_count = random.randint(1, 3)

    traits = set()

    for _ in range(trait_count):
        trait = weighted_choice(TRAIT_WEIGHTS)
        traits.add(trait)

    return {
        "user_id": user_id,
        "traits": list(traits),
    }


def build_calibrated_population(size: int = 100):
    population = []

    for i in range(size):
        population.append(
            generate_realistic_user(f"real_{i}")
        )

    return population


def get_calibrated_distribution(population):
    distribution = {}
    total = 0

    for user in population:
        for trait in user["traits"]:
            distribution[trait] = distribution.get(trait, 0) + 1
            total += 1

    for key in distribution:
        distribution[key] = distribution[key] / total

    return distribution
