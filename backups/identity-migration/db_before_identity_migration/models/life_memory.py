from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from db.database import Base


class LifeMemory(Base):

    __tablename__ = "life_memories"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)

    node_code = Column(String, index=True)

    memory_type = Column(String)

    title = Column(String)

    content = Column(Text)

    confidence = Column(Float, default=0)

    source = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
