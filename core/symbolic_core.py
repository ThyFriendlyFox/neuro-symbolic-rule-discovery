from typing import List, Dict, Any, Tuple, Optional
import uuid
from datetime import datetime
import random

from .hypothesis import Hypothesis
from .predicate_evaluator import evaluator

class SymbolicCore:
    def __init__(self):
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.observation_history: List[Dict] = []
        self.round = 0
        self.current_theory_confidence = 0.0
        print("Symbolic Core initialized - zero knowledge state. Ready for multiple competing hypotheses.")

    def add_hypothesis(self, statement: str, formal_condition: str, tags: List[str] = None) -> Hypothesis:
        """Add a new hypothesis. No longer auto-merges — maintains competing hypotheses."""
        hyp_id = str(uuid.uuid4())[:8]
        hyp = Hypothesis(
            id=hyp_id,
            statement=statement,
            formal_condition=formal_condition,
            tags=tags or [],
            last_tested=str(self.round),
            confidence=0.5
        )
        self.hypotheses[hyp_id] = hyp
        print(f"  → Added competing hypothesis [{hyp_id}]: {statement[:65]}... (conf=0.50)")
        return hyp

    def record_observation(self, observation: Dict):
        self.observation_history.append({
            **observation,
            "round": self.round,
            "timestamp": datetime.now().isoformat()
        })

    def _safe_eval_condition(self, formal_condition: str, context: Dict) -> bool:
        """Delegates to the real PredicateEvaluator."""
        normalized_context = {k.lower(): v for k, v in context.items()}
        return evaluator.evaluate(formal_condition, normalized_context)

    def evaluate_hypothesis(self, hyp_id: str, context: Dict) -> bool:
        if hyp_id not in self.hypotheses:
            return False
        hyp = self.hypotheses[hyp_id]
        result = self._safe_eval_condition(hyp.formal_condition, context)
        return result

    def update_from_result(self, hyp_id: str, supports: bool):
        if hyp_id in self.hypotheses:
            self.hypotheses[hyp_id].update(supports)

    def select_next_experiment(self) -> Tuple[int, Optional[str]]:
        """Abstract information-gain based selection. Returns (card_suggestion, spoken_suggestion).
        NO game-specific knowledge or hardcoded card values. Purely uncertainty-driven.
        The actual move interpreter lives outside (game-agnostic contract)."""
        if not self.hypotheses:
            # Zero-knowledge: return neutral placeholder; caller must interpret abstractly
            return 0, None  # 0 signals 'any valid exploratory card'

        scored = []
        for hyp in self.hypotheses.values():
            uncertainty = 1.0 - abs(hyp.confidence - 0.5)
            scored.append((uncertainty, hyp))

        scored.sort(reverse=True)
        best_hyp = scored[0][1]

        print(f"Symbolic Core: Selected hypothesis for testing: {best_hyp.id} (confidence {best_hyp.confidence:.2f}, uncertainty {scored[0][0]:.2f})")

        # Abstract decision: prefer spoken action if hypothesis mentions action/flag/meta
        tags_lower = [t.lower() for t in best_hyp.tags]
        stmt_lower = best_hyp.statement.lower()
        if any(k in tags_lower + [stmt_lower] for k in ["spoken", "action", "flag", "meta", "say"]):
            return 0, "ACTION"  # abstract spoken flag
        else:
            return 0, None  # explore without spoken, let game provide concrete card

    def get_top_hypotheses(self, n: int = 6) -> List[Hypothesis]:
        return sorted(self.hypotheses.values(), key=lambda h: h.confidence, reverse=True)[:n]

    def calculate_theory_confidence(self) -> float:
        if not self.hypotheses:
            self.current_theory_confidence = 0.0
            return 0.0
        
        avg_conf = sum(h.confidence for h in self.hypotheses.values()) / len(self.hypotheses)
        self.current_theory_confidence = round(avg_conf * 0.9, 4)
        return self.current_theory_confidence

    def next_round(self):
        self.round += 1
        return self.round

    def get_status(self) -> str:
        status = f"Symbolic Core Status (Round {self.round})\n"
        status += f"Theory Confidence: {self.current_theory_confidence:.1%}\n"
        status += f"Hypotheses tracked: {len(self.hypotheses)}\n\n"
        for hyp in self.get_top_hypotheses():
            status += f"  {hyp}\n"
        return status
