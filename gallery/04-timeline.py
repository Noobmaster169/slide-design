"""Timeline: milestones, and phases as proportional bands."""
from _common import *

c = Canvas(1600, 900, theme="light", padding=90)
title(c, "Timeline", "shipped is solid, planned is dashed, and the legend says so")
timeline.milestones(c, [
    {"label": "Import", "note": "nightly feed running"},
    {"label": "Live updates", "note": "30 second refresh"},
    {"label": "Estimates", "note": "one source covered"},
    {"label": "Offline mode", "note": "needs a cached map"},
], area=Rect(140, 170, 1320, 220), done_until=1, axis_label="time ->")
timeline.phases(c, [
    {"label": "Discovery", "weight": 1, "note": "two weeks"},
    {"label": "Build", "weight": 3, "note": "six weeks, where we are", "current": True},
    {"label": "Pilot", "weight": 2, "note": "four weeks"},
], area=Rect(140, 560, 1320, 180))
finish(c, "04-timeline")
