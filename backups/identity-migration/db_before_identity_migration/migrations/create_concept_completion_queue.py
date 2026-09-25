from sqlalchemy import text
from db.database import engine


def run():
    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS concept_completion_queue (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_id INTEGER NOT NULL,

                concept_code TEXT NOT NULL,

                current_completeness INTEGER DEFAULT 0,

                target_completeness INTEGER DEFAULT 36,

                status TEXT DEFAULT 'NEED_COMPLETION',

                created_at DATETIME,

                updated_at DATETIME,

                UNIQUE(concept_id)
            )
        """))


if __name__ == "__main__":
    run()
