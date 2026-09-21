from collections import defaultdict

from sqlalchemy import text

from db.database import SessionLocal


def aggregate_user_profile(user_id: int):
    """
    Build the canonical runtime profile consumed by Human Model V2.

    Ownership:
        modules/profile

    Sources:
        life_memories
        life_timeline

    The aggregator does not perform trait normalization.
    Trait normalization remains an upstream responsibility.
    """

    db = SessionLocal()

    try:
        trait_rows = db.execute(
            text("""
                SELECT
                    title,
                    confidence
                FROM life_memories
                WHERE user_id = :user_id
                  AND memory_type = 'TRAIT'
                ORDER BY id
            """),
            {"user_id": user_id},
        ).fetchall()

        timeline_rows = db.execute(
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
                ORDER BY id
            """),
            {"user_id": user_id},
        ).fetchall()

    finally:
        db.close()

    trait_data = defaultdict(lambda: {
        "count": 0,
        "confidence_sum": 0.0,
    })

    for row in trait_rows:
        code = row[0]

        if not code:
            continue

        confidence = float(row[1] or 0)

        trait_data[code]["count"] += 1
        trait_data[code]["confidence_sum"] += confidence

    traits = []

    for code, data in trait_data.items():
        count = data["count"]
        confidence = (
            data["confidence_sum"] / count
            if count
            else 0.0
        )

        traits.append({
            "code": code,
            "count": count,
            "confidence": confidence,
        })

    traits.sort(key=lambda item: item["code"])

    strengths = [
        trait["code"]
        for trait in traits
        if trait["confidence"] >= 0.7
    ]

    weaknesses = [
        trait["code"]
        for trait in traits
        if trait["confidence"] < 0.7
    ]

    timeline = [
        {
            "event_type": row[0],
            "title": row[1],
            "content": row[2],
            "node_code": row[3],
            "confidence": row[4],
            "timestamp": row[5],
        }
        for row in timeline_rows
    ]

    return {
        "user_id": user_id,
        "identity": {
            "status": "BUILDING",
        },
        "traits": traits,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "timeline": timeline,
        "growth_direction": "UNKNOWN",
        "profile_version": "2.0",
    }
