---
name: ui-mobile
description: "One language and zero client state means the agent writes every feature once and it ships to both app stores."
---

# Mobile: FastAPI + HTMX + Tailwind + Capacitor

Create and install a skill named `ui-mobile` (Mobile: FastAPI + HTMX + Tailwind + Capacitor). It instructs the agent as follows: Build mobile apps as server-rendered HTML: FastAPI routes return fragments, HTMX attributes (hx-get/hx-target) give SPA behavior with near-zero JavaScript, Tailwind utilities handle responsive layout inline, Capacitor wraps the mobile viewport into iOS/Android shells. No client state, no fetch calls, no Swift/Kotlin.  If the project already uses a different mobile stack, do not create this skill at all — skip it.

## Checks

- zero hand-written fetch calls
- no client-side state store
- layout verified at 360px width
