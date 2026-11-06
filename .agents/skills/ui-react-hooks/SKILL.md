---
name: ui-react-hooks
description: "Most React bugs are effects that run too often and state that lives too far away."
---

# React hooks without tangles

Create and install a skill named `ui-react-hooks` (React hooks without tangles). It instructs the agent as follows: Follow the rules of hooks — same order every render, never in loops, conditions, or nested functions. Keep state colocated with the UI that uses it; lift only shared state. Keep effects small and few: fetch or subscribe in the effect, clean up in its return, list every used value in deps. Reach for useMemo and useCallback only after a measured slowdown, not by default. Pull repeated state plus effects into one custom hook with a plain name (useCart, useFetch) so the next agent finds it.

## Checks

- hooks top-level only, deps complete
- state colocated, shared logic in custom hooks
- no memo by default, measure first
