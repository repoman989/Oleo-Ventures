"""Dex orchestrator entrypoint — V0 scaffold. Logs an objective, scopes it, and
audits the scope, each a single sequential Ollama call. No Department/Staffing
logic yet. The audit step is the first seed of the Internal Audit role from
docs/AGENT_ROLES.md, not the full thing."""

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
LOG_FILE = STATE_DIR / "objectives.json"
OLLAMA_BASE = "http://127.0.0.1:11434"

# Audit model is fixed, not dynamically resolved like the scoping model — Internal
# Audit must be a distinct model from whatever produced the work it reviews. See
# state/README.md for why this is a real independence requirement, not just cost.
AUDIT_MODEL = "llama3.2:3b"

SCOPE_SYSTEM_PROMPT = (
    "You are Dex, Chief of Staff at Oleo Ventures. Given an objective from the "
    "Founder, respond concisely (under 150 words) with four labeled sections: "
    "Deliverable, Constraints, Risk level (Low/Medium/High plus why), and "
    "Information/resources needed. Scoping only — do not delegate or assign work."
)

AUDIT_SYSTEM_PROMPT = (
    "You are Dex's Internal Audit function at Oleo Ventures. You will be given "
    "an ORIGINAL OBJECTIVE and a SCOPE RESPONSE derived from it. List only the "
    "claims, resources, or details in the SCOPE RESPONSE that are NOT directly "
    "stated or clearly implied by the OBJECTIVE — i.e. unsupported additions. "
    "Be concise. If there are none, say exactly: 'No unsupported additions found.'"
)


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def save_log(log):
    STATE_DIR.mkdir(exist_ok=True)
    LOG_FILE.write_text(json.dumps(log, indent=2))


def append_log(entry):
    log = load_log()
    log.append(entry)
    save_log(log)


def default_model():
    with urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=5) as resp:
        data = json.loads(resp.read().decode())
    models = data.get("models", [])
    if not models:
        raise RuntimeError("no Ollama models pulled — run `ollama pull <model>` first")
    return models[0]["name"]


def ollama_generate(system, prompt, model):
    payload = json.dumps(
        {
            "model": model,
            "system": system,
            "prompt": prompt,
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


def scope_objective(objective, model):
    return ollama_generate(SCOPE_SYSTEM_PROMPT, objective, model)


def audit_scope(objective, scope):
    prompt = f"ORIGINAL OBJECTIVE:\n{objective}\n\nSCOPE RESPONSE:\n{scope}"
    return ollama_generate(AUDIT_SYSTEM_PROMPT, prompt, AUDIT_MODEL)


def backfill_audit():
    log = load_log()
    changed = False
    for entry in log:
        if "scope" not in entry:
            continue
        flags = audit_scope(entry["objective"], entry["scope"])
        entry["audit_flags"] = flags
        entry["audit_model"] = AUDIT_MODEL
        changed = True
        print(f"Backfilled audit_flags for: {entry['objective']}")
        print(flags)
        print()
    if changed:
        save_log(log)
    else:
        print("Nothing to backfill — no entries have a scope yet.")


def main():
    parser = argparse.ArgumentParser(description="Dex — accept an objective, scope it, audit the scope, log it, exit.")
    parser.add_argument("objective", nargs="?", help="The objective to log. Reads from stdin if omitted.")
    parser.add_argument(
        "--backfill-audit",
        action="store_true",
        help="Re-run audit_flags for every entry that has a scope, using the current audit model, overwriting any existing audit_flags.",
    )
    args = parser.parse_args()

    if args.backfill_audit:
        backfill_audit()
        return

    objective = args.objective or sys.stdin.read().strip()
    if not objective:
        parser.error("no objective provided (arg or stdin)")

    try:
        model = default_model()
        scope = scope_objective(objective, model)
        audit_flags = audit_scope(objective, scope)
    except Exception as exc:
        print(f"Scope/audit call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    entry = {
        "objective": objective,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "scope": scope,
        "audit_flags": audit_flags,
        "audit_model": AUDIT_MODEL,
    }
    append_log(entry)
    print(f"Logged objective: {objective}")
    print()
    print(f"Scope (model: {model}):")
    print(scope)
    print()
    print(f"Audit flags (model: {AUDIT_MODEL}):")
    print(audit_flags)


if __name__ == "__main__":
    main()
