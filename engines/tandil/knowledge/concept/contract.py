"""
2FUN / TANDIL
Concept Engine Contract

Architecture:
11 Mandatory Items
25 Optional Items
11 System Items

Status:
LOCKED

Version:
1.0
"""

CONCEPT_ENGINE_VERSION = "1.0"


# ==========================================================
# MANDATORY ITEMS
# ==========================================================

MANDATORY_ITEMS = (
    "persian_title",
    "domain",
    "category",
    "canonical_meaning",
    "definition",
    "short_description",
    "source",
    "source_url",
    "source_author",
    "source_year",
    "evidence",
)


# ==========================================================
# OPTIONAL ITEMS
# ==========================================================

OPTIONAL_ITEMS = (
    "english_title",
    "arabic_title",
    "other_language_titles",
    "translations",
    "translation_language",
    "translated_text",
    "related_concepts",
    "attributes",
    "attribute_values",
    "related_questions",
    "answers",
    "missions",
    "mission_title",
    "mission_description",
    "tags",
    "difficulty",
    "notes",
    "images",
    "videos",
    "attachments",
    "examples",
    "counter_examples",
    "additional_sources",
    "validation_notes",
    "future_development_suggestions",
)


# ==========================================================
# SYSTEM ITEMS
# ==========================================================

SYSTEM_ITEMS = (
    "node_id",
    "concept_code",
    "database_id",
    "topic_id",
    "creator",
    "created_at",
    "status",
    "completeness",
    "history",
    "version",
    "snapshot_reference",
)


# ==========================================================
# ITEM STATUS
# ==========================================================

ITEM_STATUSES = (
    "NOT_STARTED",
    "PENDING",
    "APPROVED",
    "REJECTED",
)


# ==========================================================
# CONCEPT STATES
# ==========================================================

CONCEPT_STATES = (
    "OPEN_FOR_COMPLETION",
    "PENDING_REVIEW",
    "APPROVED",
    "REJECTED",
    "PUBLISHED",
    "ARCHIVED",
)


# ==========================================================
# ARCHITECTURAL COUNTS
# ==========================================================

MANDATORY_COUNT = len(MANDATORY_ITEMS)
OPTIONAL_COUNT = len(OPTIONAL_ITEMS)
SYSTEM_COUNT = len(SYSTEM_ITEMS)

VISIBLE_ITEM_COUNT = MANDATORY_COUNT + OPTIONAL_COUNT


# ==========================================================
# ARCHITECTURAL ASSERTIONS
# ==========================================================

assert MANDATORY_COUNT == 11
assert OPTIONAL_COUNT == 25
assert SYSTEM_COUNT == 11
assert VISIBLE_ITEM_COUNT == 36


# ==========================================================
# CONCEPT ARCHITECTURE RULES
# ==========================================================

CONCEPT_RULES = {
    "independent_entity": True,
    "single_truth_identity": True,
    "permanent_identifier": True,
    "reusable_across_platform": True,
    "domain_does_not_own_concept": True,
    "node_does_not_own_concept": True,
    "knowledge_unit_source": True,
    "no_direct_question_generation": True,
    "no_personality_analysis": True,
    "no_behavioral_memory": True,
}


# ==========================================================
# IDENTITY RULE
# ==========================================================

CONCEPT_CODE_RULE = {
    "generated_by": "SYSTEM",
    "generated_after": "APPROVED",
    "permanent": True,
    "user_assignable": False,
}


# ==========================================================
# UI PRESENTATION CONTRACT
# ==========================================================

STATUS_PRESENTATION = {
    "NOT_STARTED": {
        "color": "WHITE",
        "icon": "DEFAULT",
    },
    "PENDING": {
        "color": "YELLOW",
        "icon": "PENDING",
    },
    "APPROVED": {
        "color": "GREEN",
        "icon": "CHECK",
    },
    "REJECTED": {
        "color": "RED",
        "icon": "REJECT",
    },
}
