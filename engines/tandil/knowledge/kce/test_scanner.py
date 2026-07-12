from modules.knowledge.repository.repository import KnowledgeRepository
from .scanner import KnowledgeRepositoryScanner


repository = KnowledgeRepository()

scanner = KnowledgeRepositoryScanner(
    repository=repository
)

results = scanner.scan()

print("=== Scanner Report ===")

print("Nodes:", len(results))

for item in results:
    node = item["node"]

    print("----------------------")
    print("ID:", node.node_id)
    print("TITLE:", node.title)
    print("DOMAIN:", node.domain)
    print("COMPLETENESS:", node.completeness)
    print("VALID:", item["valid"])
