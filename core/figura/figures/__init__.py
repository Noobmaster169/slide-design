"""Figure recipes: each takes data and returns a finished, verified drawing.

Pick by what the figure argues, not by what looks nice:

  layers    what sits above what            stack, bands
  flow      a sequence with stages          pipeline, steps
  network   entities and their relations    hub, mesh
  timeline  when things happened            milestones, phases
  matrix    many items on few dimensions    comparison grid, heat grid
  quadrant  two axes of judgement           2x2 positioning
  funnel    narrowing quantities            stages with values
  chart     numbers                         bar, column, dot, line
  annotate  a real image explained          callouts on a screenshot
"""
from . import layers, flow, network, timeline, matrix, quadrant, funnel, chart, annotate  # noqa
