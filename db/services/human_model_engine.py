from db.services.user_evolution_engine import analyze_user_evolution
from db.services.ie002_rank_adapter import evaluate_ie002_rank
from db.services.human_model_storage import save_human_model

# 👇 اضافه شد
from db.services.learning_loop_engine import run_learning_loop


def build_human_model(user_id: int):

    # -------------------------
    # IE001: Self Model
    # -------------------------
    self_model = analyze_user_evolution(user_id, "IE001")

    # -------------------------
    # IE002: Social Model
    # -------------------------
    sample_interactions = [
        "من همیشه به قولم پایبندم",
        "این موضوع را پنهان کردم",
        "او دروغ گفت"
    ]

    ie002_result = evaluate_ie002_rank(
        user_id=user_id,
        node_code="IE002",
        interactions=sample_interactions
    )

    social_model = {
        "trust_score": ie002_result["trust_score"],
        "rank": ie002_result["rank"]["rank"]
    }

    # -------------------------
    # Fusion Logic
    # -------------------------
    avg_score = self_model["avg_score"]
    trust = social_model["trust_score"]

    if avg_score >= 6 and trust >= 1:
        personality_state = "STABLE_POSITIVE"
    elif avg_score < 4 and trust < 0:
        personality_state = "UNSTABLE"
    else:
        personality_state = "STABLE"

    if self_model["trend"] == "IMPROVING" or trust > 0:
        growth_direction = "UPWARD"
    else:
        growth_direction = "FLAT"

    model = {
        "user_id": user_id,
        "self_model": self_model,
        "social_model": social_model,
        "personality_state": personality_state,
        "growth_direction": growth_direction
    }

    # -------------------------
    # SAVE TO DB
    # -------------------------
    save_human_model(user_id, model)

    # -------------------------
    # 🧠 LEARNING LOOP (NEW)
    # -------------------------
    learning_result = run_learning_loop(user_id, model)

    # (اختیاری: اضافه کردن به خروجی)
    model["learning"] = learning_result

    return model


if __name__ == "__main__":

    result = build_human_model(1)
    print(result)
