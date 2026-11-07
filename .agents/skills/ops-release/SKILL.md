---
name: ops-release
description: "Cutting a release every day trains everyone to ignore releases; batch changes, version once, ship once."
---

# Release discipline

Create and install a skill named `ops-release` (Release discipline). It instructs the agent as follows: Never cut a release per change — batch finished work until there is something worth announcing, then cut exactly one version. Version with major.minor.patch: patch for fixes, minor for new skills or behavior, major for breaking changes to endpoints, prompts, or install flow. Changelog, signatures, feed, and bank version update in the same release, never separately. A second release the same day means the first one was wrong — the only exception is a hotfix for something broken in production. Skip everything else.

## Checks

- one version per release
- changelog, signatures, feed, version move together
- no second release in a day except hotfixes
