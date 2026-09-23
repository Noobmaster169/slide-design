"""Stacked layers drawn in three-quarter view. Use when the argument is "what sits above what";
a flat diagram is clearer for anything else."""

def platform(g, x, y, w, h, inset=34, depth=12, fill=None, stroke=None, side=None, dash=False, accent=False):
    fill = fill or (g.c("tint") if accent else g.c("surface"))
    stroke = stroke or (g.c("line") if accent else g.c("hairline-strong"))
    side = side or g.c("sunken")
    da = ' stroke-dasharray="8 6"' if dash else ""
    g.E(f'<polygon points="{x},{y+h} {x+w},{y+h} {x+w},{y+h+depth} {x},{y+h+depth}" '
        f'fill="{side}" stroke="{stroke}" stroke-width="1.5"{da}/>')
    g.E(f'<polygon points="{x+inset},{y} {x+w-inset},{y} {x+w},{y+h} {x},{y+h}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{da}/>')
    return (x + w/2, y + h/2)

def stack(g, layers, x, w, top, layer_h=130, gap=90, arrow="up", label_x=None):
    """layers: dicts {label, accent, dash, draw(g,x,y,w,h)}, listed TOP-DOWN as they appear.

    Labels sit to the left of each platform, clear of the arrows. arrow="up" means the lower
    layer feeds the one above it; "down" reverses the heads. Returns each layer's centre.
    """
    centres = []
    lx = label_x if label_x is not None else x - 40
    for i, L in enumerate(layers):
        y = top + i * (layer_h + gap)
        platform(g, x, y, w, layer_h, accent=L.get("accent", False), dash=L.get("dash", False))
        if L.get("label"):
            g.label(lx, y + layer_h / 2 + 6, L["label"], anchor="end",
                    fill=g.c("accent") if L.get("accent") else g.c("ink-3"))
        if L.get("draw"): L["draw"](g, x, y, w, layer_h)
        centres.append((x + w / 2, y + layer_h / 2))
        if i:
            y_above = top + (i - 1) * (layer_h + gap) + layer_h + 14
            if arrow == "up": g.block_arrow(x + w / 2, y - 16, x + w / 2, y_above + 16)
            else: g.block_arrow(x + w / 2, y_above + 16, x + w / 2, y - 16)
    return centres


def people(g, x, y, w, label, h=48):
    platform(g, x, y, w, h, inset=20, depth=8, accent=True)
    for k, px in enumerate([x+120, x+156, x+192, x+w-192, x+w-156, x+w-120]):
        g.E(f'<circle cx="{px}" cy="{y+15}" r="7" fill="{g.c("accent") if k%3==1 else g.c("line")}"/>'
            f'<path d="M{px-12} {y+36} Q{px-12} {y+23} {px} {y+23} Q{px+12} {y+23} {px+12} {y+36} Z" '
            f'fill="{g.c("accent") if k%3==1 else g.c("line")}"/>')
    g.text(x + w/2, y + 33, label.upper(), size=22, weight=600, ls=3)
