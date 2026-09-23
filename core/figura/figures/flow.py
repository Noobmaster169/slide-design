from ..geom import Rect, row
from .. import shapes
from ..text import fit_block, fit_size

def pipeline(c, stages, area=None, gap=80, numbered=True, vertical=False, show_io=True):
    """stages: list of dicts {name, body?, scope?, output?, tone?, draw?}.

    draw(c, rect) paints the stage's own small picture inside the box, which is what stops a
    pipeline diagram from being three words in three rectangles.
    """
    area = area or c.area
    n = len(stages)
    boxes = []
    if vertical:
        h = (area.h - gap * (n - 1)) / n
        rects = [Rect(area.x, area.y + i * (h + gap), area.w, h) for i in range(n)]
    else:
        rects = row(area, n, gap=gap)
        # Size the boxes to their content and centre the row: an empty box is a design defect,
        # not a neutral choice.
        w = rects[0].w
        sketch_h = 150 if any(st.get("draw") for st in stages) else 0
        body_h = 0
        for st in stages:
            if st.get("body"):
                size, lines = fit_block(st["body"], w - 56, 90, 17)
                body_h = max(body_h, len(lines) * size * 1.3)
        natural = 96 + sketch_h + body_h + 34
        h = min(area.h - (86 if any(st.get("output") for st in stages) else 0), natural)
        top = area.y + max(0, (area.h - h - (86 if any(st.get("output") for st in stages) else 0)) / 2)
        rects = [Rect(r.x, top, r.w, h) for r in rects]
    for i, (r, st) in enumerate(zip(rects, stages)):
        tone = st.get("tone", "soft" if i == n - 1 else "plain")
        shapes.box(c, r, None, None, tone=tone)
        if st.get("scope"):
            shapes.chip(c, r.cx, r.y - 20, st["scope"], tone="dark")
        if numbered:
            shapes.badge(c, r.x + 44, r.y + 44, i + 1)
            c.text(r.x + 76, r.y + 52, st["name"], size=fit_size(st["name"], r.w - 110, 24),
                   weight=600, anchor="start")
        else:
            c.text(r.cx, r.y + 46, st["name"], size=fit_size(st["name"], r.w - 60, 24), weight=600)
        if st.get("draw"):
            body_space = 52 if st.get("body") else 16
            st["draw"](c, Rect(r.x + 24, r.y + 84, r.w - 48, r.h - 84 - body_space))
        if st.get("body"):
            size, lines = fit_block(st["body"], r.w - 56, 60, 17)
            for k, ln in enumerate(lines):
                c.text(r.cx, r.y2 - 28 - (len(lines) - 1 - k) * size * 1.3, ln, size=size, fill=c.c("ink-2"))
        if show_io and st.get("output"):
            shapes.arrow(c, (r.cx, r.y2 + 10), (r.cx, r.y2 + 48), kind="block", width=18)
            shapes.pill(c, r.cx, r.y2 + 74, st["output"], tone="deep" if i == n - 1 else "plain", size=15)
        if i:
            p = rects[i - 1]
            if vertical: shapes.arrow(c, (p.cx, p.y2 + 10), (r.cx, r.y - 10), kind="block")
            else: shapes.arrow(c, (p.x2 + 12, p.cy), (r.x - 12, r.cy), kind="block")
        boxes.append(r)
    return boxes
