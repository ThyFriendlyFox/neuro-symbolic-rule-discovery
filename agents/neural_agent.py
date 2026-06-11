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
        """Generate abstract, game-agnostic hypotheses using template patterns.
        No hardcoded card values, parities, or game-specific strings.
        Focus on general relations between observed variables."""
        hypotheses = []
        recent_penalties = self.penalty_history[-5:]

        if not recent_penalties:
            # Early exploration - purely abstract
            hypotheses.append(Hypothesis(
                id="explore-001",
                statement="Penalties occur under certain unobserved conditions involving card properties and actions",
                formal_condition="penalty_observed == True",
                tags=["meta", "exploration"],
                confidence=0.60
            ))
            return hypotheses[:n]

        # Abstract templates - no game knowledge leaked
        # Template 1: Action flag required for certain cards
        hypotheses.append(Hypothesis(
            id=f"action-flag-{len(hypotheses)}",
            statement="Certain card values require an accompanying spoken action or flag to avoid penalty",
            formal_condition="(card_value_property > 0) and (spoken_flag == False)",
            tags=["action_required", "general"],
            confidence=0.55
        ))

        # Template 2: Sequential dependency
        hypotheses.append(Hypothesis(
            id=f"sequence-dep-{len(hypotheses)}",
            statement="The validity of a move depends on a relationship between current and previous card properties",
            formal_condition="(current_card_property != previous_card_property) and (action_flag == False)",
            tags=["sequence_rule", "general"],
            confidence=0.55
        ))

        # Template 3: Meta - dynamic or hidden state
        hypotheses.append(Hypothesis(
            id=f"meta-state-{len(hypotheses)}",
            statement="The rule set may include hidden state or dynamically activated constraints",
            formal_condition="hidden_state_active == True",
            tags=["meta", "dynamic"],
            confidence=0.50
        ))

        # Template 4: Composite pattern
        hypotheses.append(Hypothesis(
            id=f"composite-{len(hypotheses)}",
            statement="Penalties arise from conjunction of multiple observable features (card, history, spoken)",
            formal_condition="(feature_match == True) and (spoken == False)",
            tags=["composite", "general"],
            confidence=0.52
        ))

        print(f"Neural Agent: Generated {len(hypotheses)} abstract game-agnostic hypotheses this round")
        return hypotheses[:n]
