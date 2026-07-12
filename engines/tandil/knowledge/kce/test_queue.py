from engines.tandil.knowledge.kce.engine import KnowledgeCompletionEngine

engine = KnowledgeCompletionEngine()

results = engine.scan_repository()

print("Nodes:", len(results))
print("Queue Size:", engine.queue.size())
