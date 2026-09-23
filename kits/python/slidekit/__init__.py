"""slidekit: small drawing kits for slide diagrams.

Kits are visual languages, not a house style. Pick by what the diagram argues:

  blocks    boxes and arrows           anything structural; the safe default
  flow      numbered steps             a process, a pipeline, a sequence
  platforms stacked layers in 3/4 view a system with layers, who sits above and below
  graph     nodes and labelled edges   entities and their relationships
  timeline  a line with milestones     history, roadmap, phases

Mixing two kits on one slide usually means the slide has two messages.
"""
from . import blocks, flow, platforms, graph, timeline  # noqa: F401
