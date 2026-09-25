from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, CHAR
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import create_engine, inspect
from datetime import datetime
from config import DB_URL

Base = declarative_base()
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


# ===============================
# مدل‌ها
# ===============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    colony_id = Column(Integer, ForeignKey("colonies.id", ondelete="SET NULL"))
    rank = Column(String)
    stars = Column(Integer, default=0)
    credit = Column(Integer, default=100)
    violations = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    user_code = Column(CHAR(35), unique=True)
    role = Column(String, default="user")
    rank_step = Column(Integer, default=0)
    active = Column(Integer, default=1)


class ColonyGroup(Base):
    __tablename__ = "colony_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_colonies = Column(Integer, default=None)


class Colony(Base):
    __tablename__ = "colonies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey("colony_groups.id"))
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class RankLog(Base):
    __tablename__ = "rank_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    old_rank = Column(String)
    new_rank = Column(String)
    change_type = Column(String)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ColonyCouncilVote(Base):
    __tablename__ = "colony_council_votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colony_id = Column(Integer)
    user_id = Column(Integer)
    target_user_id = Column(Integer)
    vote_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# ===============================
# ایجاد جداول و مهاجرت ستون‌ها
# ===============================
def run_migrations():
    # ایجاد جداول اصلی
    Base.metadata.create_all(engine)

    # بررسی و اضافه کردن ستون active اگر وجود ندارد
    inspector = inspect(engine)
    if "active" not in [col["name"] for col in inspector.get_columns("users")]:
        with engine.connect() as conn:
            conn.execute("ALTER TABLE users ADD COLUMN active INTEGER DEFAULT 1")
            print("✅ Column 'active' added to users")

    print("🚀 ORM Migrations completed successfully.")


if __name__ == "__main__":
    run_migrations()


def run():
    print("Running migration: migrations.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrations.py done")
