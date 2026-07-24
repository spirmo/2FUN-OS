from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db.database import Base
from datetime import datetime


class RankLog(Base):
    __tablename__ = "rank_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_rank = Column(String)
    new_rank = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
