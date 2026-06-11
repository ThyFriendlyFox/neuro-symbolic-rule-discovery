from typing import List, Tuple, Optional
import random

class SimpleMaoGame:
    """
    Minimal Mao-like game for neuro-symbolic testing.
    Rules are hidden. Penalties are given for breaking unknown rules.
    New rules can be dynamically added during play.
    """
    
    def __init__(self, seed=42):
        random.seed(seed)
        self.deck = list(range(1, 53))  # simplified cards 1-52
        random.shuffle(self.deck)
        self.current_player = 0
        self.played_cards = []
        self.penalties_this_round = 0
        self.hidden_rules = [
            {"condition": "play_even_after_odd", "description": "Cannot play even card after odd card", "active": True},
            {"condition": "must_say_something_on_7", "description": "Must say a word when playing 7", "active": True},
        ]
        self.round = 0
        self.last_penalty_reason = None
        print("SimpleMaoGame initialized with hidden rules. Agent starts with zero knowledge.")

    def get_state(self) -> dict:
        return {
            "round": self.round,
            "last_card": self.played_cards[-1] if self.played_cards else None,
            "penalties_this_round": self.penalties_this_round,
            "last_penalty": self.last_penalty_reason
        }

    def play_move(self, card: int, spoken: Optional[str] = None) -> Tuple[bool, str]:
        """Returns (success, reason)"""
        self.round += 1
        self.penalties_this_round = 0
        self.last_penalty_reason = None

        if not self.played_cards:
            self.played_cards.append(card)
            return True, "First card played successfully"

        last = self.played_cards[-1]

        # Check hidden rules
        for rule in self.hidden_rules:
            if not rule["active"]:
                continue
                
            if rule["condition"] == "play_even_after_odd":
                if last % 2 == 1 and card % 2 == 0:
                    self.penalties_this_round += 1
                    self.last_penalty_reason = rule["description"]
                    return False, f"Penalty: {rule['description']}"
                    
            if rule["condition"] == "must_say_something_on_7" and card % 13 == 7:
                if not spoken or spoken.strip() == "":
                    self.penalties_this_round += 1
                    self.last_penalty_reason = rule["description"]
                    return False, f"Penalty: {rule['description']}"

        self.played_cards.append(card)
        return True, "Move accepted"

    def add_hidden_rule(self, condition: str, description: str):
        self.hidden_rules.append({
            "condition": condition,
            "description": description,
            "active": True
        })
        print(f"Game added new hidden rule: {description}")

    def get_hidden_rules_summary(self) -> List[str]:
        """Only for debugging - agent should never see this"""
        return [r["description"] for r in self.hidden_rules if r["active"]]
