#!/usr/bin/env node
import { render } from "../src/render.mjs";
import { check } from "../src/check.mjs";
import { newDeck, listThemes, listKits, cssVars } from "../src/scaffold.mjs";
import { inject } from "../src/inject.mjs";
import fs from "node:fs";
import path from "node:path";

const [cmd, ...rest] = process.argv.slice(2);
const args = rest.filter((a) => !a.startsWith("--"));
const flags = Object.fromEntries(rest.filter((a) => a.startsWith("--")).map((a) => {
  const [k, v] = a.replace(/^--/, "").split("="); return [k, v ?? true];
}));
const dir = args[0] ?? ".";

const help = `slides - build slide decks as code

  slides new <dir> [--theme=default]   scaffold a deck
  slides render [dir] [--png] [--no-pdf]
  slides check [dir]                   measure the rendered deck and report layout defects
  slides inject <marker> <svg> [dir]   place a generated SVG into the slide with that marker
  slides tokens [dir]                  print the :root block for the deck's tokens.json
  slides themes                        list themes
  slides kits                          list diagram kits

Docs: docs/method.md (how to build a deck), docs/checks.md (what check reports),
      docs/alternatives.md (when another tool fits better).`;

try {
  switch (cmd) {
    case "new": await newDeck(args[0], { theme: flags.theme }); break;
    case "render": await render(dir, { png: !!flags.png, pdf: flags.pdf !== "false" && !flags["no-pdf"] }); break;
    case "check": process.exitCode = (await check(dir)) ? 0 : 1; break;
    case "inject": inject(args[2] ?? ".", args[0], args[1]); break;
    case "tokens": {
      const f = path.join(dir, "tokens.json");
      if (!fs.existsSync(f)) throw new Error(`No tokens.json in ${dir}`);
      console.log(cssVars(JSON.parse(fs.readFileSync(f, "utf8"))));
      break;
    }
    case "themes": console.log(listThemes().join("\n")); break;
    case "kits": console.log(listKits().join("\n")); break;
    default: console.log(help);
  }
} catch (err) {
  console.error(String(err.message ?? err));
  process.exitCode = 1;
}
