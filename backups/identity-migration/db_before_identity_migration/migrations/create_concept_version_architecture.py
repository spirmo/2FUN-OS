from sqlalchemy import text
from db.database import engine


def run():
    with engine.begin() as conn:

        # =========================================================
        # 1. CONCEPT IDENTITY
        # =========================================================

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS concepts_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_code TEXT UNIQUE,

                creator TEXT,

                current_version TEXT DEFAULT '1.0',

                current_status TEXT
                    DEFAULT 'OPEN_FOR_COMPLETION',

                current_completeness INTEGER
                    DEFAULT 0,

                created_at TEXT,

                updated_at TEXT
            )
        """))

        # =========================================================
        # 2. CONCEPT VERSION
        # =========================================================

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS concept_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_id INTEGER NOT NULL,

                concept_code TEXT NOT NULL,

                version TEXT NOT NULL,

                payload TEXT NOT NULL,

                completeness INTEGER DEFAULT 0,

                status TEXT
                    DEFAULT 'OPEN_FOR_COMPLETION',

                created_by TEXT,

                created_at TEXT,

                approved_by TEXT,

                approved_at TEXT,

                snapshot_reference TEXT,

                UNIQUE(concept_code, version)
            )
        """))

        # =========================================================
        # 3. VERSION HISTORY
        # =========================================================

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS concept_version_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_id INTEGER,

                concept_code TEXT,

                version TEXT,

                actor TEXT,

                event_type TEXT,

                from_state TEXT,

                to_state TEXT,

                details TEXT,

                created_at TEXT
            )
        """))

        # =========================================================
        # 4. APPROVAL QUEUE
        # =========================================================

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS concept_approval_queue_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_id INTEGER,

                concept_code TEXT,

                version TEXT NOT NULL,

                creator_user_code TEXT,

                source_mobile_id TEXT,

                payload TEXT NOT NULL,

                status TEXT
                    DEFAULT 'SUBMITTED',

                created_at DATETIME,

                approved_by TEXT,

                reviewed_at DATETIME,

                UNIQUE(concept_code, version)
            )
        """))

        # =========================================================
        # 5. INDEXES
        # =========================================================

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_concept_versions_concept
            ON concept_versions(concept_id)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_concept_versions_code
            ON concept_versions(concept_code)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_concept_history_concept
            ON concept_version_history(concept_id)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_concept_queue_status
            ON concept_approval_queue_v2(status)
        """))


if __name__ == "__main__":
    run()
    print("Concept Version Architecture Migration created successfully.")
