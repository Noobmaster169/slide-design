"""A line with milestones. Honest about time: equal spacing means equal intervals, or say so."""
def timeline(g, items, x, y, w, done_index=None, vertical=False):
    """items: list of (label, caption). done_index: everything up to it is shipped (solid)."""
    n = len(items)
    step = w / max(1, n - 1)
    g.line(x, y, x + w, y, g.c("hairline-strong"), 3)
    for i, (label, caption) in enumerate(items):
        px = x + i * step
        shipped = done_index is not None and i <= done_index
        dash = "" if shipped else ' stroke-dasharray="4 3"'
        g.E(f'<circle cx="{px:.0f}" cy="{y:.0f}" r="13" fill="{g.c("accent") if shipped else g.c("surface")}" '
            f'stroke="{g.c("accent")}" stroke-width="3"{dash}/>')
        up = i % 2 == 0
        ty = y - 46 if up else y + 74
        g.text(px, ty, label, size=24, weight=600)
        g.block(px, ty + (-30 if up else 30), caption, 18, step * 0.95, fill=g.c("ink-2"))
