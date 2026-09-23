# Figure recipes

Each takes data and returns a drawing that has already sized and placed its own labels.

| Recipe | Argues | Key parameters | Do not use when |
|---|---|---|---|
| `layers.stack` | what sits above what | `style="band"` or `"platform"`, `arrow` | there is no real layering |
| `flow.pipeline` | a sequence of stages | `stages[{name, scope, body, output, draw}]` | the steps are not ordered |
| `network.hub` | one thing and what it touches | `edge_labels` | more than ~8 spokes |
| `network.mesh` | a small, designed graph | `nodes` as fractional positions | you want automatic layout |
| `timeline.milestones` | when things happened | `done_until` | intervals are uneven and unlabelled |
| `timeline.phases` | proportional periods | `weight`, `current` | phases do not have durations |
| `matrix.grid` | items on a few dimensions | booleans, 0..1 shading, chips | more than ~8 columns |
| `quadrant.plot` | two axes of judgement | `x`, `y` in 0..1, `highlight` | the axes are actually measurable data |
| `funnel.funnel` | narrowing quantities | `value` per stage | stages are not subsets of each other |
| `chart.bars` / `columns` / `lines` / `stat` | numbers | `emphasis`, `reference` | you need statistical charting; bring a library |
| `annotate.image` / `points` | a real image explained | `at` as fractional coordinates | the image is a drawing of the thing |

## The `draw` hook

`flow.pipeline` accepts `draw(c, rect)` per stage, and `matrix.grid` accepts `cell_render`. This is
where a figure stops being three words in three rectangles: a stage can show a miniature of its own
work, and a cell can show whatever a cell should show.

```python
def sketch(c, r):
    for i in range(3):
        c.rect(Rect(r.x + i * 46, r.y, 38, 50), c.c("surface"), c.c("edge"), r=4)

flow.pipeline(c, [{"name": "Collect", "draw": sketch, "output": "batch"}, ...])
```

## Composing

Recipes take an `area`, so several fit on one canvas: a matrix beside a quadrant, a chart under a
flow. Nothing stops you drawing straight onto the canvas around them with `shapes`.
