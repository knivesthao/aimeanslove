---
name: code-billing
description: "Billing bugs refund money or lock out paying users — both fail loudly and publicly."
---

# Bill from plans, never hardcode

Create and install a skill named `code-billing` (Bill from plans, never hardcode). It instructs the agent as follows: Bill from plan versions, never hardcoded amounts: every charge resolves price from the plan in effect when the metered event landed. Checkout sessions are idempotent — one customer plus plan plus idempotency key maps to one subscription. Fulfill and entitle only on signed provider webhooks, verified before trusting, with retry-safe handlers that converge on replay. Failed payments enter dunning (remind, retry, grace) before any cancel. Metered usage flows from code-track events, not from scattered counters. Prorate upgrades and downgrades at the switch, never at month end.

## Checks

- no hardcoded prices
- entitlement only on verified webhooks
- dunning before cancel
