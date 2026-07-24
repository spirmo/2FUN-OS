# db/migrations/migrate_users_fk.py
import sqlite3

DB_PATH = "db/2fun.db"


def migrate_users_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")  # غیرفعال کردن FK موقت
    cur = conn.cursor()

    # 1️⃣ جدول جدید با FK بساز
    cur.execute("""
        CREATE TABLE users_new (
            id INTEGER NOT NULL PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            language VARCHAR,
            state VARCHAR,
            username TEXT,
            colony_id INTEGER,
            rank TEXT,
            stars INTEGER DEFAULT 0,
            credit INTEGER DEFAULT 100,
            violations INTEGER DEFAULT 0,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_code CHAR(35) UNIQUE,
            host_colonies TEXT DEFAULT NULL,
            role TEXT DEFAULT 'user',
            rank_step INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE SET NULL
        );
    """)

    # 2️⃣ داده‌ها را منتقل کن
    cur.execute("INSERT INTO users_new SELECT * FROM users;")

    # 3️⃣ جدول قدیمی را حذف کن
    cur.execute("DROP TABLE users;")

    # 4️⃣ جدول جدید را rename کن
    cur.execute("ALTER TABLE users_new RENAME TO users;")

    # 5️⃣ index ها را دوباره بساز
    cur.execute("CREATE INDEX ix_users_id ON users (id);")
    cur.execute("CREATE INDEX ix_users_colony ON users(colony_id);")
    cur.execute("CREATE INDEX ix_users_rank ON users(rank);")
    cur.execute("CREATE UNIQUE INDEX ix_users_telegram_id ON users (telegram_id);")
    cur.execute("CREATE UNIQUE INDEX ix_users_user_code ON users (user_code);")

    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON;")  # فعال کردن FK دوباره
    conn.close()
    print("Migration users table complete ✅")


if __name__ == "__main__":
    migrate_users_table()


def run():
    print("Running migration: migrate_users_fk.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrate_users_fk.py done")
