from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class ColonyVote(Base):
    __tablename__ = "colony_votes"

    id = Column(Integer, primary_key=True)
    colony_id = Column(Integer, ForeignKey("colonies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    target_user_id = Column(Integer, ForeignKey("users.id"))
    vote_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    colony = relationship("Colony", back_populates="votes", foreign_keys=[colony_id])
    voter = relationship("User", back_populates="votes_cast", foreign_keys=[user_id])
    target_user = relationship(
        "User", back_populates="votes_targeted", foreign_keys=[target_user_id]
    )


class Colony(Base):
    __tablename__ = "colonies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rank = Column(String)
    stars = Column(Integer, default=0)
    credit = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("colony_groups.id", ondelete="SET NULL"))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    creator = relationship(
        "User", back_populates="colonies_created", foreign_keys=[created_by]
    )
    group = relationship("ColonyGroup", back_populates="colonies")
    extension = relationship(
        "ColonyExtension",
        back_populates="colony",
        uselist=False,
        cascade="all, delete-orphan",
    )
    memberships = relationship(
        "ColonyMembership", back_populates="colony", cascade="all, delete"
    )
    council_votes = relationship(
        "ColonyCouncilVote",
        back_populates="colony",
        cascade="all, delete",
        foreign_keys="ColonyCouncilVote.colony_id",
    )
    votes = relationship(
        "ColonyVote",
        back_populates="colony",
        cascade="all, delete",
        foreign_keys="ColonyVote.colony_id",
    )


class ColonyExtension(Base):
    __tablename__ = "colonies_extension"

    colony_id = Column(
        Integer, ForeignKey("colonies.id", ondelete="CASCADE"), primary_key=True
    )
    short_code = Column(String(5), unique=True)
    description = Column(Text)
    language = Column(String, default="en")
    region = Column(String)
    member_count = Column(Integer, default=0)
    score = Column(BIGINT, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    reserved1 = Column(Text)
    reserved2 = Column(Text)
    reserved3 = Column(Text)
    reserved4 = Column(Text)
    reserved5 = Column(Text)
    reserved6 = Column(Text)
    reserved7 = Column(Text)

    colony = relationship("Colony", back_populates="extension")


class ColonyGroup(Base):
    __tablename__ = "colony_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    max_colonies = Column(Integer)

    colonies = relationship("Colony", back_populates="group")


class ColonyMembership(Base):
    __tablename__ = "colony_memberships"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    colony_id = Column(Integer, ForeignKey("colonies.id", ondelete="CASCADE"))
    join_count = Column(Integer, default=0)
    last_joined_at = Column(DateTime)
    last_active_at = Column(DateTime)
    status = Column(String, default="ACTIVE")
    removal_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="memberships", foreign_keys=[user_id])
    colony = relationship(
        "Colony", back_populates="memberships", foreign_keys=[colony_id]
    )


class ColonyCouncilVote(Base):
    __tablename__ = "colony_council_votes"

    id = Column(Integer, primary_key=True)
    colony_id = Column(Integer, ForeignKey("colonies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    target_user_id = Column(Integer, ForeignKey("users.id"))
    vote_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    colony = relationship(
        "Colony", back_populates="council_votes", foreign_keys=[colony_id]
    )
    user = relationship(
        "User", back_populates="council_votes_cast", foreign_keys=[user_id]
    )
    target_user = relationship(
        "User", back_populates="council_votes_targeted", foreign_keys=[target_user_id]
    )
