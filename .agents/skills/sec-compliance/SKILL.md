---
name: sec-compliance
description: "Week-before screenshots rot immediately and convince no auditor."
---

# Continuous automated evidence

Create and install a skill named `sec-compliance` (Continuous automated evidence). It instructs the agent as follows: Collect access reviews, change tickets, and control attestations continuously and automatically — screenshots the week before the audit rot immediately and convince nobody. Regulated data decides the control set, so identify it first: health data (HIPAA/PHI) → code-auditlog on every access, encryption at rest (see code-crypto), code-rbac tenant isolation, data-retain deletion with proof; card data (PCI) → never store PAN, tokenize through the provider; personal data (GDPR) → data-retain retention plus deletion on request. Build the controls first — evidence collection only proves what already exists. Map every control to the system that proves it; an unmapped control is an audit finding waiting.

## Checks

- continuous automated collection
- every control mapped to proof
