"""The same figure in three themes. The look is data, not code."""
from _common import *

def build(theme, name):
    c = Canvas(1200, 700, theme=theme, padding=70)
    title(c, f"Theme: {theme}", "identical code, different tokens")
    layers.stack(c, [
        {"name": "surface", "items": ["Console", "CLI"]},
        {"name": "engine", "accent": True, "items": [{"label": "Planner", "body": "decides the order of work"}]},
        {"name": "storage", "items": [{"label": "Primary", "tone": "muted"}, {"label": "Replica", "tone": "muted"}]},
    ], area=Rect(180, 140, 940, 480), style="band", gap=40)
    finish(c, name)

for theme, name in [("light", "08-theme-light"), ("dark", "08-theme-dark"), ("print", "08-theme-print")]:
    build(theme, name)
