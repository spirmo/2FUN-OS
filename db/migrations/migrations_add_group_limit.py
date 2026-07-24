# db/migrations/migrations_add_group_limit_orm.py
from sqlalchemy import Column, Integer
from sqlalchemy import inspect
from db.database import engine
from db.models import ColonyGroup


def run_migration():
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns("colony_groups")]

    if "max_colonies" not in columns:
        # ستون را اضافه می‌کنیم
        with engine.connect() as conn:
            conn.execute("ALTER TABLE colony_groups ADD COLUMN max_colonies INTEGER")
            print("✅ Column max_colonies added to colony_groups")
    else:
        print("ℹ️ Column max_colonies already exists")

    print("🚀 Migration completed successfully.")


if __name__ == "__main__":
    run_migration()


def run():
    print("Running migration: migrations_add_group_limit.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrations_add_group_limit.py done")
