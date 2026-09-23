"""Tokens, themes and colour maths.

A theme is data. Swap it and every figure in a repository re-renders in the new palette, because
figures ask for roles ("accent", "ink-2") and never for hex values.
"""
import json, os, re

THEME_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "themes")

BASE = {
    "name": "base",
    "color": {
        "accent": "#175CD3", "accent-deep": "#0F3F94", "accent-soft": "#EEF4FD",
        "ink": "#101828", "ink-2": "#475467", "ink-3": "#667085",
        "surface": "#FFFFFF", "sunken": "#F9FAFB", "canvas": "#FFFFFF",
        "hairline": "#EAECF0", "edge": "#98A2B3", "edge-soft": "#B2CCF5",
        "good": "#12B76A", "warn": "#DC6803", "bad": "#D92D20", "info": "#7A5AF8",
    },
    "series": ["#175CD3", "#12B76A", "#DC6803", "#7A5AF8", "#0E7090", "#B42318"],
    "font": {"sans": "Inter, system-ui, Arial, sans-serif",
             "mono": "ui-monospace, Menlo, monospace",
             "display": "Georgia, 'Times New Roman', serif"},
    "radius": 10,
}

def load_theme(name_or_path="light"):
    if os.path.exists(str(name_or_path)):
        data = json.load(open(name_or_path))
    else:
        p = os.path.join(THEME_DIR, f"{name_or_path}.json")
        data = json.load(open(p)) if os.path.exists(p) else {}
    t = json.loads(json.dumps(BASE))
    for k, v in data.items():
        if isinstance(v, dict): t.setdefault(k, {}).update(v)
        else: t[k] = v
    return t

# --- colour maths ---------------------------------------------------------
def _rgb(c):
    c = c.strip()
    if c.startswith("#"):
        c = c[1:]
        if len(c) == 3: c = "".join(ch * 2 for ch in c)
        return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    m = re.findall(r"[\d.]+", c)
    return tuple(int(float(x)) for x in m[:3]) if len(m) >= 3 else (0, 0, 0)

def luminance(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = _rgb(c)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def readable_on(bg, theme, candidates=("ink", "surface")):
    """Pick the theme colour with the most contrast against bg."""
    best, score = None, -1
    for name in candidates:
        c = theme["color"].get(name, name)
        s = contrast(c, bg)
        if s > score: best, score = c, s
    return best

def ensure_contrast(fg, bg, minimum=4.5, toward="#000000", steps=20):
    """Darken (or lighten) fg until it is readable on bg. A mark can be any colour; the text
    beside it has to be legible, and that is a computation, not a judgement call."""
    if contrast(fg, bg) >= minimum: return fg
    target = toward if luminance(bg) > 0.5 else "#FFFFFF"
    out = fg
    for i in range(1, steps + 1):
        out = mix(fg, target, i / steps)
        if contrast(out, bg) >= minimum: return out
    return out

def mix(a, b, t):
    ra, rb = _rgb(a), _rgb(b)
    return "#%02X%02X%02X" % tuple(round(ra[i] + (rb[i] - ra[i]) * t) for i in range(3))
