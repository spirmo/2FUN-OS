from db.database import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone


class IE002Record(Base):
    __tablename__ = "ie002_records"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)
    node_code = Column(String, default="IE002")

    trust_score = Column(Integer)
    signals = Column(JSON)

    rank = Column(String)
    next_rank = Column(String)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def create_table():
    Base.metadata.create_all(engine)
    print("✔ IE002 TABLE CREATED")


if __name__ == "__main__":
    create_table()
