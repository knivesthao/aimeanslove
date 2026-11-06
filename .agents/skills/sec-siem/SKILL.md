---
name: sec-siem
description: "Logs nobody verifies won't survive scrutiny; alert floods train analysts to ignore the one that matters."
---

# Tamper-evident logs analysts can trust

Create and install a skill named `sec-siem` (Tamper-evident logs analysts can trust). It instructs the agent as follows: Aggregate auth, admin, and data-access events into tamper-evident searchable storage — and test the integrity, because logs nobody verifies won't survive scrutiny (product audit trails live in code-auditlog). Tune alerts to analyst capacity; unactioned floods train everyone to ignore the one that matters.

## Checks

- tamper-evident with tested integrity
- alerts tuned to capacity
