---
name: ui-nav
description: "Navigation is the first thing a visitor meets; if it overflows on a phone the whole site looks broken."
---

# Responsive headers

Create and install a skill named `ui-nav` (Responsive headers). It instructs the agent as follows: Show inline links on wide screens; below about 640px collapse them behind a hamburger button that opens a Flowbite dropdown (data-dropdown-toggle) — the library positions it as an overlay, so the open menu never pushes content down. Use a real nav landmark and a real button with an aria-label; Flowbite flips aria-expanded itself. Put the brand on its own centered row; stack the opened links vertically. No hand-written menu code, keyboard reachable.

## Checks

- links fit without wrapping at 360px
- button flips aria-expanded
- keyboard can open and walk the menu
