from datetime import datetime

from db.database import SessionLocal
from db.models import User


RANK_ORDER = [
    "simple",
    "D",
    "D*",
    "D**",
    "D***",
    "D****",
    "D*****",
    "C",
    "C*",
    "C**",
    "C***",
    "C****",
    "C*****",
    "B",
    "B*",
    "B**",
    "B***",
    "B****",
    "B*****",
    "A",
    "A*",
    "A**",
    "A***",
    "A****",
    "A*****",
]


def join_colony(user_id, colony_id):
    """
    Join a user to a colony using the migrated Legacy Game behavior.

    Functional parity with:
    db/migrations/promotion_engine.py::join_colony
    """
    with SessionLocal() as session:
        user = session.get(User, user_id)

        if not user:
            return

        if user.temp_ban_until and datetime.now() < user.temp_ban_until:
            print(
                f"User {user_id} banned until {user.temp_ban_until}"
            )
            return

        initial_score = (
            user.stars
            + user.credit // 10
            - user.violations * 3
        )

        rank_index = min(
            initial_score // 5,
            len(RANK_ORDER) - 1,
        )

        user.colony_id = colony_id
        user.rank = RANK_ORDER[rank_index]
        user.stars = min(rank_index, 5)

        session.commit()

        print(
            f"User {user_id} joined colony "
            f"{colony_id} with rank {user.rank}"
        )
