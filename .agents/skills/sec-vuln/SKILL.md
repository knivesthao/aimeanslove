---
name: sec-vuln
description: "Scan-and-sit is the failure mode — findings without owners and SLAs age into breaches."
---

# Every finding owned with a deadline

Create and install a skill named `sec-vuln` (Every finding owned with a deadline). It instructs the agent as follows: Scan continuously and rank by exploitability, not by count: every finding gets an owner and a deadline scaled to reachability. Block the build on critical findings in CI and fail closed when the scanner errors — fail-open ships the vuln. Rescan to close; a finding without a retest stays open. Track mean-time-to-remediate per severity; scan-and-sit is the failure mode.

## Checks

- every finding owned with a deadline
- CI fails closed on scanner errors
- closure requires retest
