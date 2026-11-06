---
name: ui-behavior
description: "Explicit text states make every outcome checkable by agents and humans alike, with no interpretation needed."
---

# Behavior contract

Create and install a skill named `ui-behavior` (Behavior contract). It instructs the agent as follows: Every mutation needs an explicit state: idle → working → done|error. Show text status, never color alone. Respect prefers-reduced-motion. Confirm destructive actions inline. Humans verify by looking; log the state string for agents. For standard widgets (dialog, menu, combo, toggle, disclosure) follow the ARIA Authoring Practices pattern, keyboard behavior included — never invent interactions the platform already defined.

## Checks

- each action exposes a text status
- reduced-motion honored
- destructive action confirms
