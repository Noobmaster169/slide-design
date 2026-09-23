# Honest comparison

| Tool | Strength | Why you might still use figura |
|---|---|---|
| Mermaid, PlantUML | fastest path from text to a diagram, renders in GitHub | you cannot control placement, and every diagram looks the same |
| Graphviz | excellent automatic graph layout at scale | layout is the router's opinion; labels collide in dense graphs |
| D3, Vega-Lite, matplotlib, plotly | serious data visualization and statistics | they chart numbers well; they do not draw explanatory diagrams |
| Excalidraw, tldraw | fast, human, hand-drawn feel | nothing is generated or regenerated; no verification |
| Figma, Illustrator | total visual control, real design tooling | not code; no diff, no data binding, no CI |
| draw.io | familiar, shareable, free | manual placement, XML nobody reads, no measurement |
| TikZ, PGFPlots | beautiful, precise, publication grade | LaTeX-only workflow and a steep curve; no runtime verification |

**Use Mermaid or Graphviz** when the diagram is throwaway or the graph is large.
**Use a charting library** when the numbers are the subject and the forms are statistical.
**Use a drawing tool** when a person is exploring visually and the artefact is a one-off.
**Use figura** when the same figures will be regenerated as the content changes, when they must
match a palette, when labels must be right rather than approximately right, and when you want the
build to fail if a figure is broken.

The ideas transfer even if the code does not: measure your text before you place it, compute
positions, mark what must not be covered, and check the result instead of trusting it.
