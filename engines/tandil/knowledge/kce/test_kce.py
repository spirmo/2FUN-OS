from .engine import KnowledgeCompletionEngine

kce = KnowledgeCompletionEngine()

for result in kce.scan_repository():
    print(result)
