from .decision_engine import DecisionEngine


def complete_mandatory():
    return {
        "persian_title": "خودشناسی",
        "domain": "SELF_DEVELOPMENT",
        "category": "GENERAL",
        "canonical_meaning": "شناخت انسان از ویژگی‌ها و توانایی‌های خود",
        "definition": "شناخت انسان از ویژگی‌ها و توانایی‌های خود",
        "short_description": "شناخت خود",
        "source": "internal",
        "source_url": "https://example.com",
        "source_author": "2FUN",
        "source_year": "2026",
        "evidence": "knowledge_node_001",
    }


def complete_all():
    concept = complete_mandatory()

    optional_items = (
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

    for key in optional_items:
        concept[key] = f"TEST_{key}"

    return concept


def test_concept_approval_failure():
    engine = DecisionEngine()

    concept = {
        "persian_title": "مفهوم ناقص",
        "definition": "",
        "source": "",
        "evidence": "",
    }

    result = engine.evaluate_concept(
        concept_id=1,
        concept=concept,
    )

    assert result["approved"] is False
    assert result["status"] == "REJECTED"
    assert result["validation"]["valid"] is False


def test_concept_approval_success_mandatory():
    engine = DecisionEngine()

    concept = complete_mandatory()

    result = engine.evaluate_concept(
        concept_id=2,
        concept=concept,
    )

    assert result["approved"] is True
    assert result["status"] == "APPROVED"
    assert result["validation"]["valid"] is True
    assert result["validation"]["completeness"] == 30
    assert result["validation"]["state"] == "INCOMPLETE"


def test_concept_approval_success_complete():
    engine = DecisionEngine()

    concept = complete_all()

    result = engine.evaluate_concept(
        concept_id=3,
        concept=concept,
    )

    assert result["approved"] is True
    assert result["status"] == "APPROVED"
    assert result["validation"]["valid"] is True
    assert result["validation"]["completeness"] == 100
    assert result["validation"]["state"] == "PUBLISHED"


if __name__ == "__main__":
    test_concept_approval_failure()
    test_concept_approval_success_mandatory()
    test_concept_approval_success_complete()

    print("Governance Engine tests passed")
