from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    language = Column(String)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # ویژگی‌های شخصیت‌شناسی
    risk_tolerance = Column(String, nullable=True)
    group_behavior = Column(String, nullable=True)
