"""Numbered steps: a process read left to right, or top to bottom."""
from .core import fit_text

def steps(g, items, x, y, w, h, gap=90, vertical=False, numbered=True, accent_last=True):
    """items: list of dicts {title, body, scope, output} - every key optional but title."""
    n = len(items)
    size = (h if vertical else w)
    extent = (size - gap * (n - 1)) / n
    centres = []
    for i, it in enumerate(items):
        last = accent_last and i == n - 1
        if vertical: bx, by, bw, bh = x, y + i * (extent + gap), w, extent
        else:        bx, by, bw, bh = x + i * (extent + gap), y, extent, h
        g.rect(bx, by, bw, bh, g.c("tint") if last else g.c("surface"),
               g.c("line") if last else g.c("hairline-strong"), r=12)
        if it.get("scope"): g.chip(bx + bw/2, by - 32, it["scope"], dark=True)
        if numbered:
            g.E(f'<circle cx="{bx+56:.0f}" cy="{by+52:.0f}" r="22" fill="{g.c("accent")}"/>')
            g.text(bx + 56, by + 60, str(i + 1), size=22, weight=600, fill=g.c("surface"))
        ts = fit_text(it["title"], 27, bw - 140)
        g.text(bx + 92, by + 61, it["title"], size=ts, weight=600, anchor="start")
        if it.get("body"): g.block(bx + bw/2, by + bh - 64, it["body"], 19, bw - 90, fill=g.c("ink-2"))
        if it.get("output"):
            g.block_arrow(bx + bw/2, by + bh + 16, bx + bw/2, by + bh + 62, w=22, hw=44, hl=14)
            g.pill(bx + bw/2, by + bh + 92, it["output"], kind="deep" if last else "plain", size=17, w=None, h=36)
        centres.append((bx + bw/2, by + bh/2))
        if i and not vertical:
            g.block_arrow(bx - gap + 12, by + bh/2, bx - 12, by + bh/2, w=30, hw=58, hl=20)
        if i and vertical:
            g.block_arrow(bx + bw/2, by - gap + 12, bx + bw/2, by - 12, w=30, hw=58, hl=20)
    return centres
