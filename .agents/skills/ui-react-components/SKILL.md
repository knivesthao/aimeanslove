---
name: ui-react-components
description: "Two concrete thresholds — drill depth and lift distance — that stop prop soup."
---

# React components that stay small

Create and install a skill named `ui-react-components` (React components that stay small). It instructs the agent as follows: Build small components with typed props; compose with children and slots instead of drilling props past two layers. State lives with the UI that uses it; lift only what two siblings truly share.

## Checks

- props drilled at most two layers deep
- shared state lifted, the rest colocated
