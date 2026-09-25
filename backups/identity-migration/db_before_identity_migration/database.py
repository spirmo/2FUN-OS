from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# ===============================
# مسیر دیتابیس
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent  # مسیر اصلی پروژه
DB_PATH = BASE_DIR / "db" / "2fun.db"

DB_URL = f"sqlite:///{DB_PATH}"  # URL SQLAlchemy برای SQLite

# ===============================
# Engine و Session
# ===============================
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},  # فقط برای SQLite
    echo=False,  # True برای debug SQL
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ===============================
# Base برای مدل‌ها
# ===============================
Base = declarative_base()
