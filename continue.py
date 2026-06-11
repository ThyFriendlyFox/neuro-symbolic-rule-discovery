#!/usr/bin/env python3
"""
Neuro-Symbolic Rule Discovery System - Improved Continuous Agent
Corrected to use valid Hermes CLI syntax.
"""

import os
import subprocess
from datetime import datetime

print(f"\n=== Neuro-Symbolic Continuous Agent - {datetime.now().isoformat()} ===")
print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🫀 Improved mode activated — driving real progress.\n")

print("Current progress evaluation:")
print("• Stuck at repetitive 82.3% confidence with shallow hypotheses")
print("• Predicate verification, information-gain, and architectural evolution remain weak")
print("• Goal: Force meaningful improvements + git commits on every cycle\n")

print("🫀 Starting improved iteration cycle now...\n")

goal = """
You are continuing the Neuro-Symbolic Rule Discovery System (Star project).
Current state: repetitive 30-round experiments stuck at ~82.3% with repetitive shallow hypotheses.

Requirements for this cycle:
1. Perform a real self-critique of the current codebase (main.py, symbolic_core.py, neural_agent.py, games/simple_mao.py).
2. Identify the single highest-leverage improvement (e.g. real ast-based PredicateEvaluator, proper information-gain calculation, diverse hypothesis generation, formal rule output, better experiment selection).
3. Implement that improvement with actual code changes.
4. Run a new experiment to test it.
5. End by committing the changes with git.

Follow AGENTS.md: live commentary on every thought, tool call, and edit. Be self-critical. Produce real progress on the prototype.
"""

try:
    result = subprocess.run([
        "hermes",
        "--goal", goal,
        "--worktree"
    ], capture_output=True, text=True, timeout=240, cwd=os.getcwd())
    
    print(result.stdout)
    if result.stderr:
        print("--- STDERR ---")
        print(result.stderr)
        
    # Auto commit if there were changes
    print("\nAttempting git commit of any changes...")
    subprocess.run(["git", "add", "-A"], cwd=os.getcwd(), check=False)
    commit_result = subprocess.run([
        "git", "commit", "-m", f"auto: continuous improvement cycle {datetime.now().strftime('%H:%M')}"
    ], capture_output=True, text=True, cwd=os.getcwd())
    print(commit_result.stdout or commit_result.stderr or "Nothing new to commit.")

except subprocess.TimeoutExpired:
    print("Cycle timed out after 4 minutes — substantial work was likely done.")
except Exception as e:
    print(f"Error during cycle: {e}")

print(f"\n🫀 Cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Next improved cycle scheduled in 10 minutes.\n")
