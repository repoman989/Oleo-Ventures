# state/

Simple persisted project state for V0.

**Format: plain JSON (`objectives.json`), not SQLite.**

Why: V0's own constraints already require state writes to be sequential (see `docs/V0_READINESS.md` §5, `docs/OPERATING_MODEL.md`) — there's no concurrent-writer scenario yet for SQLite's transactional guarantees to buy anything. JSON is human-readable, diffs cleanly in git, and adds zero dependencies. Revisit at V1, when a real worker pool introduces genuine concurrent access to state.

## Audit model independence

Each `objectives.json` entry's `audit_flags` are produced by `llama3.2:3b`, hardcoded in `dex/main.py`'s `AUDIT_MODEL`, deliberately distinct from `model` (currently `mistral:latest`, dynamically resolved), which produces the `scope` the audit is reviewing.

This is not a cost or speed optimization — a smaller model happens to be cheaper, but that's not why it's separate. Per `docs/AGENT_ROLES.md`, Internal Audit exists to challenge and verify work before it reaches the Founder, and a reviewer that is the same weights as the author under review can share the same blind spots and the same fabricated-but-plausible framing that produced the claim in the first place. Having a genuinely different model — different training, different failure modes — review the scope response is a (small, V0-scale) attempt at real independence, not just a second sample from the same source.

**Open finding, not yet resolved:** when the same two test entries were re-audited with `mistral:latest` auditing itself, it caught real unsupported additions on both. Re-run with the independent `llama3.2:3b`, it found nothing on either entry — a false negative in at least the farm-property-poc case, where the unsupported "design documents, meeting minutes" claim is still sitting in `scope` unflagged. Independence bought a genuinely different reviewer, but the smaller, weaker model it introduced appears to be under-flagging relative to the same-model check. This is a real tradeoff to watch, not evidence that independence alone improves audit quality — model capability matters too, and a 3B model may not be capable enough for this to actually work as a check. Worth revisiting once there's more than two test cases.
