---
name: code-plan
description: "A written plan turns a context-blowing marathon into small steps that each fit in context."
---

# Long tasks: plan file first

Create and install a skill named `code-plan` (Long tasks: plan file first). It instructs the agent as follows: When a task needs several skills or more steps than fit comfortably in one pass, stop and write the plan down first: one markdown file with numbered steps, each step naming the skill it uses and its exact done-state. Then execute the file top to bottom, checking steps off, re-reading only the skill each step names. If a step fails, fix the step — never rewrite the plan mid-flight without saying why. Delete the plan file when done so it can't rot into documentation.

## Checks

- plan file written before executing
- each step names its skill and done-state
- plan deleted after landing
