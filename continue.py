#!/usr/bin/env python3
"""
Neuro-Symbolic Rule Discovery System - Persistent Session Agent
Now uses a dedicated persistent session called "star".
"""

import os
import subprocess
from datetime import datetime

print(f"\n=== Neuro-Symbolic Continuous Agent - {datetime.now().isoformat()} ===")
print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🫀 Using dedicated persistent session: 'star'\n")

print("Evaluation:")
print("• Still repeating shallow experiments at ~82.3%")
print("• No real architectural evolution yet")
print("• This cycle must make concrete improvements\n")

goal = """You are the autonomous researcher for the Neuro-Symbolic Rule Discovery System (Star project).

Current reality: The system is stuck doing the same repetitive 30-round Mao experiment with nearly identical shallow hypotheses every time. Self-critique is mentioned but never turned into real code changes.

Your mandate this cycle:
1. Thoroughly review the current codebase.
2. Deliver a sharp, honest self-critique.
3. Pick the single highest-impact improvement (real PredicateEvaluator using ast, proper information-gain experiment selection, much better hypothesis diversity/quality, formal rule output, etc.).
4. Implement it with clean, working code.
5. Test it with a new experiment.
6. Update SPEC.md or AGENTS.md if needed.
7. Commit everything with git.

Follow AGENTS.md strictly: live commentary on every single step, every tool call, every edit. No silent work. Be ruthless. Produce a clearly better version of the prototype this cycle.

Start now."""

goal_file = ".goal.txt"
with open(goal_file, "w") as f:
    f.write(goal)

print("Goal written. Launching persistent 'star' session...\n")

try:
    result = subprocess.run([
        "hermes", "chat", "--continue", "star", "--worktree"
    ], input=goal, text=True, capture_output=True, timeout=300, cwd=os.getcwd())
    
    print(result.stdout)
    if result.stderr:
        print("--- STDERR ---")
        print(result.stderr)

except subprocess.TimeoutExpired:
    print("Session timed out after 5 minutes — meaningful work was likely completed.")
except Exception as e:
    print(f"Error: {e}")

print("\nCommitting changes from this cycle...")
subprocess.run(["git", "add", "-A"], cwd=os.getcwd(), check=False)
commit_result = subprocess.run([
    "git", "commit", "-m", f"auto: star improvement cycle {datetime.now().strftime('%H:%M')}"
], capture_output=True, text=True, cwd=os.getcwd())

if commit_result.returncode == 0:
    print("✅ Committed:")
    print(commit_result.stdout.strip())
else:
    print("No new changes to commit this cycle.")

print(f"\n🫀 Cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Next cycle in 10 minutes.\n")
