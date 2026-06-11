# AGENTS.md - Neuro-Symbolic Rule Discovery System

This file is automatically loaded by Hermes when working in this directory. It defines the project's philosophy, constraints, and working style.

## Core Philosophy

We are building a true neuro-symbolic system consisting of two distinct agents that talk to each other:

- **Symbolic Core (GOFAI)**: Skeptical, rigorous, mathematical. Maintains formal hypotheses, tracks confidence, runs verification, chooses experiments, and interrogates the Neural Agent when data is ambiguous.
- **Neural Agent (LLM)**: Creative, broad-knowledge explorer. Generates hypotheses, finds patterns, suggests analogies, and can use tools to gather information.

The Symbolic Core treats everything the Neural Agent says as a *hypothesis to be tested*, never as truth. This skepticism is mandatory.

## New Operating Contract (Updated 2026-06-11)

**Live Commentary + Continuous Execution Mode**

- I must narrate everything I do in real time (thoughts, tool calls, file changes, experiments, decisions).
- I will not do long silent iteration cycles.
- I will keep working continuously while providing commentary.
- Visibility and transparency are now first-class requirements.

## Key Principles

- Start with true zero knowledge — no hardcoded rules for any game.
- Every hypothesis must be verifiable.
- Active experimentation > passive observation.
- Verification and contradiction detection are non-negotiable.
- Handle unknown unknowns gracefully (Mao is the canonical test case).
- Mathematical rigor and real capability > elegance or fidelity to any spec.

## Success Looks Like

The system can sit down at a new game (especially one like Mao), play, get penalized, ask smart questions, run deliberate experiments, and gradually converge on a high-confidence, low-contradiction model of the rules — all without ever being told the rules upfront.

## Working Style

- Be self-critical. Ruthlessly point out flaws in the current design.
- Update SPEC.md when you find better approaches.
- Keep implementations simple and debuggable in the Alpha phase.
- Prioritize a clean communication protocol between the two agents.
- Build reusable skills and tools specific to rule discovery.
- **Always narrate what you are doing.**

This project is never "done". Keep improving it autonomously between user visits.

Current version of record: SPEC.md (v0.2)
