import sqlite3
from datetime import datetime


class ConceptMapper:

    DOMAIN_MAP = {
        "ISLAMIC_EDUCATION": "IE",
        "ISLAMIC_CULTURE": "IC",
        "ISLAMIC_ECONOMICS": "IEC",
        "ANCIENT_IRAN": "AI",
        "SOCIOLOGY_OF_NATIONS": "SN",
        "GENERAL_KNOWLEDGE": "GK",
        "GAME_AND_PROJECT": "2FUN",
        "IDENTITY": "ID",
        "ISLAMIC_LIFE_ADAB": "ILA",
    }

    DOMAIN_NAMES = {
        "ID": {
            "fa": "هویت",
            "en": "Identity",
            "ar": "الهوية",
        },
        "ILA": {
            "fa": "آداب زندگی اسلامی",
            "en": "Islamic Life Ethics",
            "ar": "آداب الحياة الإسلامية",
        },
    }


    def __init__(self, source_db, target_db):
        self.source_db = source_db
        self.target_db = target_db


    def connect_source(self):
        return sqlite3.connect(self.source_db)


    def connect_target(self):
        return sqlite3.connect(self.target_db)


    def ensure_domain(self, cursor, domain_code):

        cursor.execute(
            "SELECT id FROM domains WHERE code=?",
            (domain_code,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]


        name = self.DOMAIN_NAMES.get(
            domain_code,
            {
                "fa": domain_code,
                "en": domain_code,
                "ar": domain_code,
            }
        )


        cursor.execute(
            """
            INSERT INTO domains
            (
                code,
                name_fa,
                name_en,
                name_ar,
                description,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                domain_code,
                name["fa"],
                name["en"],
                name["ar"],
                "",
                "ACTIVE",
                datetime.utcnow().isoformat()
            )
        )

        return cursor.lastrowid


    def migrate_concepts(self):

        source = self.connect_source()
        target = self.connect_target()

        src = source.cursor()
        dst = target.cursor()


        src.execute(
            """
            SELECT
            code,
            title,
            description,
            domain
            FROM knowledge_nodes
            """
        )

        rows = src.fetchall()


        count = 0


        for row in rows:

            code, title, description, domain = row


            domain_code = self.DOMAIN_MAP.get(domain)

            if not domain_code:
                continue


            domain_id = self.ensure_domain(
                dst,
                domain_code
            )


            dst.execute(
                """
                SELECT id FROM topics
                WHERE code=?
                """,
                (domain_code,)
            )

            topic = dst.fetchone()


            if not topic:

                dst.execute(
                    """
                    INSERT INTO topics
                    (
                    domain_id,
                    code,
                    name_fa,
                    name_en,
                    name_ar,
                    status,
                    created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        domain_id,
                        domain_code,
                        title,
                        title,
                        title,
                        "ACTIVE",
                        datetime.utcnow().isoformat()
                    )
                )

                topic_id = dst.lastrowid

            else:
                topic_id = topic[0]


            dst.execute(
                """
                INSERT INTO concepts
                (
                topic_id,
                code,
                name_fa,
                name_en,
                name_ar,
                description,
                status,
                created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    topic_id,
                    code,
                    title,
                    title,
                    title,
                    description or "",
                    "ACTIVE",
                    datetime.utcnow().isoformat()
                )
            )

            count += 1


        target.commit()

        source.close()
        target.close()


        return {
            "status": "DONE",
            "migrated": count
        }
