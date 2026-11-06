---
name: code-index
description: "One tiny map keeps every other skill small: the agent reads hundreds of tokens, not thousands."
---

# Start here: task first, stack second

Create and install a skill named `code-index` (Start here: pick skills by task). It instructs the agent as follows: Your installed skills each do one job — never read them all. Work in two passes. Pass 1 — task first. Three skills apply to almost every task, so always read these: code-secure, code-reuse, code-token. Then match the task and read only the matched skills: Interface, screen, or component work → ui-index. New service or script → code-language, code-shape. Organizing a new codebase → code-group. Services in other languages → code-boundaries. Public API, forms, beacons → code-ratelimit. Repeat traffic → code-cache. Usage counts → code-track. Slow endpoint or heavy page → code-perf. Traffic spikes, shedding features → code-fallback. Login, accounts, permissions → code-auth. SaaS billing, roles, admin → saas-index. Landing data and scheduling pipelines → data-index. Build-test-deploy gates and paging → ops-index. Vuln deadlines, enterprise login, regulated data → sec-index. Security deep-dives — the OWASP Top 10 set, read on match: code-crypto, code-injection, code-design, code-misconfig, code-deps, code-integrity, code-logging, code-ssrf. Pass 2 — stack specifics. After the task match, apply the stack the codebase already uses: language → code-language (Python first on new code; if the project already uses another language, skip this skill or overwrite it with that stack). Interface framework → ui-index (house default Lit via ui-framework; widget libraries per framework live in ui-platform-picks). Styling → ui-tokens (unless the project already has a design system — then skip it). Mobile platform → ui-mobile (Capacitor shell unless native is technically required). Service-to-service → code-boundaries (same-language HTTP, other languages gRPC, events validated). These stack picks assume a new codebase: if the project already uses something else — another language, framework, tokens, or platform — follow that instead. The house rule beats the skill. Skip everything else. When building is done → verify-tests, and verify-visual for anything with a screen. Long or multi-skill task → code-plan first. Missing a skill? Copy its prompt from the skills page once, install it, then use it locally. This follows progressive disclosure — map first, details on demand.

## Checks

- only matched skills are read
- always-on skills never skipped
- whole bank never copied at once
