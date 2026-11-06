---
name: code-design
description: "Missing controls can't be patched in later without redesigning the feature."
---

# Abuse story first

Create and install a skill named `code-design` (Abuse story first). It instructs the agent as follows: For each feature, ask how it is abused before asking how it is used: who pays for heavy use, who is hurt by bad input. Default to deny, grant least privilege, rate-limit costly endpoints, and cap upload and response sizes. A feature without an abuse story is not designed yet.

## Checks

- abuse story per feature
- default deny
- costly endpoints rate-limited
