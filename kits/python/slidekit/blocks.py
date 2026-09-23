"""Boxes, rows, columns, grids. The default kit: least stylised, hardest to get wrong."""
from .core import text_width, fit_text, wrap_text

def box(g, x, y, w, h, title, sub=None, kind="plain", title_size=26, sub_size=18):
    if kind == "accent":   fill, stroke, tc, sc = g.c("accent"), g.c("accent"), g.c("surface"), g.c("tint")
    elif kind == "tint":   fill, stroke, tc, sc = g.c("tint"), g.c("line"), g.c("ink"), g.c("accent")
    elif kind == "muted":  fill, stroke, tc, sc = g.c("sunken"), g.c("hairline"), g.c("ink-2"), g.c("ink-3")
    else:                  fill, stroke, tc, sc = g.c("surface"), g.c("hairline-strong"), g.c("ink"), g.c("ink-2")
    g.rect(x, y, w, h, fill, stroke, r=10)
    ts = fit_text(title, title_size, w - 40)
    if sub:
        g.text(x + w/2, y + h/2 - 6, title, size=ts, weight=600, fill=tc)
        g.block(x + w/2, y + h/2 + sub_size + 6, sub, sub_size, w - 44, fill=sc)
    else:
        g.text(x + w/2, y + h/2 + ts*0.34, title, size=ts, weight=600, fill=tc)

def row(g, titles, y, x, w, h, gap=40, subtitles=None, accent_index=None, arrows=True, kinds=None):
    """Boxes left to right with arrows between. Returns the box centres."""
    n = len(titles)
    bw = (w - gap * (n - 1)) / n
    centres = []
    for i, t in enumerate(titles):
        bx = x + i * (bw + gap)
        kind = (kinds[i] if kinds else None) or ("accent" if i == accent_index else "plain")
        box(g, bx, y, bw, h, t, subtitles[i] if subtitles else None, kind=kind)
        centres.append((bx + bw/2, y + h/2))
        if arrows and i:
            g.block_arrow(bx - gap + 6, y + h/2, bx - 6, y + h/2, w=20, hw=40, hl=14)
    return centres

def column(g, titles, x, y, w, h, gap=24, subtitles=None, accent_index=None):
    out = []
    for i, t in enumerate(titles):
        by = y + i * (h + gap)
        box(g, x, by, w, h, t, subtitles[i] if subtitles else None,
            kind="accent" if i == accent_index else "plain")
        out.append((x + w/2, by + h/2))
    return out

def grid(g, cells, x, y, w, h, cols=3, gap=24, cell_h=None):
    """cells: list of (title, subtitle) or plain strings."""
    rows = (len(cells) + cols - 1) // cols
    cw = (w - gap * (cols - 1)) / cols
    ch = cell_h or (h - gap * (rows - 1)) / rows
    for i, c in enumerate(cells):
        t, s = (c, None) if isinstance(c, str) else c
        r, cc = divmod(i, cols)
        box(g, x + cc * (cw + gap), y + r * (ch + gap), cw, ch, t, s)
