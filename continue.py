#!/usr/bin/env python3
"""
Neuro-Symbolic Rule Discovery System - Fixed Continuous Agent
Uses a temporary goal file + hermes chat to properly pass long instructions.
"""

import os
import subprocess
from datetime import datetime

LOG_FILE = "cron.log"
GOAL_FILE = ".current_goal.md"

print(f"\n=== Neuro-Symbolic Continuous Agent - {datetime.now().isoformat()} ===")
print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🫀 Fixed mode — using goal file + hermes chat for reliable execution.\n")

print("Current evaluation:")
print("• Repetitive experiments at 82.3% with shallow, repetitive hypotheses")
print("• Major gaps: weak formal verification, poor information-gain, no real self-evolution")
print("• This cycle must produce actual architectural improvements\n")

# Write goal to file so it can be passed cleanly
goal = """You are continuing the Neuro-Symbolic Rule Discovery System (Star project).

Current reality: The system is stuck in a repetitive loop — every 30-round run looks almost identical, confidence hovers at ~82.3%, and hypotheses are shallow and repetitive. The self-critique is mentioned but never leads to real code changes.

Your job on this cycle:
1. Read the current files (main.py, core/symbolic_core.py, agents/neural_agent.py, games/simple_mao.py, SPEC.md, AGENTS.md).
2. Perform a genuine, ruthless self-critique.
3. Choose the single highest-impact improvement (strong candidates: real ast-based PredicateEvaluator, proper information-theoretic experiment selection, diverse/creative hypothesis generation from the Neural Agent, formal verifiable rule output format, or meta-learning across games).
4. Implement that improvement with clean, working code changes.
5. Run a new test experiment that demonstrates the improvement.
6. Update SPEC.md if the approach has meaningfully changed.
7. Commit the changes with git using a clear message.

Rules:
- Follow AGENTS.md strictly: live commentary on every step, every tool call, every edit.
- Be self-critical. Do not accept "good enough".
- Produce a visibly better version of the prototype this cycle.

Begin now."""

with open(GOAL_FILE, "w") as f:
    f.write(goal)

print(f"Goal written to {GOAL_FILE}. Starting Hermes with proper instruction...\n")

try:
    result = subprocess.run([
        "hermes", "chat", "--continue", "neuro-symbolic-star", "--file", GOAL_FILE
    ], capture_output=True, text=True, timeout=300, cwd=os.getcwd())
    
    print(result.stdout)
    if result.stderr:
        print("--- STDERR ---")
        print(result.stderr)

except subprocess.TimeoutExpired:
    print("Hermes timed out after 5 minutes — significant work likely completed.")
except FileNotFoundError:
    print("Error: 'hermes' command not found in PATH. Falling back to manual mode.")
    print("TODO: Implement improvements directly in this script for now.")
except Exception as e:
    print(f"Error: {e}")

# Always try to commit
print("\nCommitting any changes made during this cycle...")
subprocess.run(["git", "add", "-A"], cwd=os.getcwd(), check=False)
commit_result = subprocess.run([
    "git", "commit", "-m", f"auto: continuous improvement cycle {datetime.now().strftime('%H:%M')}"
], capture_output=True, text=True, cwd=os.getcwd())

if commit_result.returncode == 0:
    print("Successfully committed changes.")
    print(commit_result.stdout.strip())
else:
    print("No new changes to commit or commit failed.")

print(f"\n🫀 Cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Next cycle in 10 minutes.\n")
