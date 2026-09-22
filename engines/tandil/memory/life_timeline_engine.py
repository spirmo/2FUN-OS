from datetime import datetime, timezone

from sqlalchemy import text

from db.database import SessionLocal


def add_life_event(
    user_id: int,
    event_type: str,
    title: str,
    content: str,
    node_code: str = None,
    confidence: float = 1.0,
):
    """
    Store an event in the user's life timeline.

    Ownership:
        engines/tandil/memory

    Timeline persistence is independent from memory extraction.
    """

    db = SessionLocal()

    try:
        db.execute(
            text("""
                INSERT INTO life_timeline (
                    user_id,
                    event_type,
                    title,
                    content,
                    node_code,
                    confidence,
                    timestamp
                )
                VALUES (
                    :user_id,
                    :event_type,
                    :title,
                    :content,
                    :node_code,
                    :confidence,
                    :timestamp
                )
            """),
            {
                "user_id": user_id,
                "event_type": event_type,
                "title": title,
                "content": content,
                "node_code": node_code,
                "confidence": confidence,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        db.commit()

        return {
            "status": "EVENT_STORED",
            "user_id": user_id,
            "event_type": event_type,
        }

    except Exception as e:
        db.rollback()

        return {
            "status": "ERROR",
            "error": str(e),
        }

    finally:
        db.close()


def get_life_timeline(user_id: int):
    """
    Return the complete life timeline for a user.
    """

    db = SessionLocal()

    try:
        rows = db.execute(
            text("""
                SELECT
                    event_type,
                    title,
                    content,
                    node_code,
                    confidence,
                    timestamp
                FROM life_timeline
                WHERE user_id = :user_id
                ORDER BY id ASC
            """),
            {"user_id": user_id},
        ).fetchall()

        return [
            {
                "event_type": row[0],
                "title": row[1],
                "content": row[2],
                "node_code": row[3],
                "confidence": row[4],
                "timestamp": row[5],
            }
            for row in rows
        ]

    finally:
        db.close()
