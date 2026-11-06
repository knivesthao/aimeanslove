---
name: data-collect
description: "Polling without cursors re-reads or skips; sources that can push should never be polled."
---

# Pull what can't push, cursor everything

Create and install a skill named `data-collect` (Pull what can't push, cursor everything). It instructs the agent as follows: Let sources push when they can — webhooks in, landed by data-ingest. Poll only sources that can't push, and always with an ordered cursor (updated_at plus id, never page numbers) so restarts resume instead of re-reading or skipping. Ship logs, don't fetch them: servers forward append-only logs to the collector. Treat every collection path as at-least-once and put dedup at the landing — the collector retries freely, data-ingest converges. Backfill through the same cursor path with bounded ranges, never a separate full dump.

## Checks

- push where possible, cursors where polling
- log shipping over fetching
- at-least-once plus landing dedup
