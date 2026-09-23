from collections import defaultdict

from sqlalchemy import text

from db.database import SessionLocal
from modules.knowledge.trait_registry import TRAITS


def aggregate_user_profile(user_id: int):
    """Build the canonical runtime profile consumed by Human Model V2.

    Ownership:
        modules/profile

    Sources:
        life_memories
        life_timeline

    Trait normalization:
        Uses the central Knowledge trait registry to preserve the
        Legacy Profile Aggregator contract.
    """
    db = SessionLocal()

    try:
        traits_rows = db.execute(
            text("""
                SELECT title, content, confidence
                FROM life_memories
                WHERE user_id = :user_id
                  AND memory_type = 'TRAIT'
            """),
            {"user_id": user_id},
        ).fetchall()

        timeline_rows = db.execute(
            text("""
                SELECT
                    event_type,
                    title,
                    content,
                    confidence,
                    timestamp
                FROM life_timeline
                WHERE user_id = :user_id
                ORDER BY id ASC
            """),
            {"user_id": user_id},
        ).fetchall()
    finally:
        db.close()

    # Trait Aggregation
    trait_map = defaultdict(
        lambda: {
            "count": 0,
            "confidence_sum": 0.0,
        }
    )

    for row in traits_rows:
        title = row[0]
        confidence = float(row[2] or 0)
        trait_code = None

        # If stored as canonical code.
        if title in TRAITS:
            trait_code = title

        # If stored as Persian title.
        else:
            for code, data in TRAITS.items():
                if data["fa"] == title:
                    trait_code = code
                    break

        # Preserve Legacy behavior for unknown traits.
        if not trait_code:
            continue

        trait_map[trait_code]["count"] += 1
        trait_map[trait_code]["confidence_sum"] += confidence

    traits = []
    strengths = []
    weaknesses = []

    for code, data in trait_map.items():
        avg_confidence = (
            data["confidence_sum"] / data["count"]
        )

        trait = {
            "code": code,
            "fa": TRAITS[code]["fa"],
            "en": TRAITS[code]["en"],
            "count": data["count"],
            "confidence": round(avg_confidence, 2),
        }

        traits.append(trait)

        if avg_confidence >= 0.7:
            strengths.append(
                TRAITS[code]["fa"]
            )
        else:
            weaknesses.append(
                TRAITS[code]["fa"]
            )

    profile = {
        "user_id": user_id,
        "identity": {
            "status": "BUILDING"
        },
        "traits": traits,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "timeline": [
            {
                "event_type": row[0],
                "title": row[1],
                "content": row[2],
                "confidence": row[3],
                "timestamp": row[4],
            }
            for row in timeline_rows
        ],
        "growth_direction": "UNKNOWN",
        "profile_version": "2.0",
    }

    return profile
