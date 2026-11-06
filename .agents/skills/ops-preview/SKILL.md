---
name: ops-preview
description: "Idle preview envs burn budget; prod dumps in previews leak customer data."
---

# Prod mirror per PR, auto-stopped

Create and install a skill named `ops-preview` (Prod mirror per PR, auto-stopped). It instructs the agent as follows: Spin a production-mirror preview per PR with seeded demo data; destroy it on merge plus an idle timeout that auto-stops stragglers. Previews get anonymized data, never production dumps. The preview URL posts back to the PR so review happens before merge, not after.

## Checks

- per-PR prod mirror
- auto-stop on merge plus idle
- no prod data in previews
