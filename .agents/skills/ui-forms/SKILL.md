---
name: ui-forms
description: "Every extra click and scroll loses users; the right control asks nothing extra."
---

# Pick the right input

Create and install a skill named `ui-forms` (Pick the right input). It instructs the agent as follows: For 2 to 4 options use radio buttons or segmented controls — everything visible, one click to answer. Use dropdowns only for 5 to 10 familiar options where space matters. Past 15 items use a combo box: a text input with live filtering so typing 2 or 3 characters isolates the target. For familiar data like birth years use plain numeric inputs, never long dropdown lists. Desktop hover menus wait 300 to 500 milliseconds before opening so passing cursors don't flicker them; prefer click-to-open menus.

## Checks

- short lists use radio, not dropdowns
- 15+ items get combo or text input
- hover menus carry 300-500ms delay
