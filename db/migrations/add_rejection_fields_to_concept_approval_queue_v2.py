from sqlalchemy import text
from db.database import engine


def run():
    with engine.connect() as conn:

        # --------------------------------------------------
        # REJECTION AUDIT FIELDS
        # --------------------------------------------------

        columns = conn.execute(
            text("PRAGMA table_info(concept_approval_queue_v2)")
        ).mappings().all()

        existing = {row["name"] for row in columns}

        if "rejected_by" not in existing:
            conn.execute(
                text("""
                    ALTER TABLE concept_approval_queue_v2
                    ADD COLUMN rejected_by TEXT
                """)
            )

        if "rejection_reason" not in existing:
            conn.execute(
                text("""
                    ALTER TABLE concept_approval_queue_v2
                    ADD COLUMN rejection_reason TEXT
                """)
            )

        conn.commit()


if __name__ == "__main__":
    run()
    print(
        "Concept Approval Queue v2 rejection fields "
        "migration completed successfully."
    )
