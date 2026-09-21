# state/

Simple persisted project state for V0.

**Format: plain JSON (`objectives.json`), not SQLite.**

Why: V0's own constraints already require state writes to be sequential (see `docs/V0_READINESS.md` §5, `docs/OPERATING_MODEL.md`) — there's no concurrent-writer scenario yet for SQLite's transactional guarantees to buy anything. JSON is human-readable, diffs cleanly in git, and adds zero dependencies. Revisit at V1, when a real worker pool introduces genuine concurrent access to state.

## Audit model independence

Each `objectives.json` entry's `audit_flags` are produced by a model hardcoded in `dex/main.py`'s `AUDIT_MODEL` (currently `llama3.1:8b`), deliberately distinct from `SCOPE_MODEL` (`mistral:latest`), which produces the `scope` the audit is reviewing. Both are now pinned constants, not dynamically resolved — see the comment above `SCOPE_MODEL` in `dex/main.py` for why dynamic resolution turned out to be unsafe once more than one extra model was pulled onto this machine.

This is not a cost or speed optimization — a smaller/cheaper model happens to be an easy way to get a distinct model, but that's not why it's separate. Per `docs/AGENT_ROLES.md`, Internal Audit exists to challenge and verify work before it reaches the Founder, and a reviewer that is the same weights as the author under review can share the same blind spots and the same fabricated-but-plausible framing that produced the claim in the first place. Having a genuinely different model — different training, different failure modes — review the scope response is a (small, V0-scale) attempt at real independence, not just a second sample from the same source.

**Open question, not yet resolved: does independence alone improve audit quality, or does it also need comparable capability?** Three audit configurations have now been tried against the same test entries — same-model self-audit (`mistral:latest`), weak-independent (`llama3.2:3b`, 3B), and capable-independent (`llama3.1:8b`, 8B):

| Test entry | Same-model (mistral self-audit) | Weak-independent (llama3.2:3b) | Capable-independent (llama3.1:8b) |
|---|---|---|---|
| Vague "V0 scaffold" objective | Flagged 3 items (fabricated deadline/team context) | "No unsupported additions found" | Flagged 2 items, directly naming the fabricated "investor meeting" and "R&D team" |
| farm-property-poc summary | Flagged 4 items (incl. invented "design documents, meeting minutes") | "No unsupported additions found" | "No unsupported additions found" |
| Control: "list the exact command..." | Flagged 3 items (environment/format/docs padding) | Flagged 4 items (deliverable/constraints/risk/resources padding) | Flagged 4 items (same categories) |

Two things are still unresolved rather than settled by this data:

1. **Weak-independent looks like the outlier, not capable-independent** — on all three entries, `llama3.1:8b` found at least as much as (or more than, in entry 1) the same-model check, while `llama3.2:3b` found nothing on two of three. That's consistent with "the 3B model was too weak to audit effectively," which is what was suspected after the first two-entry run. But it's still only three data points, one model swap, and no ground truth beyond manual read-through — not enough to call this settled.
2. **The control objective did not produce a clean "nothing to flag" result from any auditor**, including the capable one. That's not necessarily a failure of the audit step — `SCOPE_SYSTEM_PROMPT` forces four fixed sections (Deliverable/Constraints/Risk level/Resources needed) regardless of how narrow the objective is, so `mistral:latest` filled Constraints/Risk/Resources with plausible-sounding padding even for a one-line command lookup, and both independent auditors correctly caught that padding as unsupported. This suggests the fixed-section scope prompt itself manufactures things to flag on narrow objectives — a separate, likely more fixable issue than audit-model choice, and one worth addressing before drawing final conclusions about audit quality from this test suite.

Revisit both points once there's a larger, more varied set of test objectives to audit.
