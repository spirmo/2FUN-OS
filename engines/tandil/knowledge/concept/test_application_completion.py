from engines.tandil.knowledge.concept.models import Concept, ConceptItem
from engines.tandil.knowledge.concept.application import ConceptApplication


class FakeEventBus:
    def __init__(self):
        self.events = []

    def emit(self, source, action, entity_type, payload):
        self.events.append({
            "source": source,
            "action": action,
            "entity_type": entity_type,
            "payload": payload,
        })
        return {"success": True}


def test_complete_item():
    concept = Concept()

    concept.set_item(
        ConceptItem(
            item_key="definition",
            base_score=30,
        )
    )

    app = ConceptApplication()

    # جایگزینی موقت EventBus واقعی با Fake
    import engines.tandil.knowledge.concept.application as application_module

    original_get_event_bus = application_module.get_event_bus
    application_module.get_event_bus = lambda: FakeEventBus()

    try:
        result = app.complete_item(
            concept,
            item_key="definition",
            value="A test definition",
            user_id="USER_1",
            difficulty="MEDIUM",
        )

        assert result["success"] is True
        assert result["item_key"] == "definition"
        assert result["completed_by"] == "USER_1"
        assert result["completeness"] == 2

        item = concept.get_item("definition")

        assert item.value == "A test definition"
        assert item.completed_by == "USER_1"
        assert item.completed_at is not None
        assert item.status == "APPROVED"

        assert app.history.count == 1
        assert app.history.events[0]["event_type"] == "ITEM_COMPLETED"

        print("ConceptApplication.complete_item: OK")

    finally:
        application_module.get_event_bus = original_get_event_bus


if __name__ == "__main__":
    test_complete_item()
    print("APPLICATION COMPLETION TEST: OK")
