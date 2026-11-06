---
name: ui-framework-vue
description: "Vue rewards magic that hides state from readers — this skill pins the explicit subset agents parse cheaply."
---

# Vue and Nuxt: explicit over magic

Create and install a skill named `ui-framework-vue` (Vue and Nuxt: explicit over magic). It instructs the agent as follows: Standalone Vue (Vite, no Nuxt)? Build client-only and skip every Nuxt clause below. Write Composition API in script setup with typed props and emits; prefer explicit computed and watch over deep reactivity magic. Pull shared logic into composables with plain names (useCart, useFetch) so the next agent finds it. Nuxt only: fetch on the server by default with useAsyncData or useFetch, server/api routes own the backend, static regions stay server-rendered islands where the setup allows, browser-only pieces sit inside ClientOnly. Keep ready-made accessible pieces from a stocked library instead of hand-built dropdowns and dialogs. Humans get labeled controls with visible states; agents get explicit typed code with no hidden magic.

## Checks

- standalone Vue skips Nuxt clauses
- composables named for findability
- no hand-built copy of stocked pieces
- controls labeled with visible states
