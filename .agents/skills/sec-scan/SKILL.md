---
name: sec-scan
description: "Fail-open scanners and floating tags silently keep the CVE in production."
---

# Block builds on vuln images and deps

Create and install a skill named `sec-scan` (Block builds on vuln images and deps). It instructs the agent as follows: Block builds on vulnerable base images and packages in CI — and fail closed when the scanner errors, because fail-open ships the vuln (runtime CVE ownership lives in sec-vuln). Pin versions and rebuild images on a schedule so fixes actually land; floating tags silently keep the CVE. Track mean-time-to-remediate; the scanner nobody watches is decoration.

## Checks

- CI blocks on critical
- fail closed on scanner errors
- images pinned and rebuilt
