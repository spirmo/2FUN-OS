from sqlalchemy import text
from db.database import engine


def run():

    with engine.connect() as conn:

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS concept_approval_queue (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            concept_code TEXT UNIQUE,

            creator_user_code TEXT,

            source_mobile_id TEXT,

            title TEXT,

            domain TEXT,

            payload TEXT,

            status TEXT DEFAULT 'SUBMITTED',

            approved_by TEXT,

            created_at DATETIME,

            reviewed_at DATETIME

        )
        """))

        conn.commit()


if __name__ == "__main__":
    run()
    print("Concept Approval Queue created")
