"""Layered view of a fictional library lending service. Kit: platforms."""
import os, sys
sys.path.insert(0, os.environ.get("SLIDEKIT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../kits/python")))
from slidekit.core import SVG, wrap, load_tokens
from slidekit import platforms, blocks

HERE = os.path.dirname(os.path.abspath(__file__))
g = SVG(load_tokens(os.path.join(HERE, "..", "tokens.json")))
g.defs()

X, W = 460, 1000
platforms.people(g, X, 236, W, "Readers and staff")
g.block_arrow(X + W/2, 300, X + W/2, 350, w=22, hw=44, hl=14)

def surfaces(g, x, y, w, h):
    blocks.row(g, ["Web catalogue", "Branch desk", "Self-service kiosk"], y=y+28, x=x+70, w=w-140, h=h-56,
               gap=24, arrows=False)
def core(g, x, y, w, h):
    g.pill(x + w/2, y + h/2, "Lending service", kind="deep", size=26, w=320, h=54)
    for i, t in enumerate(["Catalogue", "Loans", "Members", "Fines"]):
        g.pill(x + 120 + i * 200, y + h - 34, t, kind="accent", size=16, w=170, h=32)
def stores(g, x, y, w, h):
    blocks.row(g, ["Database", "Search index", "Object storage"], y=y+26, x=x+70, w=w-140, h=h-52,
               gap=24, arrows=False, kinds=["muted", "muted", "muted"])

platforms.stack(g, [
    {"label": "Surfaces", "draw": surfaces},
    {"label": "Core", "accent": True, "draw": core},
    {"label": "Stores", "draw": stores},
], x=X, w=W, top=380, layer_h=150, gap=80, arrow="up")

open(os.path.join(HERE, "01-layers.svg"), "w").write(wrap(g.out()))
