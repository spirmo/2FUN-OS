from decimal import Decimal

from engines.tandil.knowledge.concept.models import Concept, ConceptItem
from engines.tandil.knowledge.concept.application import ConceptApplication


def test_real_event_bus_integration():
    concept = Concept(
        concept_code="TEST-CONCEPT-001",
    )

    concept.system.database_id = 999
    concept.system.creator = "USER_1"

    concept.set_item(
        ConceptItem(
            item_key="definition",
            base_score=30,
        )
    )

    app = ConceptApplication()

    result = app.complete_item(
        concept,
        item_key="definition",
        value="Integration test definition",
        user_id="USER_1",
        difficulty="MEDIUM",
        base_value=Decimal("10"),
    )

    assert result["success"] is True
    assert result["event"] is not None

    print("Concept → EventBus: OK")
    print("Event result:", result["event"])


if __name__ == "__main__":
    test_real_event_bus_integration()
    print("REAL EVENT INTEGRATION TEST: OK")
