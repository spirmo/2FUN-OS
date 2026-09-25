from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from db.database import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)

    node_code = Column(String, index=True)

    question = Column(Text)

    answer = Column(Text)

    score = Column(Float, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
