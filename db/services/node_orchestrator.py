from db.services.behavior_engine import analyze_answer
from db.services.reputation_engine import calculate_reputation
from db.services.user_evolution_engine import analyze_user_evolution
from db.services.rank_engine import calculate_rank
from db.services.human_model_engine import build_human_model

from db.database import SessionLocal
from db.migrations.create_reputation_records import ReputationRecord

def run_node_pipeline(
    user_id: int,
    node_code: str,
    question: str,
    answer: str
):

    # -------------------------
    # Behavior
    # -------------------------

    behavior = analyze_answer(
        question,
        answer
    )

    # -------------------------
    # Reputation
    # -------------------------

    reputation = calculate_reputation(
        behavior
    )

    # -------------------------
    # Save Reputation
    # -------------------------

    db = SessionLocal()

    record = ReputationRecord(
        user_id=user_id,
        node_code=node_code,
        score=reputation["score"],
        level=reputation["level"],
        signals=behavior
    )

    db.add(record)
    db.commit()
    db.close()

    # -------------------------
    # Evolution
    # -------------------------

    evolution = analyze_user_evolution(
        user_id=user_id,
        node_code=node_code
    )

    # -------------------------
    # Rank
    # -------------------------

    rank = calculate_rank(
        evolution
    )

    # -------------------------
    # Human Model
    # -------------------------

    human_model = build_human_model(
        user_id=user_id,
        interactions=[answer]
    )

    return {
        "node_code": node_code,
        "behavior": behavior,
        "reputation": reputation,
        "evolution": evolution,
        "rank": rank,
        "human_model": human_model
    }
