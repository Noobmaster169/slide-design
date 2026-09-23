# What `slides check` reports

It opens the deck in a real browser, measures every slide, and reports what cannot be seen in
source. Errors fail the command (exit 1); warnings and notes do not.

| Rule | Level | Meaning |
|---|---|---|
| `slide-size` | error | a slide is not the configured canvas size |
| `text-overflow` | error | text crosses the slide edge |
| `text-overlap` | error | two pieces of text sit on top of each other |
| `text-over-shape` | error | text covers an arrow or a region marked `data-keep-clear` |
| `banned-char` | error | a character you chose to ban (configure `check.bannedChars`) |
| `page-error` | error | the page threw, or a resource failed to load |
| `font-size` | warn | text below `check.minFontSize` (default 16px) |
| `contrast` | warn | text below `check.minContrast` against its nearest opaque background |
| `title-lines` | warn | a title wraps past `check.maxTitleLines` |
| `external-resource` | warn | the deck loads something over http(s) and will not render offline |
| `img-alt` | warn | an image without alt text |
| `dead-space` | note | more than 20% of the slide bottom is empty |

Configure in `slides.config.json`:

```json
{ "check": { "minFontSize": 18, "bannedChars": ["—"], "allowExternalResources": false } }
```

## Known gaps

- Contrast is skipped when the nearest background is a gradient or an image, because the effective
  background varies across the element. Check those by eye.
- Text overlap is measured on bounding boxes, so two short labels that interleave visually without
  their boxes crossing are not reported, and rotated text is approximated.
- Only shapes marked `class="sk-arrow"` or `data-keep-clear` are protected from text sitting on
  them. Mark anything else you care about.

## What it cannot check

Whether the deck is true, whether the argument holds, whether the picture explains anything, and
whether the story is in the right order. Those need a person looking at the rendered slides. The
checker exists so that a person's attention is spent on those questions instead of on typos in
coordinates.
