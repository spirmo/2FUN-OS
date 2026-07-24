from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models.user import User
from app.levels import get_level_by_score


# ===============================
# کاربران و امتیاز
# ===============================
def get_user_points(user_id: int) -> int:
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if user:
            return user.stars
        return 0


def add_user_points(user_id: int, points: int):
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            user = User(telegram_id=user_id, stars=points)
            session.add(user)
        else:
            user.stars += points
        session.commit()


def get_user_level(score: int):
    return get_level_by_score(score)
