from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=True)
    language = Column(String, nullable=True)
    state = Column(String, nullable=True)
    username = Column(String, nullable=True)
    colony_id = Column(
        Integer, ForeignKey("colonies.id", ondelete="SET NULL"), nullable=True
    )
    home_colony_id = Column(
        Integer, ForeignKey("colonies.id", ondelete="SET NULL"), nullable=True
    )
    rank = Column(String, nullable=True)
    stars = Column(Integer, default=0)
    credit = Column(Integer, default=100)
    violations = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    user_code = Column(CHAR(35), unique=True, nullable=True)
    host_colonies = Column(Text, default=None)
    role = Column(String, default="user")
    rank_step = Column(Integer, default=0)
    active = Column(Integer, default=1)
    last_active = Column(DateTime, nullable=True)

    # Relationships
    extension = relationship(
        "UserExtension",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    colonies_created = relationship(
        "Colony",
        back_populates="creator",
        cascade="all, delete",
        foreign_keys="[Colony.created_by]",
    )
    memberships = relationship(
        "ColonyMembership",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="[ColonyMembership.user_id]",
    )
    colony = relationship("Colony", foreign_keys=[colony_id])
    home_colony = relationship("Colony", foreign_keys=[home_colony_id])

    votes_cast = relationship(
        "ColonyVote",
        back_populates="voter",
        cascade="all, delete",
        foreign_keys="[ColonyVote.user_id]",
    )
    votes_targeted = relationship(
        "ColonyVote",
        back_populates="target_user",
        cascade="all, delete",
        foreign_keys="[ColonyVote.target_user_id]",
    )
    council_votes_cast = relationship(
        "ColonyCouncilVote",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="[ColonyCouncilVote.user_id]",
    )
    council_votes_targeted = relationship(
        "ColonyCouncilVote",
        back_populates="target_user",
        cascade="all, delete",
        foreign_keys="[ColonyCouncilVote.target_user_id]",
    )

    strategic_votes = relationship(
        "StrategicVote", back_populates="voter", cascade="all, delete"
    )
    strategic_vetoes = relationship(
        "StrategicVeto", back_populates="veto_by_user", cascade="all, delete"
    )
    project_vetoes = relationship(
        "ProjectVetoEntity", back_populates="user", cascade="all, delete"
    )


class UserExtension(Base):
    __tablename__ = "users_extension"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    reserved1 = Column(Text)
    reserved2 = Column(Text)
    reserved3 = Column(Text)
    reserved4 = Column(Text)
    reserved5 = Column(Text)
    reserved6 = Column(Text)
    reserved7 = Column(Text)
    reserved8 = Column(Text)
    reserved9 = Column(Text)
    reserved10 = Column(Text)
    reserved11 = Column(Text)
    reserved12 = Column(Text)
    reserved13 = Column(Text)
    reserved14 = Column(Text)
    reserved15 = Column(Text)
    reserved16 = Column(Text)
    reserved17 = Column(Text)
    reserved18 = Column(Text)

    user = relationship("User", back_populates="extension")
