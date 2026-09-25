import os
import json
from shutil import copy2
from db.database import SessionLocal
from db.models import User

# مسیرها
JSON_DIR = "data"
BACKUP_DIR = "backup"

os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_json(file_name):
    src = os.path.join(JSON_DIR, file_name)
    dst = os.path.join(BACKUP_DIR, file_name)
    if os.path.exists(src):
        copy2(src, dst)
        print(f"✅ Backup created for {file_name}")
    else:
        print(f"⚠️ {file_name} not found")


def load_json(file_name):
    path = os.path.join(JSON_DIR, file_name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Could not parse {file_name}")
            return []


def insert_users_to_db(users):
    with SessionLocal() as session:
        inserted = 0
        for u in users:
            telegram_id = u.get("telegram_id")
            if not telegram_id:
                continue

            exists = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not exists:
                user = User(
                    telegram_id=telegram_id,
                    stars=u.get("stars", 0),
                    username=u.get("username"),
                )
                session.add(user)
                inserted += 1

        session.commit()
        print(f"✅ Inserted {inserted} users")


def main():
    for file_name in ["users.json", "scores.json", "tokens.json"]:
        backup_json(file_name)

    users = load_json("users.json")
    insert_users_to_db(users)

    print("🎉 انتقال JSON به دیتابیس انجام شد (ORM)")


if __name__ == "__main__":
    main()


def run():
    print("Running migration: json_to_db.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration json_to_db.py done")
