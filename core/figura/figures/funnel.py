from ..geom import Rect
from .. import shapes
from ..text import text_width
from ..style import ensure_contrast

def funnel(c, stages, area=None, show_drop=True):
    """stages: list of dicts {label, value}. Widths are proportional to value, so the shape is the
    data rather than a decoration."""
    area = area or c.area
    top = max(s["value"] for s in stages)
    n = len(stages)
    h = (area.h - 18 * (n - 1)) / n
    prev = None
    for i, s in enumerate(stages):
        frac = s["value"] / top
        w = area.w * frac
        r = Rect(area.cx - w / 2, area.y + i * (h + 18), w, h)
        tone = c.c("accent") if i == 0 else c.c("accent-soft")
        c.rect(r, tone, "none", r=10)
        label_fill = c.c("surface") if i == 0 else c.c("ink")
        c.text(r.cx, r.cy - 2, s["label"], size=19, weight=600, fill=label_fill)
        c.text(r.cx, r.cy + 24, f'{s["value"]:,}', size=17, fill=label_fill, face="mono")
        if show_drop and prev is not None:
            drop = (prev - s["value"]) / prev
            label = f"-{drop:.0%}"
            room = c.w - area.x2 - 16
            if room >= text_width(label, 16, "mono") + 12:
                c.text(area.x2 + 16, r.cy + 6, label, size=16, anchor="start",
                       fill=ensure_contrast(c.c("warn") if drop > 0.4 else c.c("ink-3"), c.background), face="mono")
            else:
                c.text(r.x2 - 14, r.cy + 26, label, size=15, anchor="end",
                       fill=c.c("surface") if i == 0 else c.c("ink-2"), face="mono")
        prev = s["value"]
    return area
