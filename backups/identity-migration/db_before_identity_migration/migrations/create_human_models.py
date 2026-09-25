from db.database import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone


class HumanModelRecord(Base):
    __tablename__ = "human_models"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)

    self_model = Column(JSON)
    social_model = Column(JSON)

    personality_state = Column(String)
    growth_direction = Column(String)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def create_table():
    Base.metadata.create_all(engine)
    print("✔ human_models TABLE CREATED")


if __name__ == "__main__":
    create_table()
