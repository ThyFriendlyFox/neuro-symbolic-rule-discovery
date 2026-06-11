from dataclasses import dataclass, field
from typing import Any, Dict, List
import json

@dataclass
class Hypothesis:
    id: str
    statement: str                    # Natural language description
    formal_condition: str             # Executable Python expression or predicate
    confidence: float = 0.5           # 0.0 to 1.0
    supporting_evidence: int = 0
    contradicting_evidence: int = 0
    last_tested: str = ""             # timestamp or round id
    tags: List[str] = field(default_factory=list)  # e.g. ["move_rule", "penalty_rule", "meta"]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "statement": self.statement,
            "formal_condition": self.formal_condition,
            "confidence": round(self.confidence, 4),
            "supporting": self.supporting_evidence,
            "contradicting": self.contradicting_evidence,
            "last_tested": self.last_tested,
            "tags": self.tags
        }

    def update(self, supports: bool):
        if supports:
            self.supporting_evidence += 1
        else:
            self.contradicting_evidence += 1
        
        # Simple Bayesian-style update (Laplace smoothing)
        total = self.supporting_evidence + self.contradicting_evidence
        if total > 0:
            self.confidence = (self.supporting_evidence + 1) / (total + 2)

    def __repr__(self):
        return f"H[{self.id}] {self.confidence:.2f} {self.statement[:60]}..."
