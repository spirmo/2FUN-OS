from .rules import calculate_completeness
from modules.knowledge.repository.repository import KnowledgeRepository
from .models import KnowledgeNode


class KnowledgeRepositoryAdapter:
    """
    Adapter between KCE and Knowledge Repository.
    """

    def __init__(self):
        self.repository = KnowledgeRepository()

    def all_nodes(self):
        return self.repository.all_nodes()

    def load_first_node_model(self):
        data = self.load_first_concept()

        if data is None:
            return None

        metadata = data["metadata"]


        return KnowledgeNode(
            node_id=data["node_id"],
            title=data["title"],
            status=metadata.get("Status", "NEW").upper(),
            domain=metadata.get("Domain", ""),
            completeness=calculate_completeness(metadata),
            metadata=metadata,
        )


    def load_all_node_models(self):
        nodes = []

        for data in self.repository.load_all_concepts():
            metadata = data["metadata"]

            nodes.append(
                    KnowledgeNode(
                    node_id=data["node_id"],
                    title=data["title"],
                    status=metadata.get("Status", "NEW").upper(),
                    domain=metadata.get("Domain", ""),
                    completeness=calculate_completeness(metadata),
                    metadata=metadata,
                )
            )

        return nodes


    def load_first_concept(self):
        concepts = self.repository.concepts()

        if not concepts:
            return None

        return self.repository.load_concept(concepts[0])
