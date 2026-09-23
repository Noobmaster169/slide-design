import math
from ..geom import Rect, radial, edge_point, place_label
from .. import shapes
from ..text import text_width
from ..geom import Rect as _R

def hub(c, centre, spokes, area=None, edge_labels=None, spoke_tone="accent", start=-math.pi/2):
    """One thing and what it touches.

    Spoke positions come from an ellipse; every pill's width is measured first, so an edge label
    can be placed in the clear gap between the two pills it belongs to instead of at a guessed
    fraction of the line.
    """
    area = area or c.area
    cx, cy = area.center
    rx, ry = area.w * 0.34, area.h * 0.32
    pts = radial(cx, cy, len(spokes), rx, ry, start)

    centre_w = text_width(centre, 22) + 60
    centre_box = Rect(cx - centre_w / 2, cy - 27, centre_w, 54)
    spoke_boxes = {}
    for (x, y), name in zip(pts, spokes):
        w = text_width(name, 16) + 40
        spoke_boxes[name] = Rect(x - w / 2, y - 18, w, 36)

    for (x, y), name in zip(pts, spokes):
        c.line((cx, cy), (x, y), c.c("edge-soft"), 2.2)

    if edge_labels:
        for (x, y), name in zip(pts, spokes):
            if name not in edge_labels: continue
            a = edge_point(centre_box, (x, y))
            b = edge_point(spoke_boxes[name], (cx, cy))
            shapes.chip(c, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, edge_labels[name], tone="dark")

    boxes = {}
    for (x, y), name in zip(pts, spokes):
        boxes[name] = shapes.pill(c, x, y, name, tone=spoke_tone, size=16, h=36)
    boxes["__centre__"] = shapes.pill(c, cx, cy, centre, tone="deep", size=22, h=54, pad=30)
    return boxes

def mesh(c, nodes, edges, area=None, node_size=16):
    """nodes: {name: (x_frac, y_frac)} in 0..1 of the area. edges: list of (a, b) or (a, b, label).

    Positions are yours: a readable network is a designed one. Labels are placed on the side of
    each node that is free.
    """
    area = area or c.area
    pos = {n: (area.x + fx * area.w, area.y + fy * area.h) for n, (fx, fy) in nodes.items()}
    for e in edges:
        (a, b), lab = e[:2], (e[2] if len(e) > 2 else None)
        c.line(pos[a], pos[b], c.c("edge-soft"), 2)
    boxes = {}
    for n, (x, y) in pos.items():
        boxes[n] = shapes.pill(c, x, y, n, tone="accent", size=node_size, h=34)
    for e in edges:
        if len(e) > 2:
            (a, b), lab = e[:2], e[2]
            (x1, y1), (x2, y2) = pos[a], pos[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            anchor = Rect(mx - 2, my - 2, 4, 4)
            w = text_width(lab, 14, "mono") + 22
            r, _ = place_label(anchor, w, 26, list(boxes.values()), area, gap=4,
                               order=("top", "bottom", "left", "right"))
            shapes.chip(c, r.cx, r.cy, lab, tone="dark")
    return boxes
