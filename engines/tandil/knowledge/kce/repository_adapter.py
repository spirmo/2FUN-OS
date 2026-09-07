from .rules import calculate_completeness
from db.repositories.concept_version_repository import ConceptVersionRepository
from .models import KnowledgeNode


class KnowledgeRepositoryAdapter:
    """
    Adapter between KCE and the current Concept Repository.

    KCE consumes KnowledgeNode models.
    Concept persistence remains owned by ConceptVersionRepository.
    """

    def __init__(self):
        self.repository = ConceptVersionRepository()

    def all_nodes(self):
        return {
            "concepts": self.load_all_concepts(),
            "evidences": [],
        }

    def load_all_concepts(self):
        nodes = []

        concepts = self.repository.get_all_concepts()

        for concept in concepts:
            concept_code = concept.get("concept_code")

            if not concept_code:
                continue

            version = concept.get("current_version") or "1.0"

            data = self.repository.load_concept(
                concept_code=concept_code,
                version=version,
            )

            if data is None:
                continue

            nodes.append(self._to_node(data))

        return nodes

    def load_first_concept(self):
        nodes = self.load_all_concepts()

        if not nodes:
            return None

        return nodes[0]

    def load_first_node_model(self):
        return self.load_first_concept()

    def load_all_node_models(self):
        return self.load_all_concepts()

    @staticmethod
    def _to_node(concept):
        metadata = {
            "ConceptCode": concept.concept_code,
            "Creator": concept.system.creator,
            "Version": concept.system.version,
            "Status": concept.system.status,
            "Completeness": concept.system.completeness,
        }

        for item in concept.items.values():
            metadata[item.item_key] = item.value

        title = ""

        for key in (
            "persian_title",
            "title",
            "name",
        ):
            if key in concept.items:
                title = str(concept.items[key].value)
                break

        return KnowledgeNode(
            node_id=str(concept.system.database_id),
            title=title,
            status=str(concept.system.status or "NEW").upper(),
            domain=str(
                concept.items.get("domain").value
                if "domain" in concept.items
                else ""
            ),
            completeness=int(concept.system.completeness or 0),
            metadata=metadata,
        )
