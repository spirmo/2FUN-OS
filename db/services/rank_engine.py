from db.services.user_evolution_engine import analyze_user_evolution


def calculate_rank(evolution: dict):

    avg = evolution["avg_score"]
    trend = evolution["trend"]

    # Base Rank
    if avg >= 8:
        rank = "GUARDIAN"
        permissions = ["all_access", "governance_vote"]
        next_rank = None

    elif avg >= 6:
        rank = "CONTRIBUTOR"
        permissions = ["content_create", "community_help"]
        next_rank = "GUARDIAN"

    elif avg >= 4:
        rank = "MEMBER"
        permissions = ["basic_interaction", "participation"]
        next_rank = "CONTRIBUTOR"

    else:
        rank = "VISITOR"
        permissions = ["read_only"]
        next_rank = "MEMBER"

    # Trend modifier (خیلی مهم)
    upgrade_possible = True
    if trend == "DECLINING":
        upgrade_possible = False

    return {
        "rank": rank,
        "permissions": permissions,
        "next_rank": next_rank,
        "upgrade_possible": upgrade_possible
    }


if __name__ == "__main__":

    evolution = analyze_user_evolution(1, "IE001")
    result = calculate_rank(evolution)

    print("EVOLUTION:", evolution)
    print("RANK:", result)
