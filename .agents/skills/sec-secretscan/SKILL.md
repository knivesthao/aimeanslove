---
name: sec-secretscan
description: "Alerting while the secret stays active fails; copies in history and forks outlive the fix."
---

# Revoke first, purge history, block at push

Create and install a skill named `sec-secretscan` (Revoke first, purge history, block at push). It instructs the agent as follows: Revoke the secret on detection first, investigate second — alerting while it stays active fails. Purge copies from history and forks, then rotate everything the secret could reach. Block commits containing known secret shapes at push time; detection after merge is the backup, not the plan.

## Checks

- revoke first, investigate second
- history and forks purged
- push-time blocking
