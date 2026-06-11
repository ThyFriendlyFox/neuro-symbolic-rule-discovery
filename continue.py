#!/usr/bin/env python3
"""
FINAL VERSION - Dedicated Star Improvement Agent
Uses the current active session instead of trying to create 'star'.
"""

import os
import subprocess
from datetime import datetime

print(f"\n=== [STAR] Dedicated Improvement Session - {datetime.now().isoformat()} ===")
print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

goal = """You are now the dedicated autonomous researcher for the Neuro-Symbolic Rule Discovery System called Star.

Your permanent directive is to continuously improve this system until it is a robust, game-agnostic neuro-symbolic rule discovery engine.

Current flaws:
- Fixed 30-round loop on the same Mao game
- Repetitive shallow hypotheses
- No real self-critique that leads to code changes
- No exploration of new games
- Weak verification and experiment selection

You must:
1. Review the current code thoroughly.
2. Perform real self-critique.
3. Make concrete architectural improvements (replace the fixed loop with open-ended play across procedurally generated games, implement real predicate evaluation engine, add proper information-gain, improve hypothesis creativity, add generalization, etc.).
4. Test the changes.
5. Commit the improvements with git.

Do this every time this session is resumed. Never ask for permission. Never stop improving. Provide full live commentary.

Begin immediately with a major improvement."""

print("Launching improvement cycle in current active session...\n")

try:
    result = subprocess.run([
        "hermes", "chat", "--continue", "20260611_054532_54beef0b", "--worktree"
    ], input=goal, text=True, capture_output=True, timeout=420, cwd=os.getcwd())
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
except Exception as e:
    print("Error running hermes:", str(e))

print("\nCommitting any improvements made...")
subprocess.run(["git", "add", "-A"], cwd=os.getcwd(), check=False)
subprocess.run([
    "git", "commit", "-m", f"star: autonomous improvement cycle {datetime.now().strftime('%H:%M')}"
], cwd=os.getcwd(), check=False)

print(f"\nCycle completed at {datetime.now().strftime('%H:%M:%S')}. Continuing improvement indefinitely.")
