from db.database import SessionLocal
from db.migrations.create_human_models import HumanModelRecord
from datetime import datetime, timezone


def save_human_model(user_id: int, model: dict):

    db = SessionLocal()

    record = HumanModelRecord(
        user_id=user_id,
        self_model=model["self_model"],
        social_model=model["social_model"],
        personality_state=model["personality_state"],
        growth_direction=model["growth_direction"],
        created_at=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.close()

    print("✔ HUMAN MODEL SAVED")


if __name__ == "__main__":

    sample = {
        "self_model": {"avg_score": 5.0},
        "social_model": {"trust_score": 1, "rank": "MEMBER"},
        "personality_state": "STABLE",
        "growth_direction": "UPWARD"
    }

    save_human_model(1, sample)
