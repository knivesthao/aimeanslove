---
name: ui-charts
description: "Agents read tables; humans judge shapes — charts are the human verdict layer, not the analysis."
---

# Charts humans can read, data agents already parsed

Create and install a skill named `ui-charts` (Charts humans can read, data agents already parsed). It instructs the agent as follows: Aggregate on the server and ship only chart-ready rollups — never raw rows for the browser to group. Pick the chart by the question: trend over time goes line, comparison across few categories goes bar, parts of a whole goes stacked bar and never pie past five slices, distribution goes histogram, two variables goes scatter, live numbers go big text plus sparkline. Encode by the Cleveland-McGill ranking: position on a common scale beats length beats angle beats area beats color — bars beat pies and flat beats 3D for a measured reason (Cleveland & McGill, JASA 1984). Every chart gets what color alone can't carry: direct labels, a data table alongside (the W3C's prescribed long description for charts) plus, when interactive, a declarative Vega-Lite-style JSON spec — the agent judges and regenerates from table and spec, never from pixels — and axes that start at zero for bars. Reach for a stocked chart library (Apache ECharts, Recharts) instead of hand-drawn SVG. Humans read the shape to judge; agents already read the table — the chart convinces, the numbers underneath prove.

## Checks

- server-aggregated rollups only
- chart matches the question
- labels plus table, never color alone
