from datetime import datetime, timezone

from db.database import SessionLocal
from db.migrations.create_human_models_v2 import HumanModelV2


def save_human_model_v2(model):

    db = SessionLocal()

    record = HumanModelV2(
        user_id=model["user_id"],
        trait_profile=model["trait_profile"],
        strengths=model["strengths"],
        weaknesses=model["weaknesses"],
        dominant_domains=model["dominant_domains"],
        identity_state=model["identity_state"],
        growth_direction=model["growth_direction"],
        model_version=model["model_version"],
        created_at=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.close()

    return {
        "status": "HUMAN_MODEL_V2_SAVED"
    }
