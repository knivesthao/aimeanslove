---
name: sec-index
description: "Vulns without owners sit for months — map first, scan-and-sit never."
---

# Security ops: pick sec skills

Create and install a skill named `sec-index` (Security ops: pick sec skills). It instructs the agent as follows: Your security-ops skills each do one job — never read them all. Known vulnerabilities with owners and deadlines → sec-vuln. Enterprise login, MFA, and break-glass → sec-sso. App login basics → code-auth. Anything else (image scans, secret scans, session hardening, SIEM, rotation, WAF, anomaly detection, runbooks, patching, compliance evidence) → build it from code-secure plus code-logging, and bank the pattern when it repeats a third time. Skip everything else.

## Checks

- only matched sec skills are read
- app basics stay in code-auth
