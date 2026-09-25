from db.database import SessionLocal
from sqlalchemy import text


DOMAINS = [
    ("IE", "آموزش اسلامی", "Islamic Education", "التعليم الإسلامي"),
    ("IC", "فرهنگ اسلامی", "Islamic Culture", "الثقافة الإسلامية"),
    ("IEC", "اقتصاد اسلامی", "Islamic Economics", "الاقتصاد الإسلامي"),
    ("AI", "ایران باستان", "Ancient Iran", "إيران القديمة"),
    ("SN", "جامعه‌شناسی ملت‌ها", "Sociology of Nations", "علم اجتماع الأمم"),
    ("GK", "دانش عمومی", "General Knowledge", "المعرفة العامة"),
    ("2FUN", "پلتفرم توفان", "2FUN Platform", "منصة توفان"),
]


def seed():
    db = SessionLocal()

    try:
        for code, fa, en, ar in DOMAINS:

            domain = db.execute(
                text(
                    "SELECT id FROM domains WHERE code=:code"
                ),
                {"code": code}
            ).fetchone()

            if not domain:
                db.execute(
                    text(
                        """
                        INSERT INTO domains
                        (code,name_fa,name_en,name_ar,status,created_at)
                        VALUES
                        (:code,:fa,:en,:ar,'APPROVED',datetime('now'))
                        """
                    ),
                    {
                        "code": code,
                        "fa": fa,
                        "en": en,
                        "ar": ar,
                    }
                )

                domain = db.execute(
                    text(
                        "SELECT id FROM domains WHERE code=:code"
                    ),
                    {"code": code}
                ).fetchone()


            topic_code = f"{code}_GENERAL"

            exists = db.execute(
                text(
                    "SELECT id FROM topics WHERE code=:code"
                ),
                {"code": topic_code}
            ).fetchone()


            if not exists:
                db.execute(
                    text(
                        """
                        INSERT INTO topics
                        (domain_id,code,name_fa,name_en,name_ar,status,created_at)
                        VALUES
                        (:domain_id,:code,:fa,:en,:ar,'APPROVED',datetime('now'))
                        """
                    ),
                    {
                        "domain_id": domain[0],
                        "code": topic_code,
                        "fa": f"{fa} - عمومی",
                        "en": f"{en} - General",
                        "ar": f"{ar} - عام",
                    }
                )

        db.commit()
        print("Knowledge taxonomy seed completed")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
