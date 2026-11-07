---
name: data-cdc
description: "API polling misses deletes and hammers the source; the log has every change in order."
---

# Stream the log, never poll

Create and install a skill named `data-cdc` (Stream the log, never poll). It instructs the agent as follows: Stream row inserts, updates, and deletes from the database log — deletes must propagate, which API polling can never do. Treat the log as the source of truth with ordered offsets; consumers checkpoint so restarts resume, never restart from zero. Operate the connector like production: monitor the schema-history topic, snapshot deliberately, and alert on silent stalls — the log is only truth if someone watches the tap.

## Checks

- deletes propagate
- ordered offsets with checkpoints
- no polling
