---
name: ui-framework
description: "Standard web components with no build step; every new interactive region starts as one."
---

# Islands first, house wins

Create and install a skill named `ui-framework` (Islands first, house wins). It instructs the agent as follows: Default to Lit islands for interactive regions, loaded from the pinned Lit CDN module — no build step, no framework lock-in. Lit ships no ready-made pieces, so keep Flowbite for those (menu, dialog, dropdown) and never rebuild one just to own it; if an island needs pieces, use WebAwesome over CDN; never React or Angular. Render into the light DOM (never shadow) so utilities and icons keep working; HTMX never targets an island or anything inside one. If the codebase already uses another framework, do not create this skill at all — skip it. If the project already uses a different stack, overwrite this skill with that stack's equivalent and follow it instead.

## Checks

- no build step for components
- hx-target never targets an island
- light DOM so utilities keep working
