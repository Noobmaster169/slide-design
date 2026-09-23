import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export function newDeck(dir, { theme = "default" } = {}) {
  if (fs.existsSync(dir) && fs.readdirSync(dir).length) throw new Error(`${dir} exists and is not empty`);
  const themeDir = path.join(root, "themes", theme);
  if (!fs.existsSync(themeDir)) throw new Error(`No theme "${theme}". Available: ${fs.readdirSync(path.join(root, "themes")).join(", ")}`);

  fs.mkdirSync(path.join(dir, "assets/fonts"), { recursive: true });
  fs.mkdirSync(path.join(dir, "diagrams"), { recursive: true });

  const shell = fs.readFileSync(path.join(root, "templates/deck/deck.html"), "utf8");
  const tokens = JSON.parse(fs.readFileSync(path.join(themeDir, "tokens.json"), "utf8"));
  fs.writeFileSync(path.join(dir, "deck.html"), shell.replace("/*__TOKENS__*/", cssVars(tokens)));
  fs.copyFileSync(path.join(themeDir, "tokens.json"), path.join(dir, "tokens.json"));
  fs.writeFileSync(path.join(dir, "slides.config.json"), JSON.stringify({ deck: "deck.html", check: {} }, null, 2) + "\n");
  fs.copyFileSync(path.join(root, "templates/deck/README.md"), path.join(dir, "README.md"));
  fs.copyFileSync(path.join(root, "templates/deck/example-diagram.py"), path.join(dir, "diagrams/01-diagram.py"));
  fs.writeFileSync(path.join(dir, "assets/fonts/README.md"),
    "Put your font files here and declare them with @font-face in deck.html.\n" +
    "Use fonts you are licensed to embed; open licences such as the SIL OFL are the safe default.\n");
  console.log(`new deck in ${dir} (theme: ${theme})\n  slides render ${dir} --png\n  slides check ${dir}`);
}

export function cssVars(tokens) {
  const lines = ["  :root {"];
  for (const [k, v] of Object.entries(tokens.color ?? {})) lines.push(`    --${k}: ${v};`);
  for (const [k, v] of Object.entries(tokens.font ?? {})) lines.push(`    --font-${k}: ${v};`);
  for (const [k, v] of Object.entries(tokens.size ?? {})) lines.push(`    --size-${k}: ${v}px;`);
  if (tokens.pageBackground) lines.push(`    --page-background: ${tokens.pageBackground};`);
  lines.push("  }");
  return lines.join("\n");
}

export function listThemes() {
  return fs.readdirSync(path.join(root, "themes"));
}
export function listKits() {
  const dir = path.join(root, "kits/python/slidekit");
  return fs.readdirSync(dir).filter((f) => f.endsWith(".py") && !f.startsWith("_") && f !== "core.py")
    .map((f) => f.replace(/\.py$/, ""));
}
