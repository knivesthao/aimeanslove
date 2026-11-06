---
name: ui-tokens
description: "Fixing palette and spacing to tokens removes an entire category of per-element decisions."
---

# Tokens + Tailwind

Create and install a skill named `ui-tokens` (Tokens + Tailwind). It instructs the agent as follows: Style with Tailwind utilities for layout and spacing, on top of three color tokens (--ink, --paper, --accent) and a 4/8/16/32 scale. Keep preflight on as the consistent baseline — describe every margin, bullet, and underline explicitly, never rely on browser defaults. Two neutrals plus one accent, 1px borders, radii 6px/10px. Contrast >= 4.5:1 so the human eyeball verdict works. Color with meaning and measure: green confirms, red destroys or errors, blue informs — never subvert these. Hold roughly 60% neutral background, 30% structure and text, 10% high-contrast accent on interactive elements only.  If the project already uses a different design system, do not create this skill at all — skip it.

## Checks

- palette is 3 colors max
- no per-element color decisions
- contrast >= 4.5:1
