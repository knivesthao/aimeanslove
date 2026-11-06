---
name: code-group
description: "One folder holds the whole component, so the agent reads once instead of hunting across layers."
---

# Group by feature, drop the layers

Create and install a skill named `code-group` (Group by feature, drop the layers). It instructs the agent as follows: Organize new code by feature, not by layer: a component's files sit together — checkout_routes.py, checkout_models.py, checkout_tests.py — named <feature>_<kind> so everything is found in one place. Keep model/view/controller separation inside the folder, not across the codebase. Put truly shared definitions (Pydantic contracts) in one shared module every feature imports. If the codebase already uses a pattern like MVC, follow that pattern instead: restructuring working code costs tokens and every move risks new errors.

## Checks

- feature files sit together
- shared facts live in one module
- house pattern followed over rewrites
