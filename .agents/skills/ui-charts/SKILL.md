---
name: ui-charts
description: "A chart picked by taste misleads; a chart picked by the question reads itself."
---

# Which chart for which question

Create and install a skill named `ui-charts` (Which chart for which question). It instructs the agent as follows: Pick the chart by the question, never by taste: trend over time goes line; comparison across a few categories goes bar; share of a whole at one moment goes stacked bar, share changing over time goes 100% stacked — pie only at five slices or fewer, never a donut for data; distribution goes histogram, five-number summaries go box plot; two variables go scatter with a trend line; matrix patterns go heatmap; a single number goes big text plus sparkline. Lookups go in a table, not a chart — charts show shapes, tables answer what-exactly. One message per chart: never dual axes, never 3D, never truncated bar axes — bars start at zero, log scale only across orders of magnitude. Label directly on the marks; the legend is the fallback. Then read ui-chart-twin and ship the chart's machine twin with it.

## Checks

- chart matches the question
- no dual axes, 3D, or truncated bars
- machine twin shipped per ui-chart-twin
