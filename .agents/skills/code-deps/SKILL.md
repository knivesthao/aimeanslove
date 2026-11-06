---
name: code-deps
description: "Your code inherits every vulnerability in every library it imports."
---

# Dependencies audited

Create and install a skill named `code-deps` (Dependencies audited). It instructs the agent as follows: Pin every dependency (requirements with versions), audit on a schedule (pip audit or equal), and update promptly when a fix lands. Fewer dependencies means fewer advisories: drop what the stack already covers. Never vendor a copy you will forget to patch.

## Checks

- deps pinned with versions
- audit runs on schedule
- unused deps removed
