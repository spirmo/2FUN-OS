from sqlalchemy import text
from db.database import engine


def run():
    with engine.connect() as conn:
        columns = {
            row[1]
            for row in conn.execute(
                text("PRAGMA table_info(concept_versions)")
            ).fetchall()
        }

        if "rejected_by" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE concept_versions "
                    "ADD COLUMN rejected_by TEXT"
                )
            )

        if "rejection_reason" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE concept_versions "
                    "ADD COLUMN rejection_reason TEXT"
                )
            )

        conn.commit()


if __name__ == "__main__":
    run()
    print("Concept Versions rejection fields migration completed successfully.")
