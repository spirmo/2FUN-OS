from db.database import SessionLocal
from db.migrations.create_reputation_records import ReputationRecord


def analyze_user_evolution(user_id: int, node_code: str):

    db = SessionLocal()

    records = db.query(ReputationRecord).filter(
        ReputationRecord.user_id == user_id,
        ReputationRecord.node_code == node_code
    ).all()

    db.close()

    if not records:
        return None

    scores = [r.score for r in records]

    total_attempts = len(scores)
    avg_score = sum(scores) / total_attempts

    # Trend analysis
    if total_attempts == 1:
        trend = "NEW"
    else:
        if scores[-1] > scores[0]:
            trend = "IMPROVING"
        elif scores[-1] < scores[0]:
            trend = "DECLINING"
        else:
            trend = "STABLE"

    # Level estimation
    if avg_score >= 8:
        current_level = "HIGH_TRUST"
        next_level = None
    elif avg_score >= 6:
        current_level = "TRUSTED"
        next_level = "HIGH_TRUST"
    elif avg_score >= 4:
        current_level = "NORMAL"
        next_level = "TRUSTED"
    else:
        current_level = "LOW"
        next_level = "NORMAL"

    return {
        "user_id": user_id,
        "node_code": node_code,
        "total_attempts": total_attempts,
        "avg_score": round(avg_score, 2),
        "trend": trend,
        "current_level": current_level,
        "next_level": next_level
    }


if __name__ == "__main__":

    result = analyze_user_evolution(1, "IE001")
    print(result)
