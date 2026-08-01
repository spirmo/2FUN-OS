import sqlite3


class DatabaseMerger:

    def __init__(self, target_db):
        self.target_db = target_db


    def connect(self):
        return sqlite3.connect(self.target_db)


    def concept_exists(self, cursor, code):
        cursor.execute(
            """
            SELECT id 
            FROM knowledge_nodes
            WHERE code=?
            """,
            (code,)
        )

        return cursor.fetchone()


    def merge_concepts(self, concepts):

        conn = self.connect()
        cursor = conn.cursor()

        inserted = 0
        skipped = 0

        for concept in concepts:

            code = concept["code"]

            if self.concept_exists(cursor, code):
                skipped += 1
                continue


            cursor.execute(
                """
                INSERT INTO knowledge_nodes
                (
                    code,
                    title,
                    description,
                    domain,
                    status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    code,
                    concept["title"],
                    concept.get("description", ""),
                    concept["domain"],
                    "ACTIVE"
                )
            )

            inserted += 1


        conn.commit()
        conn.close()


        return {
            "status": "DONE",
            "inserted": inserted,
            "skipped": skipped
        }
