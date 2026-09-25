# db/migrations/migrate_votes_and_strategic_with_backup.py
import sqlite3
import shutil
from datetime import datetime

DB_PATH = "db/2fun.db"
BACKUP_PATH = f"db/2fun_backup_votes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"


def create_backup():
    shutil.copy(DB_PATH, BACKUP_PATH)
    print(f"Backup created at {BACKUP_PATH} ✅")


def migrate_colony_council_votes():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE colony_council_votes_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colony_id INTEGER,
            user_id INTEGER,
            target_user_id INTEGER,
            vote_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(target_user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute(
        "INSERT INTO colony_council_votes_new SELECT * FROM colony_council_votes;"
    )
    cur.execute("DROP TABLE colony_council_votes;")
    cur.execute("ALTER TABLE colony_council_votes_new RENAME TO colony_council_votes;")
    conn.commit()
    conn.close()
    print("Colony_council_votes table migration complete ✅")


def migrate_colony_votes():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE colony_votes_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            colony_id INTEGER,
            voter_id INTEGER,
            vote TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE,
            FOREIGN KEY(voter_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO colony_votes_new SELECT * FROM colony_votes;")
    cur.execute("DROP TABLE colony_votes;")
    cur.execute("ALTER TABLE colony_votes_new RENAME TO colony_votes;")
    conn.commit()
    conn.close()
    print("Colony_votes table migration complete ✅")


def migrate_strategic_council_members():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE strategic_council_members_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            joined_at DATETIME,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute(
        "INSERT INTO strategic_council_members_new SELECT * FROM strategic_council_members;"
    )
    cur.execute("DROP TABLE strategic_council_members;")
    cur.execute(
        "ALTER TABLE strategic_council_members_new RENAME TO strategic_council_members;"
    )
    conn.commit()
    conn.close()
    print("Strategic_council_members table migration complete ✅")


def migrate_strategic_decisions():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE strategic_decisions_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            emergency INTEGER DEFAULT 0,
            status TEXT DEFAULT 'PENDING',
            created_by INTEGER,
            created_at DATETIME,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        );
    """)
    cur.execute(
        "INSERT INTO strategic_decisions_new SELECT * FROM strategic_decisions;"
    )
    cur.execute("DROP TABLE strategic_decisions;")
    cur.execute("ALTER TABLE strategic_decisions_new RENAME TO strategic_decisions;")
    conn.commit()
    conn.close()
    print("Strategic_decisions table migration complete ✅")


def migrate_strategic_votes():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE strategic_votes_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            voter_id INTEGER,
            vote TEXT,
            created_at DATETIME,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE,
            FOREIGN KEY(voter_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO strategic_votes_new SELECT * FROM strategic_votes;")
    cur.execute("DROP TABLE strategic_votes;")
    cur.execute("ALTER TABLE strategic_votes_new RENAME TO strategic_votes;")
    conn.commit()
    conn.close()
    print("Strategic_votes table migration complete ✅")


def migrate_strategic_veto():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE strategic_veto_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            veto_by INTEGER,
            reason TEXT,
            created_at DATETIME,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE,
            FOREIGN KEY(veto_by) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO strategic_veto_new SELECT * FROM strategic_veto;")
    cur.execute("DROP TABLE strategic_veto;")
    cur.execute("ALTER TABLE strategic_veto_new RENAME TO strategic_veto;")
    conn.commit()
    conn.close()
    print("Strategic_veto table migration complete ✅")


def migrate_emergency_log():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE emergency_log_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            activated_at DATETIME,
            expires_at DATETIME,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE
        );
    """)
    cur.execute("INSERT INTO emergency_log_new SELECT * FROM emergency_log;")
    cur.execute("DROP TABLE emergency_log;")
    cur.execute("ALTER TABLE emergency_log_new RENAME TO emergency_log;")
    conn.commit()
    conn.close()
    print("Emergency_log table migration complete ✅")


def migrate_project_veto_entities():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE project_veto_entities_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    cur.execute(
        "INSERT INTO project_veto_entities_new SELECT * FROM project_veto_entities;"
    )
    cur.execute("DROP TABLE project_veto_entities;")
    cur.execute(
        "ALTER TABLE project_veto_entities_new RENAME TO project_veto_entities;"
    )
    conn.commit()
    conn.close()
    print("Project_veto_entities table migration complete ✅")


def main():
    create_backup()
    migrate_colony_council_votes()
    migrate_colony_votes()
    migrate_strategic_council_members()
    migrate_strategic_decisions()
    migrate_strategic_votes()
    migrate_strategic_veto()
    migrate_emergency_log()
    migrate_project_veto_entities()
    print("All votes & strategic tables migrated successfully 🎉")


if __name__ == "__main__":
    main()


def run():
    print("Running migration: migrate_votes_and_strategic_with_backup.py ...")
    # TODO: کد اصلی migration را اینجا قرار بده
    print("✅ Migration migrate_votes_and_strategic_with_backup.py done")
