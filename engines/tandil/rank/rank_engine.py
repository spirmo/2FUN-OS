"""
2FUN / توفان
TANDIL Rank Engine

Calculates user rank from evolution score and trend.
Rank calculation is separate from Role/Permission registration.
"""


def calculate_rank(evolution: dict):
    """Calculate rank using the migrated Legacy Game contract."""
    avg = evolution["avg_score"]
    trend = evolution["trend"]

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

    upgrade_possible = trend != "DECLINING"

    return {
        "rank": rank,
        "permissions": permissions,
        "next_rank": next_rank,
        "upgrade_possible": upgrade_possible,
    }
