from .rules import calculate_completeness, minimum_validation

class KnowledgeRepositoryScanner:
    """
    Scans Knowledge Repository and evaluates nodes.
    """

    def __init__(self, repository, validator=None):
        self.repository = repository
        self.validator = validator

    def scan(self):
        results = []

        nodes = self.repository.load_all_node_models()

        for node in nodes:
            valid = minimum_validation(node)

            results.append({
                "node": node,
                "valid": valid,
            })

        return results
