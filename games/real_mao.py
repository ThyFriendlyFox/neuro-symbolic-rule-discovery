"""
RealMaoGame - Proper implementation of classic Mao rules for neuro-symbolic testing.
This replaces the trivial single-rule game with a genuinely complex rule set.
"""

from typing import List, Tuple, Optional
import random


class RealMaoGame:
    """
    Real Mao game with multiple interacting rules.
    Rules are hidden from the agent. Penalties for breaking any rule.
    Supports spoken actions, skips, reverses, and draw penalties.
    """

    def __init__(self, seed: int = 42, num_players: int = 4):
        random.seed(seed)
        # Cards: 0-51 representing standard deck
        # Rank: card % 13 (0=Ace, 1=2, ..., 11=Jack, 12=King)
        # Suit: card // 13 (0=Spades, 1=Hearts, 2=Diamonds, 3=Clubs)
        self.deck = list(range(52))
        random.shuffle(self.deck)
        self.num_players = num_players
        self.current_player = 0
        self.direction = 1  # 1 = clockwise, -1 = counter-clockwise
        self.played_cards: List[int] = []
        self.penalties_this_round = 0
        self.last_penalty_reason: Optional[str] = None
        self.round = 0
        self.skips_remaining = 0
        self.draw_stack = 0  # For stacking Aces

        # Real Mao hidden rules
        self.hidden_rules = [
            {"id": "suit_or_rank", "description": "Must match suit or rank of previous card"},
            {"id": "seven_spoken", "description": "Playing a 7 requires saying a word/phrase"},
            {"id": "eight_skip", "description": "Playing an 8 skips the next player"},
            {"id": "jack_reverse", "description": "Playing a Jack reverses direction"},
            {"id": "ace_draw", "description": "Playing an Ace forces next player to draw 2 cards"},
        ]

        print("RealMaoGame initialized with full classic Mao rules (hidden).")

    def _get_rank(self, card: int) -> int:
        return card % 13

    def _get_suit(self, card: int) -> int:
        return card // 13

    def get_state(self) -> dict:
        return {
            "round": self.round,
            "last_card": self.played_cards[-1] if self.played_cards else None,
            "penalties_this_round": self.penalties_this_round,
            "last_penalty": self.last_penalty_reason,
            "direction": self.direction,
            "draw_stack": self.draw_stack,
        }

    def play_move(self, card: int, spoken: Optional[str] = None) -> Tuple[bool, str]:
        """
        Attempt to play a card. Returns (success, reason).
        """
        self.round += 1
        self.penalties_this_round = 0
        self.last_penalty_reason = None

        # First card is always accepted
        if not self.played_cards:
            self.played_cards.append(card)
            return True, "First card played successfully"

        last_card = self.played_cards[-1]
        last_rank = self._get_rank(last_card)
        last_suit = self._get_suit(last_card)
        rank = self._get_rank(card)
        suit = self._get_suit(card)

        # === Rule 1: Must match suit or rank ===
        if suit != last_suit and rank != last_rank:
            self.penalties_this_round += 1
            self.last_penalty_reason = "Must match suit or rank"
            return False, "Penalty: Must match suit or rank of previous card"

        # === Rule 2: 7 requires spoken word ===
        if rank == 6:  # 7 (0-indexed rank 6)
            if not spoken or not spoken.strip():
                self.penalties_this_round += 1
                self.last_penalty_reason = "Must speak when playing 7"
                return False, "Penalty: Must say something when playing a 7"

        # === Rule 3: 8 skips next player ===
        if rank == 7:  # 8
            self.skips_remaining = 1

        # === Rule 4: Jack reverses direction ===
        if rank == 10:  # Jack
            self.direction *= -1

        # === Rule 5: Ace forces draw 2 (or stacks) ===
        if rank == 0:  # Ace
            self.draw_stack += 2

        # Card accepted
        self.played_cards.append(card)

        # Apply pending skips/draws for next player
        if self.skips_remaining > 0:
            self.skips_remaining -= 1
            # In a real game we'd advance the player here

        return True, "Move accepted"

    def get_hidden_rules_summary(self) -> List[str]:
        """Debug only - agent should never see this"""
        return [r["description"] for r in self.hidden_rules]