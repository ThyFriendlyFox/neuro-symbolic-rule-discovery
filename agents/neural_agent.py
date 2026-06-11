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
            print(f"Neural Agent (Gemma) error: {e} — using fallback hypotheses for robustness")
            return self._generate_fallback_hypotheses(recent_obs, recent_penalties, n)

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
    def _generate_fallback_hypotheses(self, observations, penalties, n=5):
        """Fallback when LLM unavailable: generate basic verifiable hypotheses from observations."""
        hypotheses = []
        hypotheses.append(Hypothesis(
            id=f"fallback-parity-{len(hypotheses)}",
            statement="Move validity depends on parity relationship between current and previous card",
            formal_condition="(card % 2 == 0) and (previous_card % 2 == 1)",
            tags=["parity", "fallback"],
            confidence=0.4
        ))
        hypotheses.append(Hypothesis(
            id=f"fallback-spoken-{len(hypotheses)}",
            statement="Certain cards require a spoken action",
            formal_condition="(card % 13 == 7) and (spoken is None or str(spoken).strip() == '')",
            tags=["action_required", "fallback"],
            confidence=0.45
        ))
        print(f"Neural Agent: Using {len(hypotheses)} fallback hypotheses")
        return hypotheses[:n]
