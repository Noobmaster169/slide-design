# Using the output

figura writes a standalone SVG. Where it goes is your problem, and that is deliberate.

**Slides.** Inline the SVG in an HTML deck, or drop the PNG into PowerPoint, Keynote or Google
Slides. Draw at the slide's pixel size (1920x1080) and it lands exactly.

**Documents.** SVG in Markdown works on GitHub and in most static site generators. For Word or
InDesign, use the PNG at 2x or the PDF.

**Web.** Inline the SVG so CSS can style it, or use `<img>`. Elements keep their structure, so
hover and click handlers can be attached after the fact.

**Print.** Use the `print` theme: flat colours, hairlines that survive photocopying, no soft tints.
Render to PDF with `rsvg-convert -f pdf`.

**Dark interfaces.** Render twice, once per theme, and swap with `prefers-color-scheme`. Do not
invert a light figure; the `dark` theme has its own steps for a reason.

**Fonts.** The SVG names font families, it does not embed them. For a figure that must look
identical everywhere, either rasterise to PNG, or convert text to paths in your export step, or
stick to a widely available family.
