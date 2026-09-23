// Resolves a Playwright install. Set PLAYWRIGHT_MODULE to reuse an existing one.
export async function chromium() {
  const mod = process.env.PLAYWRIGHT_MODULE ?? "playwright";
  try {
    const pw = await import(mod);
    return pw.chromium ?? pw.default?.chromium;
  } catch (err) {
    throw new Error(
      `Could not load Playwright from "${mod}".\n` +
      `Install it (npm i -D playwright && npx playwright install chromium)\n` +
      `or point PLAYWRIGHT_MODULE at an existing install.\n${err.message}`
    );
  }
}

export async function openDeck(deckPath, { width, height }) {
  const launch = await chromium();
  const browser = await launch.launch({ chromiumSandbox: false, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("requestfailed", (r) => errors.push(`request failed: ${r.url()}`));
  await page.goto("file://" + deckPath, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  return { browser, page, errors };
}
