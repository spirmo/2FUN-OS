# ================================
# STEP 3 — GROWTH ENGINE (RULE-BASED)
# 2FUN / TANDIL SYSTEM
# ================================

from db.database import SessionLocal
from db.models import User


# ================================
# 1. XP CALCULATION ENGINE
# ================================
def calculate_xp(user):
    """
    محاسبه امتیاز رشد کاربر
    """

    stars = getattr(user, "stars", 0)
    credit = getattr(user, "credit", 0)
    rank_step = getattr(user, "rank_step", 0)
    violations = getattr(user, "violations", 0)

    xp = (
        stars * 2 +
        credit * 1 +
        rank_step * 3
    ) - (violations * 5)

    return max(xp, 0)


# ================================
# 2. RANK SYSTEM RULES
# ================================
def calculate_rank(xp):
    """
    تبدیل XP به Rank
    """

    if xp < 50:
        return "Member"

    elif xp < 150:
        return "Active Member"

    elif xp < 300:
        return "Senior Contributor"

    elif xp < 600:
        return "Trusted Member"

    elif xp < 1000:
        return "Governance Candidate"

    else:
        return "Elite"


# ================================
# 3. PROGRESSION UPDATE ENGINE
# ================================
def update_user_progress(user_id):
    """
    بروزرسانی رشد کاربر در دیتابیس
    """

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        # تبدیل ORM object به dict ساده
        user_data = {
            "stars": user.stars,
            "credit": user.credit,
            "rank_step": user.rank_step,
            "violations": user.violations
        }

        # محاسبه XP و Rank
        xp = calculate_xp(user_data)
        rank = calculate_rank(xp)

        # ذخیره در دیتابیس
        user.rank = rank
        user.stars = xp  # فعلاً XP روی stars نگه داشته شده

        db.commit()

        return {
            "user_id": user_id,
            "xp": xp,
            "rank": rank
        }

    finally:
        db.close()
