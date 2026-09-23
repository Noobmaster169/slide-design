# What is different here

Most ways of making a diagram sit at one of two extremes.

**Auto-layout tools** (Mermaid, Graphviz, PlantUML) take a description and place everything for you.
You get a diagram in ten seconds and no control over the result: labels land where the router puts
them, and every diagram in the world made this way looks the same.

**Drawing tools** (Figma, Illustrator, Excalidraw, slide editors) give total control and no memory.
Nothing is computed, nothing can be regenerated, and a change of palette means an afternoon.

figura sits between them, and the mechanism is small:

### 1. Text is measured before anything is drawn

`figura.text` gives the width of a string at a size and face without a browser. That single fact
enables the rest: a box can be sized to its content, a font size can be fitted to a box, a label can
be placed in the gap between two shapes, and a wrapped paragraph's height is known in advance. Tools
that hand layout to a router cannot do this. Tools where a human drags boxes do it by eye.

### 2. Positions are computed

`figura.geom` turns an area into rows, columns, grids and radial positions, and routes orthogonal
and curved connectors between them. Even spacing is arithmetic, not luck, which means a figure
survives a change of content.

### 3. The canvas records what it draws

Every element is kept with its bounding box and its role. That turns "is this figure broken?" into
a geometry question, answerable in milliseconds with no rendering:

- text that leaves the canvas
- two labels on top of each other
- a label covered by a shape drawn after it
- a label sitting on an arrow
- text below a readable size
- text whose contrast against what is behind it is too low

### 4. The recipes are opinionated, and the opinions are in one place

A recipe such as `figures.flow.pipeline` sizes its boxes to content, places its scope chips clear of
the boxes, picks a readable colour for a label on a shaded cell, and rounds its axis ticks. When one
of those rules is wrong, it is fixed once and every figure in every repository improves.

## What it does not do

It will not invent a layout for a graph of two hundred nodes; that is a router's job, and `mesh`
asks you for positions on purpose. It does not animate. It does not read your data model. And it
cannot tell you whether the figure is worth drawing: a clean figure of a bad argument is still bad.
