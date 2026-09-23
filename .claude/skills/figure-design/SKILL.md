---
name: figure-design
description: "Generate explanatory figures (diagrams, architecture views, flows, networks, timelines, matrices, funnels, annotated screenshots and small charts) as verified SVG using this repository's figura library. Use whenever a diagram or visualization would explain something better than prose, or when asked to draw, diagram, visualize or illustrate a system, process or result."
---

# Figures

Draw with `core/figura`. Read `docs/why.md` once; it explains why the API is shaped this way.

## Procedure

1. **Say the claim in one sentence.** The figure argues that sentence or it should not exist.
2. **Pick the recipe from `docs/recipes.md`** by what the claim argues, not by what looks nice.
   Layering, sequence, relationships, time, coverage, judgement, narrowing, quantity, a real image.
3. **Write a script** in the project's figure directory: build a `Canvas`, call the recipe, and
   pass real values. Invent nothing.
4. **Verify in the script**: `assert not [f for f in c.verify() if f.level == "error"]`. A figure
   that cannot pass its own check does not ship.
5. **Render the PNG and look at it.** The checker catches collisions; only looking catches a box
   three times taller than its content, an axis labelled 35.65, or a figure that argues nothing.
6. **Re-run `node verify/measure.mjs`** when the face is unusual or a box is tight.

## Rules

- Measure text (`figura.text`) before placing it; never guess a width.
- Compute positions from `figura.geom`; never nudge a number until it looks right.
- Ask for roles (`c.c("accent")`), never hex, so themes keep working.
- Mark anything a label must not cover with `keep_clear=True`.
- One accent; status colours only for status; planned work drawn differently from shipped work.
- Fix defects in the recipe, not in the one figure: every other figure improves.

## Not this library

Statistical charting, automatic layout of large graphs, animation. See `docs/alternatives.md`.
