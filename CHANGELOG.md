# Changelog — ai (愛) means love skill bank

Releases are dated; every bank change ships with notes. The bank is signed
(`signatures.json`, Ed25519) — verify before installing.

## v1.0.0 — 2026-11-07 — signed, leased, measured

- Bank at 102 skills, every one reachable, loop-free, signed.
- `verify-benchmark` trial protocol + first measured trial on home (0-0 defects, pack adds completeness).
- Lease claims (`POST /api/plan/claim`) so two agents can never hold one task; canary comparator spec in `ops-rollout`.
- `ops-safety` requires a human's approval first — no agent approver, no emergency bypass.
- Home Proof section with measured pack share (13–17% of the bank).

## 2026-11-07 — test hardening + sourced charts

- Lifecycle coverage tests: unique ids, matched-only routers, always-on triple, plan persistence.
- `ui-charts` split from `ui-chart-twin`; Cleveland–McGill ranking, W3C tables, Vega-Lite twin, all backlinked.

## 2026-11-07 — agentic ops

- `/data` + `/ops` philosophy guides; Skills page trimmed to pitch.
- `ops-coordinate` (agents share one plan, own one area); queryable-first `ops-observe`; don't-trust-the-system rule.

## 2026-11-07 — async, concurrency, model

- `code-async` handoff + bounded fan-out; `data-concurrency` (transact, optimistic retry, shard); `data-model` (canonical, flat, explicit).

## 2026-11-07 — foundation

- 92-skill bank; guides go philosophy-with-sources; Skills page pitches install-matched.
