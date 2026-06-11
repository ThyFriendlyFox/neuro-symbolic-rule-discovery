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
        hypotheses = []
        recent_penalties = self.penalty_history[-5:]

        if not recent_penalties:
            # Early exploration hypothesis
            hypotheses.append(Hypothesis(
                id="explore-001",
                statement="There exist hidden rules that cause penalties on specific card combinations or actions",
                formal_condition="penalty_observed == True",
                tags=["meta", "exploration"],
                confidence=0.75
            ))
            return hypotheses[:n]

        # Analyze the most recent penalty
        last_penalty_str = str(recent_penalties[-1]).lower()

        if "say a word" in last_penalty_str or "spoken" in last_penalty_str or "7" in last_penalty_str:
            hypotheses.append(Hypothesis(
                id="spoken-001",
                statement="Must say a specific word (like 'Mao') when playing 7s or other special cards",
                formal_condition="card % 13 == 7 and not spoken",
                tags=["spoken_rule", "special_card"],
                confidence=0.85
            ))

        if "even" in last_penalty_str or "odd" in last_penalty_str or "parity" in last_penalty_str:
            hypotheses.append(Hypothesis(
                id="parity-001",
                statement="Cannot play an even card immediately after an odd card (parity restriction)",
                formal_condition="previous_card % 2 == 1 and current_card % 2 == 0",
                tags=["move_restriction", "parity"],
                confidence=0.82
            ))

        # Meta hypothesis about rule evolution
        hypotheses.append(Hypothesis(
            id="meta-dynamic-001",
            statement="The game can introduce new hidden rules dynamically during play",
            formal_condition="new_rule_introduced == True",
            tags=["meta", "dynamic_rules"],
            confidence=0.65
        ))

        # General pattern hypothesis
        hypotheses.append(Hypothesis(
            id="pattern-001",
            statement="Penalties are triggered by specific combinations of card value, previous card, and spoken words",
            formal_condition="penalty_pattern_detected == True",
            tags=["meta", "pattern"],
            confidence=0.70
        ))

        print(f"Neural Agent: Generated {len(hypotheses)} specific hypotheses this round")
        return hypotheses[:n]
