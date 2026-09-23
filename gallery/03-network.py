"""Network: a hub, and a mesh with placed labels."""
from _common import *

c = Canvas(1600, 900, theme="light", padding=80)
title(c, "Network", "relationships, with edge labels pushed out of the middle")
network.hub(c, "Scheduler", ["Calendar feed", "Rooms", "People", "Notifications", "Audit log"],
            area=Rect(80, 130, 740, 720),
            edge_labels={"Calendar feed": "reads", "Notifications": "publishes", "Audit log": "appends"})
network.mesh(c, {
    "Ingest": (0.12, 0.22), "Queue": (0.5, 0.12), "Worker": (0.86, 0.3),
    "Store": (0.6, 0.62), "API": (0.15, 0.72), "Client": (0.85, 0.82),
}, [("Ingest", "Queue"), ("Queue", "Worker", "pulls"), ("Worker", "Store", "writes"),
    ("API", "Store", "reads"), ("Client", "API")], area=Rect(880, 150, 640, 660))
finish(c, "03-network")
