"""Shared harness for gallery figures: build, verify, save, and fail loudly on a defect."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))
from figura.canvas import Canvas          # noqa: E402
from figura.geom import Rect              # noqa: E402
from figura import shapes                 # noqa: E402
from figura.figures import (layers, flow, network, timeline,  # noqa: E402
                            matrix, quadrant, funnel, chart, annotate)

def title(c, text, sub=None):
    c.text(c.padding, 56, text, size=30, weight=600, anchor="start", face="display")
    if sub: c.text(c.padding, 84, sub, size=16, anchor="start", fill=c.c("ink-3"))

def finish(c, name):
    findings = c.verify()
    errors = [f for f in findings if f.level == "error"]
    for f in findings: print("   ", f)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".svg")
    c.save(out, png=bool(os.environ.get("FIGURA_PNG")))
    print(f"    {name}: {len(errors)} errors, {len(findings) - len(errors)} warnings -> {os.path.basename(out)}")
    if errors:
        raise SystemExit(f"{name} has {len(errors)} geometry errors")
