from sqlalchemy import Column, Integer, String, Text
from db.database import Base


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, nullable=False)

    code = Column(String, unique=True, index=True)

    name_fa = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    name_ar = Column(String, nullable=False)

    description = Column(Text)

    status = Column(
        String,
        default="PENDING"
    )

    created_at = Column(String)


class ConceptItem(Base):
    __tablename__ = "concept_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    concept_id = Column(Integer, nullable=False)

    item_key = Column(String, nullable=False)

    item_value = Column(Text)

    is_required = Column(Integer, default=0)

    created_at = Column(String)


class ConceptSystem(Base):
    __tablename__ = "concept_system"

    id = Column(Integer, primary_key=True, autoincrement=True)

    concept_id = Column(Integer, nullable=False)

    node_id = Column(String)

    concept_code = Column(String)

    creator = Column(String)

    status = Column(String, default="PENDING")

    completeness = Column(Integer, default=0)

    history = Column(Text)

    version = Column(String, default="1.0")

    snapshot_reference = Column(String)

    created_at = Column(String)
