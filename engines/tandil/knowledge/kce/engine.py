from datetime import datetime
from .repository_adapter import KnowledgeRepositoryAdapter
from .queue import CompletionQueue
from .history import HistoryManager
from .rules import can_transition, minimum_validation


class KnowledgeCompletionEngine:
    """
    Knowledge Completion Engine (KCE)
    """

    def load_first_node_model(self):
        return self.repository.load_first_node_model()

    def validate(self, node):
        return minimum_validation(node)

    def scan_repository(self):
        results = []

        for node in self.load_all_nodes():
            results.append({
                "node_id": node.node_id,
                "valid": self.validate(node),
                "status": node.status,
                "completeness": node.completeness,
            })

        return results


    def load_all_nodes(self):
        return self.repository.load_all_node_models()

    def load_all_nodes(self):
        return self.repository.load_all_node_models()

    def __init__(self):
        self.queue = CompletionQueue()
        self.history = HistoryManager()
        self.repository = KnowledgeRepositoryAdapter()

    def list_nodes(self):
        return self.repository.all_nodes()

    def transition(self, node, next_state):
        current = node.status

        if not can_transition(current, next_state):
            return {
                "success": False,
                "current": current,
                "requested": next_state,
            }

        node.status = next_state

        self.history.record({
            "node_id": node.node_id,
            "from": current,
            "to": next_state,
            "timestamp": datetime.utcnow().isoformat()
        })

        if next_state == "NEED_COMPLETION":
            self.queue.add(node)

        return {
            "success": True,
            "status": node.status,
        }
    def load_first_node(self):
        return self.repository.load_first_concept()
