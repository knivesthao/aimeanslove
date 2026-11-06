---
name: ui-react-components
description: "Small components with one job are cheap to generate and safe to reuse."
---

# React components that stay small

Create and install a skill named `ui-react-components` (React components that stay small). It instructs the agent as follows: Build small components — one job each, props typed, composition over deep prop drilling (children and slots over five layers of props). State lives with the UI that uses it; lift only what two siblings truly share. Every list gets a stable key from the data, never the array index. No manual DOM writes — refs are the escape hatch, not the tool. Style with className plus your pipeline's CSS; keep ready-made pieces from a stocked library instead of hand-built dropdowns and dialogs. Apply the generic component rules too (see ui-framework).

## Checks

- one job per component, props typed
- lists use stable data keys
- no manual DOM writes
