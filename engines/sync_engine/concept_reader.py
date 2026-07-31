import sqlite3


class ConceptReader:

    def __init__(self, db_path):
        self.db_path = db_path


    def connect(self):
        return sqlite3.connect(self.db_path)


    def get_concepts(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM concepts
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    def get_concept_items(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM concept_items
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    def get_concept_system(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM concept_system
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    def get_concept_extensions(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM concept_extensions
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows
