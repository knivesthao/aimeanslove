---
name: code-index
description: "One tiny map keeps every other skill small: the agent reads hundreds of tokens, not thousands."
---

# Start here: pick skills by task

Create and install a skill named `code-index` (Start here: pick skills by task). It instructs the agent as follows: Your installed skills each do one job — never read them all. Three skills apply to almost every task, so always read these: code-secure, code-reuse, code-token. Then match the task and read only the matched skills: Interface, screen, or component work → ui-index. New service or script → code-language, code-shape. Organizing a new codebase → code-group. Services in other languages → code-boundaries. Public API, forms, beacons → code-ratelimit. Repeat traffic → code-cache. Usage counts → code-track. Slow endpoint or heavy page → code-perf. Traffic spikes, shedding features → code-fallback. Login, accounts, permissions → code-auth. Security deep-dives, read on match: code-crypto, code-injection, code-design, code-misconfig, code-deps, code-integrity, code-logging, code-ssrf. These stack picks assume a new codebase: if the project already uses something else — another language, framework, or tokens — follow that instead. The house rule beats the skill. Skip everything else. When building is done → verify-tests, and verify-visual for anything with a screen. Missing a skill? Copy its prompt from the board once, install it, then use it locally. This follows progressive disclosure, the Agent Skills model — map first, details on demand: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

## Checks

- only matched skills are read
- always-on skills never skipped
- whole bank never copied at once
