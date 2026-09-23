from ..geom import Rect, place_label
from .. import shapes
from ..text import text_width

def plot(c, items, area=None, x_label=("low", "high"), y_label=("low", "high"),
         axis_titles=("", ""), quadrant_names=None, highlight=None):
    """items: list of dicts {name, x, y} with x and y in 0..1. Labels are placed where they fit."""
    area = area or c.area
    c.rect(area, c.c("sunken"), c.c("hairline"), r=12)
    c.line((area.cx, area.y), (area.cx, area.y2), c.c("hairline"), 1.5)
    c.line((area.x, area.cy), (area.x2, area.cy), c.c("hairline"), 1.5)
    reserved = []
    if quadrant_names:
        # In the corners, not the centres: the centre of a quadrant is where the items land.
        corners = [(0.03, 0.06, "start"), (0.97, 0.06, "end"), (0.03, 0.97, "start"), (0.97, 0.97, "end")]
        for (qx, qy, anchor), name in zip(corners, quadrant_names):
            x, y = area.x + qx * area.w, area.y + qy * area.h
            box = c.text(x, y, name.upper(), size=14, weight=600, tracking=2, anchor=anchor,
                         fill=c.c("ink-3"), opacity=.9)
            reserved.append(box)
    c.text(area.x, area.y2 + 28, x_label[0], size=15, anchor="start", fill=c.c("ink-3"))
    c.text(area.x2, area.y2 + 28, x_label[1], size=15, anchor="end", fill=c.c("ink-3"))
    c.text(area.x - 18, area.y2, y_label[0], size=15, anchor="end", fill=c.c("ink-3"))
    c.text(area.x - 18, area.y + 12, y_label[1], size=15, anchor="end", fill=c.c("ink-3"))
    if axis_titles[0]: c.text(area.cx, area.y2 + 56, axis_titles[0], size=16, weight=600, fill=c.c("ink-2"))
    if axis_titles[1]: c.text(area.x - 18, area.cy, axis_titles[1], size=16, weight=600, anchor="end", fill=c.c("ink-2"))

    placed = list(reserved)
    for it in items:
        x = area.x + it["x"] * area.w
        y = area.y2 - it["y"] * area.h
        hot = highlight and it["name"] in highlight
        c.circle(x, y, 11 if hot else 8, fill=c.c("accent") if hot else c.c("ink-3"))
        anchor = Rect(x - 8, y - 8, 16, 16)
        w, h = text_width(it["name"], 16) + 8, 22
        r, _ = place_label(anchor, w, h, placed, area.inset(-40), gap=10,
                           order=("right", "top", "left", "bottom"))
        c.text(r.x, r.y + 16, it["name"], size=16, anchor="start",
               weight=600 if hot else 400, fill=c.c("ink") if hot else c.c("ink-2"))
        placed.append(r); placed.append(anchor)
    return area
