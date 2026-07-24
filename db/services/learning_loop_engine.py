from db.database import SessionLocal
from db.migrations.create_human_models import HumanModelRecord
from datetime import datetime, timezone
from db.services.drift_memory_engine import store_drift

def run_learning_loop(user_id: int, new_model: dict):
    """
    این موتور مسئول یادگیری از تغییرات مدل کاربر است
    """

    db = SessionLocal()

    # ----------------------------
    # گرفتن آخرین مدل کاربر
    # ----------------------------
    last_model = (
        db.query(HumanModelRecord)
        .filter(HumanModelRecord.user_id == user_id)
        .order_by(HumanModelRecord.id.desc())
        .first()
    )

    if not last_model:
        db.close()
        return {
            "status": "NO_PREVIOUS_MODEL",
            "action": "INITIALIZE"
        }

    old_self = last_model.self_model or {}
    new_self = new_model.get("self_model", {})

    # ----------------------------
    # مقایسه تغییرات (Drift Detection)
    # ----------------------------
    drift = 0

    old_score = old_self.get("avg_score", 0)
    new_score = new_self.get("avg_score", 0)

    drift += abs(new_score - old_score)

    old_trend = old_self.get("trend")
    new_trend = new_self.get("trend")

    if old_trend != new_trend:
        drift += 1

    # ----------------------------
    # تصمیم‌گیری یادگیری
    # ----------------------------
    if drift >= 2:
        learning_state = "HIGH_ADAPTATION"
    elif drift > 0:
        learning_state = "MODERATE_ADAPTATION"
    else:
        learning_state = "STABLE"

    # ----------------------------
    # ذخیره state جدید (optional)
    # ----------------------------
    last_model.growth_direction = learning_state
    last_model.created_at = datetime.now(timezone.utc)

    db.add(last_model)
    db.commit()
    db.close()

    # ذخیره drift برای تاریخچه تکاملی
    store_drift(user_id, {
        "drift_score": drift,
        "learning_state": learning_state,
        "previous_avg": old_score,
        "current_avg": new_score
    })
    return {
        "user_id": user_id,
        "drift_score": drift,
        "learning_state": learning_state,
        "previous_avg": old_score,
        "current_avg": new_score
    }
