# db/core/engine.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import (
    User,
    UserExtension,
    RankLog,
    Colony,
    ColonyGroup,
    ColonyMembership,
    ColonyCouncilVote,
    ColonyVote,
    StrategicCouncilMember,
    StrategicDecision,
    StrategicVote,
    StrategicVeto,
    ProjectVetoEntity,
)
from config import MAX_USER_STEP, INACTIVITY_DAYS, VIOLATION_LIMIT, TEMP_BAN_DAYS


# ===============================
# Migration اتوماتیک
# ===============================
def run_migrations():
    import db.migrations

    db.migrations.run_migrations()


# ===============================
# کاربران
# ===============================
def get_users():
    with SessionLocal() as session:
        return session.query(User).all()


def update_user_rank(user_id: int, new_rank: str):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if user:
            user.rank = new_rank
            session.commit()


def insert_rank_log(user_id, old_rank, new_rank, change_type, reason):
    with SessionLocal() as session:
        log = RankLog(
            user_id=user_id,
            old_rank=old_rank,
            new_rank=new_rank,
            change_type=change_type,
            reason=reason,
        )
        session.add(log)
        session.commit()


# ===============================
# ثبت تخلف کاربر
# ===============================
def add_violation(user_id, reason, colony_host_id=None):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return
        user.violations += 1
        session.commit()
        print(f"User {user_id} violation added → total = {user.violations}")

        if user.violations >= VIOLATION_LIMIT and user.colony_id:
            user.colony_id = None
            user.temp_ban_until = datetime.utcnow() + timedelta(days=TEMP_BAN_DAYS)
            session.commit()
            print(f"User {user_id} auto-removed from colony (violation limit)")


# ===============================
# حذف خودکار کاربران غیرفعال
# ===============================
def auto_remove_inactive_users():
    cutoff_date = datetime.utcnow() - timedelta(days=INACTIVITY_DAYS)
    with SessionLocal() as session:
        users = session.query(User).filter(User.last_active != None).all()
        for user in users:
            if user.last_active < cutoff_date:
                if user.colony_id:
                    user.colony_id = None
                    print(
                        f"User {user.id} ({user.username}) auto-removed from host colony due to inactivity"
                    )
                elif not user.colony_id and user.home_colony_id:
                    user.colony_id = user.home_colony_id
                    print(f"User {user.id} ({user.username}) returned to home colony")
        session.commit()


# ===============================
# ارتقاء مرحله‌ای و شرطی
# ===============================
RANK_ORDER = [
    "simple",
    "D",
    "D*",
    "D**",
    "D***",
    "D****",
    "D*****",
    "C",
    "C*",
    "C**",
    "C***",
    "C****",
    "C*****",
    "B",
    "B*",
    "B**",
    "B***",
    "B****",
    "B*****",
    "A",
    "A*",
    "A**",
    "A***",
    "A****",
    "A*****",
]


def promote_user_step(user_id):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user or user.role in ["leader", "deputy1", "deputy2"]:
            return
        if user.rank_step + 1 < len(RANK_ORDER):
            old_rank = RANK_ORDER[user.rank_step]
            new_rank = RANK_ORDER[user.rank_step + 1]
            user.rank = new_rank
            user.rank_step += 1
            session.commit()
            insert_rank_log(user.id, old_rank, new_rank, "PROMOTION", "Step Promotion")
            print(f"User {user.id} promoted: {old_rank} → {new_rank}")


def promote_user_conditional(user_id):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user or user.role in ["leader", "deputy1", "deputy2"]:
            return
        score = user.stars + user.credit // 10 - user.violations * 3
        steps_to_promote = min(score // 5, MAX_USER_STEP - user.rank_step)
        for _ in range(steps_to_promote):
            promote_user_step(user.id)


# ===============================
# مدیریت کلونی و گروه
# ===============================
def create_colony_group(leader_id, group_name, max_colonies=None):
    with SessionLocal() as session:
        group = ColonyGroup(name=group_name, max_colonies=max_colonies)
        session.add(group)
        session.commit()
        print(
            f"Leader {leader_id} created colony group '{group_name}' → max {max_colonies}"
        )
        return group.id


def create_colony(leader_id, colony_name, group_id):
    with SessionLocal() as session:
        colony = Colony(name=colony_name, group_id=group_id, created_by=leader_id)
        session.add(colony)
        session.commit()
        print(f"Leader {leader_id} created colony '{colony_name}'")
        return colony.id


# ===============================
# رأی‌گیری ارکان کلونی
# ===============================
def vote_remove_user(colony_id, target_user_id, voter_user_id, approve=True):
    with SessionLocal() as session:
        target_user = session.get(User, target_user_id)
        if not target_user or target_user.colony_id != colony_id:
            print("User is not a member of this colony.")
            return

        exists = (
            session.query(ColonyCouncilVote)
            .filter_by(
                colony_id=colony_id,
                target_user_id=target_user_id,
                user_id=voter_user_id,
            )
            .first()
        )
        if exists:
            print("This voter has already voted.")
            return

        vote = ColonyCouncilVote(
            colony_id=colony_id,
            target_user_id=target_user_id,
            user_id=voter_user_id,
            vote_type="APPROVE" if approve else "REJECT",
        )
        session.add(vote)
        session.commit()

        approve_count = (
            session.query(ColonyCouncilVote)
            .filter_by(
                colony_id=colony_id, target_user_id=target_user_id, vote_type="APPROVE"
            )
            .count()
        )
        if approve_count >= 3:
            target_user.colony_id = None
            session.commit()
            print(
                f"User {target_user_id} removed from colony {colony_id} by council vote"
            )


# ===============================
# شورای راهبردی، رأی‌گیری و وتو
# ===============================
def add_to_strategic_council(user_id):
    with SessionLocal() as session:
        exists = (
            session.query(StrategicCouncilMember).filter_by(user_id=user_id).first()
        )
        if not exists:
            member = StrategicCouncilMember(
                user_id=user_id, joined_at=datetime.utcnow(), active=1
            )
            session.add(member)
            session.commit()
            print(f"User {user_id} added to strategic council")


def cast_strategic_vote(decision_id, voter_id, vote_value):
    with SessionLocal() as session:
        vote = StrategicVote(
            decision_id=decision_id,
            voter_id=voter_id,
            vote=vote_value,
            created_at=datetime.utcnow(),
        )
        session.add(vote)
        session.commit()


def apply_strategic_veto(decision_id, user_id, reason):
    with SessionLocal() as session:
        veto = StrategicVeto(
            decision_id=decision_id,
            veto_by=user_id,
            reason=reason,
            created_at=datetime.utcnow(),
        )
        session.add(veto)
        session.commit()


def add_project_veto_entity(user_id, role):
    with SessionLocal() as session:
        entity = ProjectVetoEntity(user_id=user_id, role=role, active=1)
        session.add(entity)
        session.commit()
