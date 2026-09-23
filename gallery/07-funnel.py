"""Funnel: widths are the data, drop-off is stated."""
from _common import *

c = Canvas(1400, 900, theme="light", padding=100)
title(c, "Funnel", "each stage's width is its value; the drop is printed, not implied")
funnel.funnel(c, [
    {"label": "Saw the page", "value": 12400},
    {"label": "Started", "value": 5200},
    {"label": "Finished setup", "value": 2100},
    {"label": "Returned in a week", "value": 980},
], area=Rect(220, 180, 900, 600))
finish(c, "07-funnel")
