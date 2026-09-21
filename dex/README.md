# dex/

V0 scaffold for the Dex orchestrator.

- `main.py` — accepts an objective (as an arg or via stdin), logs it to `../state/objectives.json`, and exits. No delegation, staffing, or model calls yet.
- `ollama_check.py` — standalone reachability test against the local Ollama server (`GET /`). Confirms the server responds; makes no model or generation call.

No framework (CrewAI or otherwise) and no multi-agent logic here yet — that selection waits on `docs/V0_READINESS.md`'s findings, per the plan's discovery-phase rule.
