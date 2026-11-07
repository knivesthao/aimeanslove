---
name: code-legacy
description: "Rewrites stall for years; strangulation ships every quarter."
---

# Strangle the monolith

Create and install a skill named `code-legacy` (Strangle the monolith). It instructs the agent as follows: Follow the existing patterns first — restructuring is costly and error-prone. Carve by seam: put new behavior behind the old interface, route traffic slice by slice, and let the replacement grow while the monolith shrinks. Isolate with anti-corruption layers so legacy quirks never leak into new code. Delete dead paths only after the new path carries everything with clean drills. Never a flag-day rewrite.

## Checks

- existing patterns followed first
- traffic moves slice by slice
- no flag-day rewrite
