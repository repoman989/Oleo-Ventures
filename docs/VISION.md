# Vision

The goal is not a large collection of permanently running AI personalities. The goal is a resource-aware organization that assembles the smallest capable team for whatever objective the Founder gives it.

## Principles
- **Local-first** — use owned compute whenever practical.
- **Resource-aware** — CPU, RAM, GPU, VRAM, storage, power, time, and API cost are operating constraints, not afterthoughts.
- **Dynamic staffing** — create logical employees only when an initiative requires them; release them when it's done.
- **Model-efficient** — multiple employees share the same underlying model rather than one model loaded per employee.
- **Auditable** — important work is challenged and verified (Internal Audit) before it reaches the Founder.
- **Expandable** — additional PCs, servers, GPUs, and cloud models can join as company resources later.

## Core architecture principle
The company structure is logical, not physical. Ten employees does not mean ten independently loaded models — a single local model can perform several logically separate roles sequentially, with different instructions, context, tools, and assignments. Concurrency is introduced only where the hardware and expected benefit justify it — which V0_READINESS.md shows is currently narrow: one GPU-resident model, serialized inference.
