from db.database import SessionLocal
from db.migrations.create_reputation_records import ReputationRecord
from datetime import datetime, timezone


def save_reputation(user_id: int, node_code: str, signals: dict, result: dict):

    db = SessionLocal()

    record = ReputationRecord(
        user_id=user_id,
        node_code=node_code,
        score=result["score"],
        level=result["level"],
        signals=signals,
        created_at=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.close()

    print("✔ Reputation SAVED to DB")


if __name__ == "__main__":

    sample_signals = {
        "self_awareness": 0,
        "honesty": 1,
        "reflection_depth": 1,
        "defensiveness": 0
    }

    sample_result = {
        "score": 5,
        "level": "NORMAL"
    }

    save_reputation(
        user_id=1,
        node_code="IE001",
        signals=sample_signals,
        result=sample_result
    )
