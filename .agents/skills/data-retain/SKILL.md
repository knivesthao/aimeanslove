---
name: data-retain
description: "Keep-forever drowns storage budgets and turns every breach into a GDPR incident."
---

# Expire per policy, prove deletion

Create and install a skill named `data-retain` (Expire per policy, prove deletion). It instructs the agent as follows: Expire or cold-store every dataset per written policy — cost and GDPR exposure both grow with keep-forever. PII gets the shortest retention and deletion on request with proof. Archive in open formats so cold data stays readable without the original cluster. Square erasure with immutable backups by key-per-subject shredding: destroying one subject's key deletes them from every backup holding it — deletion with proof, restores that still work.

## Checks

- policy per dataset, enforced
- PII deletable with proof
- open-format archives
