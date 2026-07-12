from dataclasses import dataclass, field
from typing import Dict


@dataclass
class KnowledgeNode:
    node_id: str
    title: str
    status: str
    domain: str
    completeness: int = 0
    metadata: Dict = field(default_factory=dict)
