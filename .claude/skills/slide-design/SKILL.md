---
name: slide-design
description: "Build or redesign slides in this repository: pitch decks, talks, architecture and product slides. Use when asked for a deck, slides, a presentation, a slide diagram, or to improve or restyle existing slides. Produces an HTML deck plus PDF and per-slide PNGs, checked by `slides check`."
---

# Slide design

This repository is the toolkit. Read `docs/method.md` first; it is the procedure this skill follows.

## Procedure

1. Collect verified facts. Nothing goes on a slide that you cannot point at a source for.
2. Write the deck as one claim per slide before any layout.
3. Pick a layout per slide from `docs/layouts.md`.
4. `slides new <dir> --theme=<theme>`, then edit `deck.html`.
5. Draw only what a picture explains better than a sentence; pick one kit per slide from
   `docs/diagrams.md`; generate it with a script in `diagrams/`.
6. `slides render <dir> --png`, then **open every image and look at it**.
7. `slides check <dir>`, fix errors, re-render, look again.

## The gate

**A slide is not done until its rendered PNG has been viewed.** Never claim a deck is finished,
or that a fix worked, from the source alone. `slides check` catches measurable defects; it cannot
tell you whether the slide makes its point.

## Rules that matter more than taste

- One accent colour; status colours only for status.
- One message per slide; one sentence per point.
- Real screenshots for things that exist; drawings for structure.
- Built and planned must look different (solid versus dashed) and read differently in words.
- Keep the deck self-contained: fonts and images local, no CDN.
- Change only the slides you were asked to change.

## Scope

For `.pptx` output use a PowerPoint skill instead. For charts, apply chart-specific guidance for
form and colour first, then draw with these kits.
