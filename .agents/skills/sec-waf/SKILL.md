---
name: sec-waf
description: "Monitor-only is decoration; copied defaults break legit users until someone disables everything."
---

# Blocking rules tuned to real traffic

Create and install a skill named `sec-waf` (Blocking rules tuned to real traffic). It instructs the agent as follows: Run WAF and input-filter rules in blocking mode tuned to legitimate traffic — monitor-only is decoration, and copied defaults break real users until someone disables the whole thing. Payload shapes live in code-injection; the WAF enforces what that skill defines. Exempt nothing sensitive from logging; tune on false positives weekly after launch.

## Checks

- blocking mode, tuned
- no monitor-only
- false positives tuned
