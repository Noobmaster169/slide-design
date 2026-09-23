"""Charts: the numbers a figure needs, without a second tool."""
from _common import *

c = Canvas(1600, 900, theme="light", padding=80)
title(c, "Charts", "thin marks, one accent, direct labels, one axis")
chart.bars(c, [
    {"label": "This approach", "value": 0.97, "emphasis": True},
    {"label": "Previous release", "value": 0.82},
    {"label": "Baseline", "value": 0.55},
], area=Rect(80, 150, 720, 220), label_w=260, max_value=1.0,
   value_fmt=lambda v: f"{v:.2f}", reference={"value": 0.9, "label": "target"})
chart.columns(c, [{"label": "Q1", "value": 18}, {"label": "Q2", "value": 24},
                  {"label": "Q3", "value": 31, "emphasis": True}],
              area=Rect(900, 130, 600, 300))
chart.lines(c, [{"name": "Requests", "values": [12, 18, 17, 26, 31]},
                {"name": "Errors", "values": [4, 3, 5, 2, 2]}],
            area=Rect(80, 470, 780, 340), x_labels=["Mon", "Tue", "Wed", "Thu", "Fri"])
chart.stat(c, Rect(960, 500, 480, 260), "31k", "requests last week", "up from 26k")
finish(c, "06-charts")
