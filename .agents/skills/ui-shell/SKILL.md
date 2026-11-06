---
name: ui-shell
description: "Humans get the interface they prefer; metadata makes it legible to agents without dumbing it down."
---

# UI shell in 40 lines

Create and install a skill named `ui-shell` (UI shell in 40 lines). It instructs the agent as follows: Build mobile-first: design at 360px width, then scale up — full-monitor layouts only when the task genuinely needs a big screen. Semantic HTML shell (<header>/<main>/<footer>), one stylesheet, no UI framework. System font stack, 2 colors + 1 accent, 4px spacing scale. Humans get the UI they prefer — icon-only buttons and custom controls included — but every control must expose machine-readable metadata: a real <button>/<a>/<input>, a visible label or aria-label, and a data-action naming what it does. Pull icons from Lucide: `<i data-lucide='name'>` plus one `lucide.createIcons()` call; never hand-write SVG paths — the agent picks icon names, not pixels. Hand-drawn icons burn tokens and time for a worse result: Lucide is already in the model's training so the agent knows every name, and already familiar to users so people recognize each icon on sight.

## Checks

- layout verified at 360px width
- every control has a label or aria-label
- custom controls expose role + data-action
