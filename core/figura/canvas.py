"""The canvas records what it draws.

Every element is kept with its bounding box and its role (text, shape, keep-clear), which is what
makes `figure.verify()` possible without a browser: overlapping labels, text off the canvas, text
covering an arrow and unreadable contrast are all geometry questions once you have measured text.
"""
import os, subprocess, tempfile
from .style import load_theme, contrast
from .text import text_width, wrap, fit_size
from .geom import Rect

class Element:
    __slots__ = ("kind", "box", "svg", "meta")
    def __init__(self, kind, box, svg, meta=None):
        self.kind, self.box, self.svg, self.meta = kind, box, svg, meta or {}

class Canvas:
    def __init__(self, width=1600, height=900, theme="light", background=None, padding=48):
        self.w, self.h = width, height
        self.t = load_theme(theme) if isinstance(theme, str) else theme
        self.background = background if background is not None else self.c("canvas")
        self.padding = padding
        self.el = []
        self._defs = []

    # --- tokens
    def c(self, name): return self.t["color"].get(name, name)
    def font(self, face): return self.t["font"].get(face, face)
    def series(self, i): return self.t["series"][i % len(self.t["series"])]
    @property
    def area(self): return Rect(self.padding, self.padding, self.w - 2 * self.padding, self.h - 2 * self.padding)

    # --- low level
    def raw(self, svg, box=None, kind="shape", **meta):
        self.el.append(Element(kind, box, svg, meta)); return box

    def defs(self, svg): self._defs.append(svg)

    def text(self, x, y, s, size=18, weight=400, fill=None, anchor="middle", face="sans",
             tracking=0, baseline="alphabetic", opacity=1, keep=True):
        fill = fill or self.c("ink")
        w = text_width(s, size, face, tracking)
        left = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
        top = {"alphabetic": y - size * 0.78, "middle": y - size * 0.5, "hanging": y}[baseline]
        box = Rect(left, top, w, size * 1.02)
        esc = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
               if "&#" not in s and "&amp;" not in s else s)
        svg = (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{self.font(face)}" font-size="{size}" '
               f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{tracking}" '
               f'opacity="{opacity}" dominant-baseline="{baseline}">{esc}</text>')
        return self.raw(svg, box, kind="text" if keep else "shape", size=size, fill=fill, s=s, face=face)

    def paragraph(self, x, y, s, size=18, max_w=320, leading=1.35, **kw):
        lines = wrap(s, size, max_w, kw.get("face", "sans"))
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * leading, ln, size=size, **kw)
        return y + len(lines) * size * leading

    def rect(self, box: Rect, fill="none", stroke="none", r=None, sw=1.5, dash=None, extra="", keep_clear=False):
        r = self.t["radius"] if r is None else r
        d = f' stroke-dasharray="{dash}"' if dash else ""
        svg = (f'<rect x="{box.x:.1f}" y="{box.y:.1f}" width="{box.w:.1f}" height="{box.h:.1f}" rx="{r}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')
        return self.raw(svg, box, kind="keep-clear" if keep_clear else "shape", fill=fill)

    def line(self, p1, p2, color=None, sw=2, dash=None, cap="round"):
        (x1, y1), (x2, y2) = p1, p2
        d = f' stroke-dasharray="{dash}"' if dash else ""
        svg = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color or self.c("edge")}" '
               f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')
        box = Rect(min(x1, x2) - sw, min(y1, y2) - sw, abs(x2 - x1) + 2 * sw, abs(y2 - y1) + 2 * sw)
        return self.raw(svg, box)

    def path(self, d, stroke=None, fill="none", sw=2, dash=None, box=None, keep_clear=False, extra=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        svg = (f'<path d="{d}" fill="{fill}" stroke="{stroke or self.c("edge")}" stroke-width="{sw}" '
               f'stroke-linejoin="round" stroke-linecap="round"{da} {extra}/>')
        return self.raw(svg, box, kind="keep-clear" if keep_clear else "shape")

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=1.5, extra=""):
        svg = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
        return self.raw(svg, Rect(cx - r, cy - r, 2 * r, 2 * r), fill=fill)

    # --- output
    def to_svg(self, standalone=True):
        body = "\n  ".join(e.svg for e in self.el)
        defs = ("<defs>" + "".join(self._defs) + "</defs>") if self._defs else ""
        bg = f'<rect width="{self.w}" height="{self.h}" fill="{self.background}"/>' if self.background else ""
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">' if standalone
                else f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">')
        return f"{head}\n  {defs}{bg}\n  {body}\n</svg>\n"

    def save(self, path, png=False, scale=2):
        path = os.path.abspath(path)
        open(path, "w").write(self.to_svg())
        if png:
            from .render import svg_to_png
            svg_to_png(path, path[:-4] + ".png" if path.endswith(".svg") else path + ".png", scale)
        return path

    # --- verification
    def verify(self, min_font=14, min_contrast=4.5, tol=1.5):
        from .verify import verify_canvas
        return verify_canvas(self, min_font=min_font, min_contrast=min_contrast, tol=tol)
