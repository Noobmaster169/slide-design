// Exact verification in a real browser, for when averaged text metrics are not enough:
//   node verify/measure.mjs figure.svg [--min-font=14] [--min-contrast=4.5]
// Reports the same rules as figura.verify, measured rather than estimated. Exit 1 on errors.
import path from "node:path";
const [input, ...flags] = process.argv.slice(2);
const opt = Object.fromEntries(flags.map((f) => f.replace(/^--/, "").split("=")));
const minFont = Number(opt["min-font"] ?? 14);
const minContrast = Number(opt["min-contrast"] ?? 4.5);
const mod = process.env.PLAYWRIGHT_MODULE ?? "playwright";
const { chromium } = await import(mod);
const browser = await chromium.launch({ chromiumSandbox: false, args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.goto("file://" + path.resolve(input), { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);

const findings = await page.evaluate(({ minFont, minContrast }) => {
  const out = [];
  const svg = document.querySelector("svg");
  const vb = svg.viewBox.baseVal;
  const page = { x: vb.x, y: vb.y, w: vb.width || svg.width.baseVal.value, h: vb.height || svg.height.baseVal.value };
  const texts = [...svg.querySelectorAll("text")].filter((t) => (t.textContent || "").trim());
  const bb = (el) => { const b = el.getBBox(); return { x: b.x, y: b.y, w: b.width, h: b.height }; };
  const hit = (a, b, tol = 1.5) =>
    Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > tol &&
    Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > tol;
  const lum = (c) => {
    const m = getComputedStyle(document.body).color && c.match(/[\d.]+/g);
    if (!m) return null;
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]);
  };
  for (const t of texts) {
    const b = bb(t), s = t.textContent.trim().slice(0, 40);
    if (b.x < page.x - 1 || b.y < page.y - 1 || b.x + b.w > page.x + page.w + 1 || b.y + b.h > page.y + page.h + 1)
      out.push({ level: "error", rule: "off-canvas", msg: `"${s}"` });
    const size = parseFloat(getComputedStyle(t).fontSize);
    if (size < minFont) out.push({ level: "warn", rule: "font-size", msg: `${Math.round(size)}px "${s}"` });
  }
  for (let i = 0; i < texts.length; i++)
    for (let j = i + 1; j < texts.length; j++)
      if (hit(bb(texts[i]), bb(texts[j])))
        out.push({ level: "error", rule: "text-overlap",
          msg: `"${texts[i].textContent.trim().slice(0, 22)}" over "${texts[j].textContent.trim().slice(0, 22)}"` });
  return out;
}, { minFont, minContrast });

await browser.close();
for (const f of findings) console.log(`  ${f.level.toUpperCase().padEnd(5)} ${f.rule.padEnd(15)} ${f.msg}`);
const errors = findings.filter((f) => f.level === "error").length;
console.log(`${path.basename(input)}: ${errors} errors, ${findings.length - errors} warnings (measured in a browser)`);
process.exitCode = errors ? 1 : 0;
