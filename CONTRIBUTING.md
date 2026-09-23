# Contributing

## What fits here

- New **kits** (visual languages) and **themes**. More variety is the point; this project should not
  push one house style.
- New **checks**, especially ones that catch a defect a person would otherwise have to spot by eye.
- Docs that make the method clearer, or that honestly describe when another tool is a better fit.
- Example decks whose content is invented or public. No client work, no internal material.

## What does not fit

- A single "official" look, or changes that make the default theme harder to replace.
- Checks that enforce taste rather than a measurable defect.
- Examples containing anything confidential, or logos and screenshots you do not have the right to
  redistribute.
- Bundled fonts without a licence that permits redistribution and embedding.

## Ground rules for changes

1. Every change keeps `npm run render:examples && npm run check:examples` green.
2. A new kit ships with a docs row in `docs/diagrams.md` and at least one example slide.
3. A new check ships with its row in `docs/checks.md`, a level (error, warn or note) and a
   justification for that level. Errors block a build, so they must be defects, not opinions.
4. Look at the rendered PNGs before opening the pull request, and say in the description that you did.

## Local setup

```bash
npm i -D playwright && npx playwright install chromium
node bin/slides.mjs new /tmp/demo && node bin/slides.mjs render /tmp/demo --png
```

Python 3.9+ for the kits; no Python packages required.
