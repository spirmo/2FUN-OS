from db.database import SessionLocal
from db.models.knowledge_node import KnowledgeNode

from engines.tandil.memory.life_timeline_engine import add_life_event
from engines.tandil.memory.life_memory_engine import store_memory
from engines.tandil.memory.domain_trait_loader import (
    DOMAIN_TRAIT_FILES,
    normalize_trait,
)


def get_node_domain(node_code):
    db = SessionLocal()

    try:
        node = (
            db.query(KnowledgeNode)
            .filter(KnowledgeNode.code == node_code)
            .first()
        )
    finally:
        db.close()

    if not node:
        return None

    return node.domain


def extract_memories(node_code, answer):
    memories = []
    found_traits = set()

    domain = get_node_domain(node_code)

    if not domain:
        return memories

    trait_map = DOMAIN_TRAIT_FILES.get(domain, {})

    answer = answer.strip()

    for keyword, trait_code in trait_map.items():
        if keyword in answer:
            canonical_trait = normalize_trait(trait_code)

            if canonical_trait in found_traits:
                continue

            found_traits.add(canonical_trait)

            memories.append({
                "memory_type": "TRAIT",
                "title": canonical_trait,
                "content": answer,
                "confidence": 0.8,
            })

    return memories


def process_answer(user_id, node_code, answer):
    memories = extract_memories(node_code, answer)

    results = []

    for memory_data in memories:
        memory = store_memory(
            user_id=user_id,
            node_code=node_code,
            memory_type=memory_data["memory_type"],
            title=memory_data["title"],
            content=memory_data["content"],
            confidence=memory_data["confidence"],
        )

        add_life_event(
            user_id=user_id,
            event_type=memory_data["memory_type"],
            title=memory_data["title"],
            content=memory_data["content"],
            node_code=node_code,
            confidence=memory_data["confidence"],
        )

        results.append(memory)

    return results
