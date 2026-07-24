from sqlalchemy import Column, Integer, String, Text
from db.database import Base


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    id = Column(Integer, primary_key=True)

    code = Column(String, unique=True, index=True)
    domain = Column(String)
    name = Column(String)
    title = Column(String)

    description = Column(Text)
    purpose = Column(Text)

    indicators = Column(Text)
    positive_signs = Column(Text)
    negative_signs = Column(Text)

    sources = Column(Text)
    related_nodes = Column(Text)

    question_types = Column(Text)
    mission_types = Column(Text)

    capabilities = Column(Text)
    capability_justification = Column(Text)

    temporal_evolution = Column(Text)
    future_evolution = Column(Text)

    meta_data = Column(Text)

    version = Column(String)
    status = Column(String)
