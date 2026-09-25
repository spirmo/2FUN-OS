from db.database import SessionLocal
from datetime import datetime

def log_reputation(user_id: int, node_code: str, score: int, level: str):

    db = SessionLocal()

    record = {
        "user_id": user_id,
        "node_code": node_code,
        "score": score,
        "level": level,
        "created_at": datetime.utcnow()
    }

    # فعلاً ساده (مرحله بعد جدول DB می‌سازیم)
    print("LOGGED:", record)

    db.close()
    return record


if __name__ == "__main__":
    log_reputation(
        user_id=1,
        node_code="IE001",
        score=5,
        level="NORMAL"
    )
