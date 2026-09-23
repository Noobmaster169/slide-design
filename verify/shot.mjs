// Rasterise an SVG (or HTML) file with headless Chromium: node verify/shot.mjs in.svg out.png [scale]
import fs from "node:fs";
import path from "node:path";
const [input, output, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg ?? 2);
const mod = process.env.PLAYWRIGHT_MODULE ?? "playwright";
const { chromium } = await import(mod);
const svg = fs.readFileSync(path.resolve(input), "utf8");
const m = svg.match(/width="(\d+)"[^>]*height="(\d+)"/);
const [w, h] = m ? [Number(m[1]), Number(m[2])] : [1600, 900];
const browser = await chromium.launch({ chromiumSandbox: false, args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
await page.goto("file://" + path.resolve(input), { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: output, omitBackground: false });
await browser.close();
console.log(`wrote ${output} (${w}x${h} @${scale}x)`);
