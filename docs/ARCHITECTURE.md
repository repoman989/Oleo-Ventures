# Architecture

## Open item: hardware reconciliation — deferred, not blocking
Project memory shows Precision 7740 #1/#2 as a candidate future K3s cluster; the farmweather/home-lab session recap shows four Latitude 7490s (Hermes/Aegis/Harvest-named) as dormant/unknown state. This only matters at V2 (Distributed Oleo) — V0 is single-machine and doesn't depend on resolving it.

## V0 state — confirmed
Primary Windows 11 Pro laptop: i9-9980HK (8c/16t), 64GB RAM, Quadro RTX 3000 (~6GB VRAM, unconfirmed via nvidia-smi), 512GB NVMe (126GB free). See docs/V0_READINESS.md for the full sizing assessment.

## Infrastructure evolution
- **V0 — Single-machine prototype:** primary Windows machine, Dex, Ollama, Python workers, simple persisted project state.
- **V1 — Local worker pool:** job queue, structured assignments, worker lifecycle, Internal Audit, resource accounting, controlled concurrency.
- **V2 — Distributed Oleo:** approved networked workstations/servers join as worker nodes.
- **V3 — Hybrid company:** cloud consultants, external tools, energy-aware scheduling, cost-based routing.

## Governance and safety
| Mechanism | What it does |
| --- | --- |
| GitOps-only writes | Every change is a commit/PR; a GitOps controller has real write access; Nick merges |
| Ticket-driven intake | A feature/business idea becomes a ticket first, never a direct trigger to an employee |
| Escalation matrix | Money always escalates. Routine code = normal PR gate. Net-new Venture ideas escalate before effort is spent |
| Centralized logging | Every employee writes structured findings into one store |
| Resource read/write split | Reading is open to any employee; writing routes through Internal Audit, then Executive Approval |

## Known deferred overlaps
farm-property-poc (nested, no remote) shares domain territory with farmweather/field_fusion/ghcn-weather-pipeline. Acknowledged, not yet assigned to Research/Internal Audit — revisit before either project scales further.
