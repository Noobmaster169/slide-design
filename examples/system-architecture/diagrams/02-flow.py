"""Borrowing a book, as three steps. Kit: flow."""
import os, sys
sys.path.insert(0, os.environ.get("SLIDEKIT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../kits/python")))
from slidekit.core import SVG, wrap, load_tokens
from slidekit import flow

HERE = os.path.dirname(os.path.abspath(__file__))
g = SVG(load_tokens(os.path.join(HERE, "..", "tokens.json")))
g.defs()

flow.steps(g, [
    {"title": "Find", "scope": "any reader", "body": "Search the catalogue and see which branch holds a copy.", "output": "a hold"},
    {"title": "Collect", "scope": "at a branch", "body": "The hold is matched to a physical copy and checked out.", "output": "a loan"},
    {"title": "Return", "scope": "within 21 days", "body": "The copy goes back on the shelf and the hold queue advances.", "output": "shelf again"},
], x=180, y=380, w=1560, h=240, gap=100)

open(os.path.join(HERE, "02-flow.svg"), "w").write(wrap(g.out()))
