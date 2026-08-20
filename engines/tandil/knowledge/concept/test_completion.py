from engines.tandil.knowledge.concept.models import Concept, ConceptItem
from engines.tandil.knowledge.concept.completeness import refresh_completeness


def test_item_completion():
    concept = Concept()

    item = ConceptItem(
        item_key="definition",
        value="A test definition",
        status="APPROVED",
        completed_by="USER_1",
    )

    concept.set_item(item)

    completeness = refresh_completeness(concept)

    assert concept.get_item("definition") is not None
    assert concept.get_item("definition").completed_by == "USER_1"
    assert concept.get_item("definition").value == "A test definition"
    assert completeness == 2

    print("Concept item completion: OK")


if __name__ == "__main__":
    test_item_completion()
    print("CONCEPT COMPLETION TEST: OK")
