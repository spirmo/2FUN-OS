from .repository import KnowledgeRepository

repo = KnowledgeRepository()

concept = repo.concepts()[0]

node = repo.load_concept(concept)

print(node)
