from .validators import validate_node
from .importer import import_node


class KnowledgeInjectionWorkflow:
    """
    Coordinates the complete Knowledge Injection process.
    """

    def process(self, json_file: str, repository: str):
        """
        Execute the Knowledge Injection workflow.
        """

        result = import_node(json_file, repository)

        return {
            "success": result["valid"],
            "status": result["status"],
            "completeness": result["completeness"],
            "errors": result["errors"],
            "file": result["file"],
        }
