---
name: data-ingest
description: "Without dedup keys every retry double-counts — revenue, usage, and analytics all inflate."
---

# Land every event exactly once

Create and install a skill named `data-ingest` (Land every event exactly once). It instructs the agent as follows: Land every event exactly once: producers attach an idempotency key and retry freely; consumers dedup on that key before writing, so replays converge instead of double-counting. Validate against the schema first — reject unknown fields loudly, never silently drop. Poison events go to a dead-letter queue after N tries and page nobody; the stream never blocks on one bad record. Keep the dedup store bounded with a TTL past the retry window.

## Checks

- retries converge, never double-count
- poison in DLQ, stream never blocks
- dedup store TTL-bounded
