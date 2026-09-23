// Put a generated full-slide SVG into the deck, replacing whatever is there.
// The deck is the output; the script is the source. Never hand-edit injected SVG.
import fs from "node:fs";
import path from "node:path";
import { loadConfig } from "./config.mjs";

export function inject(dir, marker, svgFile) {
  const cfg = loadConfig(dir);
  const deckPath = path.resolve(dir, cfg.deck);
  const s = fs.readFileSync(deckPath, "utf8");
  const a = s.indexOf(marker);
  if (a < 0) throw new Error(`Marker not found in ${cfg.deck}: ${marker}`);
  const b = s.indexOf("</section>", a);
  if (b < 0) throw new Error(`No </section> after ${marker}`);

  let seg = s.slice(a, b);
  const svg = fs.readFileSync(path.resolve(svgFile), "utf8").trimEnd();
  const key = "<svg";
  const i = seg.indexOf(key);
  if (i >= 0 && seg.slice(i, i + 200).includes('left:0; top:0')) {
    const j = seg.indexOf("</svg>", i) + "</svg>".length;
    seg = seg.slice(0, i) + svg + seg.slice(j);
  } else {
    const k = seg.indexOf(">", seg.indexOf("<section")) + 1;
    seg = seg.slice(0, k) + "\n  " + svg + seg.slice(k);
  }
  fs.writeFileSync(deckPath, s.slice(0, a) + seg + s.slice(b));
  console.log(`${marker} <- ${path.basename(svgFile)}`);
}
