# Diagrams

Kits are visual languages. Pick by what the diagram argues, not by which looks nicest.

| Kit | Argues | Avoid when |
|---|---|---|
| `blocks` | structure: parts and how they connect | it would be clearer as a sentence |
| `flow` | a process with an order and outputs | the steps are not really sequential |
| `platforms` | layering: who sits above and below | there is no real layering; use `blocks` |
| `graph` | entities and relationships | more than ~8 nodes, or edges cross badly |
| `timeline` | history, roadmap, phases | intervals are wildly uneven and unlabelled |

Mixing two kits on one slide usually means the slide has two messages.

## Writing a diagram script

```python
from slidekit.core import SVG, wrap, load_tokens
from slidekit import blocks

g = SVG(load_tokens("tokens.json"))
g.defs()
blocks.row(g, ["Collect", "Transform", "Publish"], y=430, x=260, w=1400, h=180, accent_index=2)
open("03-pipeline.svg", "w").write(wrap(g.out()))
```

Rules that keep diagrams editable:

- Compute coordinates from lists and loops. Even spacing should be arithmetic, not luck.
- Measure text with `text_width`, `fit_text` and `wrap_text` instead of guessing. SVG does not wrap.
- Label a shape outside it when the shape is small, inside when it is large.
- One arrow per connection. A bundle of thin lines is noise pretending to be complexity.
- Mark anything a label must not cover; `block_arrow` already carries `class="sk-arrow"`, which
  `slides check` protects.

## Other drawing options

Nothing stops you embedding Mermaid, Graphviz or D3 output, or a hand-drawn Excalidraw SVG. Keep it
inline and offline: a deck that fetches from a CDN fails in the room where the wifi does not work.
