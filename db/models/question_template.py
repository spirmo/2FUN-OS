from sqlalchemy import Column, Integer, String, Text

from db.database import Base


class QuestionTemplate(Base):
    __tablename__ = "question_templates"

    id = Column(Integer, primary_key=True)

    node_code = Column(String, index=True)

    question_type = Column(String)

    template = Column(Text)

    difficulty = Column(Integer, default=1)

    version = Column(String, default="1.0")

    status = Column(String, default="ACTIVE")


