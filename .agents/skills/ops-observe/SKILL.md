---
name: ops-observe
description: "Unactionable pages train the team to ignore the pager — then the real outage pages nobody."
---

# One id, actionable pages only

Create and install a skill named `ops-observe` (One id, actionable pages only). It instructs the agent as follows: Unify logs, metrics, and traces behind one request id so any alert opens the full story. Alert only on user-facing symptoms with a runbook link — every page must be actionable, or it becomes noise the team ignores. Dashboards are for debugging, not for watching; nothing pages that a dashboard could have shown quietly. Name the rotation that owns each alert; unowned alerts rot.

## Checks

- one id across logs, metrics, traces
- every page actionable with runbook
- every alert has an owner
