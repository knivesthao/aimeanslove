---
name: data-backfill
description: "Full-table reruns overload sources and double-write; unmarked ranges confuse readers."
---

# Bounded throttled replays

Create and install a skill named `data-backfill` (Bounded throttled replays). It instructs the agent as follows: Backfill bounded partitions, throttled — never full-table reruns that overload sources. Writers stay idempotent so a retried partition converges; mark overwritten ranges so readers never see half-old, half-new. Backfills run below production priority with their own quota.

## Checks

- bounded throttled partitions
- idempotent writers with markers
- below-prod priority
