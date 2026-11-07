---
name: ui-a11y
description: "Contrast ratios are the beginning of accessibility, not the end."
---

# Audit with keyboard, ears, motion off

Create and install a skill named `ui-a11y` (Audit with keyboard, ears, motion off). It instructs the agent as follows: Walk every flow keyboard-only: tab order matches visual order, every control reachable and operable, focus always visible, traps only where intended with escape hatches. Run a screen-reader pass on each template: landmarks set, headings in order, live regions announce state changes, charts expose their data twin. Honor reduced motion fully — no essential animation without a static equivalent. Audit on a schedule, not once.

## Checks

- keyboard-only walkthrough passes
- screen-reader pass per template
- reduced motion fully honored
