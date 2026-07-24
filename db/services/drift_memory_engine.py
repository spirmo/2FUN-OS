from db.database import SessionLocal
from db.migrations.create_human_models import HumanModelRecord
from datetime import datetime, timezone


def store_drift(user_id: int, drift_data: dict):

    db = SessionLocal()

    record = HumanModelRecord(
        user_id=user_id,
        self_model={
            "type": "DRIFT_MEMORY",
            "data": drift_data
        },
        social_model={},
        personality_state=drift_data.get("learning_state", "UNKNOWN"),
        growth_direction="EVOLUTION_TRACKED",
        created_at=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.close()

    return {
        "status": "DRIFT_STORED",
        "user_id": user_id
    }
