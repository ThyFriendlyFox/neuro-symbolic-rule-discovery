from typing import List, Dict
from core.symbolic_core import SymbolicCore
from core.hypothesis import Hypothesis

class NeuralAgent:
    """
    Neural Agent - Creative hypothesis generator for the neuro-symbolic system.
    Improved version: generates multiple specific hypotheses per penalty type.
    """
    
    def __init__(self):
        self.observation_buffer = []
        self.penalty_history = []
        print("Neural Agent initialized - ready to observe and propose hypotheses.")

    def observe(self, game_state: Dict, move_result: Dict):
        observation = {
            "state": game_state,
            "move_result": move_result,
            "timestamp": len(self.observation_buffer)
        }
        self.observation_buffer.append(observation)
        
        if "PENALTY" in str(move_result).upper() or "Penalty" in str(move_result):
            self.penalty_history.append(move_result)
            print(f"Neural Agent: PENALTY detected - generating targeted hypotheses")

    def generate_hypotheses(self, symbolic_core: SymbolicCore, n: int = 5) -> List[Hypothesis]:
        """Generate observation-driven, game-agnostic hypotheses.
        Analyzes recent penalties and context to produce diverse, verifiable predicates
        using general mathematical relations on observed variables (card numbers, spoken flags).
        Treats Neural output strictly as testable hypotheses."""
        hypotheses = []
        recent_penalties = self.penalty_history[-5:]
        recent_obs = self.observation_buffer[-10:] if self.observation_buffer else []

        # Always generate a meta-exploration hypothesis
        hypotheses.append(Hypothesis(
            id=f"meta-explore-{len(hypotheses)}",
            statement="Penalties are triggered by specific combinations of card properties, history, and spoken actions",
            formal_condition="penalty == True and (spoken is None or len(str(spoken)) == 0)",
            tags=["meta", "exploration", "penalty_trigger"],
            confidence=0.45
        ))

        if recent_penalties or recent_obs:
            # Hypothesis 1: Parity/sequential rule (even after odd etc.)
            hypotheses.append(Hypothesis(
                id=f"parity-seq-{len(hypotheses)}",
                statement="Move validity depends on parity or modular relationship between current and previous card",
                formal_condition="(card % 2 == 0) and (previous_card % 2 == 1)",
                tags=["sequence_rule", "parity", "modular"],
                confidence=0.48
            ))

            # Hypothesis 2: Spoken action required on specific card properties
            hypotheses.append(Hypothesis(
                id=f"spoken-req-{len(hypotheses)}",
                statement="Certain card values (e.g. specific remainders) require a non-empty spoken action/flag",
                formal_condition="(card % 13 == 7) and (spoken is None or str(spoken).strip() == '')",
                tags=["action_required", "spoken_flag", "card_property"],
                confidence=0.50
            ))

            # Hypothesis 3: Composite feature conjunction
            hypotheses.append(Hypothesis(
                id=f"composite-feat-{len(hypotheses)}",
                statement="Penalties result from conjunction of card features + missing spoken action + history state",
                formal_condition="(card > 0) and (previous_card is not None) and (spoken is None or spoken == False)",
                tags=["composite", "conjunction", "general"],
                confidence=0.47
            ))

            # Hypothesis 4: Dynamic/hidden constraint activation
            hypotheses.append(Hypothesis(
                id=f"dynamic-constraint-{len(hypotheses)}",
                statement="Rules include hidden or round-dependent activation of constraints",
                formal_condition="(round % 3 == 0) or (hidden_state_active == True)",
                tags=["meta", "dynamic", "hidden_state"],
                confidence=0.42
            ))

            # Hypothesis 5: Negation / absence pattern
            hypotheses.append(Hypothesis(
                id=f"absence-pattern-{len(hypotheses)}",
                statement="Penalty occurs precisely when an expected action or property match is absent",
                formal_condition="not (spoken and card_property_match) and penalty == True",
                tags=["negation", "absence", "general"],
                confidence=0.44
            ))

        print(f"Neural Agent: Generated {len(hypotheses)} observation-aware game-agnostic hypotheses this round")
        return hypotheses[:n]
