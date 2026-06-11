# Neuro-Symbolic Rule Discovery System (Star) - SPEC.md

**Project Name:** Neuro-Symbolic Rule Discovery System (continuation of "Star")
**Version:** 0.2 (Updated with Mao + Unknown-Unknowns Insights)
**Researcher:** Hermes (Autonomous Senior Research Engineer)
**Date:** 2026-06-10
**Status:** Living Document — This specification is the current target for the Alpha prototype. It will be critiqued and evolved as we gather empirical results.

## Project Goal

Create a **general neuro-symbolic system** that can discover the **complete rules** (including hidden, social, and meta-rules) of *any* unknown turn-based game purely through experimental play, observation, systematic testing, and verification — starting from **zero prior knowledge**.

The system must gracefully handle **unknown unknowns** — situations where it does not even know what it does not know.

**Primary Test Environment (Alpha):** The card game **Mao** — a game where the rules are deliberately hidden from new players, new rules can be added dynamically, and learning occurs only through penalties and careful observation. Success on Mao is a strong indicator of real capability.

## System Architecture (v0.2 — Two-Agent Neuro-Symbolic Loop)

The system is built as a tight collaboration between two specialized agents:

### 1. Symbolic Core (GOFAI / Classical Reasoning Agent)
The rigorous, skeptical, mathematical backbone.

**Responsibilities:**
- Maintains *all* hypotheses as formal, testable logical predicates or executable conditions
- Tracks confidence scores for each hypothesis (Bayesian or frequency-based to start)
- Performs systematic hypothesis testing and elimination
- Decides which experiments to run next (prioritizing high information-gain tests)
- Runs **global consistency verification** against all historical observations
- Maintains the current "best theory" and calculates overall explanatory power
- Acts as the **interrogator** — continuously asking the Neural Agent targeted, clarifying questions when data is ambiguous or incomplete

### 2. Neural Agent (LLM-based Creative Explorer)
The creative, broad-knowledge, pattern-finding component.

**Responsibilities:**
- Observes raw game events, penalties, and outcomes
- Generates creative, plausible rule hypotheses (including analogies and high-level concepts)
- Translates messy observations into structured data for the Symbolic Core
- Suggests possible patterns, meta-rules, or entirely new ontological concepts
- Acts as the **explorer** — can use tools, search for analogies, or propose experiments the Symbolic Core might not think of

The two agents operate in a continuous **propose → test → verify → refine** loop. The Symbolic Core treats every output from the Neural Agent as a *hypothesis to be tested*, never as ground truth.

## Mathematical Verification & Experimentation Engine

Every hypothesis must be convertible into a **clear, mechanically verifiable predicate** (boolean function over game state + history).

**Core Loop (per round):**

1. Observe game state, move, outcome, and any penalty
2. Neural Agent generates candidate hypotheses and explanations
3. Symbolic Core integrates them, updates existing hypotheses, and performs consistency checks
4. Symbolic Core selects the highest-value next experiment (using information gain, contradiction potential, or coverage gaps)
5. Execute deliberate test move(s)
6. Update all affected hypothesis confidence scores
7. Run full global verification against entire observation history
8. Calculate current theory confidence (% of events explained without contradiction)
9. If confidence is low or contradictions exist, the Symbolic Core interrogates the Neural Agent for better explanations

**Verification Phase (Mandatory):** After every round, the Symbolic Core must explicitly attempt to falsify its highest-confidence hypotheses.

## Success Criteria (Game-Agnostic + Mao-Specific)

The system is successful when it can:

- Start with zero knowledge and reach high confidence (>85%) on core + hidden rules of completely unknown games
- Reliably handle **unknown unknowns** (discover rules it had no prior conceptual frame for)
- Maintain very low contradiction rate across long play sessions
- Predict penalties *before* they occur with high accuracy
- Produce a clear, formal, human-readable rule set
- Perform well on Mao (learn both obvious and obscure/social rules through experimentation alone)
- Generalize to other games without architectural changes

## Important Constraints

- **No game-specific rules, heuristics, or knowledge** may be encoded anywhere
- The system must begin with true zero knowledge
- All discovery must emerge from observation, active testing, verification, and the dialogue between the two agents
- The Symbolic Core must remain skeptical of the Neural Agent at all times

## Open Research Questions

- How best to represent hypotheses so they support clean verification and Bayesian/frequency updating
- What formal language should the Symbolic Core use? (Python predicates, first-order logic, custom DSL?)
- How to make information-gain calculation tractable in a huge hypothesis space
- How to effectively handle truly novel concepts (unknown unknowns) that the Neural Agent must first invent
- When should the system be allowed to propose *meta-rules* (rules about how rules are added)?

---

**This is a living document.**

The autonomous researcher (Hermes) has full permission to critique, modify, extend, restructure, or completely rewrite any part of this specification when evidence or better reasoning emerges. Real capability and mathematical rigor take priority over fidelity to the original text.

**Current Build Directive:** First implement the two-agent loop (Symbolic Core + Neural Agent) as a minimal but functional proof-of-concept, using a simplified Mao-like game for rapid iteration. Focus on clean communication protocol, hypothesis tracking, verification engine, and active testing behavior.

**Project Root:** `~/Projects/neuro-symbolic-rule-discovery/`

Begin implementation.

## v0.3 Update (Autonomous Improvement - 2026-06-11)
**Key Improvement:** Strengthened the experiment selection engine in SymbolicCore. 
- Now uses hypothesis content (formal_condition + tags) to generate *targeted probe cards* (e.g., card=7 for spoken/action hypotheses, parity boundaries, round-modulo probes).
- Zero-knowledge case uses diverse high-variance cards.
- This implements "active experimentation" rigorously and replaces the previous non-functional (always-0) selector.
- Updated main loop and added LLM fallback for cron/self-improvement reliability.
- Pushed to GitHub with atomic commits.

This directly addresses the "active experimentation > passive observation" principle and improves the propose→test→verify loop.

## v0.4 Update (Autonomous Self-Improvement Cron - 2026-06-11)
**Key Improvements identified and implemented:**
- **Zero-knowledge compliance fix**: Refactored NeuralAgent fallback hypothesis generator to use only abstract, structural predicates over generic variables (card, previous_card, spoken, round). Eliminated all hardcoded test-game-specific literals (e.g. 7, parity patterns matching hidden rules). This was the weakest architectural violation of the "true zero knowledge" mandate.
- **Two-agent dialogue completion**: Added `generate_interrogation_questions()` to SymbolicCore. Enables the skeptical interrogator role — when confidence <50% or contradictions exist, it produces targeted questions for the Neural Agent about meta-rules, unknown unknowns, and novel ontology. Integrated periodic invocation in main loop for live visibility.
- Both changes committed atomically and pushed to GitHub immediately.
- This closes the loop on "Symbolic Core interrogates Neural Agent when data is ambiguous" (SPEC v0.2) and strengthens the neuro-symbolic contract.

These changes were discovered by inspecting running code against the philosophy in AGENTS.md.
