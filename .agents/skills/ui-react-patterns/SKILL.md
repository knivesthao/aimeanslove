---
name: ui-react-patterns
description: "Each widget pins the one shape agents get wrong — everything the model already knows is left out."
---

# React widgets: library first, pinned shape

Create and install a skill named `ui-react-patterns` (React widgets: library first, pinned shape). It instructs the agent as follows: Never hand-build these ten — pick the stocked library, build the pinned shape, and read only the named leaves. Data table → TanStack Table plus ui-react-components, ui-react-perf: page on the server, render only the visible window. Multi-step wizard → hook-form plus ui-react-hooks, ui-forms, ui-behavior: one state object at the wizard root, validate each step on exit. Combo and autocomplete → cmdk plus ui-react-hooks, ui-forms: debounce typing, abort the stale fetch. Calendar and date picker → react-day-picker plus ui-react-components, ui-react-hooks: derive highlights from two boundary dates, never per-cell state. Modal, dialog, drawer → Radix Dialog plus ui-react-components, ui-behavior: trap focus inside, return it on close, unmount when shut. Chat and feed → subscribe in effect plus ui-react-hooks, ui-react-perf: append with functional updates, pin scroll with a ref, unsubscribe on unmount. Kanban drag-drop → dnd-kit plus ui-react-components, ui-react-hooks: columns hold card-id arrays, reorder by index splice, never mutate in place. Rich text editor → TipTap plus ui-react-components, code-reuse: leave the editor uncontrolled, sync content on change only, never mirror keystrokes in React state. Media player → refs plus ui-react-hooks, ui-behavior: drive sliders through refs, never setState per frame. Accordion and tree sidebar → Radix Accordion plus ui-react-components, ui-behavior: one expanded id in state, never a boolean per item. Humans get the library's accessible piece with real labels and visible states.

## Checks

- library picked before hand-building
- widget built in the pinned shape
- only named leaves read per widget
- controls labeled with visible states
