---
name: code-crypto
description: "Homegrown crypto fails silently; platform crypto fails loudly and rarely."
---

# No homegrown crypto

Create and install a skill named `code-crypto` (No homegrown crypto). It instructs the agent as follows: Use vetted crypto only: TLS for data in motion, platform encryption (KMS, age, or libsodium) for data at rest — never a hand-rolled cipher. Secrets live in environment variables, never in code or logs. Passwords are hashed, not encrypted (see code-auth); API tokens are random, scoped, and expire.

## Checks

- no hand-rolled ciphers
- no secret in code or logs
- tokens expire and are scoped
