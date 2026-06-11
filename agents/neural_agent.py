from typing import List, Dict
import openai
import json
import re
from core.symbolic_core import SymbolicCore
from core.hypothesis import Hypothesis

# LM Studio local server configuration
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "google/gemma-4-e4b"

client = openai.OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key="lm-studio"
)


class NeuralAgent:
    """
    Neural Agent powered by local Gemma model via LM Studio.
    Completely game-agnostic. Works with any turn-based environment
    that provides observations, actions, and penalties.
    """

    def __init__(self):
        self.observation_buffer: List[Dict] = []
        self.penalty_history: List[Dict] = []
        print("Neural Agent initialized — connected to Gemma (game-agnostic mode).")

    def observe(self, observation: Dict, action_result: Dict):
        entry = {
            "observation": observation,
            "result": action_result,
            "timestamp": len(self.observation_buffer)
        }
        self.observation_buffer.append(entry)

        if "penalty" in str(action_result).lower() or "PENALTY" in str(action_result).upper():
            self.penalty_history.append(action_result)
            print(f"Neural Agent: Penalty detected — querying Gemma for hypotheses")

    def generate_hypotheses(self, symbolic_core: SymbolicCore, n: int = 5) -> List[Hypothesis]:
        recent_penalties = self.penalty_history[-6:]
        recent_obs = self.observation_buffer[-10:] if self.observation_buffer else []

        if not recent_penalties and not recent_obs:
            return []

        prompt = self._build_abstract_prompt(recent_obs, recent_penalties)

        try:
            response = client.chat.completions.create(
                model=LMSTUDIO_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a hypothesis generator for a neuro-symbolic rule discovery system. "
                            "You have ZERO knowledge of the specific game. "
                            "You only see abstract observations, actions, and penalties from an unknown environment with a dealer. "
                            "Generate general, testable hypotheses about hidden rules. "
                            "Output ONLY a JSON array."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.75,
                max_tokens=900,
            )

            content = response.choices[0].message.content.strip()
            hypotheses = self._parse_hypotheses(content)
            print(f"Neural Agent (Gemma): Generated {len(hypotheses)} game-agnostic hypotheses")
            return hypotheses[:n]

        except Exception as e:
            print(f"Neural Agent (Gemma) error: {e}")
            return []

    def respond_to_interrogation(self, questions: List[str], symbolic_core: SymbolicCore) -> List[Dict]:
        """Respond to Symbolic Core's interrogation questions using Gemma.
        This properly closes the two-agent dialogue loop.
        """
        if not questions:
            return []

        print(f"Neural Agent: Responding to {len(questions)} interrogation questions from Symbolic Core...")

        responses = []
        for question in questions:
            try:
                prompt = f"""You are the Neural Agent in a neuro-symbolic rule discovery system.
You have been asked the following meta-question by the Symbolic Core:

"{question}"

Answer thoughtfully and propose 1-2 new abstract hypotheses that could help resolve the ambiguity or contradiction.
Return only a JSON object with keys: "answer", "new_hypotheses" (list of strings)."""

                response = client.chat.completions.create(
                    model=LMSTUDIO_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a precise, game-agnostic hypothesis generator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=400,
                )

                content = response.choices[0].message.content.strip()
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    data = json.loads(match.group(0))
                    responses.append({
                        "question": question,
                        "answer": data.get("answer", ""),
                        "new_hypotheses": data.get("new_hypotheses", [])
                    })
                else:
                    responses.append({"question": question, "answer": content, "new_hypotheses": []})

            except Exception as e:
                responses.append({"question": question, "answer": f"Error: {e}", "new_hypotheses": []})

        return responses

    def _build_abstract_prompt(self, observations: List[Dict], penalties: List[Dict]) -> str:
        return f"""Environment observations (last 10):
{json.dumps(observations, indent=2)}

Recent penalties (last 6):
{json.dumps(penalties, indent=2)}

You do not know what game this is. Generate 5 diverse, abstract hypotheses about the hidden rules of this environment.

Each hypothesis must be a JSON object with:
- "statement": natural language description of a possible rule
- "formal_condition": a logical expression using variables like state_var, action, previous_action, penalty, dealer_response, history
- "tags": list of abstract categories
- "confidence": float 0.35–0.75

Return ONLY a valid JSON array."""

    def _parse_hypotheses(self, content: str) -> List[Hypothesis]:
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if not match:
            return []

        try:
            data = json.loads(match.group(0))
            hypotheses = []
            for item in data:
                if isinstance(item, dict) and "statement" in item:
                    hyp = Hypothesis(
                        id=f"gemma-{len(hypotheses)}",
                        statement=item.get("statement", ""),
                        formal_condition=item.get("formal_condition", "True"),
                        tags=item.get("tags", ["abstract"]),
                        confidence=float(item.get("confidence", 0.5))
                    )
                    hypotheses.append(hyp)
            return hypotheses
        except Exception:
            return []