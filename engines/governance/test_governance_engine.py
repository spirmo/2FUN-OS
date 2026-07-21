from .decision_engine import DecisionEngine


def test_concept_approval_success():
    engine = DecisionEngine()

    concept = {
        "title_fa": "خودشناسی",
        "definition": "شناخت انسان از ویژگی‌ها و توانایی‌های خود",
        "source": "internal",
        "evidence": "knowledge_node_001",
    }

    result = engine.evaluate_concept(
        concept_id=1,
        concept=concept,
    )

    assert result["approved"] is True
    assert result["status"] == "APPROVED"


def test_concept_approval_failure():
    engine = DecisionEngine()

    concept = {
        "title_fa": "مفهوم ناقص",
        "definition": "",
        "source": "",
        "evidence": "",
    }

    result = engine.evaluate_concept(
        concept_id=2,
        concept=concept,
    )

    assert result["approved"] is False
    assert result["status"] == "REJECTED"


if __name__ == "__main__":
    test_concept_approval_success()
    test_concept_approval_failure()

    print(
        "Governance Engine tests passed"
    )
