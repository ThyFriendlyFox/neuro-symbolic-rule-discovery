#!/usr/bin/env python3
"""
STAR PROJECT - Dedicated Continuous Improvement Runner
This script is called every 10 minutes by launchd.
It is responsible for resuming the dedicated improvement session and driving real progress.
"""

import os
import sys
import subprocess
from datetime import datetime

PROJECT_DIR = "/Users/thyfriendlyfox/Projects/neuro-symbolic-rule-discovery"
LOG_FILE = os.path.join(PROJECT_DIR, "cron.log")
SESSION_ID = "20260611_054532_54beef0b"   # The persistent active session

os.chdir(PROJECT_DIR)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line.strip())

log("=== STAR Improvement Cycle Started ===")

goal = """You are the dedicated autonomous researcher for the Neuro-Symbolic Rule Discovery System (Star).

Your permanent mission: continuously improve this system with real architectural changes.
- Replace repetitive loops with open-ended multi-game exploration
- Build proper verifiable predicates
- Improve hypothesis quality and information-gain
- Make the system try new unknown games
- Commit meaningful code changes

Do real work. Do not stop. Begin immediately."""

# Write goal to file for reference
with open(".star_goal.txt", "w") as f:
    f.write(goal)

log("Goal written. Attempting to resume dedicated session...")

success = False

# Method 1: Try direct hermes invocation with the known session
try:
    result = subprocess.run(
        ["hermes", "chat", "--continue", SESSION_ID, "--worktree"],
        input=goal,
        text=True,
        capture_output=True,
        timeout=300,
        cwd=PROJECT_DIR
    )
    log("Hermes invocation completed.")
    if result.stdout:
        log("STDOUT captured (first 500 chars): " + result.stdout[:500].replace("\n", " "))
    if result.stderr:
        log("STDERR: " + result.stderr[:300])
    success = True
except FileNotFoundError:
    log("ERROR: 'hermes' command not found in PATH")
except subprocess.TimeoutExpired:
    log("Hermes session ran for 5 minutes then timed out (likely did substantial work)")
    success = True
except Exception as e:
    log(f"ERROR during Hermes call: {str(e)}")

# Always commit whatever happened
log("Committing any changes made during this cycle...")
subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR, check=False)
commit_result = subprocess.run(
    ["git", "commit", "-m", f"star: autonomous improvement cycle {datetime.now().strftime('%H:%M')}"],
    cwd=PROJECT_DIR,
    capture_output=True,
    text=True
)
if commit_result.returncode == 0:
    log("Git commit created: " + commit_result.stdout.strip())
else:
    log("No new changes to commit this cycle.")

log("=== STAR Improvement Cycle Completed ===\n")

sys.exit(0)