from sqlalchemy import Column, Integer, String, Text, DateTime
from db.database import Base
from datetime import datetime


class ConceptApprovalQueue(Base):

    __tablename__ = "concept_approval_queue"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Global Concept Identity
    concept_code = Column(
        String,
        unique=True,
        index=True
    )

    # Owner
    creator_user_code = Column(
        String,
        index=True
    )

    # Source information
    source_mobile_id = Column(
        String,
        nullable=True
    )

    title = Column(
        String
    )

    domain = Column(
        String
    )

    # Concept package snapshot
    payload = Column(
        Text
    )

    status = Column(
        String,
        default="SUBMITTED"
    )

    # Approval information
    approved_by = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    reviewed_at = Column(
        DateTime,
        nullable=True
    )
