from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from db.database import Base


class UserGovernance(Base):
    __tablename__ = "users_governance"

    user_code = Column(String, primary_key=True, index=True)

    trust_index = Column(Float, default=0)
    risk_index = Column(Float, default=0)
    stability_index = Column(Float, default=0)
    governance_score = Column(Float, default=0)

    discipline_status = Column(String)
    violation_history = Column(Integer, default=0)
    loyalty_index = Column(Float, default=0)
    retention_probability = Column(Float, default=0)
    long_term_participation = Column(Float, default=0)

    governance_status = Column(String, default="NOT_ELIGIBLE")
    strike_count = Column(Integer, default=0)

    stability_started_at = Column(DateTime)
    recovery_until = Column(DateTime)

    governance_level = Column(String, default="OBSERVER")
    stake_locked = Column(Float, default=0)

    # reserved fields
    reserved01 = Column(Text)
    reserved02 = Column(Text)
    reserved03 = Column(Text)
    reserved04 = Column(Text)
    reserved05 = Column(Text)
    reserved06 = Column(Text)
    reserved07 = Column(Text)
    reserved08 = Column(Text)
    reserved09 = Column(Text)
    reserved10 = Column(Text)
    reserved11 = Column(Text)
    reserved12 = Column(Text)
    reserved13 = Column(Text)
    reserved14 = Column(Text)
    reserved15 = Column(Text)
