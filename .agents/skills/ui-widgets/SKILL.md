---
name: ui-widgets
description: "Ten widgets cover most interface work in any framework — each pins the shape agents get wrong."
---

# Common widgets: library first, pinned shape

Create and install a skill named `ui-widgets` (Common widgets: library first, pinned shape). It instructs the agent as follows: Never hand-build these ten — pick your ecosystem's stocked library (names per framework live in ui-platform-picks), build the pinned shape, and read only the named leaves. Data table → code-perf, code-reuse: page on the server where one exists, otherwise paginate client-side; render only the visible window. Multi-step wizard → ui-forms, ui-behavior: one state object at the wizard root, validate each step on exit. Combo and autocomplete → ui-forms, ui-behavior: debounce typing, abort the stale fetch. Calendar and date picker → ui-behavior, code-reuse: derive highlights from two boundary dates, never per-cell state. Modal, dialog, drawer → ui-behavior, code-reuse: trap focus inside, return it on close, unmount when shut. Chat and feed → code-perf, code-reuse: append-only updates, pin scroll to the newest message, unsubscribe on unmount. Kanban drag-drop → code-reuse, ui-behavior: columns hold card-id arrays, reorder by index splice, never mutate in place. Rich text editor → code-reuse: leave the editor uncontrolled, sync content on change only, never mirror keystrokes in component state. Media player → ui-behavior, code-reuse: drive sliders through a direct element handle, never rerender per frame. Accordion and tree sidebar → ui-behavior, ui-nav: one expanded id in state, never a boolean per item. Humans get the library's accessible piece with real labels and visible states; agents keep small typed pieces, colocated state, and stable keys around it.

## Checks

- library picked before hand-building
- widget built in the pinned shape
- only named leaves read per widget
- controls labeled with visible states
