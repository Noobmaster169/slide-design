# Theming

`tokens.json` is the single source. `slides tokens .` prints the `:root` block; paste it into
`deck.html` (or generate it in your build). `slidekit` reads the same file, so SVG and CSS cannot
drift.

Bundled themes: `default` (light), `dark`, `high-contrast`. They exist to make the point that the
look is a choice. Change every value.

## Making a theme yours

1. Pick one accent. It means "this is the subject". Everything else is ink and surfaces.
2. Set an ink scale (primary, secondary, muted) and check it against your surface, not against
   white, if your surface is dark.
3. Reserve status colours (good, warning, serious) for status only.
4. Choose at most three faces: display, sans, mono. Licence them for embedding; open licences such
   as the SIL OFL are the safe default. Put the files in `assets/fonts/` and declare `@font-face`.
   A deck that loads fonts from a CDN renders differently offline and on the day.
5. Run `slides check .` and fix contrast warnings before you like it too much.

## Brand decks

If your organisation has a design system, map it onto `tokens.json` and keep the archetypes. The
method is independent of the palette.
