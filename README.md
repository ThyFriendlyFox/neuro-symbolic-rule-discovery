# Neuro-Symbolic Rule Discovery System

A neuro-symbolic AI system for discovering the complete rules of unknown turn-based games through active experimentation, observation, and verification — starting from zero prior knowledge.

## Overview

This project implements a two-agent architecture:

- **Symbolic Core (GOFAI)**: Skeptical, rigorous mathematical agent that maintains formal hypotheses, performs verification, tracks confidence, and selects high-value experiments.
- **Neural Agent (LLM)**: Creative explorer that generates hypotheses, identifies patterns, and proposes experiments.

The system is designed to handle games like **Mao**, where rules are hidden and learned only through penalties and systematic testing. It emphasizes handling "unknown unknowns" and maintaining mathematical rigor.

## Key Features

- Zero-knowledge rule discovery
- Formal hypothesis representation and verification
- Information-gain driven experimentation
- Global consistency checking
- Continuous neuro-symbolic dialogue loop
- Game-agnostic design (tested primarily on Mao)

## Project Structure

```
neuro-symbolic-rule-discovery/
├── agents/           # Neural Agent implementation
├── core/             # Symbolic Core (hypotheses, predicates, verification)
├── games/            # Game environments (e.g., simplified Mao)
├── main.py           # Entry point
├── supervisor.py     # Orchestration and monitoring
├── SPEC.md           # Living technical specification
├── AGENTS.md         # Project philosophy and working style
└── README.md         # This file
```

## Getting Started

```bash
git clone https://github.com/ThyFriendlyFox/neuro-symbolic-rule-discovery.git
cd neuro-symbolic-rule-discovery
python main.py
```

## Status

**Alpha stage** — Active development. The system is being iteratively improved through autonomous research cycles.

Current focus: Robust hypothesis tracking, contradiction detection, and effective handling of novel rule concepts in complex games like Mao.

## Documentation

- [SPEC.md](SPEC.md) — Detailed technical specification and research questions
- [AGENTS.md](AGENTS.md) — Core philosophy, constraints, and operating contract

## License

Research prototype. See individual files for details.

---

*This project is never "done". Continuous autonomous improvement between sessions.*
