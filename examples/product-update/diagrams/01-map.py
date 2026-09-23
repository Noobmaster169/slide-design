"""What the service connects to. Kit: graph."""
import os, sys
sys.path.insert(0, os.environ.get("SLIDEKIT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../kits/python")))
from slidekit.core import SVG, wrap, load_tokens
from slidekit import graph

HERE = os.path.dirname(os.path.abspath(__file__))
g = SVG(load_tokens(os.path.join(HERE, "..", "tokens.json")))
g.defs()

graph.hub(g, 960, 610, "Trip planner", ["Timetables", "Live positions", "Fares", "Accessibility", "Alerts"],
          r=250, node_w=210,
          label_edges={"Timetables": "reads", "Live positions": "subscribes", "Alerts": "publishes",
                       "Fares": "estimates", "Accessibility": "reads"})
g.label(960, 980, "five feeds, none of them ours", fill=g.c("ink-3"))
open(os.path.join(HERE, "01-map.svg"), "w").write(wrap(g.out()))
