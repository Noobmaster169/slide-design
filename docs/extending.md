# Writing your own

## A figure script

```python
import sys; sys.path.insert(0, "core")
from figura.canvas import Canvas
from figura.geom import Rect
from figura import shapes
from figura.figures import flow

c = Canvas(1600, 900, theme="light")       # theme is a name in themes/ or a dict
flow.pipeline(c, [...], area=c.area.inset(40))
assert not [f for f in c.verify() if f.level == "error"]
c.save("out.svg", png=True)
```

## A new shape

Shapes take the canvas first, measure their text, draw, and return a `Rect` so callers can place
things against them.

```python
from figura.text import text_width, fit_size

def tag(c, x, y, label, tone="accent"):
    w = text_width(label, 15) + 24
    r = Rect(x - w / 2, y - 14, w, 28)
    c.rect(r, c.c(tone), "none", r=6)
    c.text(x, y + 5, label, size=15, fill=c.c("surface"))
    return r
```

Mark anything a label must not cover with `keep_clear=True` on `c.rect` or `c.path`, and the
verifier will enforce it.

## A new recipe

A recipe is a function `(canvas, data, area=None, **options) -> boxes`. Rules that keep recipes
usable by other people:

1. Accept an `area` and default to `c.area`, so it can be composed.
2. Size to content: measure text, then decide the box, never the reverse.
3. Return the boxes you drew, so callers can annotate them.
4. Ask for roles (`c.c("accent")`), never hex values, so themes work.
5. Verify a worked example in your test and let it fail the build.

## Themes

`themes/*.json` override `color`, `series`, `font` and `radius`. Every figure re-renders in a new
theme with no code change; `gallery/08-dark-and-print.py` renders one figure in three.
