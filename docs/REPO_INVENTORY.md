# Repository Inventory

Inventory only — nothing moved, renamed, or modified. Scanned the full user profile (`C:\Users\nick_`) for `.git` directories; the machine has a single physical disk / logical volume (`C:`), so this covers the whole machine. Captured 2026-09-20.

## `cropcast`

- **Path:** `C:\Users\nick_\cropcast`
- **Remote:** `git@github.com:repoman989/cropcast.git`
- **Branch:** `master`
- **Last commit:** 2026-09-16 — `fd18af8` — "Add developer onboarding docs: environments.md and CONTRIBUTING.md"
- **README (first paragraph):** CropCast is a mobile app for growers, built as a companion to the [farmweather](https://github.com/repoman989/farmweather) backend. It surfaces field-level weather, forecast, and crop-risk data from the farmweather platform in a mobile-first experience. This repo is separate from farmweather's codebase and git history. The app will be built with Expo / React Native.

## `doge-assessment`

- **Path:** `C:\Users\nick_\doge-assessment`
- **Remote:** `https://github.com/MARecruiting/NicholasD.git`
- **Branch:** `main`
- **Last commit:** 2026-03-10 — `4939c9e` — "Remove data_README.md"
- **README (first paragraph):** DOGE/USDS Data Engineering Take-Home Assessment — a comparison of old and new healthcare claims processing systems using CMS DE-SynPUF synthetic data.

## `farm-property-poc`

- **Path:** `C:\Users\nick_\farm-property-poc\farm-property-poc` (note: nested one level — the outer `farm-property-poc` folder is not itself a repo)
- **Remote:** none configured
- **Branch:** `master`
- **Last commit:** 2026-09-19 — `a08d674` — "feat: add bottom camera toolbar (rotate/tilt arrows + hand pan tool)"
- **README (first paragraph):** Farm Property AI Sandbox — Proof of Concept. A local, offline-capable 3D viewer for a single real farm property, built from real satellite imagery and elevation data. Proof of concept only.

## `farmweather`

- **Path:** `C:\Users\nick_\farmweather`
- **Remote:** `git@github.com:repoman989/farmweather.git`
- **Branch:** `master`
- **Last commit:** 2026-09-16 — `53d6f32` — "Add v2.8 design doc (rate limiting, GDD historical average, demo account)"
- **README (first paragraph):** Farm Weather, Crop Suitability & Yield Potential — DuckDB (transformation) + PostgreSQL/PostGIS (storage) + FastAPI (serving), built against the v2.0 project design document.

## `field_fusion` (FieldFusion)

- **Path:** `C:\Users\nick_\field_fusion`
- **Remote:** `git@github-fieldfusion:repoman989/FieldFusion.git` (uses a host-alias SSH remote, `github-fieldfusion`, distinct from the other repos' `github.com`)
- **Branch:** `main`
- **Last commit:** 2026-09-20 — `f2c0f19` — "Remove stale orphaned-table note from data dictionary"
- **README:** none present at repo root. Top-level contents: `docs/`, `local_scripts/`, `pipeline/`.

## `GeoLocator/my-locations-app`

- **Path:** `C:\Users\nick_\GeoLocator\my-locations-app`
- **Remote:** none configured (checked `.git/config` directly)
- **Branch:** `master` (read from `.git/HEAD`)
- **Last commit:** unavailable — git refused to read history because it flags this directory as "dubious ownership" (`detected dubious ownership in repository`). Resolving that requires either a `git config --global --add safe.directory` entry or the `GIT_TEST_DEBUG_UNSAFE_DIRECTORIES` env var, both of which are configuration changes, so left untouched per "don't modify anything, anywhere." Branch/remote above were read directly from the plain-text `.git/HEAD` and `.git/config` files instead, which required no git trust override.
- **README (first paragraph):** Default Expo boilerplate readme — "Welcome to your Expo app 👋 — This is an Expo project created with `create-expo-app`." No project-specific description.

## `github_repos/darknet`

- **Path:** `C:\Users\nick_\github_repos\darknet`
- **Remote:** `https://github.com/pjreddie/darknet` (upstream open-source project, not a `repoman989` repo)
- **Branch:** `master`
- **Last commit:** 2022-07-18 — `f6afaab` — "Update README.md" (oldest last-commit date of any repo found; long dormant)
- **README (first paragraph):** Darknet is an open source neural network framework written in C and CUDA. Fast, easy to install, supports CPU and GPU computation.

## `imageGenerationAI`

- **Path:** `C:\Users\nick_\imageGenerationAI`
- **Remote:** `https://github.com/repoman989/imageGenerationAI.git`
- **Branch:** `main`
- **Last commit:** 2025-05-23 — `d4f215f` — "Initial commit" (only commit — no activity since)
- **README (first paragraph):** None — the README contains only the title `# imageGenerationAI`, no body text.

## `Oleo-Ventures` (this repo)

- **Path:** `C:\Users\nick_\Oleo-Ventures`
- **Remote:** `git@github.com:repoman989/Oleo-Ventures.git`
- **Branch:** `main`
- **Last commit:** none — repo has no commits yet
- **README:** none present yet

---

## Summary

| Repo | Remote host | Last activity | Notes |
|---|---|---|---|
| cropcast | github.com/repoman989 | 2026-09-16 | active |
| doge-assessment | github.com/MARecruiting | 2026-03-10 | take-home assessment, external org |
| farm-property-poc | none | 2026-09-19 | local-only, no remote |
| farmweather | github.com/repoman989 | 2026-09-16 | active |
| field_fusion | github.com/repoman989 (alt SSH host alias) | 2026-09-20 | most recently active; no README |
| GeoLocator/my-locations-app | none | unknown (git-blocked) | Expo boilerplate, unmodified README |
| github_repos/darknet | github.com/pjreddie | 2022-07-18 | third-party upstream clone, not authored by this user |
| imageGenerationAI | github.com/repoman989 | 2025-05-23 | single initial commit, no further work |
| Oleo-Ventures | github.com/repoman989 | no commits | this repo, mid-setup |

9 git repositories found under `C:\Users\nick_`. No repos found elsewhere on the machine (single logical drive).
