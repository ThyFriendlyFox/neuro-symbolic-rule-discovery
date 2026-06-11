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

    def select_next_experiment(self, game_state: Optional[Dict] = None) -> Tuple[int, Optional[str]]:
        """Strong experiment selection: uses hypothesis to propose concrete test moves.
        Generates candidate cards likely to falsify/support the formal_condition (boundary testing).
        Returns (suggested_card, spoken_suggestion). This drives active experimentation."""
        if not self.hypotheses:
            # True zero-knowledge exploration: try diverse cards
            return random.choice([7, 14, 21, 28, 35, 42, 49, 3, 11, 19]), None

        scored = []
        for hyp in self.hypotheses.values():
            uncertainty = 1.0 - abs(hyp.confidence - 0.5)
            evidence_count = hyp.supporting_evidence + hyp.contradicting_evidence
            info_gain = uncertainty * (1.0 / (evidence_count + 1.5))
            scored.append((info_gain, hyp.id, hyp))

        scored.sort(reverse=True, key=lambda x: x[0])
        best_hyp = scored[0][2]

        print(f"Symbolic Core: Selected hypothesis for testing: {best_hyp.id} (conf {best_hyp.confidence:.2f}, info_gain {scored[0][0]:.3f})")

        tags_lower = [t.lower() for t in best_hyp.tags]
        stmt_lower = best_hyp.statement.lower()
        formal = best_hyp.formal_condition.lower()

        spoken = None
        card = 0

        # Intelligent card suggestion based on hypothesis content (active testing)
        if any(k in tags_lower + [stmt_lower, formal] for k in ["spoken", "action", "flag", "say", "action_required", "7"]):
            card = 7  # Test the classic "say something on 7" rule
            spoken = "test" if "action" in tags_lower else None
        elif any(k in tags_lower + [stmt_lower, formal] for k in ["parity", "even", "odd", "modular", "% 2"]):
            # Test parity boundary
            card = 14 if random.random() > 0.5 else 15  # even after possible odd
        elif any(k in tags_lower + [stmt_lower, formal] for k in ["sequence", "previous", "consecutive"]):
            card = random.randint(1, 52)
        elif "round" in formal or "dynamic" in tags_lower:
            card = (self.round % 13) * 4 + 1  # round-dependent probe
        else:
            # Default: high-variance probe cards for unknown unknowns
            card = random.choice([7, 13, 21, 26, 39, 52, 1, 11, 33])

        if spoken is None and any(k in formal for k in ["spoken", "say", "action"]):
            spoken = "probe"

        print(f"  → Active experiment: card={card}, spoken='{spoken or ''}' to test '{best_hyp.statement[:50]}...'")
        return card, spoken

    def verify_global_consistency(self) -> Dict[str, Any]:
        """Run verification over observation history to detect contradictions.
        Returns summary of consistent vs contradicted hypotheses."""
        if not self.observation_history:
            return {"consistent": 0, "contradicted": 0, "total": 0}

        consistent = 0
        contradicted = 0
        for hyp_id, hyp in self.hypotheses.items():
            hyp_consistent = True
            for obs in self.observation_history[-20:]:  # recent window
                ctx = obs.get("context", {})
                try:
                    result = self._safe_eval_condition(hyp.formal_condition, ctx)
                    expected_penalty = not obs.get("success", True)
                    if result != expected_penalty:
                        hyp_consistent = False
                        break
                except:
                    hyp_consistent = False
            if hyp_consistent:
                consistent += 1
            else:
                contradicted += 1
        return {"consistent": consistent, "contradicted": contradicted, "total": len(self.hypotheses)}

    def calculate_theory_confidence(self) -> float:
        if not self.hypotheses:
            self.current_theory_confidence = 0.0
            return 0.0

        # More rigorous: weighted by evidence strength + average confidence
        total_evidence = 0
        weighted_sum = 0.0
        for h in self.hypotheses.values():
            ev = h.supporting_evidence + h.contradicting_evidence
            total_evidence += ev
            weighted_sum += h.confidence * (ev + 1)

        if total_evidence == 0:
            avg = sum(h.confidence for h in self.hypotheses.values()) / len(self.hypotheses)
            self.current_theory_confidence = round(avg * 0.85, 4)
        else:
            self.current_theory_confidence = round(weighted_sum / (total_evidence + len(self.hypotheses)), 4)

        # Apply consistency penalty
        consistency = self.verify_global_consistency()
        if consistency["total"] > 0:
            consistency_ratio = consistency["consistent"] / consistency["total"]
            self.current_theory_confidence *= (0.7 + 0.3 * consistency_ratio)

        return self.current_theory_confidence

    def get_top_hypotheses(self, n: int = 6) -> List[Hypothesis]:
        return sorted(self.hypotheses.values(), key=lambda h: h.confidence, reverse=True)[:n]

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
