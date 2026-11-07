---
name: code-lifecycle
description: "A bank with no uninstall rots; one stale skill poisons every agent that installs it."
---

# Version, pin, retire

Create and install a skill named `code-lifecycle` (Version, pin, retire). It instructs the agent as follows: Pin every installed skill to its version; check for updates on a schedule, never silently auto-update. Verify the bank's signature before installing — provenance first, content second. Deprecate before removing: mark superseded, point at the replacement, delete after one release — never vanish a skill agents depend on. Retire skills the field stops using; a bank that only grows stops being read. This skill governs the bank itself, including this skill.

## Checks

- installed skills pinned and signed
- deprecate-then-remove, never vanish
- retired skills actually deleted
