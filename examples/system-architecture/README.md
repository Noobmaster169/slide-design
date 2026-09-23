# Deck

```bash
slides render . --png      # deck.pdf and preview/slide-NN.png
slides check .             # measure the rendered deck for layout defects
open preview/              # then look at every slide yourself
```

- `deck.html` is the deck. One `<section class="slide">` per slide.
- `tokens.json` is the palette and type scale. Edit it, then paste the new `:root` block
  (`slides tokens .`) into `deck.html`.
- `diagrams/NN-*.py` draw full-slide SVGs. Run one, then inject it:
  `python3 diagrams/01-diagram.py && slides inject '<!-- 03 drawn' diagrams/01-diagram.svg`
- `assets/` holds fonts and images. Keep the deck self-contained: no CDN links.
