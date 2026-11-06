---
name: data-streams
description: "Batch logic on streams mishandles late events; a stalled watermark is a silent outage."
---

# Windows plus watermarks

Create and install a skill named `data-streams` (Windows plus watermarks). It instructs the agent as follows: Transform unbounded streams with windows plus watermarks so late and out-of-order events settle correctly. Never batch logic on a stream — every unbounded grouping needs a trigger for when it emits. Track watermark lag as the health metric; a stalled watermark is the outage.

## Checks

- windows plus watermarks
- every grouping has an emit trigger
- watermark lag monitored
