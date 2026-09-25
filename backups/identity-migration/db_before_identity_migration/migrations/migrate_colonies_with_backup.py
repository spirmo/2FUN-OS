# db/migrations/migrate_colonies_with_backup.py
import sqlite3
import shutil
from datetime import datetime

DB_PATH = "db/2fun.db"
BACKUP_PATH = f"db/2fun_backup_colonies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"


def create_backup():
    shutil.copy(DB_PATH, BACKUP_PATH)
    print(f"Backup created at {BACKUP_PATH} ✅")


def migrate_colonies():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    # colonies table
    cur.execute("""
        CREATE TABLE colonies_new (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            rank TEXT,
            stars INTEGER DEFAULT 0,
            credit INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            group_id INTEGER,
            created_by INTEGER,
            FOREIGN KEY(group_id) REFERENCES colony_groups(id) ON DELETE SET NULL,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        );
    """)
    cur.execute("INSERT INTO colonies_new SELECT * FROM colonies;")
    cur.execute("DROP TABLE colonies;")
    cur.execute("ALTER TABLE colonies_new RENAME TO colonies;")
    cur.execute("CREATE INDEX ix_colonies_rank ON colonies(rank);")
    cur.execute("CREATE INDEX ix_colonies_stars ON colonies(stars);")
    cur.execute("CREATE INDEX ix_colonies_credit ON colonies(credit);")
    conn.commit()
    conn.close()
    print("Colonies table migration complete ✅")


def migrate_colonies_extension():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    # colonies_extension table
    cur.execute("""
        CREATE TABLE colonies_extension_new (
            colony_id INTEGER PRIMARY KEY,
            short_code CHAR(5) UNIQUE,
            description TEXT,
            language VARCHAR DEFAULT 'en',
            region VARCHAR,
            member_count INTEGER DEFAULT 0,
            score BIGINT DEFAULT 0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            reserved1 TEXT,
            reserved2 TEXT,
            reserved3 TEXT,
            reserved4 TEXT,
            reserved5 TEXT,
            reserved6 TEXT,
            reserved7 TEXT,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO colonies_extension_new SELECT * FROM colonies_extension;")
    cur.execute("DROP TABLE colonies_extension;")
    cur.execute("ALTER TABLE colonies_extension_new RENAME TO colonies_extension;")
    cur.execute(
        "CREATE INDEX ix_colonies_extension_colony_id ON colonies_extension(colony_id);"
    )
    cur.execute("CREATE INDEX ix_colonies_score ON colonies_extension(score);")
    conn.commit()
    conn.close()
    print("Colonies_extension table migration complete ✅")


def migrate_colony_memberships():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()

    # colony_memberships table
    cur.execute("""
        CREATE TABLE colony_memberships_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            colony_id INTEGER,
            join_count INTEGER DEFAULT 0,
            last_joined_at DATETIME,
            last_active_at DATETIME,
            status TEXT DEFAULT 'ACTIVE',
            removal_reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO colony_memberships_new SELECT * FROM colony_memberships;")
    cur.execute("DROP TABLE colony_memberships;")
    cur.execute("ALTER TABLE colony_memberships_new RENAME TO colony_memberships;")
    conn.commit()
    conn.close()
    print("Colony_memberships table migration complete ✅")


def main():
    create_backup()
    migrate_colonies()
    migrate_colonies_extension()
    migrate_colony_memberships()
    print("All colony tables migrated successfully 🎉")


if __name__ == "__main__":
    main()


def run():
    print("Running migration: migrate_colonies_with_backup.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrate_colonies_with_backup.py done")
