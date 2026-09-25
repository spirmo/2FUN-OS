from db.database import SessionLocal
from db.migrations.create_ie002_records import IE002Record
from datetime import datetime, timezone


def save_ie002(user_id: int, signals: dict, trust_score: int, rank_result: dict):

    db = SessionLocal()

    record = IE002Record(
        user_id=user_id,
        trust_score=trust_score,
        signals=signals,
        rank=rank_result["rank"],
        next_rank=rank_result.get("next_rank"),
        created_at=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.close()

    print("✔ IE002 SAVED TO DB")


if __name__ == "__main__":

    sample_signals = {
        "trustworthiness": 1,
        "honesty": -1,
        "consistency": 1,
        "manipulation_risk": 1
    }

    save_ie002(
        user_id=1,
        signals=sample_signals,
        trust_score=1,
        rank_result={"rank": "MEMBER", "next_rank": "CONTRIBUTOR"}
    )
