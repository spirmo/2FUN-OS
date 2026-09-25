from sqlalchemy import inspect, text

from db.database import engine


def migrate():
    inspector = inspect(engine)
    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "temp_ban_until" in columns:
        print("TEMP_BAN_COLUMN=ALREADY_EXISTS")
        return

    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN temp_ban_until DATETIME"
            )
        )

    print("TEMP_BAN_COLUMN=ADDED")


if __name__ == "__main__":
    migrate()
