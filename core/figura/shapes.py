"""Shapes that size themselves to their content.

Every shape here measures its label first: a box grows to fit its text, a pill's width comes from
its string, a callout picks a side that is free. That is the difference between a figure that was
generated and one that looks drawn.
"""
from .geom import Rect, edge_point, place_label
from .text import text_width, fit_size, fit_block, wrap

def box(c, r: Rect, title=None, body=None, tone="plain", title_size=22, body_size=16, pad=16, keep_clear=False):
    fills = {
        "plain":  (c.c("surface"), c.c("edge"), c.c("ink"), c.c("ink-2")),
        "soft":   (c.c("accent-soft"), c.c("edge-soft"), c.c("ink"), c.c("accent")),
        "accent": (c.c("accent"), c.c("accent"), c.c("surface"), "#E8F0FE"),
        "deep":   (c.c("accent-deep"), c.c("accent-deep"), c.c("surface"), "#D8E4FB"),
        "muted":  (c.c("sunken"), c.c("hairline"), c.c("ink-2"), c.c("ink-3")),
        "ghost":  ("none", c.c("edge"), c.c("ink-2"), c.c("ink-3")),
    }
    fill, stroke, tc, sc = fills[tone]
    c.rect(r, fill, stroke, keep_clear=keep_clear)
    inner = r.w - 2 * pad
    if title and body:
        ts = fit_size(title, inner, title_size)
        c.text(r.cx, r.cy - 4, title, size=ts, weight=600, fill=tc)
        bs, lines = fit_block(body, inner, r.h / 2 - pad, body_size)
        for i, ln in enumerate(lines):
            c.text(r.cx, r.cy + 22 + i * bs * 1.3, ln, size=bs, fill=sc)
    elif title:
        ts = fit_size(title, inner, title_size)
        c.text(r.cx, r.cy + ts * 0.34, title, size=ts, weight=600, fill=tc)
    return r

def pill(c, cx, cy, label, tone="accent", size=16, h=34, min_w=0, pad=20):
    w = max(min_w, text_width(label, size) + 2 * pad)
    r = Rect(cx - w / 2, cy - h / 2, w, h)
    fills = {"accent": (c.c("accent"), c.c("surface")), "deep": (c.c("accent-deep"), c.c("surface")),
             "plain": (c.c("surface"), c.c("ink")), "muted": (c.c("sunken"), c.c("ink-2")),
             "good": (c.c("good"), c.c("surface")), "warn": (c.c("warn"), c.c("surface"))}
    fill, tc = fills[tone]
    c.rect(r, fill, c.c("edge") if tone in ("plain", "muted") else fill, r=h / 2)
    c.text(cx, cy + size * 0.35, label, size=size, weight=500, fill=tc)
    return r

def chip(c, cx, cy, label, size=14, tone="muted"):
    w = text_width(label, size, "mono") + 22
    r = Rect(cx - w / 2, cy - 13, w, 26)
    fill = {"muted": c.c("sunken"), "dark": c.c("ink-2"), "soft": c.c("accent-soft")}[tone]
    tc = {"muted": c.c("ink-2"), "dark": c.c("surface"), "soft": c.c("accent")}[tone]
    c.rect(r, fill, c.c("hairline") if tone == "muted" else fill, r=13)
    c.text(cx, cy + size * 0.35, label, size=size, fill=tc, face="mono")
    return r

def arrow(c, p1, p2, kind="thin", label=None, color=None, dash=None, both=False, width=26):
    """kind: thin (a relation), block (a flow between stages), elbow (orthogonal routing)."""
    import math
    col = color or c.c("edge")
    (x1, y1), (x2, y2) = p1, p2
    if kind == "block":
        vertical = abs(y2 - y1) > abs(x2 - x1)
        hw, hl, a = width * 1.9, width * 0.8, width / 2
        if vertical:
            d = 1 if y2 > y1 else -1; base = y2 - d * hl; start = y1 + (d * hl if both else 0)
            pts = [(x1-a,start),(x1-a,base),(x1-hw/2,base),(x1,y2),(x1+hw/2,base),(x1+a,base),(x1+a,start)]
            if both: pts += [(x1+hw/2,start),(x1,y1),(x1-hw/2,start)]
        else:
            d = 1 if x2 > x1 else -1; base = x2 - d * hl; start = x1 + (d * hl if both else 0)
            pts = [(start,y1-a),(base,y1-a),(base,y1-hw/2),(x2,y1),(base,y1+hw/2),(base,y1+a),(start,y1+a)]
            if both: pts += [(start,y1+hw/2),(x1,y1),(start,y1-hw/2)]
        d_attr = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts) + " Z"
        box = Rect(min(p[0] for p in pts), min(p[1] for p in pts),
                   max(p[0] for p in pts) - min(p[0] for p in pts),
                   max(p[1] for p in pts) - min(p[1] for p in pts))
        c.path(d_attr, stroke=c.c("edge-soft"), fill=c.c("accent-soft"), sw=1.5, box=box, keep_clear=True, dash=dash)
    elif kind == "elbow":
        from .geom import elbow
        c.path(elbow(p1, p2), stroke=col, sw=2.2, dash=dash)
        _head(c, (x2, y2), math.atan2(0, 1 if x2 > x1 else -1), col)
    else:
        c.line(p1, p2, col, 2.2, dash=dash)
        _head(c, p2, math.atan2(y2 - y1, x2 - x1), col)
        if both: _head(c, p1, math.atan2(y1 - y2, x1 - x2), col)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        chip(c, mx, my, label, tone="dark")
    return (x2, y2)

def _head(c, p, angle, col, size=9):
    import math
    x, y = p
    a1, a2 = angle + math.pi * 0.82, angle - math.pi * 0.82
    c.path(f"M{x + size*2*math.cos(a1):.0f} {y + size*2*math.sin(a1):.0f} L{x:.0f} {y:.0f} "
           f"L{x + size*2*math.cos(a2):.0f} {y + size*2*math.sin(a2):.0f}", stroke=col, sw=2.2)

def platform(c, r: Rect, tone="plain", inset=0.035, depth=12, dash=None):
    """A layer seen in three-quarter view. Only when 'above and below' is the point."""
    fills = {"plain": (c.c("surface"), c.c("edge")), "soft": (c.c("accent-soft"), c.c("edge-soft")),
             "muted": (c.c("sunken"), c.c("hairline"))}
    fill, stroke = fills[tone]
    ins = r.w * inset
    c.path(f"M{r.x:.0f} {r.y2:.0f} H{r.x2:.0f} V{r.y2+depth:.0f} H{r.x:.0f} Z",
           fill=c.c("sunken"), stroke=stroke, sw=1.4, dash=dash)
    c.path(f"M{r.x+ins:.0f} {r.y:.0f} H{r.x2-ins:.0f} L{r.x2:.0f} {r.y2:.0f} H{r.x:.0f} Z",
           fill=fill, stroke=stroke, sw=1.4, dash=dash,
           box=Rect(r.x, r.y, r.w, r.h))
    return r

def callout(c, target: Rect, text, avoid, bounds, size=15, max_w=220, side_order=("right", "top", "bottom", "left")):
    """A note pointing at something, placed where it does not collide."""
    lines = wrap(text, size, max_w)
    w = max(text_width(l, size) for l in lines) + 24
    h = len(lines) * size * 1.35 + 18
    r, side = place_label(target, w, h, avoid, bounds, gap=18, order=side_order)
    c.rect(r, c.c("surface"), c.c("edge"), r=8)
    for i, ln in enumerate(lines):
        c.text(r.x + 12, r.y + 20 + i * size * 1.35, ln, size=size, anchor="start", fill=c.c("ink-2"))
    anchor = edge_point(r, target.center)
    c.line(anchor, edge_point(target, r.center), c.c("edge"), 1.6, dash="4 3")
    return r

def badge(c, cx, cy, n, r=18, tone="accent"):
    c.circle(cx, cy, r, fill=c.c(tone))
    c.text(cx, cy + r * 0.36, str(n), size=r * 1.05, weight=600, fill=c.c("surface"))
    return Rect(cx - r, cy - r, 2 * r, 2 * r)

def legend(c, x, y, items, size=15, gap=26):
    """items: list of (label, color) or (label, color, 'dashed')."""
    cx = x
    for it in items:
        label, color = it[0], it[1]
        style = it[2] if len(it) > 2 else None
        if style == "dashed":
            c.rect(Rect(cx, y - 9, 26, 18), "none", color, r=4, dash="4 3")
        else:
            c.rect(Rect(cx, y - 9, 26, 18), color, color, r=4)
        c.text(cx + 34, y + size * 0.35, label, size=size, anchor="start", fill=c.c("ink-2"))
        cx += 34 + text_width(label, size) + gap
    return Rect(x, y - 12, cx - x, 24)
