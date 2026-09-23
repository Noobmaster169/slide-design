// Opens the deck in a real browser and measures it. Catches the defects that are invisible in
// source: text past a slide edge, labels on top of each other, type too small to read, low
// contrast, resources that will not load offline.
import path from "node:path";
import { openDeck } from "./browser.mjs";
import { loadConfig } from "./config.mjs";

const IN_PAGE = ({ slideSelector, opt }) => {
  const out = [];
  const R = (el) => el.getBoundingClientRect();
  const vis = (el) => {
    const s = getComputedStyle(el);
    if (s.display === "none" || s.visibility === "hidden" || +s.opacity === 0) return false;
    const r = R(el);
    return r.width > 0 && r.height > 0;
  };
  const textOf = (el) => (el.textContent || "").trim();
  const isLeafText = (el) => {
    if (!textOf(el)) return false;
    return ![...el.children].some((c) => textOf(c));
  };
  const lum = (c) => {
    const m = c.match(/[\d.]+/g); if (!m) return null;
    const [r, g, b, a = 1] = m.map(Number);
    if (a < 1) return null;
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const bgOf = (el) => {
    for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.backgroundImage && s.backgroundImage !== "none") return { gradient: true };
      const l = lum(s.backgroundColor);
      if (l !== null) return { lum: l };
    }
    return { lum: 1 };
  };
  const overlap = (a, b) => {
    const w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    return w > opt.overlapTolerance && h > opt.overlapTolerance ? { w, h } : null;
  };
  const push = (slide, level, rule, msg, sample) => out.push({ slide, level, rule, msg, sample });

  const slides = [...document.querySelectorAll(slideSelector)];
  slides.forEach((slide, i) => {
    const n = i + 1;
    const sr = R(slide);
    if (Math.abs(sr.width - opt.width) > 1 || Math.abs(sr.height - opt.height) > 1)
      push(n, "error", "slide-size", `slide is ${Math.round(sr.width)}x${Math.round(sr.height)}, expected ${opt.width}x${opt.height}`);

    // --- text elements: HTML leaves plus SVG <text>
    const htmlText = [...slide.querySelectorAll("*")].filter((el) => !(el instanceof SVGElement) && vis(el) && isLeafText(el));
    const svgText = [...slide.querySelectorAll("text")].filter((el) => vis(el) && textOf(el));
    const texts = [...htmlText, ...svgText];

    for (const el of texts) {
      const r = R(el), t = textOf(el).slice(0, 48);
      if (r.left < sr.left - 1 || r.right > sr.right + 1 || r.top < sr.top - 1 || r.bottom > sr.bottom + 1)
        push(n, "error", "text-overflow", `text crosses the slide edge: "${t}"`);
      const size = parseFloat(getComputedStyle(el).fontSize);
      if (size && size < opt.minFontSize)
        push(n, "warn", "font-size", `${Math.round(size)}px text, minimum is ${opt.minFontSize}px: "${t}"`);
      const bg = bgOf(el);
      const fg = lum(getComputedStyle(el).color ?? (el.getAttribute("fill") || ""));
      if (!bg.gradient && bg.lum !== undefined && fg !== null) {
        const ratio = (Math.max(fg, bg.lum) + 0.05) / (Math.min(fg, bg.lum) + 0.05);
        if (ratio < opt.minContrast)
          push(n, "warn", "contrast", `contrast ${ratio.toFixed(1)}:1 below ${opt.minContrast}:1: "${t}"`);
      }
      if (opt.bannedChars.length) {
        const hit = opt.bannedChars.find((c) => textOf(el).includes(c));
        if (hit) push(n, "error", "banned-char", `contains ${JSON.stringify(hit)}: "${t}"`);
      }
    }

    // --- text on text
    for (let a = 0; a < texts.length; a++) {
      for (let b = a + 1; b < texts.length; b++) {
        if (texts[a].contains(texts[b]) || texts[b].contains(texts[a])) continue;
        const o = overlap(R(texts[a]), R(texts[b]));
        if (o) push(n, "error", "text-overlap",
          `"${textOf(texts[a]).slice(0, 28)}" overlaps "${textOf(texts[b]).slice(0, 28)}" by ${Math.round(o.w)}x${Math.round(o.h)}px`);
      }
    }

    // --- text on a shape that must stay readable (arrows, marked regions)
    const keepClear = [...slide.querySelectorAll(".sk-arrow, [data-keep-clear]")].filter(vis);
    for (const t of texts) {
      for (const k of keepClear) {
        if (k.contains(t)) continue;
        const o = overlap(R(t), R(k));
        if (o) push(n, "error", "text-over-shape",
          `"${textOf(t).slice(0, 28)}" sits on an arrow or protected shape (${Math.round(o.w)}x${Math.round(o.h)}px)`);
      }
    }

    // --- titles that run too long
    for (const el of slide.querySelectorAll("[data-title], h1, h2")) {
      if (!vis(el)) continue;
      const cs = getComputedStyle(el);
      const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
      const lines = Math.round(R(el).height / lh);
      if (lines > opt.maxTitleLines)
        push(n, "warn", "title-lines", `title wraps to ${lines} lines (max ${opt.maxTitleLines}): "${textOf(el).slice(0, 40)}"`);
    }

    // --- offline safety and alt text
    for (const el of slide.querySelectorAll("img, image, script, link, use")) {
      const url = el.getAttribute("src") || el.getAttribute("href") || el.getAttribute("xlink:href") || "";
      if (/^https?:/i.test(url) && !opt.allowExternalResources)
        push(n, "warn", "external-resource", `loads ${url.slice(0, 60)}; a deck should render offline`);
      if (el.tagName.toLowerCase() === "img" && opt.requireImageAlt && !el.hasAttribute("alt"))
        push(n, "warn", "img-alt", `image without alt: ${(el.getAttribute("src") || "").slice(0, 50)}`);
    }

    // --- dead space at the bottom (informational: some layouts want it)
    const contentBottom = [...slide.querySelectorAll("*")].filter(vis)
      .reduce((m, el) => Math.max(m, R(el).bottom), sr.top);
    const empty = (sr.bottom - contentBottom) / sr.height;
    if (empty > 0.2) push(n, "info", "dead-space", `bottom ${Math.round(empty * 100)}% of the slide is empty`);
  });

  return { count: slides.length, findings: out };
};

export async function check(dir) {
  const cfg = loadConfig(dir);
  const deckPath = path.resolve(dir, cfg.deck);
  const { browser, page, errors } = await openDeck(deckPath, cfg);
  const res = await page.evaluate(IN_PAGE, {
    slideSelector: cfg.slideSelector,
    opt: { ...cfg.check, width: cfg.width, height: cfg.height }
  });
  await browser.close();

  for (const e of errors) res.findings.push({ slide: 0, level: "error", rule: "page-error", msg: e });

  const order = { error: 0, warn: 1, info: 2 };
  res.findings.sort((a, b) => a.slide - b.slide || order[a.level] - order[b.level]);
  const counts = { error: 0, warn: 0, info: 0 };
  for (const f of res.findings) counts[f.level]++;

  console.log(`${res.count} slides checked in ${path.basename(dir)}`);
  let last = null;
  for (const f of res.findings) {
    if (f.slide !== last) { console.log(`\n  slide ${String(f.slide).padStart(2, "0")}`); last = f.slide; }
    const tag = { error: "ERROR", warn: " WARN", info: " INFO" }[f.level];
    console.log(`    ${tag}  ${f.rule.padEnd(18)} ${f.msg}`);
  }
  console.log(`\n${counts.error} errors, ${counts.warn} warnings, ${counts.info} notes`);
  if (!counts.error) console.log("No blocking issues. Now look at the rendered images: a checker cannot tell you the deck makes its point.");
  return counts.error === 0;
}
