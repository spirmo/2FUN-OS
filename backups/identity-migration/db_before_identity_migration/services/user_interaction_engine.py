from db.services.human_model_engine import build_human_model


def run_user_session(user_id: int, answers: list):

    """
    answers = پاسخ‌های واقعی کاربر
    """

    print("🧠 SESSION STARTED")

    # -----------------------------
    # تبدیل پاسخ واقعی به رفتار
    # -----------------------------
    interactions = []

    for a in answers:
        interactions.append(a)

    # -----------------------------
    # اتصال به Human Model
    # (فعلاً از داخل engine نمونه می‌گیرد)
    # -----------------------------
    model = build_human_model(user_id)

    print("\n📊 FINAL MODEL:")
    print(model)

    return model


if __name__ == "__main__":

    # -----------------------------
    # TEST: ورودی واقعی کاربر
    # -----------------------------
    user_answers = [
        "من به قولم پایبندم",
        "گاهی اطلاعات را پنهان می‌کنم",
        "سعی می‌کنم صادق باشم"
    ]

    run_user_session(user_id=1, answers=user_answers)
