from db.database import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone

class ReputationRecord(Base):
    __tablename__ = "reputation_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    node_code = Column(String, index=True)

    score = Column(Integer)
    level = Column(String)

    signals = Column(JSON)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def create_table():
    Base.metadata.create_all(engine)
    print("Reputation table created")


if __name__ == "__main__":
    create_table()
