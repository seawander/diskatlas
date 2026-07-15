#!/usr/bin/env node
/* Tests for the pure helpers in frontend/app.js (no DOM needed). */
const path = require("path");
const L = require(path.join(__dirname, "..", "frontend", "app.js"));

let fails = 0;
function ok(cond, msg) {
  if (!cond) { fails++; console.error("FAIL", msg); }
  else console.log("ok  ", msg);
}
function close(a, b, tol, msg) { ok(Math.abs(a - b) <= tol, msg + ` (${a} vs ${b})`); }

/* wrapRA */
ok(L.wrapRA(370) === 10 && L.wrapRA(-10) === 350, "wrapRA wraps");

/* projection round-trip incl. RA wrap */
const view = { ra0: 350, dec0: 10, ppd: 7 };
for (const [ra, dec] of [[355, 12], [5, -3], [349.9, 10], [180, 60]]) {
  const p = L.project(ra, dec, view, 1000, 600);
  const u = L.unproject(p.x, p.y, view, 1000, 600);
  close(L.wrapRA(u.ra - ra), 0, 1e-9, `roundtrip RA ${ra}`);
  close(u.dec, dec, 1e-9, `roundtrip Dec ${dec}`);
}
/* RA increases leftward: bigger RA -> smaller x */
const pA = L.project(352, 10, view, 1000, 600);
const pB = L.project(348, 10, view, 1000, 600);
ok(pA.x < pB.x, "RA leftward convention");

/* galactic center should map near RA 266.4, Dec -28.94 */
const gc = L.galToEq(0, 0);
close(gc.ra, 266.405, 0.1, "galactic center RA");
close(gc.dec, -28.936, 0.1, "galactic center Dec");
/* NGP l arbitrary, b=90 -> Dec 27.13 */
const ngp = L.galToEq(123, 90);
close(ngp.dec, 27.128, 0.05, "NGP Dec");

/* ecliptic: lam=90 -> Dec = +23.44 */
close(L.eclToEq(90).dec, 23.439, 0.01, "ecliptic max Dec");

/* formatting */
ok(L.fmtWl(1250) === "1.25 mm", "fmtWl mm: " + L.fmtWl(1250));
ok(L.fmtWl(880) === "0.88 mm", "fmtWl sub-mm displays as mm: " + L.fmtWl(880));
ok(L.fmtWl(160) === "160 μm", "fmtWl FIR stays um: " + L.fmtWl(160));
ok(L.fmtWl(1.65).indexOf("μm") > 0, "fmtWl um");

/* links */
ok(L.arxivUrl({ arxiv: "1812.04040" }).endsWith("/abs/1812.04040"), "arxiv url");
ok(L.adsUrl({ bibcode: "2018ApJ...869L..41A" }).includes("2018ApJ...869L..41A"), "ads bibcode url");
ok(L.adsUrl({ arxiv: "1812.04040" }).includes("arXiv:1812.04040"), "ads arxiv fallback");

/* filtering */
const systems = [
  { id: "a", name: "A", categories: ["protoplanetary"], planets: [], images: [{ file: "x", survey: "DSHARP" }] },
  { id: "b", name: "B", categories: ["debris"], planets: [{ name: "b" }], images: [{}] },
  { id: "c", name: "C star", categories: [], planets: [{ name: "b" }], images: [] }
];
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1 }, "").length === 3, "filter all");
ok(L.filterSystems(systems, { proto: 0, debris: 1, planetonly: 1 }, "").length === 2, "filter proto off");
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1, planethost: 1 }, "").length === 2, "planet hosts");
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1, hasimg: 1 }, "").length === 1, "has image");
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1 }, "c st")[0].id === "c", "search");
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1 }, "dsharp")[0].id === "a", "survey search");
ok(L.filterSystems(systems, { proto: 1, debris: 1, planetonly: 1 }, "shar").length === 1, "survey substring search");
ok(L.sysColorKey(systems[2]) === "planetonly", "color key");

process.exit(fails ? 1 : 0);
