from db.database import engine
from sqlalchemy import text


def upgrade():
    with engine.begin() as conn:

        columns = [
            ("governance_status", "TEXT DEFAULT 'NOT_ELIGIBLE'"),
            ("strike_count", "INTEGER DEFAULT 0"),
            ("stability_started_at", "DATETIME"),
            ("recovery_until", "DATETIME"),
            ("governance_level", "TEXT DEFAULT 'OBSERVER'"),
            ("stake_locked", "REAL DEFAULT 0")
        ]

        existing = conn.execute(
            text("PRAGMA table_info(users_governance)")
        ).fetchall()

        existing_cols = {row[1] for row in existing}

        for col_name, col_type in columns:
            if col_name not in existing_cols:
                conn.execute(
                    text(
                        f"ALTER TABLE users_governance "
                        f"ADD COLUMN {col_name} {col_type}"
                    )
                )
                print(f"[OK] added: {col_name}")

    print("Governance v1.2 migration completed.")


if __name__ == "__main__":
    upgrade()
