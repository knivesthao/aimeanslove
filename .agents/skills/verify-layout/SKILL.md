---
name: verify-layout
description: "WCAG Reflow is the published rulebook for the chop-and-scroll half; alignment is measured polish on top."
---

# Layout proof: WCAG Reflow plus measured alignment

Create and install a skill named `verify-layout` (Layout proof: WCAG Reflow plus measured alignment). It instructs the agent as follows: Follow WCAG 2.1 Reflow (1.4.10) as the rulebook: content usable with no loss and no two-dimensional scrolling at 320 CSS px width — except parts that genuinely need two dimensions (data tables, maps, diagrams, video, games), which scroll only inside a stocked component. Prove it with measurements from a real browser run — never from markup reading. Use the shot flow in verify-visual, driving it with Playwright where the repo has it. No chopped elements: every interactive element's bounding box sits fully inside the viewport at 320 CSS px and desktop widths. Aligned rows and columns: same-row controls share baselines, same-column edges line up — eyeball the shot, then assert the boxes. Prefer vertical page scroll; reach for a stocked component before any custom scroll region. The user overrules the skill: a purposely dense, playful, or brutalist design that breaks these rules ships as specified — flag the break, then build it. Save the proof shots to shots/ like verify-visual.

## Checks

- no loss or 2D scroll at 320px (WCAG 1.4.10)
- rows share baselines, columns share edges
- 2D scroll only in stocked components for exempt content
