from sqlalchemy import text
from db.database import SessionLocal


def upgrade():
    with SessionLocal() as db:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS translation_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                translation_key TEXT NOT NULL,
                language TEXT NOT NULL,
                translation TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'Draft',
                version TEXT NOT NULL DEFAULT '1.0',

                created_by TEXT,
                verified_by TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,

                source_type TEXT NOT NULL DEFAULT 'MANUAL',

                UNIQUE (translation_key, language, version)
            )
        """))

        db.commit()


if __name__ == "__main__":
    upgrade()
