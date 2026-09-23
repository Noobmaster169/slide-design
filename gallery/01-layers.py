"""Layers: what sits above what. Content is invented."""
from _common import *

c = Canvas(1600, 900, theme="light", padding=140)
title(c, "Layers", "for when the argument is what sits above what")
layers.stack(c, [
    {"name": "people", "items": [{"label": "Analysts"}, {"label": "Support"}, {"label": "Automations"}]},
    {"name": "service", "accent": True, "items": [
        {"label": "Query engine", "body": "plans and runs requests"},
        {"label": "Permissions", "body": "who may see what"}]},
    {"name": "stores", "items": [{"label": "Warehouse", "tone": "muted"}, {"label": "Object store", "tone": "muted"},
                                 {"label": "Cache", "tone": "muted"}]},
], area=Rect(220, 150, 1200, 660), style="band", gap=56)
finish(c, "01-layers")
