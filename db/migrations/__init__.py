# db/migrations/__init__.py


def run_migrations():
    """
    اجرای همه migrationهای موجود به ترتیب.
    """
    print("🚀 Running all migrations...")

    # هر فایل migration باید یک تابع run() داشته باشد
    from . import migrate_core_with_backup
    from . import migrate_colonies_with_backup
    from . import migrate_votes_and_strategic_with_backup
    from . import migrate_users_fk

    migrate_core_with_backup.run()
    migrate_colonies_with_backup.run()
    migrate_votes_and_strategic_with_backup.run()
    migrate_users_fk.run()

    print("✅ All migrations completed.")
