import json
from db.database import SessionLocal
from db.models.knowledge_node import KnowledgeNode

db = SessionLocal()

node = KnowledgeNode(
    code="IE001",
    domain="ISLAMIC_EDUCATION",
    name="SELF_KNOWLEDGE",
    title="خودشناسی",

    description="شناخت آگاهانه انسان از خود در مسیر کمال",
    purpose="self awareness and spiritual growth",

    indicators=json.dumps(["شناخت ضعف", "شناخت قوت"]),
    positive_signs=json.dumps(["خودآگاهی", "پذیرش نقد"]),
    negative_signs=json.dumps(["غرور", "خودفریبی"]),

    sources=json.dumps(["قرآن", "نهج البلاغه", "صحیفه سجادیه"]),

    related_nodes=json.dumps(["SELF_CONFIDENCE", "FAITH"]),

    question_types=json.dumps(["REFLECTION", "SELF_ASSESSMENT"]),
    mission_types=json.dumps(["self_analysis"]),

    capabilities=json.dumps({"education": "active"}),

    capability_justification="Islamic foundation of self knowledge",

    temporal_evolution="from myth to digital identity",

    future_evolution="AI-human self awareness",

    meta_data=json.dumps({"version": "1.0"}),

    version="1.0",
    status="ACTIVE"
)

db.add(node)
db.commit()
db.close()

print("IE001 INSERTED SUCCESSFULLY")
