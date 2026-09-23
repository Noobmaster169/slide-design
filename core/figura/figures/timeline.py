from ..geom import Rect
from .. import shapes
from ..text import wrap, text_width

def milestones(c, items, area=None, done_until=None, axis_label=None):
    """items: list of dicts {label, note?, at?}. at is 0..1 along the axis; even spacing if omitted.

    Shipped is solid, planned is dashed, and the difference is stated in the legend rather than
    left to colour.
    """
    area = area or c.area
    y = area.cy
    c.line((area.x, y), (area.x2, y), c.c("edge"), 3)
    n = len(items)
    for i, it in enumerate(items):
        t = it.get("at", i / max(1, n - 1))
        x = area.x + t * area.w
        done = done_until is not None and i <= done_until
        c.circle(x, y, 13, fill=c.c("accent") if done else c.c("surface"), stroke=c.c("accent"), sw=3,
                 extra="" if done else ' stroke-dasharray="4 3"')
        up = i % 2 == 0
        ty = y - 46 if up else y + 62
        c.text(x, ty, it["label"], size=21, weight=600)
        if it.get("note"):
            width = area.w / max(2, n) * 1.1
            lines = wrap(it["note"], 15, width)
            for k, ln in enumerate(lines):
                c.text(x, ty + (-26 - (len(lines) - 1 - k) * 20 if up else 26 + k * 20), ln, size=15, fill=c.c("ink-3"))
    if axis_label:
        c.text(area.x2, y + 34, axis_label, size=14, anchor="end", fill=c.c("ink-3"), face="mono")
    shapes.legend(c, area.x, area.y2 + 24, [("shipped", c.c("accent")), ("planned", c.c("accent"), "dashed")])
    return y

def phases(c, items, area=None):
    """items: list of dicts {label, weight, note?} drawn as proportional bands."""
    area = area or c.area
    total = sum(i.get("weight", 1) for i in items)
    x = area.x
    for i, it in enumerate(items):
        w = area.w * it.get("weight", 1) / total
        r = Rect(x, area.y, w - 6, area.h)
        tone = "soft" if it.get("current") else "plain"
        shapes.box(c, r, it["label"], it.get("note"), tone=tone)
        x += w
    return area
