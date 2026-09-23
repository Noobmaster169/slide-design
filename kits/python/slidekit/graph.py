"""Nodes and labelled edges. Use when relationships are the point; keep it under a dozen nodes,
and put the emphasised node in the centre so the eye lands there."""
import math

def hub(g, cx, cy, centre, spokes, r=260, node_w=170, label_edges=None, label_at=0.72, start=-math.pi/2):
    """Spokes on an ellipse around a centre node.

    label_at places an edge label as a fraction of the way from centre to node; keep it well past
    0.5 so labels do not pile up around the middle. Keep a hub under about eight spokes.
    """
    pos = {}
    rx, ry = r * 1.9, r * 1.15
    for i, name in enumerate(spokes):
        a = start + i * 2 * math.pi / len(spokes)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        pos[name] = (x, y)
        g.line(cx, cy, x, y, g.c("line"), 2.5)
        if label_edges and name in label_edges:
            g.chip(cx + (x - cx) * label_at, cy + (y - cy) * label_at, label_edges[name], dark=True)
    for name, (x, y) in pos.items():
        g.pill(x, y, name, kind="accent", size=17, w=node_w, h=34)
    g.pill(cx, cy, centre, kind="deep", size=24, w=max(230, node_w + 80), h=54)
    return pos

def edges(g, pos, pairs):
    """pairs: list of (a, b) or (a, b, label) between already-placed nodes."""
    for p in pairs:
        (a, b), lab = p[:2], (p[2] if len(p) > 2 else None)
        (x1, y1), (x2, y2) = pos[a], pos[b]
        g.line(x1, y1, x2, y2, g.c("accent"), 2)
        if lab: g.chip((x1 + x2) / 2, (y1 + y2) / 2, lab, dark=True)
