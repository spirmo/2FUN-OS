from db.database import engine


def run_migration():
    with engine.begin() as connection:

        connection.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS uvi_transfer_operations (
                operation_id TEXT PRIMARY KEY,
                source_user_id TEXT NOT NULL,
                destination_user_id TEXT NOT NULL,
                amount TEXT NOT NULL,
                currency TEXT NOT NULL,
                debit_transaction_id TEXT NOT NULL UNIQUE,
                credit_transaction_id TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            )
        """)
        connection.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS uvi_ledger_entries (
                transaction_id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                amount TEXT NOT NULL,
                currency TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}'
            )
        """)
        connection.exec_driver_sql("""
            CREATE INDEX IF NOT EXISTS ix_uvi_ledger_user_currency
            ON uvi_ledger_entries (user_id, currency)
        """)
        connection.exec_driver_sql("""
            CREATE INDEX IF NOT EXISTS ix_uvi_ledger_event_id
            ON uvi_ledger_entries (event_id)
        """)


def run():
    run_migration()
