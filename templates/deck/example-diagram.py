"""One drawn slide. Run it, then inject the SVG into the deck:

    python3 diagrams/01-diagram.py
    slides inject '<!-- 03 drawn' diagrams/01-diagram.svg

Kits live in kits/python/slidekit: blocks, platforms, graph, flow, timeline.
Pick the one that matches the argument (docs/diagrams.md), not the one that looks nicest.
"""
import os, sys
sys.path.insert(0, os.environ.get("SLIDEKIT", os.path.expanduser("~/ai/slides/kits/python")))

from slidekit.core import SVG, wrap, load_tokens
from slidekit import blocks

T = load_tokens(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tokens.json"))
g = SVG(T)
g.defs()

cols = blocks.row(g, ["Input", "Process", "Output"], y=430, x=260, w=1400, h=180,
                  accent_index=2, subtitles=["what arrives", "what happens to it", "what you get"])
open(os.path.splitext(os.path.abspath(__file__))[0] + ".svg", "w").write(wrap(g.out()))
