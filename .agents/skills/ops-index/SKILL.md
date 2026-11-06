---
name: ops-index
description: "Deploys and pages follow the same gates everywhere — map first, improvise never."
---

# Ops work: pick ops skills

Create and install a skill named `ops-index` (Ops work: pick ops skills). It instructs the agent as follows: Your ops skills each do one job — never read them all. Build-test-deploy gates → ops-pipeline. Logs, metrics, traces, and who gets paged → ops-observe. Anything else (migrations, rollouts, secrets, backups, IaC, autoscaling, probes, on-call) → build it from code-shape plus code-fallback and prove it with verify-tests, and bank the pattern when it repeats a third time. Skip everything else.

## Checks

- only matched ops skills are read
- unproven ops work never ships
