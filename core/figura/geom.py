"""Geometry and layout. Positions are computed, never nudged."""
import math

class Rect:
    __slots__ = ("x", "y", "w", "h")
    def __init__(self, x, y, w, h): self.x, self.y, self.w, self.h = x, y, w, h
    @property
    def x2(self): return self.x + self.w
    @property
    def y2(self): return self.y + self.h
    @property
    def cx(self): return self.x + self.w / 2
    @property
    def cy(self): return self.y + self.h / 2
    @property
    def center(self): return (self.cx, self.cy)
    def inset(self, d): return Rect(self.x + d, self.y + d, self.w - 2 * d, self.h - 2 * d)
    def moved(self, dx, dy): return Rect(self.x + dx, self.y + dy, self.w, self.h)
    def overlaps(self, o, tol=0.0):
        return (min(self.x2, o.x2) - max(self.x, o.x) > tol and
                min(self.y2, o.y2) - max(self.y, o.y) > tol)
    def contains(self, o):
        return o.x >= self.x and o.y >= self.y and o.x2 <= self.x2 and o.y2 <= self.y2
    def side(self, name):
        return {"top": (self.cx, self.y), "bottom": (self.cx, self.y2),
                "left": (self.x, self.cy), "right": (self.x2, self.cy)}[name]
    def __repr__(self): return f"Rect({self.x:.0f},{self.y:.0f},{self.w:.0f},{self.h:.0f})"

def row(area, n, gap=32, ratios=None):
    """Split a Rect into n columns. ratios weights the widths."""
    ratios = ratios or [1] * n
    total = sum(ratios)
    free = area.w - gap * (n - 1)
    out, x = [], area.x
    for r in ratios:
        w = free * r / total
        out.append(Rect(x, area.y, w, area.h)); x += w + gap
    return out

def column(area, n, gap=24, ratios=None):
    ratios = ratios or [1] * n
    total = sum(ratios)
    free = area.h - gap * (n - 1)
    out, y = [], area.y
    for r in ratios:
        h = free * r / total
        out.append(Rect(area.x, y, area.w, h)); y += h + gap
    return out

def grid(area, cols, count, gap=24, aspect=None):
    rows = math.ceil(count / cols)
    cw = (area.w - gap * (cols - 1)) / cols
    ch = cw / aspect if aspect else (area.h - gap * (rows - 1)) / rows
    return [Rect(area.x + (i % cols) * (cw + gap), area.y + (i // cols) * (ch + gap), cw, ch)
            for i in range(count)]

def radial(cx, cy, n, rx, ry=None, start=-math.pi / 2):
    ry = ry if ry is not None else rx
    return [(cx + rx * math.cos(start + i * 2 * math.pi / n),
             cy + ry * math.sin(start + i * 2 * math.pi / n)) for i in range(n)]

def elbow(p1, p2, bias=0.5, vertical_first=False):
    """Orthogonal path between two points, as an SVG path string."""
    (x1, y1), (x2, y2) = p1, p2
    if vertical_first:
        my = y1 + (y2 - y1) * bias
        return f"M{x1:.0f} {y1:.0f} V{my:.0f} H{x2:.0f} V{y2:.0f}"
    mx = x1 + (x2 - x1) * bias
    return f"M{x1:.0f} {y1:.0f} H{mx:.0f} V{y2:.0f} H{x2:.0f}"

def curve(p1, p2, k=0.5):
    (x1, y1), (x2, y2) = p1, p2
    dx = (x2 - x1) * k
    return f"M{x1:.0f} {y1:.0f} C{x1+dx:.0f} {y1:.0f} {x2-dx:.0f} {y2:.0f} {x2:.0f} {y2:.0f}"

def edge_point(r: Rect, toward):
    """Where a line from the centre of r toward a point leaves r's boundary."""
    tx, ty = toward
    dx, dy = tx - r.cx, ty - r.cy
    if dx == 0 and dy == 0: return r.center
    sx = (r.w / 2) / abs(dx) if dx else float("inf")
    sy = (r.h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return (r.cx + dx * s, r.cy + dy * s)

def place_label(anchor: Rect, w, h, avoid, bounds: Rect, gap=10,
                order=("top", "right", "bottom", "left")):
    """First position around anchor whose box clears everything in avoid and stays in bounds."""
    cands = {
        "top": Rect(anchor.cx - w / 2, anchor.y - gap - h, w, h),
        "bottom": Rect(anchor.cx - w / 2, anchor.y2 + gap, w, h),
        "left": Rect(anchor.x - gap - w, anchor.cy - h / 2, w, h),
        "right": Rect(anchor.x2 + gap, anchor.cy - h / 2, w, h),
    }
    for name in order:
        c = cands[name]
        if bounds.contains(c) and not any(c.overlaps(a, 1) for a in avoid):
            return c, name
    return cands[order[0]], order[0]
