from typing import List, Dict
import openai
from core.symbolic_core import SymbolicCore
from core.hypothesis import Hypothesis

# LM Studio local server configuration
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "google/gemma-4-e4b"

client = openai.OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key="lm-studio"   # LM Studio doesn't require a real key
)


class NeuralAgent:
    """
    Neural Agent powered by local Gemma model via LM Studio.
    Generates hypotheses dynamically by calling the real LLM.
    """

    def __init__(self):
        self.observation_buffer = []
        self.penalty_history = []
        print("Neural Agent initialized — connected to Gemma via LM Studio.")

    def observe(self, game_state: Dict, move_result: Dict):
        observation = {
            "state": game_state,
            "move_result": move_result,
            "timestamp": len(self.observation_buffer)
        }
        self.observation_buffer.append(observation)

        if "PENALTY" in str(move_result).upper() or "Penalty" in str(move_result):
            self.penalty_history.append(move_result)
            print(f"Neural Agent: PENALTY detected — will query Gemma for hypotheses")

    def generate_hypotheses(self, symbolic_core: SymbolicCore, n: int = 5) -> List[Hypothesis]:
        """Query Gemma to generate observation-driven hypotheses."""
        recent_penalties = self.penalty_history[-5:]
        recent_obs = self.observation_buffer[-8:] if self.observation_buffer else []

        if not recent_penalties and not recent_obs:
            return []

        # Build prompt for Gemma
        prompt = self._build_prompt(recent_obs, recent_penalties)

        try:
            response = client.chat.completions.create(
                model=LMSTUDIO_MODEL,
                messages=[
                    {"role": "system", "content": 
                     "You are a precise hypothesis generator for a neuro-symbolic rule discovery system. "
                     "Output only valid JSON array of hypothesis objects with keys: statement, formal_condition, tags, confidence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800,
            )

            content = response.choices[0].message.content.strip()
            hypotheses = self._parse_hypotheses(content)
            print(f"Neural Agent (Gemma): Generated {len(hypotheses)} hypotheses")
            return hypotheses[:n]

        except Exception as e:
            print(f"Neural Agent (Gemma) error: {e}")
            return []

    def _build_prompt(self, observations: List[Dict], penalties: List[Dict]) -> str:
        return f"""Recent observations:
{observations}

Recent penalties:
{penalties}

Generate 4-6 diverse, verifiable hypotheses about the hidden rules.
Each hypothesis must have:
- statement: natural language description
- formal_condition: logical predicate using variables like card, spoken, previous_card, round, penalty
- tags: list of categories
- confidence: float between 0.3 and 0.8

Return ONLY a JSON array."""

    def _parse_hypotheses(self, content: str) -> List[Hypothesis]:
        import json
        import re

        # Try to extract JSON array
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if not match:
            return []

        try:
            data = json.loads(match.group(0))
            hypotheses = []
            for i, item in enumerate(data):
                if isinstance(item, dict) and "statement" in item:
                    hyp = Hypothesis(
                        id=f"gemma-{len(hypotheses)}",
                        statement=item.get("statement", ""),
                        formal_condition=item.get("formal_condition", "True"),
                        tags=item.get("tags", ["gemma"]),
                        confidence=float(item.get("confidence", 0.5))
                    )
                    hypotheses.append(hyp)
            return hypotheses
        except Exception:
            return []