"""Matrix and quadrant: many items on few dimensions, and two axes of judgement."""
from _common import *

c = Canvas(1600, 900, theme="light", padding=80)
title(c, "Matrix and quadrant", "coverage as shading, position as judgement")
matrix.grid(c, ["Search", "Exports", "Alerts", "Audit"], ["Web", "Mobile", "API"],
            [[True, True, 0.4], [True, False, 0.9], [0.6, False, True], [{"text": "planned", "tone": "soft"}, False, 0.2]],
            area=Rect(80, 170, 700, 520), row_label_w=200,
            legend_items=[("supported", c.c("good")), ("coverage", c.c("accent"))])
quadrant.plot(c, [
    {"name": "Search", "x": 0.82, "y": 0.72}, {"name": "Exports", "x": 0.35, "y": 0.6},
    {"name": "Alerts", "x": 0.62, "y": 0.28}, {"name": "Audit", "x": 0.2, "y": 0.25},
], area=Rect(900, 200, 600, 480), quadrant_names=["nice to have", "invest", "ignore", "keep working"],
   axis_titles=("effort", "value"), highlight=["Search"])
finish(c, "05-matrix-quadrant")
