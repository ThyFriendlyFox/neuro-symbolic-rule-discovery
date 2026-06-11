#!/usr/bin/env python3
"""
Dedicated Persistent Session Runner for Star Project
This script is called by launchd every 10 minutes.
It resumes the dedicated 'star' session with a strong improvement goal.
"""

import os
import subprocess
from datetime import datetime

print(f"\n=== [STAR] Neuro-Symbolic Continuous Improvement - {datetime.now().isoformat()} ===")
print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🫀 Dedicated 'star' session activated. Improving the prototype.\n")

goal = """You are the dedicated autonomous researcher for the Neuro-Symbolic Rule Discovery System (Star).

Your only purpose is to continuously improve this system. Do not stop. Do not ask for permission.

Current problems:
- The system is stuck in a repetitive 30-round Mao loop with shallow, repetitive hypotheses.
- It is not trying new games.
- It is not doing real self-critique that leads to architectural changes.
- Verification is weak. Information-gain is rudimentary. Hypothesis generation is not creative.

Instructions for every cycle:
1. Review the current codebase (main.py, symbolic_core.py, neural_agent.py, simple_mao.py, SPEC.md, AGENTS.md).
2. Write a sharp self-critique.
3. Make at least one significant architectural improvement (e.g. replace fixed 30-round loop with open-ended play across multiple generated games, implement real PredicateEvaluator with ast, add proper information-gain driven experiment selection, make NeuralAgent generate truly diverse and novel hypotheses, add generalization across games, etc.).
4. Test the improvement thoroughly.
5. Update documentation if needed.
6. Commit all changes with a clear git commit message.

Follow AGENTS.md strictly: live commentary on every single thought, tool call, file edit, and decision. Never do silent work. Be extremely self-critical and ambitious.

This session must drive continuous, visible progress on the Star prototype. Do not stop improving.

Begin now."""

with open(".star_goal.txt", "w") as f:
    f.write(goal)

print("Goal prepared. Resuming dedicated 'star' session with improvement mandate...\n")

try:
    result = subprocess.run([
        "hermes", "chat", "--continue", "star", "--worktree"
    ], input=goal, text=True, capture_output=True, timeout=360, cwd=os.getcwd())
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except subprocess.TimeoutExpired:
    print("Long-running improvement cycle completed (timeout).")
except Exception as e:
    print("Error:", str(e))

print("\nCommitting progress...")
subprocess.run(["git", "add", "-A"], cwd=os.getcwd(), check=False)
subprocess.run([
    "git", "commit", "-m", f"auto: star improvement cycle {datetime.now().strftime('%Y-%m-%d %H:%M')}"
], cwd=os.getcwd(), check=False)

print(f"\n🫀 Star session cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Continuing improvement in 10 minutes. Not stopping.\n")
