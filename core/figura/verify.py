"""Geometry-level verification, with no browser involved.

A figure that passes is not automatically good, but a figure that fails is certainly broken, and
the failure is reported before anyone renders it.
"""
from .geom import Rect
from .style import contrast

class Finding:
    def __init__(self, level, rule, msg): self.level, self.rule, self.msg = level, rule, msg
    def __repr__(self): return f"{self.level.upper():5} {self.rule:16} {self.msg}"

def verify_canvas(canvas, min_font=14, min_contrast=4.5, tol=1.5):
    f = []
    page = Rect(0, 0, canvas.w, canvas.h)
    texts = [e for e in canvas.el if e.kind == "text" and e.box]
    keep = [e for e in canvas.el if e.kind == "keep-clear" and e.box]

    for e in texts:
        if not page.contains(e.box):
            f.append(Finding("error", "off-canvas", f'text leaves the canvas: "{e.meta.get("s","")[:40]}"'))
        if e.meta.get("size", 99) < min_font:
            f.append(Finding("warn", "font-size", f'{e.meta["size"]:.0f}px: "{e.meta.get("s","")[:40]}"'))

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if texts[i].box.overlaps(texts[j].box, tol):
                f.append(Finding("error", "text-overlap",
                                 f'"{texts[i].meta.get("s","")[:24]}" over "{texts[j].meta.get("s","")[:24]}"'))

    for e in texts:
        for k in keep:
            if e.box.overlaps(k.box, tol):
                f.append(Finding("error", "text-over-shape",
                                 f'"{e.meta.get("s","")[:24]}" sits on a shape marked keep-clear'))

    # a shape drawn after a text covers it: the defect a text-vs-text check cannot see
    order = {id(e): i for i, e in enumerate(canvas.el)}
    opaque = [e for e in canvas.el if e.kind in ("shape", "keep-clear") and e.box
              and e.meta.get("fill") not in (None, "none")]
    for e in texts:
        for sh in opaque:
            if order[id(sh)] > order[id(e)] and e.box.overlaps(sh.box, tol) and not sh.box.contains(e.box):
                f.append(Finding("error", "text-occluded",
                                 f'"{e.meta.get("s","")[:24]}" is partly covered by a shape drawn later'))
                break

    # contrast against the nearest filled shape behind the text, else the canvas background
    shapes = [e for e in canvas.el if e.kind in ("shape", "keep-clear") and e.box and e.meta.get("fill") not in (None, "none")]
    for e in texts:
        bg = canvas.background
        for s in shapes:
            if s.box.contains(e.box) or s.box.overlaps(e.box, 4):
                bg = s.meta["fill"]
        fg = e.meta.get("fill")
        if fg and bg and not str(bg).startswith("url"):
            try:
                r = contrast(fg, bg)
                if r < min_contrast:
                    f.append(Finding("warn", "contrast", f'{r:.1f}:1 for "{e.meta.get("s","")[:30]}"'))
            except Exception:
                pass
    return f

def report(findings, name="figure"):
    errs = [x for x in findings if x.level == "error"]
    for x in findings: print(f"  {x}")
    print(f"{name}: {len(errs)} errors, {len(findings) - len(errs)} warnings")
    return not errs
