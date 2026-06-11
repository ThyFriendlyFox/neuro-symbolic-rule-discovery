from typing import List, Dict
import openai
import json
import re
import random
import os
from core.symbolic_core import SymbolicCore
from core.hypothesis import Hypothesis

# LM Studio local server configuration
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "google/gemma-4-e4b"

client = openai.OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key="lm-studio"
)

SIMULATION_MODE = os.environ.get("NEUROSYMBOLIC_SIMULATION", "0") == "1"


class NeuralAgent:
    """
    Neural Agent powered by local Gemma model via LM Studio.
    Completely game-agnostic. Works with any turn-based environment
    that provides observations, actions, and penalties.
    Enhanced with robust fallback for fully autonomous cron operation.
    Supports NEUROSYMBOLIC_SIMULATION=1 env var for fully offline cron runs.
    """

    def __init__(self):
        self.observation_buffer: List[Dict] = []
        self.penalty_history: List[Dict] = []
        mode_str = "SIMULATION (offline, fallback only)" if SIMULATION_MODE else "Gemma (game-agnostic mode)"
        print(f"Neural Agent initialized — {mode_str}.")

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

        if SIMULATION_MODE:
            print("  NeuralAgent: SIMULATION mode active — using only fallback hypotheses (no LLM calls)")
            return self._generate_fallback_hypotheses(n)

        if not recent_penalties and not recent_obs:
            # Bootstrap with fallback for true zero-knowledge autonomous start
            print("  NeuralAgent: No observations yet — bootstrapping with fallback hypotheses")
            return self._generate_fallback_hypotheses(n)

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
            print("  → Falling back to pattern-based synthetic hypotheses (cron robustness)")
            return self._generate_fallback_hypotheses(n)

    def respond_to_interrogation(self, questions: List[str], symbolic_core: SymbolicCore) -> List[Dict]:
        """Respond to Symbolic Core's interrogation questions using Gemma.
        This properly closes the two-agent dialogue loop.
        """
        if not questions:
            return []

        if SIMULATION_MODE:
            print("  NeuralAgent: SIMULATION mode active — skipping LLM interrogation (offline mode)")
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

    def _generate_fallback_hypotheses(self, n: int = 5) -> List[Hypothesis]:
        """Robust fallback for autonomous cron runs when LLM unavailable.
        Generates structurally diverse, verifiable hypotheses with ZERO knowledge
        of any specific game rules or card values. All conditions are generic.
        """
        candidates = [
            Hypothesis(
                id=f"fb-parity-{random.randint(1000,9999)}",
                statement="Rule involves parity/even-odd property of played card relative to previous",
                formal_condition="(state_var % 2) == (previous_action % 2)",
                tags=["parity", "move_rule"],
                confidence=0.45
            ),
            Hypothesis(
                id=f"fb-spoken-{random.randint(1000,9999)}",
                statement="Certain states or actions require a spoken response or flag to avoid penalty",
                formal_condition="(action or spoken) and (state_var > 0)",
                tags=["spoken", "action_required"],
                confidence=0.50
            ),
            Hypothesis(
                id=f"fb-sequence-{random.randint(1000,9999)}",
                statement="Played card must follow sequence or be within range of previous card",
                formal_condition="abs(state_var - previous_action) <= 3 or (state_var > previous_action)",
                tags=["sequence", "consecutive"],
                confidence=0.40
            ),
            Hypothesis(
                id=f"fb-modular-{random.randint(1000,9999)}",
                statement="Rule depends on modular arithmetic involving round or state value",
                formal_condition="(round % 3 == 0) or ((state_var % 4) == 0)",
                tags=["modular", "round", "dynamic"],
                confidence=0.42
            ),
            Hypothesis(
                id=f"fb-meta-{random.randint(1000,9999)}",
                statement="Meta-rule: new rules or constraints can be introduced dynamically based on history",
                formal_condition="history > 8 and (dealer_response is not None)",
                tags=["meta", "dynamic_rule"],
                confidence=0.35
            ),
        ]
        random.shuffle(candidates)
        return candidates[:n]
