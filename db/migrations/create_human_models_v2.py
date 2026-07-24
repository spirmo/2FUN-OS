from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime
)

from datetime import datetime, timezone

from db.database import Base


class HumanModelV2(Base):

    __tablename__ = "human_models_v2"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)

    trait_profile = Column(JSON)

    strengths = Column(JSON)

    weaknesses = Column(JSON)

    dominant_domains = Column(JSON)

    identity_state = Column(String)

    growth_direction = Column(String)

    model_version = Column(
        String,
        default="2.0"
    )

    created_at = Column(
        DateTime,
        default=lambda:
        datetime.now(timezone.utc)
    )
