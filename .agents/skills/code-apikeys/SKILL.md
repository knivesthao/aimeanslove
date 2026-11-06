---
name: code-apikeys
description: "A leaked plaintext key database hands attackers access; god-mode scopes hand them everything."
---

# Hashed, scoped, revocable keys

Create and install a skill named `code-apikeys` (Hashed, scoped, revocable keys). It instructs the agent as follows: Store only hashes of customer API keys — a leaked database must not leak access. Scope every key least-privilege with per-key rate limits, rotation, and instant revocation. Show the secret once at creation, never again. Attribute every call to its key for metering and abuse tracing.

## Checks

- hashes stored, shown once
- scoped with per-key limits
- instant revocation
