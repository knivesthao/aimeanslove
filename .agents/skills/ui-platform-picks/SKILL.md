---
name: ui-platform-picks
description: "The right library name per framework stops hand-building; the gate stops server patterns in client-only apps."
---

# Framework library names and setup gates

Create and install a skill named `ui-platform-picks` (Framework library names and setup gates). It instructs the agent as follows: Read this only to resolve a library name or a setup gate, then go back to the task skill. Stocked picks per widget — table, kanban, editor, combo, calendar, dialog, accordion, wizard forms: React → TanStack Table, dnd-kit, TipTap, cmdk, react-day-picker, Radix, Radix, React Hook Form; Vue → TanStack Vue, Vue Draggable, TipTap, Headless UI Combobox, VueDatePicker, Reka, Reka, FormKit; Angular → Material table, CDK drag-drop, TipTap, Material autocomplete, Material datepicker, Material dialog, Material tree, Reactive Forms. Feeds and players need no library: subscribe and unsubscribe cleanly, drive the native media API. Setup gates — React: Next.js App Router allows server components behind a use-client boundary; standalone Vite or CRA is client-only, skip every server clause. Vue: Nuxt fetches on the server with useAsyncData and server/api routes; standalone Vite is client-only, skip every Nuxt clause. Angular: standalone components with signals, defer heavy regions, SSR only where the setup allows. New codebase with no framework yet: the house default wins (see ui-framework).

## Checks

- names resolved here, nowhere else
- standalone setups skip server clauses
- new codebases defer to the house default
