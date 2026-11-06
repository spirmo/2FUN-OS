# db/migrations/__init__.py


def run_migrations():
    """
    اجرای همه migrationهای موجود به ترتیب.
    """
    print("🚀 Running all migrations...")

    from db.database import engine
    from . import migrate_core_with_backup
    from . import migrate_colonies_with_backup
    from . import migrate_votes_and_strategic_with_backup
    from . import migrate_users_fk
    from . import create_uvi_ledger_tables
    from financial_core.twofunc.migrations import (
        create_twofunc_release_state,
        create_daily_settlement_tables,
    )

    migrate_core_with_backup.run()
    migrate_colonies_with_backup.run()
    migrate_votes_and_strategic_with_backup.run()
    migrate_users_fk.run()

    with engine.begin() as connection:
        create_twofunc_release_state.run_migration(connection)
        create_daily_settlement_tables.run_migration(connection)

    create_uvi_ledger_tables.run()

    print("✅ All migrations completed.")
