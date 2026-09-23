from ..geom import Rect, row
from .. import shapes
from ..text import fit_size, text_width

def stack(c, layers, area=None, style="platform", gap=64, label_side="auto", arrow="up", arrow_label=None):
    """layers: top-down list of dicts {name, items?, tone?, dash?, note?}.

    style="platform" draws three-quarter view (use only when layering is the argument),
    style="band" draws flat bands (safer default).
    """
    area = area or c.area
    if label_side == "auto":
        widest = max((text_width(L.get("name", "").upper(), 16, tracking=2) for L in layers), default=0)
        label_side = "left" if area.x - widest - 24 > 8 else "above"
    n = len(layers)
    h = (area.h - gap * (n - 1)) / n
    boxes = []
    for i, L in enumerate(layers):
        r = Rect(area.x, area.y + i * (h + gap), area.w, h)
        tone = L.get("tone", "soft" if L.get("accent") else "plain")
        if style == "platform":
            shapes.platform(c, r, tone=tone, dash=L.get("dash"))
        else:
            c.rect(r, c.c("accent-soft") if tone == "soft" else c.c("surface"),
                   c.c("edge-soft") if tone == "soft" else c.c("edge"),
                   dash=L.get("dash"))
        if L.get("name"):
            if label_side == "left":
                c.text(area.x - 24, r.cy + 6, L["name"].upper(), size=16, weight=600, anchor="end",
                       tracking=2, fill=c.c("accent") if tone == "soft" else c.c("ink-3"))
            else:
                # "above" labels sit at the left end of the band: the centre is where arrows run
                c.text(r.x + 4, r.y - 14, L["name"].upper(), size=16, weight=600, tracking=2,
                       anchor="start", fill=c.c("accent") if tone == "soft" else c.c("ink-3"))
        items = L.get("items") or []
        if items:
            inner = Rect(r.x + r.w * 0.06, r.y + 18, r.w * 0.88, r.h - 36)
            cells = row(inner, len(items), gap=18)
            for cell, it in zip(cells, items):
                if isinstance(it, str): it = {"label": it}
                shapes.box(c, cell, it["label"], it.get("body"), tone=it.get("tone", "plain"),
                           title_size=min(22, fit_size(it["label"], cell.w - 28, 22)))
        if L.get("note"):
            c.text(r.x2 + 20, r.cy + 5, L["note"], size=15, anchor="start", fill=c.c("ink-3"))
        boxes.append(r)
        if i:
            prev = boxes[i - 1]
            p1 = (r.cx, r.y - 12); p2 = (prev.cx, prev.y2 + 14)
            a, b = (p1, p2) if arrow == "up" else (p2, p1)
            shapes.arrow(c, a, b, kind="block", width=22, label=arrow_label if i == 1 else None)
    return boxes
