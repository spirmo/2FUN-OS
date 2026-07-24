from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class StrategicCouncilMember(Base):
    __tablename__ = "strategic_council_members"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    joined_at = Column(DateTime)
    active = Column(Integer, default=1)

    user = relationship("User")


class StrategicDecision(Base):
    __tablename__ = "strategic_decisions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    emergency = Column(Integer, default=0)
    status = Column(String, default="PENDING")
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime)

    creator = relationship("User")
    votes = relationship(
        "StrategicVote", back_populates="decision", cascade="all, delete"
    )
    vetoes = relationship(
        "StrategicVeto", back_populates="decision", cascade="all, delete"
    )
    emergencies = relationship(
        "EmergencyLog", back_populates="decision", cascade="all, delete"
    )


class StrategicVote(Base):
    __tablename__ = "strategic_votes"
    id = Column(Integer, primary_key=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    voter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vote = Column(String)
    created_at = Column(DateTime)

    decision = relationship("StrategicDecision", back_populates="votes")
    voter = relationship("User", back_populates="strategic_votes")


class StrategicVeto(Base):
    __tablename__ = "strategic_veto"
    id = Column(Integer, primary_key=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    veto_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reason = Column(Text)
    created_at = Column(DateTime)

    decision = relationship("StrategicDecision", back_populates="vetoes")
    veto_by_user = relationship("User", back_populates="strategic_vetoes")


class EmergencyLog(Base):
    __tablename__ = "emergency_log"
    id = Column(Integer, primary_key=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    activated_at = Column(DateTime)
    expires_at = Column(DateTime)
    active = Column(Integer, default=1)

    decision = relationship("StrategicDecision", back_populates="emergencies")


class ProjectVetoEntity(Base):
    __tablename__ = "project_veto_entities"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(String)
    active = Column(Integer, default=1)

    user = relationship("User", back_populates="project_vetoes")
