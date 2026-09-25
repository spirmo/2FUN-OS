from db.database import SessionLocal
from db.models.knowledge_node import KnowledgeNode


def seed_ie002():

    db = SessionLocal()

    existing = db.query(KnowledgeNode).filter_by(code="IE002").first()
    if existing:
        print("IE002 already exists")
        db.close()
        return

    node = KnowledgeNode(
        code="IE002",
        domain="ISLAMIC_EDUCATION",
        name="TRUST",
        title="اعتماد اجتماعی",

        description="توانایی انسان در ایجاد، حفظ و تحلیل اعتماد در روابط انسانی",

        purpose="social trust building and ethical interaction",

        indicators='["صداقت در تعامل", "وفاداری", "شفافیت رفتاری"]',

        positive_signs='["امانت‌داری", "پایبندی به قول", "شفافیت"]',

        negative_signs='["خیانت", "دروغ", "سوءاستفاده"]',

        sources='["قرآن", "نهج البلاغه", "صحیفه سجادیه"]',

        related_nodes='["IE001"]',

        question_types='["TRUST_TEST", "SOCIAL_BEHAVIOR"]',

        mission_types='["TRUST_BUILDING"]',

        capabilities='["trust_evaluation"]',

        capability_justification="Evaluates social trust behavior",

        temporal_evolution="from personal integrity to social trust",

        future_evolution="trust-based social governance",

        meta_data='{"version": "1.0"}',

        version="1.0",
        status="ACTIVE"
    )

    db.add(node)
    db.commit()
    db.close()

    print("✔ IE002 CREATED")


if __name__ == "__main__":
    seed_ie002()
