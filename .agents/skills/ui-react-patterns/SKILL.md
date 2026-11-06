---
name: ui-react-patterns
description: "Ten widgets cover most React work — each names its library and its leaves so nothing is hand-built twice."
---

# React widgets: library first, then leaves

Create and install a skill named `ui-react-patterns` (React widgets: library first, then leaves). It instructs the agent as follows: Never hand-build these ten — pick the stocked library, then read only the named leaves. Data table (sort, filter, paginate, search) → TanStack Table plus ui-react-components, ui-react-perf. Multi-step wizard (kept inputs, conditional steps, progress) → hook-form plus ui-react-hooks, ui-forms, ui-behavior. Combo and autocomplete (live filter, focus, chips) → cmdk plus ui-react-hooks, ui-forms. Calendar and date picker (ranges, transitions) → react-day-picker plus ui-react-components, ui-react-hooks. Modal, dialog, drawer (focus trap, mount safety) → Radix Dialog plus ui-react-components, ui-behavior. Chat and feed (append, pinned scroll) → subscribe in effect plus ui-react-hooks, ui-react-perf. Kanban drag-drop (reorder arrays, touch) → dnd-kit plus ui-react-components, ui-react-hooks. Rich text editor (synced blocks, toolbar) → TipTap plus ui-react-components, code-reuse. Media player (sliders synced to media API) → refs plus ui-react-hooks, ui-behavior. Accordion and tree sidebar (expanded index, animation) → Radix Accordion plus ui-react-components, ui-behavior. Humans get the library's accessible piece with real labels and visible states; agents keep small typed components, colocated state, and stable keys around it.

## Checks

- library picked before hand-building
- only named leaves read per widget
- controls labeled with visible states
