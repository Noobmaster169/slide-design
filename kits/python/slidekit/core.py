"""Drawing core shared by every kit. Coordinates are slide pixels (default 1920 x 1080).

Compute positions from lists and loops so spacing is even by construction. Nudging numbers
until a render looks right produces a diagram nobody can safely edit later.
"""
import json, os

FALLBACK = {
    "color": {"accent": "#175CD3", "accent-deep": "#0F3F94", "ink": "#101828", "ink-2": "#475467",
              "ink-3": "#667085", "hairline": "#EAECF0", "hairline-strong": "#98A2B3",
              "line": "#B2CCF5", "surface": "#FFFFFF", "sunken": "#F9FAFB", "tint": "#EEF4FD",
              "good": "#12B76A", "warning": "#DC6803", "serious": "#7A5AF8"},
    "font": {"display": "Georgia, serif", "sans": "system-ui, Arial, sans-serif",
             "mono": "ui-monospace, Menlo, monospace"},
    "pageBackground": "#FFFFFF",
}

def load_tokens(path=None):
    if path and os.path.exists(path):
        t = json.load(open(path))
        for k, v in FALLBACK.items():
            t.setdefault(k, v)
            if isinstance(v, dict):
                for kk, vv in v.items(): t[k].setdefault(kk, vv)
        return t
    return json.loads(json.dumps(FALLBACK))

# Average glyph width as a fraction of font size. Accurate to a few percent, which is enough to
# centre, fit and avoid collisions without rendering first.
_RATIO = {"sans": 0.545, "mono": 0.600, "display": 0.500}

def text_width(t, size, face="sans", ls=0):
    t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return len(t) * size * _RATIO.get(face, 0.55) + max(0, len(t) - 1) * ls

def fit_text(t, size, max_w, face="sans", min_size=10):
    while size > min_size and text_width(t, size, face) > max_w:
        size -= 1
    return size

def wrap_text(t, size, max_w, face="sans"):
    words, lines, cur = t.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_width(trial, size, face) > max_w:
            lines.append(cur); cur = w
        else: cur = trial
    if cur: lines.append(cur)
    return lines

class SVG:
    def __init__(self, tokens=None, width=1920, height=1080):
        self.t = tokens or load_tokens()
        self.w, self.h = width, height
        self.o = []

    # --- tokens
    def c(self, name): return self.t["color"].get(name, name)
    def f(self, face): return self.t["font"].get(face, face)

    def E(self, s): self.o.append(s)
    def out(self): return "\n".join(self.o)

    def defs(self, background=None):
        a = self.c("accent")
        self.E(f'<defs>'
               f'<linearGradient id="pipe" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="{self.c("line")}" stop-opacity=".55"/>'
               f'<stop offset=".5" stop-color="{self.c("surface")}"/>'
               f'<stop offset="1" stop-color="{self.c("line")}" stop-opacity=".55"/></linearGradient>'
               f'<linearGradient id="pipev" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{self.c("line")}" stop-opacity=".55"/>'
               f'<stop offset=".5" stop-color="{self.c("surface")}"/>'
               f'<stop offset="1" stop-color="{self.c("line")}" stop-opacity=".55"/></linearGradient>'
               f'<filter id="sh" x="-20%" y="-20%" width="140%" height="160%">'
               f'<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="{a}" flood-opacity=".18"/>'
               f'</filter></defs>')
        if background: self.E(f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{background}"/>')

    # --- primitives
    def text(self, x, y, t, size=18, weight=400, fill=None, anchor="middle", face="sans", ls=0, opacity=1):
        self.E(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{self.f(face)}" font-size="{size}" '
               f'font-weight="{weight}" fill="{fill or self.c("ink")}" text-anchor="{anchor}" '
               f'letter-spacing="{ls}" opacity="{opacity}">{t}</text>')

    def block(self, x, y, t, size, max_w, lh=1.35, **kw):
        """Wrapped text; returns y after the last line. SVG does not wrap, so lines are placed."""
        ls = wrap_text(t, size, max_w, kw.get("face", "sans"))
        for i, line in enumerate(ls): self.text(x, y + i * size * lh, line, size=size, **kw)
        return y + len(ls) * size * lh

    def rect(self, x, y, w, h, fill="none", stroke="none", r=8, sw=1.2, extra=""):
        self.E(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line(self, x1, y1, x2, y2, color=None, sw=2.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.E(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
               f'stroke="{color or self.c("hairline-strong")}" stroke-width="{sw}"{d}/>')

    def arrow(self, x1, y1, x2, y2, color=None, sw=2.5, head=9):
        """Thin arrow for a minor hop. Use block_arrow for a connection between layers."""
        import math
        col = color or self.c("hairline-strong")
        self.line(x1, y1, x2, y2, col, sw)
        a = math.atan2(y2 - y1, x2 - x1)
        for s in (-0.5, 0.5):
            self.line(x2, y2, x2 - head * 2 * math.cos(a - s), y2 - head * 2 * math.sin(a - s), col, sw)

    def block_arrow(self, x1, y1, x2, y2, both=False, w=34, hw=66, hl=22, dash=False):
        """One thick arrow. Vertical or horizontal; one connection, never a bundle of lines."""
        vertical = abs(x2 - x1) < abs(y2 - y1)
        grad = "pipe" if vertical else "pipev"
        a, h = w / 2, hw / 2
        if vertical:
            d = 1 if y2 > y1 else -1; base = y2 - d * hl; start = y1 + (d * hl if both else 0)
            pts = [(x1-a,start),(x1-a,base),(x1-h,base),(x1,y2),(x1+h,base),(x1+a,base),(x1+a,start)]
            if both: pts += [(x1+h,start),(x1,y1),(x1-h,start)]
        else:
            d = 1 if x2 > x1 else -1; base = x2 - d * hl; start = x1 + (d * hl if both else 0)
            pts = [(start,y1-a),(base,y1-a),(base,y1-h),(x2,y1),(base,y1+h),(base,y1+a),(start,y1+a)]
            if both: pts += [(start,y1+h),(x1,y1),(start,y1-h)]
        da = ' stroke-dasharray="6 5"' if dash else ""
        self.E('<polygon class="sk-arrow" points="' + " ".join(f"{p:.0f},{q:.0f}" for p, q in pts) +
               f'" fill="url(#{grad})" stroke="{self.c("line")}" stroke-width="1.5" stroke-linejoin="round"{da}/>')

    def pill(self, x, y, t, kind="accent", size=18, w=None, h=38):
        w = w or text_width(t, size) + 36
        if kind == "accent": self.rect(x-w/2, y-h/2, w, h, self.c("accent"), self.c("accent"), r=h/2, extra='filter="url(#sh)"'); col = self.c("surface")
        elif kind == "deep": self.rect(x-w/2, y-h/2, w, h, self.c("accent-deep"), self.c("accent-deep"), r=h/2, extra='filter="url(#sh)"'); col = self.c("surface")
        else: self.rect(x-w/2, y-h/2, w, h, self.c("surface"), self.c("hairline-strong"), r=h/2, sw=1.4); col = self.c("ink")
        self.text(x, y + size * 0.36, t, size=size, weight=500, fill=col)
        return w

    def chip(self, x, y, t, dark=False, size=17):
        face = "sans" if dark else "mono"
        w = text_width(t, size, face) + 26
        if dark:
            self.rect(x-w/2, y-15, w, 30, self.c("ink-3"), self.c("ink-3"), r=15)
            self.text(x, y+6, t, size=size, fill=self.c("surface"), face=face)
        else:
            self.rect(x-w/2, y-15, w, 30, self.c("surface"), self.c("hairline-strong"), r=15)
            self.text(x, y+6, t, size=size, fill=self.c("ink-2"), face=face)

    def label(self, x, y, t, size=18, ls=2.5, fill=None, anchor="middle"):
        self.text(x, y, t.upper(), size=size, weight=600, ls=ls, fill=fill or self.c("ink-2"), anchor=anchor)

def wrap(svg, width=1920, height=1080):
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'style="position:absolute; left:0; top:0">\n{svg}\n  </svg>')
