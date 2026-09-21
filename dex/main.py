"""Dex orchestrator entrypoint — V0 scaffold. Logs an objective and scopes it
with a single sequential Ollama call. No Department/Staffing logic yet."""

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
LOG_FILE = STATE_DIR / "objectives.json"
OLLAMA_BASE = "http://127.0.0.1:11434"

SCOPE_SYSTEM_PROMPT = (
    "You are Dex, Chief of Staff at Oleo Ventures. Given an objective from the "
    "Founder, respond concisely (under 150 words) with four labeled sections: "
    "Deliverable, Constraints, Risk level (Low/Medium/High plus why), and "
    "Information/resources needed. Scoping only — do not delegate or assign work."
)


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def append_log(entry):
    STATE_DIR.mkdir(exist_ok=True)
    log = load_log()
    log.append(entry)
    LOG_FILE.write_text(json.dumps(log, indent=2))


def default_model():
    with urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=5) as resp:
        data = json.loads(resp.read().decode())
    models = data.get("models", [])
    if not models:
        raise RuntimeError("no Ollama models pulled — run `ollama pull <model>` first")
    return models[0]["name"]


def scope_objective(objective, model):
    payload = json.dumps(
        {
            "model": model,
            "system": SCOPE_SYSTEM_PROMPT,
            "prompt": objective,
            "stream": False,
        }
    ).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode())
    return result["response"].strip()


def main():
    parser = argparse.ArgumentParser(description="Dex — accept an objective, scope it, log it, exit.")
    parser.add_argument("objective", nargs="?", help="The objective to log. Reads from stdin if omitted.")
    args = parser.parse_args()

    objective = args.objective or sys.stdin.read().strip()
    if not objective:
        parser.error("no objective provided (arg or stdin)")

    try:
        model = default_model()
        scope = scope_objective(objective, model)
    except Exception as exc:
        print(f"Scope call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    entry = {
        "objective": objective,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "scope": scope,
    }
    append_log(entry)
    print(f"Logged objective: {objective}")
    print()
    print(f"Scope (model: {model}):")
    print(scope)


if __name__ == "__main__":
    main()
