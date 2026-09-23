import fs from "node:fs";
import path from "node:path";
import { openDeck } from "./browser.mjs";
import { loadConfig } from "./config.mjs";

export async function render(dir, { png = false, pdf = true } = {}) {
  const cfg = loadConfig(dir);
  const deckPath = path.resolve(dir, cfg.deck);
  if (!fs.existsSync(deckPath)) throw new Error(`No deck at ${deckPath}`);
  const { browser, page, errors } = await openDeck(deckPath, cfg);

  if (pdf) {
    await page.emulateMedia({ media: "print" });
    await page.pdf({
      path: path.resolve(dir, cfg.out.pdf),
      width: `${cfg.width}px`, height: `${cfg.height}px`,
      printBackground: true, preferCSSPageSize: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });
    console.log(`wrote ${path.join(dir, cfg.out.pdf)}`);
  }

  if (png) {
    await page.emulateMedia({ media: "screen" });
    const out = path.resolve(dir, cfg.out.png);
    fs.mkdirSync(out, { recursive: true });
    for (const f of fs.readdirSync(out)) if (f.startsWith("slide-")) fs.unlinkSync(path.join(out, f));
    const slides = page.locator(cfg.slideSelector);
    const n = await slides.count();
    for (let i = 0; i < n; i++) {
      await slides.nth(i).screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, "0")}.png`) });
    }
    console.log(`wrote ${n} slide images to ${path.join(dir, cfg.out.png)}/`);
    console.log("Now open them. A deck is not finished until someone has looked at every slide.");
  }

  await browser.close();
  if (errors.length) console.warn("page reported:\n  " + errors.join("\n  "));
}
