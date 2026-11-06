---
name: code-track
description: "You can't improve what you never counted — and you can't un-leak what you logged."
---

# Emit events, plug the sink later

Create and install a skill named `code-track` (Emit events, plug the sink later). It instructs the agent as follows: Code emits events; sinks decide where they land. Call one tiny emit helper at the interesting moments — used, copied, failed, slow. The helper writes somewhere boring today (a local JSONL file) and a real sink tomorrow (ClickHouse, analytics) without callers changing. Count actions, never identities: no names, emails, or keys in events. Roll noisy events into buckets and surface them slowly, so displays stay readable and cheap.

## Checks

- one emit helper everywhere
- no identities in events
- sink swaps without touching callers
