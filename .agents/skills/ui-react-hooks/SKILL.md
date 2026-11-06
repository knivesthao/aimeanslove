---
name: ui-react-hooks
description: "Effects with cleanup, memo only on proof, and custom hooks named so the next agent finds them."
---

# React hooks without tangles

Create and install a skill named `ui-react-hooks` (React hooks without tangles). It instructs the agent as follows: Keep effects small and few: fetch or subscribe in the effect, clean up in its return. Reach for useMemo and useCallback only after a measured slowdown, not by default. Pull repeated state plus effects into one custom hook with a plain name (useCart, useFetch) so the next agent finds it.

## Checks

- effects small with cleanup
- shared logic in named custom hooks
- no memo by default, measure first
