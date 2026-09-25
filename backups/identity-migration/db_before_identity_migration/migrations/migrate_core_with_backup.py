# db/migrations/migrate_core_with_backup.py
import sqlite3
import shutil
from datetime import datetime

DB_PATH = "db/2fun.db"
BACKUP_PATH = f"db/2fun_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"


def create_backup():
    shutil.copy(DB_PATH, BACKUP_PATH)
    print(f"Backup created at {BACKUP_PATH} ✅")


def migrate_users():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    # users table
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
    cur.execute("INSERT INTO users_new SELECT * FROM users;")
    cur.execute("DROP TABLE users;")
    cur.execute("ALTER TABLE users_new RENAME TO users;")
    cur.execute("CREATE INDEX ix_users_id ON users (id);")
    cur.execute("CREATE INDEX ix_users_colony ON users(colony_id);")
    cur.execute("CREATE INDEX ix_users_rank ON users(rank);")
    cur.execute("CREATE UNIQUE INDEX ix_users_telegram_id ON users (telegram_id);")
    cur.execute("CREATE UNIQUE INDEX ix_users_user_code ON users (user_code);")
    conn.commit()
    conn.close()
    print("Users table migration complete ✅")


def migrate_users_extension():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE users_extension_new (
            user_id INTEGER PRIMARY KEY,
            reserved1 TEXT,
            reserved2 TEXT,
            reserved3 TEXT,
            reserved4 TEXT,
            reserved5 TEXT,
            reserved6 TEXT,
            reserved7 TEXT,
            reserved8 TEXT,
            reserved9 TEXT,
            reserved10 TEXT,
            reserved11 TEXT,
            reserved12 TEXT,
            reserved13 TEXT,
            reserved14 TEXT,
            reserved15 TEXT,
            reserved16 TEXT,
            reserved17 TEXT,
            reserved18 TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO users_extension_new SELECT * FROM users_extension;")
    cur.execute("DROP TABLE users_extension;")
    cur.execute("ALTER TABLE users_extension_new RENAME TO users_extension;")
    cur.execute("CREATE INDEX ix_users_extension_user_id ON users_extension(user_id);")
    conn.commit()
    conn.close()
    print("Users_extension table migration complete ✅")


def migrate_rank_logs():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE rank_logs_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            old_rank TEXT,
            new_rank TEXT,
            change_type TEXT,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO rank_logs_new SELECT * FROM rank_logs;")
    cur.execute("DROP TABLE rank_logs;")
    cur.execute("ALTER TABLE rank_logs_new RENAME TO rank_logs;")
    conn.commit()
    conn.close()
    print("Rank_logs table migration complete ✅")


def main():
    create_backup()
    migrate_users()
    migrate_users_extension()
    migrate_rank_logs()
    print("All core tables migrated successfully 🎉")


if __name__ == "__main__":
    main()


def run():
    print("Running migration: migrate_core_with_backup.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrate_core_with_backup.py done")
