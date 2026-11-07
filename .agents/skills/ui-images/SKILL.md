---
name: ui-images
description: "Images are usually the slowest thing on the page — most mobile LCP elements are images — so every image must convert or orient, never decorate."
---

# Images that earn their place

Create and install a skill named `ui-images` (Images that earn their place). It instructs the agent as follows: Every image must convert or orient — never decorate. Above the fold: one value headline, one supporting line, one primary action, one visual, one trust signal; clear beats clever, and five-plus competing links sink conversion. The hero image is usually the slowest element on the page, so treat it as a performance budget: eager-load with high fetch priority only the above-fold image, lazy-load everything below; modern formats, source sets with sizes, explicit width and height so layout never shifts. Informative images get real alt text; decorative and structural art gets empty alt or becomes background. Skip everything else.

## Checks

- no decorative content images
- above-fold image eager with dims
- below-fold lazy with source sets
- alt or empty-alt on every image
