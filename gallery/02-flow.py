"""Flow: a sequence with stages, each showing its own small picture and what it produces."""
from _common import *

def sketch_docs(c, r):
    for i in range(3):
        c.rect(Rect(r.x + 12 + i * 46, r.y + 6, 38, 50), c.c("surface"), c.c("edge"), r=4)

def sketch_split(c, r):
    shapes.pill(c, r.cx, r.y + 22, "matched", tone="plain", size=14, h=28)
    shapes.pill(c, r.cx, r.y + 58, "unmatched", tone="muted", size=14, h=28)

def sketch_graph(c, r):
    pts = [(r.cx, r.y + 14), (r.x + 26, r.y + 62), (r.x2 - 26, r.y + 62)]
    for p in pts[1:]: c.line(pts[0], p, c.c("edge-soft"), 2)
    for p in pts: c.circle(*p, 9, fill=c.c("accent"))

c = Canvas(1600, 900, theme="light", padding=90)
title(c, "Flow", "stages, what each one is given, and what it hands on")
flow.pipeline(c, [
    {"name": "Collect", "scope": "every file", "body": "Read whatever arrives, keep the original.", "output": "raw batch", "draw": sketch_docs},
    {"name": "Reconcile", "scope": "pairs only", "body": "Compare the two sides field by field.", "output": "matched set", "draw": sketch_split},
    {"name": "Relate", "scope": "everything read", "body": "Turn the result into linked records.", "output": "knowledge graph", "draw": sketch_graph},
], area=Rect(90, 170, 1420, 480), gap=70)
finish(c, "02-flow")
