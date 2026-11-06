---
name: sec-runbooks
description: "Undrilled runbooks mean improvisation during the breach that matters."
---

# Containment playbooks that get drilled

Create and install a skill named `sec-runbooks` (Containment playbooks that get drilled). It instructs the agent as follows: Write containment playbooks per breach class — isolation, credential rotation, customer notice — and drill them (rotation process lives in ops-oncall). Severity levels and escalation paths are decided in advance, not mid-breach. Every drill updates the playbook or it rots.

## Checks

- containment per breach class
- drilled, not shelved
- drills update the playbook
