from sqlalchemy import text
from db.core.engine import SessionLocal
from db.core.user_id import generate_user_id, generate_personal_code


def add_user_id_column():
    with SessionLocal() as session:
        cols = session.execute(text("PRAGMA table_info(users);")).fetchall()
        column_names = [c[1] for c in cols]

        if "user_id" not in column_names:
            session.execute(text("ALTER TABLE users ADD COLUMN user_id TEXT;"))
            session.commit()
            print("✅ user_id column added")
        else:
            print("ℹ️ user_id already exists")


def backfill_user_ids():
    with SessionLocal() as session:
        # 🚀 RAW SQL instead of ORM (FIX IMPORTANT)
        users = session.execute(text("""
            SELECT id, user_code, telegram_id
            FROM users
        """)).fetchall()

        for u in users:
            user_id = u[0]

            personal = generate_personal_code()

            country = 123
            province = 1
            county = 1
            city = 1

            structured_id = generate_user_id(
                country, province, county, city, personal
            )

            session.execute(text("""
                UPDATE users
                SET user_id = :user_id
                WHERE id = :id
            """), {"user_id": structured_id, "id": user_id})

        session.commit()
        print(f"✅ Backfilled {len(users)} users")


def create_unique_index():
    with SessionLocal() as session:
        session.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS ix_users_user_id
            ON users(user_id);
        """))
        session.commit()
        print("✅ Unique index created")


def run_migration():
    add_user_id_column()
    backfill_user_ids()
    create_unique_index()


if __name__ == "__main__":
    run_migration()
    print("🎯 Migration completed safely")
