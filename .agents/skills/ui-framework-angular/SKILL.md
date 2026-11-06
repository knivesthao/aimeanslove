---
name: ui-framework-angular
description: "Angular ships islands natively — @defer decides what loads when, so the initial bundle stays small."
---

# Angular: standalone and deferred

Create and install a skill named `ui-framework-angular` (Angular: standalone and deferred). It instructs the agent as follows: Build standalone components — no NgModules for new code — with signals for state and @if/@for in templates. Wrap below-fold and heavy regions in @defer with placeholder, loading, and error blocks and a viewport or interaction trigger: deferred code splits into its own file and loads only when needed. Use reactive forms, Angular Material or CDK for ready-made pieces, and SSR with hydration where the setup allows. Apply the generic component rules too (see ui-framework).

## Checks

- standalone components, signals for state
- heavy regions deferred with fallback blocks
- ready-made pieces over hand-built
