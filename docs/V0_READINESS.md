# V0 Readiness Assessment

Based entirely on `docs/DISCOVERY.md` (captured 2026-09-20). Where discovery didn't capture the data needed for a claim, that's called out explicitly in §6 rather than guessed.

## 1. What local AI workloads this machine can reasonably support

Hardware: i9-9980HK (8c/16t, mobile Coffee Lake-H), 64GB RAM, NVIDIA Quadro RTX 3000 (nominal 6GB VRAM — see caveat below), 512GB NVMe with 126GB free.

- **Small-to-mid quantized LLMs via Ollama, GPU-accelerated.** A 7B–8B parameter model at 4-bit quantization (Q4_K_M or similar GGUF) typically needs ~4–6GB of VRAM for weights plus KV cache at modest context lengths. That fits inside a 6GB card with limited headroom — this is the realistic sweet spot for this machine.
- **One GPU-resident model at a time.** 6GB doesn't leave room for a second model loaded concurrently alongside a 7-8B model.
- **Larger models (13B+) are borderline-to-unrealistic for GPU acceleration.** They either won't fit or will force Ollama to offload layers to CPU, which works but is materially slower — usable for background/batch tasks, not for anything in an interactive orchestration loop.
- **CPU-only inference is a viable fallback given 64GB RAM**, for cases where GPU residency isn't available or a larger model is needed — but throughput will be far below GPU-accelerated small models, so it changes the class of workload it's suitable for (batch, not interactive).
- **Orchestration and worker processes (Dex, Python workers) are cheap** relative to the above — the 8c/16t CPU and 64GB RAM are not the constraint for that part of the system; the GPU is.

## 2. Bottlenecks

**VRAM is the binding constraint, and it's also the least-confirmed number.**

- Discovery flagged that WMI reported the Quadro RTX 3000 at 4GB, but this is a known `Win32_VideoController` reporting quirk (32-bit field truncation) on cards with >4GB VRAM — the card is nominally 6GB. **This was never confirmed with `nvidia-smi`.** Until it is, treat 6GB as the working assumption, not a verified fact.
- Ollama's `OLLAMA_CONTEXT_LENGTH` default was observed at `2048` — conservative, but note that raising context length directly eats into the same VRAM budget as model weights via KV cache growth. Any decision to raise context length has a real VRAM cost on this hardware.
- `OLLAMA_MAX_LOADED_MODELS:0` and `OLLAMA_NUM_PARALLEL:0` are both "auto" — Ollama will make its own sizing decisions based on available memory it detects. On a 6GB card, auto-detected parallelism is likely to be low; this needs to be observed empirically, not assumed.
- Storage (126GB free) is adequate but not abundant for a model library — useful 7-8B GGUF quantized models commonly run several GB each, so the free space supports maybe a dozen or so before requiring pruning. Not an immediate bottleneck, but worth tracking as models accumulate.
- CPU and RAM are not bottlenecks for the workloads described in §1 — they're the slack resources in this system, not the constraint.

## 3. Recommended division of responsibilities (single machine: Dex + Ollama + Python workers, concurrent)

- **GPU / VRAM (~6GB nominal, unconfirmed):** reserved exclusively for the single active Ollama-loaded model. Nothing else on this machine should compete for GPU memory — no second local model, no GPU-based embeddings running alongside it. Model load/unload should be treated as an exclusive operation.
- **CPU (8c/16t):** leave headroom for Ollama's own CPU-side work (tokenization, sampling, any CPU-offloaded layers) — figure roughly 1-2 cores of slack for that. The remaining 6-7 cores / 12-14 threads are available for Dex's orchestration loop and the Python worker pool. Dex itself should be lightweight (I/O and control flow, not compute), so most of that budget goes to workers.
- **RAM (64GB):** generous relative to everything else here. Budget a modest reserve (roughly 8-16GB) for Ollama's model weights/KV cache/OS overhead, and treat the remainder as available to Python workers, Dex, and the OS. RAM is not expected to be the limiting factor at V0 scale.
- **Storage (126GB free):** budget space for the Ollama model library, plus Dex's own state/logs/repo checkouts. Not unlimited — should be monitored as models and state data accumulate, but not a V0 blocker.

## 4. Concurrent local workers — estimate

This needs to be split into two categories, because they hit different constraints:

- **Workers that call the local LLM (Ollama):** given the VRAM ceiling and that only one model can realistically be GPU-resident, concurrent *generation* requests against that model should be assumed low — on the order of **1-2 concurrent inference calls** before KV-cache VRAM pressure and latency degradation become a risk. This is a reasoned estimate from the hardware numbers, not a measured one — discovery captured no model actually loaded or exercised, so there's no real throughput or VRAM-under-load data yet (see §6).
- **Workers doing non-LLM work** (file I/O, git operations, data parsing, log writes): the 8c/16t CPU and 64GB RAM comfortably support more concurrency here — a working estimate is **4-6 concurrent lightweight Python worker processes** without contention, though this too is untested.
- **Recommendation for V0:** gate all Ollama-bound calls through a single queue/semaphore (effectively serializing inference), and allow a small pool of non-LLM workers to run in parallel. Treat both numbers above as starting points to validate empirically once a model is actually pulled and load-tested, not as final limits.

## 5. Sequential vs. parallelizable

**Strictly sequential:**
- All calls to the local Ollama model for generation — serialize through one queue/gate given the single-GPU, ~6GB VRAM constraint, to avoid VRAM contention or OOM.
- Model load/unload/swap operations in Ollama — must not overlap with an in-flight inference call.
- Writes to shared state (the planned `state/` store) — needs sequential access or proper locking regardless of whether it ends up as JSON or SQLite, to avoid corruption or lost updates.

**Safe to parallelize:**
- Non-LLM Python worker tasks: file I/O, git operations, parsing, local data fetching, report/log generation.
- Read-only access to persisted state.
- Any calls to external (non-local, non-GPU-bound) network APIs, if those get introduced later — they don't compete with this machine's GPU/CPU budget the way local inference does.

## 6. What's still unknown — needed before writing any Dex code

- **Actual usable VRAM is unconfirmed.** The only number on record (WMI's 4GB) is flagged in DISCOVERY.md as unreliable. Nothing in discovery ran `nvidia-smi`. This is the single most important number to confirm before committing to a model-size strategy.
- **No model has ever been pulled or run on this machine.** There's no data on real load time, real VRAM footprint under inference, or tokens/sec for any candidate model size (7B vs 8B vs 13B) — everything in §1-§4 about model sizing is inference from published model-size norms applied to the hardware specs, not a measurement taken on this machine.
- **Ollama's actual GPU engagement is unconfirmed.** Discovery only observed that the Ollama server starts and lists an empty model table; it never observed Ollama actually dispatching work to the Quadro RTX 3000 vs. falling back to CPU or the Intel iGPU. `OLLAMA_INTEL_GPU` was `false` at time of capture, but that alone doesn't confirm CUDA/GPU-layer usage is working.
- **No concurrency or load testing has been done.** The worker-count estimates in §4 are reasoned from CPU/RAM/VRAM specs, not measured — the real answer requires loading a model and hitting it with concurrent requests while watching VRAM and latency.
- **No baseline for an actual Dex/worker process footprint**, since no Dex code exists yet — CPU/RAM cost per worker is unknown until the V0 scaffold runs.
- **Storage growth rate is unknown** — how many models and how much state/log data accumulate over time in real use hasn't been observed.
- **Docker and WSL were both present but stopped at capture time.** If either gets started during real Dex operation, they'll compete for CPU/RAM that this assessment currently treats as available; discovery didn't test that scenario.

**Bottom line:** the hardware supports a V0 built around one small-to-mid (7-8B, 4-bit) GPU-resident model with serialized inference calls and a modest pool of parallel non-LLM workers — but the VRAM number underneath that whole plan is unverified, and nothing about real model behavior on this machine has been measured yet. Confirming VRAM via `nvidia-smi` and running one real model through Ollama are the two highest-value next steps before locking in sizing decisions.
