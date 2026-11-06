---
name: code-plan
description: "One batched fetch plus parallel independents beats sequential steps that each re-read."
---

# Plan once, fetch once, run wide

Create and install a skill named `code-plan` (Plan once, fetch once, run wide). It instructs the agent as follows: When a task needs several skills, plan before executing. Five steps or fewer in one live session: keep the numbered list inline and skip the file. Longer or interruptible: write one markdown file with numbered steps, each naming its skill and its exact done-state. Mark each step independent or blocked (naming the step it waits for); execute all unblocked steps together, sequential only where one step's output feeds the next. Fetch every named skill once during planning, in one batched request — execution fetches nothing. If a step fails, fix the step — never rewrite the plan mid-flight without saying why. Delete the plan file when done so it can't rot into documentation.

## Checks

- file only when long or interruptible
- independents run together, dependents wait
- all skills fetched once up front, none during execution
- plan deleted after landing
