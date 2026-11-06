---
name: ops-observe
description: "Unactionable pages train the team to ignore the pager — then the real outage pages nobody."
---

# One id, actionable pages only

Create and install a skill named `ops-observe` (One id, actionable pages only). It instructs the agent as follows: Unify logs, metrics, and traces behind one request id so any alert opens the full story. Alert only on user-facing symptoms with a runbook link — every page must be actionable, or it becomes noise the team ignores. Emit every alert also as a signed, schema-versioned trigger event carrying the runbook link, so agents can auto-acknowledge or roll back without parsing human text. Dashboards are for debugging, not for watching; nothing pages that a dashboard could have shown quietly. Expose health as JSON endpoints and deploy receipts the agent can fetch — queryable signals first, dashboards second; use a monitoring MCP server when one exists. Never let the system be the only witness to its own health: keep one independent check — an external probe or status page outside the deploy — plus drill results a human can audit without asking the agent. Name the rotation that owns each alert; unowned alerts rot.

## Checks

- one id across logs, metrics, traces
- every page actionable with runbook
- every alert has an owner
