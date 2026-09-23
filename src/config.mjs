import fs from "node:fs";
import path from "node:path";

export const DEFAULTS = {
  deck: "deck.html",
  slideSelector: "section.slide",
  width: 1920,
  height: 1080,
  out: { pdf: "deck.pdf", png: "preview" },
  check: {
    minFontSize: 16,          // px, below this a slide is unreadable from the back of a room
    minContrast: 4.5,         // WCAG AA for body text
    maxTitleLines: 3,
    bannedChars: [],          // e.g. ["—"] to ban em dashes; empty by default
    allowExternalResources: false,
    requireImageAlt: true,
    overlapTolerance: 2       // px of intersection ignored before reporting an overlap
  }
};

export function loadConfig(dir) {
  const file = path.join(dir, "slides.config.json");
  const user = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
  return {
    ...DEFAULTS, ...user,
    out: { ...DEFAULTS.out, ...(user.out ?? {}) },
    check: { ...DEFAULTS.check, ...(user.check ?? {}) }
  };
}
