"""Dex orchestrator entrypoint — V0 scaffold, no delegation logic yet."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
LOG_FILE = STATE_DIR / "objectives.json"


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def append_log(entry):
    STATE_DIR.mkdir(exist_ok=True)
    log = load_log()
    log.append(entry)
    LOG_FILE.write_text(json.dumps(log, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Dex — accept an objective, log it, exit.")
    parser.add_argument("objective", nargs="?", help="The objective to log. Reads from stdin if omitted.")
    args = parser.parse_args()

    objective = args.objective or sys.stdin.read().strip()
    if not objective:
        parser.error("no objective provided (arg or stdin)")

    entry = {
        "objective": objective,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }
    append_log(entry)
    print(f"Logged objective: {objective}")


if __name__ == "__main__":
    main()
