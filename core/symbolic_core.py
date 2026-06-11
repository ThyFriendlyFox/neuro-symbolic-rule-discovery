from typing import List, Dict, Any
import uuid
from datetime import datetime

from .hypothesis import Hypothesis

class SymbolicCore:
    def __init__(self):
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.observation_history: List[Dict] = []
        self.round = 0
        self.current_theory_confidence = 0.0
        print("Symbolic Core initialized - zero knowledge state.")

    def add_hypothesis(self, statement: str, formal_condition: str, tags: List[str] = None) -> Hypothesis:
        hyp_id = str(uuid.uuid4())[:8]
        hyp = Hypothesis(
            id=hyp_id,
            statement=statement,
            formal_condition=formal_condition,
            tags=tags or [],
            last_tested=str(self.round)
        )
        self.hypotheses[hyp_id] = hyp
        print(f"Symbolic Core: New hypothesis added [{hyp_id}] {statement}")
        return hyp

    def record_observation(self, observation: Dict):
        self.observation_history.append({
            **observation,
            "round": self.round,
            "timestamp": datetime.now().isoformat()
        })
        print(f"Symbolic Core: Recorded observation (round {self.round})")

    def evaluate_hypothesis(self, hyp_id: str, game_state: Any, move: Any) -> bool:
        """Very simple evaluator for POC - in real version this would execute the formal_condition safely."""
        if hyp_id not in self.hypotheses:
            return False
        
        hyp = self.hypotheses[hyp_id]
        # For Alpha, we will simulate verification logic in the game loop
        # This stub returns True for now - will be replaced with real predicate execution
        print(f"  → Evaluated {hyp_id}: {hyp.statement} → (stub: True)")
        return True

    def update_from_result(self, hyp_id: str, supports: bool):
        if hyp_id in self.hypotheses:
            self.hypotheses[hyp_id].update(supports)
            print(f"Symbolic Core: Updated {hyp_id} → confidence now {self.hypotheses[hyp_id].confidence:.3f}")

    def get_top_hypotheses(self, n: int = 5) -> List[Hypothesis]:
        return sorted(self.hypotheses.values(), key=lambda h: h.confidence, reverse=True)[:n]

    def calculate_theory_confidence(self) -> float:
        if not self.hypotheses:
            self.current_theory_confidence = 0.0
            return 0.0
        
        avg_conf = sum(h.confidence for h in self.hypotheses.values()) / len(self.hypotheses)
        coverage = min(1.0, len(self.observation_history) / 50)  # simplistic
        self.current_theory_confidence = round(avg_conf * coverage, 4)
        return self.current_theory_confidence

    def next_round(self):
        self.round += 1
        print(f"\n--- Round {self.round} ---")
        return self.round

    def get_status(self) -> str:
        status = f"Symbolic Core Status (Round {self.round})\n"
        status += f"Theory Confidence: {self.current_theory_confidence:.1%}\n"
        status += f"Hypotheses tracked: {len(self.hypotheses)}\n\n"
        for hyp in self.get_top_hypotheses(6):
            status += f"  {hyp}\n"
        return status
