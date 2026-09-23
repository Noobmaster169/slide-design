# Verification

Two levels, same rules.

## Geometry check, no browser

```python
findings = c.verify(min_font=14, min_contrast=4.5)
```

Runs in milliseconds off the recorded bounding boxes. Use it in the figure script itself and fail
the build; the gallery does exactly this.

| Rule | Level | Catches |
|---|---|---|
| `off-canvas` | error | a label that leaves the drawing |
| `text-overlap` | error | two labels on top of each other |
| `text-occluded` | error | a label covered by a shape drawn after it |
| `text-over-shape` | error | a label on an arrow or a region marked keep-clear |
| `font-size` | warn | text too small to read at the size it will be shown |
| `contrast` | warn | text against what is actually behind it |

## Browser check, exact

```bash
node verify/measure.mjs figure.svg --min-font=14
```

Re-measures with real font metrics in Chromium. Use it when the face is unusual, when a box is
tight, or in CI as a second opinion. The estimated metrics are within a few percent for Latin text;
scripts with complex shaping need this pass.

## What neither can tell you

Whether the figure is honest, whether the form suits the argument, and whether it was worth drawing.
Render the PNG and look at it. In building this library, the checker caught label collisions and
unreadable shading; looking caught boxes that were three times taller than their content and an axis
labelled 35.65. Both passes are necessary.
