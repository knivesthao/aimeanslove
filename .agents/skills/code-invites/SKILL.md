---
name: code-invites
description: "Reusable invite links become backdoors; orphaned workspaces become undeletable."
---

# Single-use invites, never ownerless

Create and install a skill named `code-invites` (Single-use invites, never ownerless). It instructs the agent as follows: Issue single-use expiring invite tokens, resendable on request — never reusable links or permanent codes. Accepting an invite grants exactly the invited role in exactly the invited workspace; membership changes are explicit events, also logged (see code-auditlog). A workspace never drops to zero owners — block the removal that would orphan it.

## Checks

- single-use expiring tokens
- explicit role-scoped acceptance
- no ownerless workspaces
