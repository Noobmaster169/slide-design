"""Callouts over a real image. A screenshot with three labelled points beats a drawing of a
screenshot, and this keeps the labels off each other and off the thing they point at."""
from ..geom import Rect
from .. import shapes

def image(c, href, area=None, frame=True, alt=""):
    area = area or c.area
    if frame:
        c.rect(Rect(area.x - 10, area.y - 10, area.w + 20, area.h + 20), c.c("surface"), c.c("edge"), r=12)
    c.raw(f'<image href="{href}" x="{area.x:.0f}" y="{area.y:.0f}" width="{area.w:.0f}" '
          f'height="{area.h:.0f}" preserveAspectRatio="xMidYMid slice"><title>{alt}</title></image>',
          area, kind="shape")
    return area

def points(c, img_area, notes, max_w=230, side_order=("right", "top", "bottom", "left")):
    """notes: list of dicts {at: (x_frac, y_frac), text, number?}. Markers on the image, notes
    placed outside it where they do not collide."""
    placed = [img_area]
    bounds = Rect(0, 0, c.w, c.h).inset(24)
    for i, nt in enumerate(notes):
        fx, fy = nt["at"]
        x, y = img_area.x + fx * img_area.w, img_area.y + fy * img_area.h
        marker = shapes.badge(c, x, y, nt.get("number", i + 1), r=17)
        r = shapes.callout(c, marker, nt["text"], placed, bounds, max_w=max_w, side_order=side_order)
        placed.append(r)
    return placed
