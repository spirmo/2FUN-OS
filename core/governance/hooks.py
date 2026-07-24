from db.database import SessionLocal
from db.models.governance import UserGovernance
from db.models.user import User


# =========================
# CORE SESSION HELPER
# =========================

def get_session():
    return SessionLocal()


# =========================
# INTERNAL GET OR CREATE
# =========================

def _get_or_create_gov(session, user_code: str):
    gov = session.query(UserGovernance).filter_by(
        user_code=user_code
    ).first()

    if not gov:
        gov = UserGovernance(
            user_code=user_code,
            governance_score=0,
            trust_index=0,
            risk_index=0,
            stability_index=0,
            strike_count=0,
            governance_status="NOT_ELIGIBLE"
        )
        session.add(gov)
        session.flush()

    return gov


# =========================
# CORE HOOKS (USED BY ROUTER)
# =========================

def on_xp_change(user_id: int, xp_delta: int):
    session = get_session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user or not user.user_code:
            return

        gov = _get_or_create_gov(session, user.user_code)

        gov.governance_score += xp_delta * 0.1
        gov.trust_index += xp_delta * 0.05

        session.commit()

    except Exception as e:
        session.rollback()
        print("[XP HOOK ERROR]", e)

    finally:
        session.close()


def on_violation(user_id: int, severity: int = 1):
    session = get_session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user or not user.user_code:
            return

        gov = _get_or_create_gov(session, user.user_code)

        gov.strike_count += severity
        gov.risk_index += severity * 10

        if gov.strike_count >= 3:
            gov.governance_status = "SUSPENDED"

        session.commit()

    finally:
        session.close()


def on_activity(user_id: int):
    session = get_session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user or not user.user_code:
            return

        gov = _get_or_create_gov(session, user.user_code)

        gov.stability_index += 1
        gov.trust_index += 0.2

        gov.stability_index = min(gov.stability_index, 100)
        gov.trust_index = min(gov.trust_index, 100)

        session.commit()

    finally:
        session.close()


# =========================
# ELIGIBILITY CHECK
# =========================

def is_eligible(user_code: str) -> bool:
    session = get_session()
    try:
        gov = session.query(UserGovernance).filter_by(
            user_code=user_code
        ).first()

        if not gov:
            return False

        return (
            gov.governance_score >= 10 and
            gov.strike_count < 3 and
            gov.risk_index < 70
        )

    finally:
        session.close()



