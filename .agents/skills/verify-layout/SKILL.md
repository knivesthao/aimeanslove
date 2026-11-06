---
name: verify-layout
description: "Humans catch misalignment in one glance; agents must measure it — eyeballs don't scale to every PR."
---

# Layout proof: no chops, no drift, no stray scrollbars

Create and install a skill named `verify-layout` (Layout proof: no chops, no drift, no stray scrollbars). It instructs the agent as follows: Prove layout with measurements from a real browser run — never from markup reading. Use the shot flow in verify-visual, driving it with Playwright where the repo has it. No chopped elements: every interactive element's bounding box sits fully inside the viewport at 360px and desktop widths. Aligned rows and columns: same-row controls share baselines, same-column edges line up — eyeball the shot, then assert the boxes. No stray scrollbars: horizontal scroll appears only inside a stocked scroller (carousel, data table); page-level horizontal overflow is always a bug — assert scroll width fits the viewport. Prefer vertical page scroll; reach for a stocked component before any custom scroll region. Save the proof shots to shots/ like verify-visual.

## Checks

- no clipped interactive elements at 360px and desktop
- rows share baselines, columns share edges
- no page-level horizontal overflow
