from pathlib import Path
import re

class KnowledgeRepository:
    """
    Repository for Knowledge Nodes.
    """

    def __init__(self, root="modules/knowledge/domains"):
        self.root = Path(root)

    def concepts(self):
        return sorted(self.root.rglob("concepts/*.md"))

    def evidences(self):
        return sorted(self.root.rglob("evidences/*.md"))

    def all_nodes(self):
        return {
            "concepts": self.concepts(),
            "evidences": self.evidences(),
        }

    def load_all_concepts(self):
        nodes = []

        for concept in self.concepts():
            nodes.append(self.load_concept(concept))
        return nodes

    def load_concept(self, path):
        """
        Load a concept markdown file.
        """

        text = path.read_text(encoding="utf-8")

        node_id = path.stem.split("_")[0]

        title = ""

        for line in text.splitlines():
            line = line.strip()

            if line.startswith("# "):
                title = line[2:].strip()
                break



        metadata = {}

        lines = text.splitlines()

        i = 0 
        while i < len(lines) - 1:
            key = lines[i].strip()

            if key.endswith(":"):
                value = lines[i + 1].strip()
                metadata[key[:-1]] = value
            i += 1

        return {
            "node_id": node_id,
            "title": title,
            "path": path,
            "metadata": metadata,
            "content": text,
        }


