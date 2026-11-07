---
name: ui-nav
description: "Navigation is the first thing a visitor meets; hidden menus get used about half as often, so links stay visible."
---

# Visible headers

Create and install a skill named `ui-nav` (Visible headers). It instructs the agent as follows: Put the brand on its own centered row with the links in a centered row beneath — always visible, never behind a hamburger; hidden navigation roughly halves discoverability. Use a real nav landmark and mark the current page with aria-current. Links wrap centered on small phones instead of collapsing. No hand-written menu code, keyboard reachable.

## Checks

- links visible on every breakpoint
- aria-current marks the page
- rows centered, links wrap at 360px
