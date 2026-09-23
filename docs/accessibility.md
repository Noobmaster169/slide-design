# Accessibility and the room

- **Contrast.** `slides check` warns below 4.5:1. Projectors wash out; 7:1 for body text is safer.
- **Size.** 16px is the floor this repo enforces by default; for a large room start at 24px body
  text and raise `check.minFontSize` to match.
- **Colour is never the only signal.** Status needs a word or a shape as well as a hue. Roughly one
  in twelve men has a colour vision deficiency.
- **Alt text.** Images carry `alt`. The PDF keeps text as text, so it can be read aloud and searched.
- **Motion.** None here by design. A printed PDF cannot animate, and a deck that depends on
  animation cannot be sent to anyone.
- **Language and direction.** Set `<html lang>`. For right-to-left scripts, set `dir="rtl"` on the
  deck and mirror your layouts; the kits draw left to right unless you tell them otherwise.
- **The handout question.** If people will read it without you, the deck needs sentences, not
  fragments. Consider a separate written document instead of denser slides.
