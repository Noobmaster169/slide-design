"""Where the work is. Kit: timeline. Shipped is solid, planned is dashed."""
import os, sys
sys.path.insert(0, os.environ.get("SLIDEKIT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../kits/python")))
from slidekit.core import SVG, wrap, load_tokens
from slidekit import timeline

HERE = os.path.dirname(os.path.abspath(__file__))
g = SVG(load_tokens(os.path.join(HERE, "..", "tokens.json")))
g.defs()

timeline.timeline(g, [
    ("Timetable import", "nightly feed, running since launch"),
    ("Live positions", "vehicle feed added, 30 second refresh"),
    ("Fare estimates", "in progress, one operator covered"),
    ("Offline journeys", "planned, needs a cached map"),
], x=260, y=560, w=1400, done_index=1)

g.label(260, 900, "shipped", anchor="start", fill=g.c("accent"))
g.label(1660, 900, "planned", anchor="end", fill=g.c("ink-3"))
open(os.path.join(HERE, "02-roadmap.svg"), "w").write(wrap(g.out()))
