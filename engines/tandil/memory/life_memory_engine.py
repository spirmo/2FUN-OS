from db.database import SessionLocal
from db.models.life_memory import LifeMemory


def store_memory(
    user_id,
    node_code,
    memory_type,
    title,
    content,
    confidence=0.5,
    source="answer",
):
    """
    Store a life memory in the canonical runtime database.

    Ownership:
        engines/tandil/memory

    This function persists memory only.
    Memory extraction and timeline management are separate responsibilities.
    """

    db = SessionLocal()

    try:
        row = LifeMemory(
            user_id=user_id,
            node_code=node_code,
            memory_type=memory_type,
            title=title,
            content=content,
            confidence=confidence,
            source=source,
        )

        db.add(row)
        db.commit()

        return {
            "status": "MEMORY_STORED",
        }

    finally:
        db.close()
