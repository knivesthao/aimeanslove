---
name: sec-patch
description: "Exempted exec and legacy machines become the persistent foothold."
---

# Fleet-wide patching, no exemptions

Create and install a skill named `sec-patch` (Fleet-wide patching, no exemptions). It instructs the agent as follows: Push OS, browser, and agent updates fleet-wide with CIS baselines — including exec and legacy machines, because exemptions become the persistent foothold. Patch windows are scheduled and measured; unpatched stragglers page their owners.

## Checks

- fleet-wide including exemptions
- measured patch windows
