from datetime import datetime, timedelta
from db.database import SessionLocal
from db.models import User, RankLog, ColonyGroup, Colony
from config import MAX_USER_STEP, INACTIVITY_DAYS

VIOLATION_LIMIT = 3
TEMP_BAN_DAYS = 120

rank_order = [
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


# ===============================
# لاگ رنک
# ===============================
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
# ارتقاء مرحله‌ای
# ===============================
def promote_user_step(user_id):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user or user.role in ["leader", "deputy1", "deputy2"]:
            return

        if user.rank_step + 1 < len(rank_order):
            old_rank = rank_order[user.rank_step]
            user.rank_step += 1
            user.rank = rank_order[user.rank_step]
            session.commit()

            insert_rank_log(user.id, old_rank, user.rank, "PROMOTION", "Step Promotion")
            print(f"User {user.id} promoted: {old_rank} → {user.rank}")


# ===============================
# ارتقاء شرطی
# ===============================
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
# ثبت تخلف
# ===============================
def add_violation(user_id, reason, colony_id=None):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return

        user.violations += 1
        print(f"User {user_id} violation added → total = {user.violations}")

        if user.violations >= VIOLATION_LIMIT:
            user.colony_id = None
            user.temp_ban_until = datetime.now() + timedelta(days=TEMP_BAN_DAYS)
            print(f"User {user_id} removed & banned for {TEMP_BAN_DAYS} days")

        session.commit()


# ===============================
# حذف کاربران غیرفعال
# ===============================
def auto_remove_inactive_users():
    cutoff_date = datetime.now() - timedelta(days=INACTIVITY_DAYS)

    with SessionLocal() as session:
        users = session.query(User).filter(User.last_active != None).all()

        for user in users:
            if user.last_active < cutoff_date:
                if user.colony_id:
                    user.colony_id = None
                    print(f"User {user.id} auto-removed due to inactivity")
                elif user.home_colony_id:
                    user.colony_id = user.home_colony_id
                    print(f"User {user.id} returned to home colony")

        session.commit()


# ===============================
# ورود به کلونی
# ===============================
def join_colony(user_id, colony_id):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return

        if user.temp_ban_until and datetime.now() < user.temp_ban_until:
            print(f"User {user_id} banned until {user.temp_ban_until}")
            return

        initial_score = user.stars + user.credit // 10 - user.violations * 3
        rank_index = min(initial_score // 5, len(rank_order) - 1)

        user.colony_id = colony_id
        user.rank = rank_order[rank_index]
        user.stars = min(rank_index, 5)

        session.commit()
        print(f"User {user_id} joined colony {colony_id} with rank {user.rank}")


# ===============================
# ایجاد گروه و کلونی
# ===============================
def create_colony_group(leader_id, group_name, max_colonies=None):
    with SessionLocal() as session:
        group = ColonyGroup(name=group_name, max_colonies=max_colonies)
        session.add(group)
        session.commit()
        print(f"Leader {leader_id} created group '{group_name}'")
        return group.id


def create_colony(leader_id, colony_name, group_id):
    with SessionLocal() as session:
        colony = Colony(name=colony_name, group_id=group_id, created_by=leader_id)
        session.add(colony)
        session.commit()
        print(f"Leader {leader_id} created colony '{colony_name}'")
        return colony.id


def run():
    print("Running migration: promotion_engine.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration promotion_engine.py done")
