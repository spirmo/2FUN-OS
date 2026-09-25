from TANDIL_GOVERNANCE.core_engine.event_bus.event_bus import event_bus
from db.models.xp_log import XPLog
from datetime import datetime
from db.database import SessionLocal
from db.models.user import User

import time
from collections import defaultdict

# =========================
# CONFIG XP SYSTEM
# =========================

BASE_XP_MAP = {
    "login": 1,
    "message": 2,
    "daily": 5,
    "action": 3,
}

ROLE_MULTIPLIER = {
    "user": 1.0,
    "active": 1.2,
    "contributor": 1.5,
    "leader": 2.0,
}

# =========================
# XP EVENTS v2
# =========================

XP_COOLDOWN = defaultdict(float)

USER_XP_TODAY = defaultdict(int)

USER_STREAK = defaultdict(int)

LAST_LOGIN = {}

DAILY_XP_LIMIT = 200


def check_cooldown(user_code: str, action: str):
    key = f"{user_code}:{action}"

    now = time.time()

    if now - XP_COOLDOWN[key] < 30:
        return False

    XP_COOLDOWN[key] = now

    return True


def check_daily_limit(user_code: str, xp: int):
    if USER_XP_TODAY[user_code] + xp > DAILY_XP_LIMIT:
        return False

    USER_XP_TODAY[user_code] += xp

    return True


def update_streak(user_code: str):
    now = time.time()

    if user_code in LAST_LOGIN:
        diff = now - LAST_LOGIN[user_code]

        if diff < 86400:
            USER_STREAK[user_code] += 1
        else:
            USER_STREAK[user_code] = 1
    else:
        USER_STREAK[user_code] = 1

    LAST_LOGIN[user_code] = now

    return USER_STREAK[user_code]


def streak_multiplier(streak: int):
    if streak >= 7:
        return 2.0

    if streak >= 3:
        return 1.5

    if streak >= 1:
        return 1.1

    return 1.0


# =========================
# CORE XP CALCULATOR
# =========================

def calculate_xp(base_xp: int, role: str, rank_step: int) -> int:
    multiplier = ROLE_MULTIPLIER.get(role or "user", 1.0)

    difficulty = 1 / (1 + rank_step * 0.15)

    xp = base_xp * multiplier * difficulty

    return max(1, int(xp))


# =========================
# LOG XP
# =========================

def log_xp(session, user, action, xp_gained, multiplier):
    log = XPLog(
        user_code=user.user_code,
        action=action,
        xp_gained=xp_gained,
        multiplier=multiplier,
        rank_step=user.rank_step,
        created_at=datetime.utcnow()
    )

    session.add(log)


# =========================
# RANK SYSTEM
# =========================

RANK_TABLE = [
    (0, "ROOKIE"),
    (100, "MEMBER"),
    (300, "ACTIVE"),
    (700, "ELITE"),
    (1500, "LEGEND"),
]


def check_rank_up(user):
    for threshold, rank in reversed(RANK_TABLE):
        if user.stars >= threshold:
            if user.rank != rank:
                user.rank = rank
                user.rank_step += 1

            break


# =========================
# ADD XP TO USER
# =========================

def add_xp(user_code: str, action: str):
    session = SessionLocal()

    user = session.query(User).filter(
        User.user_code == user_code
    ).first()

    if not user:
        session.close()
        return {"error": "USER_NOT_FOUND"}

    if not check_cooldown(user_code, action):
        session.close()
        return {"error": "COOLDOWN_ACTIVE"}

    base_xp = BASE_XP_MAP.get(action, 1)

    streak = update_streak(user_code)

    streak_bonus = streak_multiplier(streak)

    multiplier = ROLE_MULTIPLIER.get(
        user.role or "user",
        1.0
    )

    difficulty = 1 / (1 + user.rank_step * 0.15)

    gained_xp = int(
        base_xp
        * multiplier
        * difficulty
        * streak_bonus
    )

    if not check_daily_limit(user_code, gained_xp):
        session.close()
        return {"error": "DAILY_LIMIT_REACHED"}

    user.stars += gained_xp

    check_rank_up(user)

    log_xp(
        session,
        user,
        action,
        gained_xp,
        multiplier
    )

    session.commit()

     event_bus.emit("XP_GAINED", {
         "user_id": user.id,
         "xp": xp
    })



    result = {
        "user": user_code,
        "action": action,
        "xp_gained": gained_xp,
        "streak": streak,
        "total_stars": user.stars,
    }

    session.close()

    return result
