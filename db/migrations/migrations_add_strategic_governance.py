from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from db.database import engine, Base
from datetime import datetime


# جدول‌ها به‌صورت ORM
class StrategicCouncilMember(Base):
    __tablename__ = "strategic_council_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Integer, default=1)


class StrategicDecision(Base):
    __tablename__ = "strategic_decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    emergency = Column(Integer, default=0)
    status = Column(String, default="PENDING")
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class StrategicVote(Base):
    __tablename__ = "strategic_votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    voter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vote = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    decision = relationship("StrategicDecision", backref="votes")
    voter = relationship("User", backref="strategic_votes")


class StrategicVeto(Base):
    __tablename__ = "strategic_veto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    veto_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    decision = relationship("StrategicDecision", backref="vetoes")
    veto_by_user = relationship("User", backref="strategic_vetoes")


class EmergencyLog(Base):
    __tablename__ = "emergency_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    decision_id = Column(
        Integer, ForeignKey("strategic_decisions.id", ondelete="CASCADE")
    )
    activated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    active = Column(Integer, default=1)

    decision = relationship("StrategicDecision", backref="emergencies")


class ProjectVetoEntity(Base):
    __tablename__ = "project_veto_entities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(String)
    active = Column(Integer, default=1)

    user = relationship("User", backref="project_vetoes")


# اجرای مایگریشن
def run_migration():
    Base.metadata.create_all(bind=engine)
    print("🚀 Strategic & emergency tables created successfully with ORM")


if __name__ == "__main__":
    run_migration()


def run():
    print("Running migration: migrations_add_strategic_governance.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrations_add_strategic_governance.py done")
