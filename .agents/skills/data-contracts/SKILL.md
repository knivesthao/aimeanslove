---
name: data-contracts
description: "A breaking rename with no contract silently breaks every downstream reader."
---

# Versioned schemas, additive only

Create and install a skill named `data-contracts` (Versioned schemas, additive only). It instructs the agent as follows: Version every event and table schema in one registry with compatibility checks on publish. Additive changes only — new optional fields, never renames or type changes without a new version. Consumers pin the version they read; producers support the last N versions through a dual-write window.

## Checks

- schemas versioned in one registry
- additive-only evolution
- consumers pin versions
