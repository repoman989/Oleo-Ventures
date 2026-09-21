# Agent Roles

## Departments
Executive · Research · Engineering · Data & Analytics · Finance · Operations · Creative · Internal Audit

## Persistent roles — not hired per Initiative
- **Dex — Chief of Staff.** Company-wide orchestration and final synthesis.
- **Operations (homelab/security admin).** Continuous monitoring, patching, scheduling.
- **Controller (cross-Venture analytics).** Continuous KPI rollup, read-only.

## Employee ranks and compute strategy
| Rank | Compute approach | Lifecycle |
| --- | --- | --- |
| Intern | Small/fast model, short context | Ephemeral |
| Analyst / Engineer | Primary local model, moderate context | Assignment-based |
| Senior | Best available local model | Used selectively |
| Department Head | Higher reasoning budget, delegates | Created when useful |
| Consultant | External API, explicit cost controls | On demand |

## V0 capacity note
Given ~6GB VRAM (unconfirmed): one GPU-resident model serves all ranks sequentially for now — rank determines prompt/context strategy, not a separate loaded model per rank.
