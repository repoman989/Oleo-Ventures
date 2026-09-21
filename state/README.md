# state/

Simple persisted project state for V0.

**Format: plain JSON (`objectives.json`), not SQLite.**

Why: V0's own constraints already require state writes to be sequential (see `docs/V0_READINESS.md` §5, `docs/OPERATING_MODEL.md`) — there's no concurrent-writer scenario yet for SQLite's transactional guarantees to buy anything. JSON is human-readable, diffs cleanly in git, and adds zero dependencies. Revisit at V1, when a real worker pool introduces genuine concurrent access to state.
