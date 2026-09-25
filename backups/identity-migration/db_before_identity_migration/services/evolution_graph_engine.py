from db.database import SessionLocal
from db.migrations.create_human_models import HumanModelRecord


def build_evolution_graph(user_id: int, node_code: str = "IE001"):

    db = SessionLocal()

    models = db.query(HumanModelRecord).filter_by(user_id=user_id).all()

    db.close()

    if not models:
        return None

    timeline = []

    for i, m in enumerate(models):
        self_model = m.self_model or {}

        timeline.append({
            "t": i + 1,
            "score": self_model.get("avg_score", 0),
            "state": m.personality_state,
            "growth": m.growth_direction
        })

    scores = [t["score"] for t in timeline]

    if len(scores) == 1:
        trend = "NEW"
    elif scores[-1] > scores[0]:
        trend = "IMPROVING"
    elif scores[-1] < scores[0]:
        trend = "DECLINING"
    else:
        trend = "STABLE"

    if trend == "IMPROVING":
        prediction = "HIGH_STABILITY"
        risk = "LOW"
    elif trend == "DECLINING":
        prediction = "LOW_STABILITY"
        risk = "HIGH"
    else:
        prediction = "MEDIUM_STABILITY"
        risk = "MEDIUM"

    return {
        "user_id": user_id,
        "node_code": node_code,
        "timeline": timeline,
        "trend": trend,
        "prediction": prediction,
        "risk": risk
    }
