import sqlite3


class DatabaseImporter:

    def __init__(self, db_path):
        self.db_path = db_path


    def connect(self):
        return sqlite3.connect(self.db_path)


    def get_tables(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        tables = cursor.fetchall()

        conn.close()

        return [table[0] for table in tables]
