from db.services.ie002_behavior_engine import analyze_trust_behavior
from db.services.rank_engine import calculate_rank
from db.services.user_evolution_engine import analyze_user_evolution


def evaluate_ie002_rank(user_id: int, node_code: str, interactions: list):

    # -----------------------------
    # 1. تحلیل رفتار اعتماد (IE002)
    # -----------------------------
    signals = analyze_trust_behavior(interactions)

    # -----------------------------
    # 2. گرفتن وضعیت تکاملی کاربر
    # -----------------------------
    evolution = analyze_user_evolution(user_id, node_code)

    if evolution is None:
        evolution = {
            "avg_score": 0,
            "trend": "NEW",
            "current_level": "UNKNOWN",
            "next_level": "UNKNOWN",
            "node_code": node_code,
            "total_attempts": 0
        }

    # -----------------------------
    # 3. محاسبه trust score
    # -----------------------------
    trust_score = (
        signals.get("trustworthiness", 0)
        + signals.get("consistency", 0)
        + signals.get("honesty", 0)
        - signals.get("manipulation_risk", 0)
    )

    # -----------------------------
    # 4. merge evolution + trust
    # -----------------------------
    combined_evolution = evolution.copy()
    combined_evolution["avg_score"] = (
        combined_evolution.get("avg_score", 0) + trust_score * 0.5
    )

    # -----------------------------
    # 5. rank calculation
    # -----------------------------
    rank_result = calculate_rank(combined_evolution)

    # -----------------------------
    # خروجی نهایی
    # -----------------------------
    return {
        "signals": signals,
        "trust_score": trust_score,
        "evolution": combined_evolution,
        "rank": rank_result
    }


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":

    sample_interactions = [
        "من همیشه به قولم پایبندم",
        "این موضوع را پنهان کردم",
        "او دروغ گفت"
    ]

    result = evaluate_ie002_rank(
        user_id=1,
        node_code="IE002",
        interactions=sample_interactions
    )

    print(result)
