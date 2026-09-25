from sqlalchemy import Column, Integer, String, DateTime, Float
from db.database import Base
from datetime import datetime


class XPLog(Base):
    __tablename__ = "xp_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_code = Column(String, index=True)
    action = Column(String)

    xp_gained = Column(Integer)
    multiplier = Column(Float)

    rank_step = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
