# Machine Discovery

Read-only audit. Plain findings only, no recommendations. Captured 2026-09-20.

## OS

- Microsoft Windows 11 Pro
- Version 10.0.26200 (Build 26200), 64-bit

## CPU

- Intel(R) Core(TM) i9-9980HK CPU @ 2.40GHz
- 8 cores / 16 logical processors
- Max clock speed reported: 2400 MHz (base; boost not reflected here)

## RAM

- 63.76 GB total physical memory
- 2 modules, 32 GB each, 2667 MHz (manufacturer ID reported as `80AD000080AD` — raw SMBIOS code, not a resolved name)

## GPU

- NVIDIA Quadro RTX 3000 — driver 32.0.15.8092
  - WMI reports 4 GB adapter RAM; this is a known WMI/`Win32_VideoController` reporting quirk on cards with >4GB VRAM (32-bit field truncation) — the Quadro RTX 3000 is nominally a 6GB card. Treat the WMI figure as unreliable; confirm via `nvidia-smi` if precise VRAM is needed.
- Intel(R) UHD Graphics 630 — driver 31.0.101.2137, 1 GB (shared) reported

## Storage

- 1 physical disk: SK hynix PC601 NVMe, 512 GB (476.94 GB as reported), Healthy
- 1 logical volume: `C:` — 348.91 GB size, 125.54 GB free, NTFS

## Python

- `python` → 3.13.5
- `python3` → 3.12.10
- Two Python versions present on PATH under different command names.

## Git

- git version 2.37.1.windows.1

## Ollama

- Client version 0.6.5
- Was **not running** at the start of the audit.
- Running `ollama ps` to check loaded models had the side effect of auto-starting the Ollama background server (`ollama app.exe`, `ollama.exe`), since the client auto-launches the server on first command. No models were loaded (empty `ollama ps` table).
- Models directory configured: `C:\Users\nick_\.ollama\models`
- GPU config: `OLLAMA_INTEL_GPU:false`, no CUDA/HIP env vars set — defaults, not evidence of actual GPU usage since no model was loaded to observe it.
- **Note:** the server was left running after this audit (an attempt to stop it back was blocked by the session's permission policy). It can be stopped manually if a truly clean state is wanted.

## Docker

- Docker CLI installed: version 26.1.1, build 4cf5afa
- Docker Desktop plugins present (buildx, compose, scout, etc.)
- Daemon **not running** at time of audit (`docker info` failed to connect to `//./pipe/docker_engine`)

## WSL

- WSL status: default distribution `Ubuntu`, default version 2
- Distros registered:
  - `Ubuntu` — Stopped — WSL2
  - `docker-desktop-data` — Stopped — WSL2
  - `docker-desktop` — Stopped — WSL2
- None running at time of audit.

## Network Adapters

| Adapter | Description | Status | Link Speed |
|---|---|---|---|
| Wi-Fi | Intel(R) Wi-Fi 6 AX200 160MHz | Up | 229 Mbps |
| Ethernet | Intel(R) Ethernet Connection (7) I219-LM | Disconnected | 0 bps |
| Bluetooth Network Connection | Bluetooth PAN | Disconnected | 3 Mbps |
| Tailscale | Tailscale Tunnel | Up | 100 Gbps (virtual, not physical) |
| vEthernet (WSL) | Hyper-V Virtual Ethernet Adapter | Up | 10 Gbps (virtual) |

Machine is currently connected via Wi-Fi only; Ethernet is present but disconnected.
