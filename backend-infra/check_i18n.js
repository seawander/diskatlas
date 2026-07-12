#!/usr/bin/env node
/* CI guard: every UI language in frontend/i18n.js has every key present in `en`.
 *
 * i18n.js sets window.I18N = { en:{...}, zh:{...}, ... } and window.I18N_LANGS.
 * We evaluate it in a minimal `window` shim (no DOM), take `en` as the source of
 * truth, and report any key missing from another language block. `t()` falls
 * back to English at runtime, so missing keys are not fatal to users — but they
 * mean untranslated chrome, which this check surfaces before it ships.
 *
 * Exit 1 if any language is missing keys (or a declared language block is
 * absent entirely); exit 0 when all languages are complete.
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const src = fs.readFileSync(
  path.join(__dirname, "..", "frontend", "i18n.js"), "utf8");

const sandbox = { window: {} };
vm.runInNewContext(src, sandbox);

const I18N = sandbox.window.I18N || {};
const declared = (sandbox.window.I18N_LANGS || []).map((p) => p[0]);
const langs = declared.length ? declared : Object.keys(I18N);

if (!I18N.en) {
  console.error("ERROR: no `en` block in i18n.js — cannot check completeness");
  process.exit(1);
}
const enKeys = Object.keys(I18N.en);
let missingTotal = 0;

for (const lang of langs) {
  const block = I18N[lang];
  if (!block) {
    console.error(`ERROR: language '${lang}' declared but has no I18N block`);
    missingTotal += enKeys.length;
    continue;
  }
  const missing = enKeys.filter((k) => !(k in block));
  if (missing.length) {
    missingTotal += missing.length;
    console.error(
      `ERROR: '${lang}' missing ${missing.length} key(s): ${missing.join(", ")}`);
  } else {
    console.log(`ok   ${lang}: ${enKeys.length}/${enKeys.length} keys`);
  }
}

console.log(
  `\n${langs.length} languages, ${enKeys.length} keys each; ` +
  `${missingTotal} missing.`);
process.exit(missingTotal ? 1 : 0);
