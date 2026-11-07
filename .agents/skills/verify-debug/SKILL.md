---
name: verify-debug
description: "A wrong agent needs a debugger, not a re-read; bisect the run to the guilty step."
---

# Diagnose the run, not the intent

Create and install a skill named `verify-debug` (Diagnose the run, not the intent). It instructs the agent as follows: When the output is wrong, reproduce first with the smallest input that still fails. Bisect the plan: re-run steps in order against their done-states until one lies — the guilty step is the first whose output fails its check. Read receipts, samples, and drill records, never the agent's explanation of what it meant. Fix the step, not the plan; if two steps disagree, the contract between them is the bug. Record the failure shape so the next run recognizes it.

## Checks

- smallest failing input reproduced
- guilty step bisected by done-state
- contract fixed when steps disagree
