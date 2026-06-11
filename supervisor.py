#!/usr/bin/env python3
"""
Star Meta-Supervisor
Runs every 10 minutes. Manages multiple active projects by resuming their Hermes sessions
with fresh context from recent logs + project specs.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

PROJECTS_FILE = Path(__file__).parent / "active_projects.json"
LOG_FILE = Path(__file__).parent / "supervisor.log"
HERMES = "hermes"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_projects():
    if not PROJECTS_FILE.exists():
        # Default starter project
        default = {
            "projects": [
                {
                    "name": "star",
                    "path": str(Path(__file__).parent),
                    "session_id": "20260611_054532_54beef0b",
                    "spec_file": "SPEC.md",
                    "agents_file": "AGENTS.md"
                }
            ]
        }
        PROJECTS_FILE.write_text(json.dumps(default, indent=2))
        return default
    return json.loads(PROJECTS_FILE.read_text())


def get_recent_logs(session_id: str, max_chars: int = 4000) -> str:
    """Try to get recent output from the session using hermes sessions export if available."""
    try:
        result = subprocess.run(
            [HERMES, "sessions", "export", session_id],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            logs = result.stdout[-max_chars:]
            return logs
    except Exception:
        pass
    return "[Could not retrieve recent session logs]"


def build_prompt(project: dict) -> str:
    name = project["name"]
    path = project["path"]
    spec = Path(path) / project.get("spec_file", "SPEC.md")
    agents = Path(path) / project.get("agents_file", "AGENTS.md")

    spec_text = spec.read_text()[:2000] if spec.exists() else "No SPEC.md found."
    agents_text = agents.read_text()[:1500] if agents.exists() else "No AGENTS.md found."

    logs = get_recent_logs(project["session_id"])

    prompt = f"""You are continuing work on the project "{name}".

Project directory: {path}

=== SPEC.md (excerpt) ===
{spec_text}

=== AGENTS.md (excerpt) ===
{agents_text}

=== Recent session activity ===
{logs}

Please continue improving this project according to its SPEC.md and AGENTS.md.
Focus on making real architectural and code progress. Do not ask for permission.
Begin working now.
"""
    return prompt


def run_supervisor():
    log("=== Meta-Supervisor cycle started ===")
    data = load_projects()

    for proj in data.get("projects", []):
        name = proj["name"]
        session_id = proj["session_id"]
        log(f"Processing project: {name} (session {session_id})")

        prompt = build_prompt(proj)

        try:
            result = subprocess.run(
                [HERMES, "chat", "--continue", session_id, "--worktree"],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=300
            )
            log(f"  Hermes finished for {name}. Return code: {result.returncode}")
            if result.stdout:
                log(f"  Output (truncated): {result.stdout[:600].replace(chr(10), ' ')}")
        except Exception as e:
            log(f"  ERROR running Hermes for {name}: {e}")

        # Commit whatever happened
        try:
            os.chdir(proj["path"])
            subprocess.run(["git", "add", "-A"], check=False)
            subprocess.run(
                ["git", "commit", "-m", f"auto: supervisor cycle {datetime.now().strftime('%H:%M')} - {name}"],
                check=False,
                capture_output=True
            )
        except Exception:
            pass

    log("=== Meta-Supervisor cycle completed ===\n")


if __name__ == "__main__":
    run_supervisor()