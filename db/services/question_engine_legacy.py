import json
from db.database import SessionLocal
from db.models.knowledge_node import KnowledgeNode


def generate_questions(node_code: str):
    db = SessionLocal()

    node = db.query(KnowledgeNode).filter(
        KnowledgeNode.code == node_code
    ).first()

    if not node:
        return []

    questions = []

    # IE001 logic (simple starter engine)
    if node.code == "IE001":
        questions = [
            "اگر بخواهی خودت را توصیف کنی، از کجا شروع می‌کنی؟",
            "کدام ضعف در خودت را سخت‌تر می‌پذیری؟",
            "آخرین باری که درباره خودت اشتباه فکر کردی کی بود؟",
            "چه چیزی در خودت هست که هنوز کامل نمی‌شناسی؟",
            "اگر بخواهی خودت را بهتر کنی، اولین قدم چیست؟"
        ]

    db.close()
    return questions


if __name__ == "__main__":
    qs = generate_questions("IE001")
    for q in qs:
        print("-", q)
