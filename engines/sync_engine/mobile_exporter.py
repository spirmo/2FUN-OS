import sqlite3
from datetime import datetime


class MobileExporter:

    DOMAIN_MAP = {
        "IE": "ISLAMIC_EDUCATION",
        "IC": "ISLAMIC_CULTURE",
        "IEC": "ISLAMIC_ECONOMICS",
        "AI": "ANCIENT_IRAN",
        "SN": "SOCIOLOGY_OF_NATIONS",
        "GK": "GENERAL_KNOWLEDGE",
        "2FUN": "GAME_AND_PROJECT",
        "ID": "IDENTITY",
        "ILA": "ISLAMIC_LIFE_ADAB",
    }


    def __init__(self, mobile_db, ecosystem_db):
        self.mobile_db = mobile_db
        self.ecosystem_db = ecosystem_db


    def connect_mobile(self):
        return sqlite3.connect(self.mobile_db)


    def connect_ecosystem(self):
        return sqlite3.connect(self.ecosystem_db)


    def export_concepts(self):

        mobile = self.connect_mobile()
        ecosystem = self.connect_ecosystem()

        src = mobile.cursor()
        dst = ecosystem.cursor()


        src.execute(
            """
            SELECT
            c.code,
            c.name_fa,
            c.description,
            t.code
            FROM concepts c
            JOIN topics t
            ON c.topic_id = t.id
            """
        )

        rows = src.fetchall()

        count = 0


        for code, title, description, domain_code in rows:

            domain = self.DOMAIN_MAP.get(domain_code)

            if not domain:
                continue


            dst.execute(
                """
                SELECT id
                FROM knowledge_nodes
                WHERE code=?
                """,
                (code,)
            )

            exists = dst.fetchone()


            if exists:
                continue


            dst.execute(
                """
                INSERT INTO knowledge_nodes
                (
                code,
                domain,
                title,
                description,
                status,
                version
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    domain,
                    title,
                    description or "",
                    "ACTIVE",
                    "1.0"
                )
            )

            count += 1


        ecosystem.commit()

        mobile.close()
        ecosystem.close()


        return {
            "status": "DONE",
            "exported": count
        }
