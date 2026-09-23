"""Charts with the design decisions already made: thin marks, one accent, recessive axes, direct
labels where they help, and the value printed next to the mark rather than on a second axis.

For anything beyond these forms, use a charting library and bring the SVG in; the point here is
that a number in a figure should not need a second tool.
"""
from ..geom import Rect
from .. import shapes
from ..style import ensure_contrast
from ..text import text_width, fit_size

def nice_ticks(mx, count=4):
    """Round axis steps. An axis labelled 35.65 tells the reader the tool picked the number."""
    import math
    if mx <= 0: return [0], 1
    raw = mx / (count - 1)
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    top = step * math.ceil(mx / step)
    return [step * i for i in range(int(top / step) + 1)], top


def _nice(v):
    return f"{v:,.0f}" if abs(v) >= 100 or float(v).is_integer() else f"{v:,.2f}".rstrip("0").rstrip(".")

def bars(c, items, area=None, label_w=280, max_value=None, value_fmt=_nice, reference=None, bar_h=34):
    """Horizontal bars, one series. items: list of dicts {label, value, tone?, note?}."""
    area = area or c.area
    mx = max_value or max(i["value"] for i in items) * 1.08
    n = len(items)
    gap = max(14, (area.h - n * bar_h) / max(1, n - 1)) if n > 1 else 0
    plot_x = area.x + label_w
    plot_w = area.w - label_w - 120
    if reference is not None:
        rx = plot_x + plot_w * (reference["value"] / mx)
        c.line((rx, area.y - 8), (rx, area.y + n * (bar_h + gap)), c.c("edge"), 1.5, dash="5 4")
        c.text(rx, area.y - 18, reference.get("label", ""), size=14, fill=c.c("ink-3"))
    for i, it in enumerate(items):
        y = area.y + i * (bar_h + gap)
        c.text(area.x + label_w - 20, y + bar_h / 2 + 6, it["label"],
               size=fit_size(it["label"], label_w - 30, 18), anchor="end",
               weight=600 if it.get("emphasis") else 400,
               fill=c.c("ink") if it.get("emphasis") else c.c("ink-2"))
        w = plot_w * (it["value"] / mx)
        tone = it.get("tone") or ("accent" if it.get("emphasis") or i == 0 else "edge")
        c.rect(Rect(plot_x, y, w, bar_h), c.c(tone), "none", r=6)
        c.text(plot_x + w + 14, y + bar_h / 2 + 6, value_fmt(it["value"]), size=17, anchor="start",
               face="mono", fill=c.c("ink"))
        if it.get("note"):
            c.text(plot_x + w + 14, y + bar_h / 2 + 26, it["note"], size=13, anchor="start", fill=c.c("ink-3"))
    c.line((plot_x, area.y - 10), (plot_x, area.y + n * (bar_h + gap) - gap + 10), c.c("edge"), 1.5)
    return area

def columns(c, items, area=None, max_value=None, value_fmt=_nice, baseline_label=None):
    """Vertical columns for a small number of categories."""
    area = area or c.area
    mx = max_value or max(i["value"] for i in items) * 1.15
    n = len(items)
    cw = area.w / n
    bw = min(cw * 0.55, 110)
    for i, it in enumerate(items):
        x = area.x + cw * (i + 0.5)
        h = (area.h - 60) * (it["value"] / mx)
        r = Rect(x - bw / 2, area.y2 - 40 - h, bw, h)
        c.rect(r, c.c(it.get("tone", "accent" if it.get("emphasis") else "edge-soft")), "none", r=6)
        c.text(x, r.y - 12, value_fmt(it["value"]), size=17, face="mono")
        c.text(x, area.y2 - 12, it["label"], size=fit_size(it["label"], cw - 12, 17), fill=c.c("ink-2"))
    c.line((area.x, area.y2 - 40), (area.x2, area.y2 - 40), c.c("edge"), 1.5)
    if baseline_label:
        c.text(area.x, area.y2 - 48, baseline_label, size=13, anchor="start", fill=c.c("ink-3"))
    return area

def lines(c, series, area=None, x_labels=None, y_max=None, y_fmt=_nice, direct_labels=True):
    """series: list of dicts {name, values:[...], tone?}. One axis only; never two scales."""
    area = area or c.area
    plot = Rect(area.x + 60, area.y + 10, area.w - 180, area.h - 70)
    n = max(len(s["values"]) for s in series)
    ticks, mx = nice_ticks(y_max or max(max(s["values"]) for s in series) * 1.08)
    for t in ticks:
        gy = plot.y2 - plot.h * (t / mx)
        c.line((plot.x, gy), (plot.x2, gy), c.c("hairline"), 1)
        c.text(plot.x - 14, gy + 5, y_fmt(t), size=14, anchor="end", fill=c.c("ink-3"), face="mono")
    for si, s in enumerate(series):
        col = c.c(s["tone"]) if s.get("tone") else c.series(si)
        pts = [(plot.x + plot.w * i / (n - 1), plot.y2 - plot.h * (v / mx)) for i, v in enumerate(s["values"])]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        c.path(d, stroke=col, sw=2.6)
        c.circle(*pts[-1], 5, fill=col)
        if direct_labels:
            c.text(pts[-1][0] + 14, pts[-1][1] + 5, s["name"], size=16, anchor="start",
                   fill=ensure_contrast(col, c.background), weight=600)
    if x_labels:
        for i, lab in enumerate(x_labels):
            c.text(plot.x + plot.w * i / (n - 1), plot.y2 + 28, lab, size=14, fill=c.c("ink-3"))
    return area

def stat(c, area, value, label, note=None, tone="accent"):
    """One number, said once, at the size it deserves."""
    size = min(int(area.h * 0.52), int(area.w / max(3, len(str(value))) * 1.5))
    c.text(area.cx, area.cy + size * 0.18, str(value), size=size, weight=400, face="display", fill=c.c(tone))
    c.text(area.cx, area.cy + size * 0.62, label, size=max(15, int(size * 0.17)), fill=c.c("ink-2"))
    if note:
        c.text(area.cx, area.cy + size * 0.62 + 24, note, size=14, fill=c.c("ink-3"))
    return area
