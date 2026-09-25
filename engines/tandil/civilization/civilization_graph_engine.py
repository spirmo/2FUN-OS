from sqlalchemy import text

from db.database import SessionLocal


def build_civilization_graph():
    """
    Build the civilization graph from canonical life-memory traits.

    Migrated from Legacy:
    core/civilization/civilization_graph_engine.py

    Runtime source:
    life_memories where memory_type='TRAIT'
    """

    db = SessionLocal()

    try:
        rows = db.execute(
            text(
                """
                SELECT
                    user_id,
                    title
                FROM life_memories
                WHERE memory_type = 'TRAIT'
                """
            )
        ).fetchall()
    finally:
        db.close()

    users = {}

    for user_id, trait in rows:
        users.setdefault(user_id, set()).add(trait)

    edges = []

    user_ids = list(users.keys())

    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
            u1 = user_ids[i]
            u2 = user_ids[j]

            shared = users[u1] & users[u2]

            if shared:
                edges.append(
                    {
                        "source": u1,
                        "target": u2,
                        "shared_traits": list(shared),
                        "weight": len(shared),
                    }
                )

    return {
        "nodes": [
            {
                "user_id": uid,
                "traits": list(traits),
            }
            for uid, traits in users.items()
        ],
        "edges": edges,
        "graph_version": "1.0",
    }
