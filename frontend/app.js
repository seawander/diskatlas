/* Resolved Disks & Imaged Planets — all-sky atlas.
   Vanilla JS, offline, file:// friendly. Pure helpers are exported for node tests. */
"use strict";

/* ---------------- pure helpers (testable) ---------------- */

const D2R = Math.PI / 180, R2D = 180 / Math.PI;

function wrapRA(ra) { ra = ra % 360; return ra < 0 ? ra + 360 : ra; }

/* Equirectangular; RA increases LEFTWARD (sky convention). view = {ra0, dec0, ppd} */
function project(ra, dec, view, W, H) {
  let d = wrapRA(ra) - wrapRA(view.ra0);
  if (d > 180) d -= 360;
  if (d < -180) d += 360;
  const yc = (H + (view.topInset || 0)) / 2;   // vertical center of the area below the fixed header
  return { x: W / 2 - d * view.ppd, y: yc - (dec - view.dec0) * view.ppd };
}
function unproject(x, y, view, W, H) {
  const yc = (H + (view.topInset || 0)) / 2;
  const ra = wrapRA(view.ra0 - (x - W / 2) / view.ppd);
  const dec = view.dec0 + (yc - y) / view.ppd;
  return { ra, dec };
}

/* galactic (l,b) -> equatorial J2000 (deg) */
function galToEq(l, b) {
  const aG = 192.85948 * D2R, dG = 27.12825 * D2R, lNCP = 122.93192 * D2R;
  l *= D2R; b *= D2R;
  const sinDec = Math.sin(b) * Math.sin(dG) +
    Math.cos(b) * Math.cos(dG) * Math.cos(lNCP - l);
  const dec = Math.asin(sinDec);
  const y = Math.cos(b) * Math.sin(lNCP - l);
  const x = Math.sin(b) * Math.cos(dG) - Math.cos(b) * Math.sin(dG) * Math.cos(lNCP - l);
  const ra = wrapRA((aG + Math.atan2(y, x)) * R2D);
  return { ra, dec: dec * R2D };
}
/* ecliptic lon (deg, lat=0) -> equatorial */
function eclToEq(lam) {
  const eps = 23.43928 * D2R; lam *= D2R;
  const ra = Math.atan2(Math.sin(lam) * Math.cos(eps), Math.cos(lam)) * R2D;
  const dec = Math.asin(Math.sin(eps) * Math.sin(lam)) * R2D;
  return { ra: wrapRA(ra), dec };
}

function fmtWl(um) {
  if (um == null) return "?";
  /* >=300 um displays as mm, matching the WL_BANDS "mm" band (>0.3mm) */
  if (um >= 300) { const mm = um / 1000; return (mm >= 10 ? mm.toFixed(0) : mm.toFixed(2).replace(/0+$/, "").replace(/\.$/, "")) + " mm"; }
  if (um < 0.01) return (um * 1000).toFixed(1) + " nm";
  return (um >= 10 ? um.toFixed(0) : +um.toFixed(2)) + " μm";
}
function arxivUrl(p) { return p && p.arxiv ? "https://arxiv.org/abs/" + p.arxiv : null; }
/* SciX (the successor to NASA ADS): https://scixplorer.org/abs/<bibcode>/abstract */
function adsUrl(p) {
  if (!p) return null;
  if (p.bibcode) return "https://scixplorer.org/abs/" + encodeURIComponent(p.bibcode) + "/abstract";
  if (p.arxiv) return "https://scixplorer.org/abs/arXiv:" + p.arxiv + "/abstract";
  return null;
}
/* Every paper a system records (image, planet discovery, extra_papers), indexed
   by "<first-author surname>|<year>" so an inline citation mention in free-text
   notes can link to that real abstract instead of a blind author search. */
/* surname key for citation matching: last whitespace-separated token, accents
   stripped, lowercased — so "Huélamo"/"Huelamo" collide and "van Capelleveen"
   keys on "capelleveen". Both citeIndex and linkifyCitations use it, so a
   mention links to the recorded paper regardless of accent spelling. */
function citeSurname(name) {
  return String(name).trim().split(/\s+/).pop()
    .normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase();
}
function citeIndex(s) {
  const idx = {};
  const add = p => {
    if (!p || !p.first_author || !p.year) return;
    const url = adsUrl(p) || arxivUrl(p);
    if (!url) return;
    const surname = citeSurname(p.first_author);
    const key = surname + "|" + p.year;
    if (!idx[key]) idx[key] = url;                 // first paper for a surname/year wins
  };
  (s.images || []).forEach(i => add(i.paper));
  (s.planets || []).forEach(pl => { add(pl.paper); (pl.extra_papers || []).forEach(add); });
  return idx;
}
/* Turn "Mesa+2023", "Kenworthy et al. 2025", "Smith & Terrile 1984" citation
   mentions inside already-HTML-escaped free text into links: to the real
   abstract when the system already records that paper, else a SciX search. */
function linkifyCitations(escapedText, idx) {
  if (!escapedText) return "";
  idx = idx || {};
  const link = (m, name, year) => {
    const surname = citeSurname(name);
    const href = idx[surname + "|" + year] ||
      "https://scixplorer.org/search?q=" +
      encodeURIComponent('author:"' + name + '" year:' + year) + "&sort=score+desc";
    return '<a href="' + href + '" target="_blank" rel="noopener">' + m + "</a>";
  };
  return escapedText
    .replace(/\b((?:(?:De|Del|Van|Von|Le|La|Di|Da|Mac|Mc|El|O')\s+)?[A-Z][A-Za-zÀ-ÿ'-]+)\+((?:19|20)\d{2}[a-z]?)\b/g,
             (m, n, y) => link(m, n, y.replace(/[a-z]$/, "")))
    .replace(/\b((?:(?:De|Del|Van|Von|Le|La|Di|Da|Mac|Mc|El|O')\s+)?[A-Z][A-Za-zÀ-ÿ'-]+)(?:\s*(?:&amp;|&)\s*[A-Z][A-Za-zÀ-ÿ'-]+)?\s+et al\.?,?\s+\(?((?:19|20)\d{2})\)?/g,
             (m, n, y) => link(m, n, y))
    .replace(/\b([A-Z][A-Za-zÀ-ÿ'-]+)\s*(?:&amp;|&)\s*[A-Z][A-Za-zÀ-ÿ'-]+\s+\(?((?:19|20)\d{2})\)?/g,
             (m, n, y) => link(m, n, y));
}

function citeStr(p) {
  if (!p) return "citation missing";
  const j = p.journal ? ", " + p.journal : "";
  return (p.first_author || "?") + " et al. " + (p.year || "") + j;
}

function sysHasPlanet(s) { return (s.planets || []).length > 0; }
function planetMethod(p) { return p.method || "imaging"; }
function activePlanets(s) {
  return (s.planets || []).filter(p => p.status !== "refuted");
}
function sysHasImagedPlanet(s) {
  return activePlanets(s).some(p => planetMethod(p) !== "transit");
}
/* every companion claim refuted (kept for the historical record) — rendered
   as a HOLLOW marker so the map doesn't promise an active companion */
function sysRefutedOnly(s) {
  return (s.planets || []).length > 0 && activePlanets(s).length === 0;
}
/* CSS marker class for a system's type icon (adds the hollow variant) */
function mkClass(s) {
  const k = sysColorKey(s);
  return k === "planetonly" && sysRefutedOnly(s) ? k + " hollow" : k;
}
function sysHasImage(s) { return (s.images || []).some(i => i.file); }
function sysColorKey(s) {
  const c = s.categories || [];
  if (c.includes("quasar")) return "quasar";
  if (c.includes("protoplanetary")) return "proto";
  if (c.includes("debris")) return "debris";
  if (c.includes("evolved")) return "evolved";
  return "planetonly";
}
/* distinct SHAPE per category (colorblind + B/W-print friendly): circle/triangle/diamond/square/hexagon */
const SYS_SHAPE = { proto: "circle", debris: "triangle", planetonly: "diamond", quasar: "square", evolved: "hexagon" };
const SYS_GLYPH = { proto: "●", debris: "▲", planetonly: "◆", quasar: "■", evolved: "⬢" };
function sysShape(key) { return SYS_SHAPE[key] || "circle"; }
function sysGlyph(key) { return SYS_GLYPH[key] || "●"; }
/* wavelength bands (ordered): a record falls in the first band it is < max of */
const WL_BANDS = [
  { key: "opt", label: "Visible", sub: "<1μm", max: 1 },
  { key: "nir", label: "NIR", sub: "1–5μm", max: 5 },
  { key: "mir", label: "MIR", sub: "5–300μm", max: 300 },
  { key: "mm", label: "mm", sub: ">0.3mm", max: Infinity }
];
function wlBand(um) {
  if (um == null) return "nir";
  for (const b of WL_BANDS) if (um < b.max) return b.key;
  return "mm";
}
/* matrix column key for an image record */
function imgCol(im) { return im.type === "planet" ? "planet" : wlBand(im.wavelength_um); }
function facShort(f) {
  return (f || "?").replace("VLT-", "").replace("Gemini-", "").replace("Subaru-", "")
    .replace("Keck-", "").replace("/HRC", "").replace(" coronagraph", "").trim();
}
/* coarse modality predicates (match coverage_audit: mm = mm-interferometry, nir = scattered light) */
function sysHasMm(s) { return (s.images || []).some(i => i.type === "disk_mm" && wlBand(i.wavelength_um) === "mm"); }
function sysHasNir(s) { return (s.images || []).some(i => i.type === "disk_scattered"); }

/* every distinct paper a system records (image credits + planet discoveries +
   extra_papers), so the search box can answer "is paper X already in the
   atlas, and where?" — memoized on the system object. */
function sysPapers(s) {
  if (s.__papers) return s.__papers;
  const seen = new Set(), out = [];
  const add = p => {
    if (!p) return;
    const k = (p.arxiv || p.bibcode || "") + "|" + (p.first_author || "") + "|" + (p.year || "");
    if (k === "||" || seen.has(k)) return;
    seen.add(k); out.push(p);
  };
  (s.images || []).forEach(i => add(i.paper));
  (s.planets || []).forEach(pl => { add(pl.paper); (pl.extra_papers || []).forEach(add); });
  return (s.__papers = out);
}
function paperTokens(p) { return [p.first_author, p.year, p.arxiv, p.bibcode].filter(Boolean).join(" ").toLowerCase(); }
/* distinct survey/program tags across a system's image records (DSHARP, exoALMA,
   MAPS, AGE-PRO, REASONS, ALICE, the fragmented Taurus tags, …) — scientific
   data, matched verbatim and never translated. Memoized. */
function sysSurveys(s) {
  if (s.__surveys) return s.__surveys;
  const seen = new Set(), out = [];
  (s.images || []).forEach(i => { if (i.survey && !seen.has(i.survey)) { seen.add(i.survey); out.push(i.survey); } });
  return (s.__surveys = out);
}
/* search haystack: system name/id/alt_names PLUS each recorded paper's
   author/year/arXiv/bibcode (not titles — too noisy). Surveys are matched
   separately (surveyMatch), NOT folded in here — substring would let "SONS"
   collide with "REASONS". Memoized. */
function sysHay(s) {
  if (s.__hay != null) return s.__hay;
  const parts = [s.name, s.id, ...(s.alt_names || [])].filter(Boolean).map(x => String(x).toLowerCase());
  return (s.__hay = parts.concat(sysPapers(s).map(paperTokens)).join(" "));
}
/* survey match: query is a prefix of the whole tag OR of any of its tokens
   (split on non-alphanumerics). So "sons"→SONS not REASONS, "age-pro"→AGE-PRO,
   and "taurus"→SPHERE-Taurus / Taurus-Long2019. Case-insensitive. */
function surveyMatch(v, q) {
  const lv = v.toLowerCase();
  return lv.startsWith(q) || lv.split(/[^a-z0-9]+/).some(t => t && t.startsWith(q));
}
/* the recorded paper / survey a query matched (for annotating a result row) */
function matchedPaper(s, q) { return sysPapers(s).find(p => paperTokens(p).includes(q)) || null; }
function matchedSurvey(s, q) { return sysSurveys(s).find(v => surveyMatch(v, q)) || null; }

function filterSystems(systems, f, q) {
  q = (q || "").trim().toLowerCase();
  const facSet = f.facilities && f.facilities.size ? f.facilities : null;
  const instSet = f.instruments && f.instruments.size ? f.instruments : null;
  const bandSet = f.bands && f.bands.size ? f.bands : null;
  const missSet = f.missing && f.missing.size ? f.missing : null;
  const contSet = f.content && f.content.size ? f.content : null;
  const survSet = f.surveys && f.surveys.size ? f.surveys : null;
  return systems.filter(s => {
    const key = sysColorKey(s);
    if (key === "proto" && !f.proto) return false;
    if (key === "debris" && !f.debris) return false;
    if (key === "planetonly") {
      /* hollow-◆ systems (every companion claim refuted) have their own
         toggle; missing key = visible, matching the quasar/evolved pattern */
      if (sysRefutedOnly(s) ? f.refutedonly === false : !f.planetonly) return false;
    }
    if (key === "quasar" && f.quasar === false) return false;
    if (key === "evolved" && f.evolved === false) return false;
    if (f.planethost && !sysHasImagedPlanet(s)) return false;
    if (f.hasimg && !sysHasImage(s)) return false;
    if (facSet) {
      const fs = new Set((s.images || []).flatMap(i => i.fac_keys || []));
      /* ALL selected facilities must have visited the system (shift-click combines);
         selecting VLT also counts VLTI records; VLTI stays specific */
      const hit = [...facSet].every(x => fs.has(x) || (x === "VLT" && fs.has("VLTI")));
      if (!hit) return false;
    }
    if (instSet) {
      const is = [...new Set((s.images || []).map(i => i.instr_key).filter(Boolean))];
      /* a selected PARENT instrument (no "/") also matches its sub-instruments, e.g.
         "SPHERE" matches SPHERE + SPHERE/IRDIS + SPHERE/ZIMPOL + SPHERE/IFS; a specific
         "SPHERE/IRDIS" matches only itself (parent ⊇ children, one-directional) */
      const instrHit = x => is.some(k => k === x || (!x.includes("/") && k.startsWith(x + "/")));
      if (![...instSet].every(instrHit)) return false;
    }
    if (bandSet) {
      /* a record belongs to its wavelength band AND (if a companion) the planet band,
         so a "MIR" filter matches TWA 7's MIR companion-detection record too. */
      const bs = new Set();
      for (const im of (s.images || [])) { bs.add(wlBand(im.wavelength_um)); if (im.type === "planet") bs.add("planet"); }
      if (![...bandSet].some(x => bs.has(x))) return false;
    }
    if (contSet) {
      /* continuum vs (spectral-)line data products; same ANY-of semantics as bands */
      const cs = new Set((s.images || []).map(i => i.content).filter(Boolean));
      if (![...contSet].some(x => cs.has(x))) return false;
    }
    if (missSet) {
      if (missSet.has("mm") && sysHasMm(s)) return false;
      if (missSet.has("nir") && sysHasNir(s)) return false;
      if (missSet.has("planet") && sysHasImagedPlanet(s)) return false;
    }
    if (survSet) {
      /* observed in ANY of the selected programs (union), exact tag match */
      const ss = new Set((s.images || []).map(i => i.survey).filter(Boolean));
      if (![...survSet].some(x => ss.has(x))) return false;
    }
    if (q && !sysHay(s).includes(q) && !matchedSurvey(s, q)) return false;   // name/id/alt/paper substring, OR a survey prefix
    return true;
  });
}

/* node test hook */
if (typeof module !== "undefined" && module.exports) {
  module.exports = { wrapRA, project, unproject, galToEq, eclToEq, fmtWl,
    arxivUrl, adsUrl, filterSystems, sysColorKey, wlBand, imgCol, facShort, sysShape, sysGlyph };
}

/* ---------------- browser app ---------------- */
if (typeof window !== "undefined") (function () {

  const A = window.ATLAS || { systems: [], stats: {}, generated: "?" };
  const SYS = A.systems.filter(s => true);
  const PLOT = () => SYS.filter(s => s.ra_deg != null && visible.has(s.id));

  /* ---------- i18n ---------- */
  const I18N = window.I18N || { en: {} };
  let lang = localStorage.getItem("atlas_lang") || (navigator.language || "en").slice(0, 2).toLowerCase();
  if (!I18N[lang]) lang = "en";
  function t(k) {
    const L = I18N[lang] || {};
    return L[k] != null ? L[k] : (I18N.en[k] != null ? I18N.en[k] : k);
  }
  function applyStaticI18n() {
    document.documentElement.lang = lang;
    document.documentElement.dir = (window.I18N_RTL || []).indexOf(lang) >= 0 ? "rtl" : "ltr";
    document.title = "diskatlas: " + t("title");
    document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
    document.querySelectorAll("[data-i18n-title]").forEach(el => { el.title = t(el.dataset.i18nTitle); });
    document.querySelectorAll("[data-i18n-aria]").forEach(el => { el.setAttribute("aria-label", t(el.dataset.i18nAria)); });
  }
  function setLang(l) {
    lang = I18N[l] ? l : "en";
    localStorage.setItem("atlas_lang", lang);
    applyStaticI18n();
    draw();                                     // refresh statsline
    if (currentView === "matrix") buildMatrix();
    else if (currentView === "tonight") computeTonight();
    if (currentSys) openDetail(currentSys);
  }
  const CAT_KEY = { protoplanetary: "cat_proto", debris: "cat_debris", quasar: "cat_quasar", evolved: "cat_evolved" };
  function catLabel(c) { return t(CAT_KEY[c] || c); }

  const canvas = document.getElementById("sky");
  const ctx = canvas.getContext("2d");
  const tooltip = document.getElementById("tooltip");
  const detail = document.getElementById("detail");
  const searchEl = document.getElementById("search");
  const listEl = document.getElementById("searchlist");

  const COL = {};
  function refreshCOL() {
    const CSS = getComputedStyle(document.body || document.documentElement);
    COL.proto = CSS.getPropertyValue("--proto").trim() || "#3fd0c9";
    COL.debris = CSS.getPropertyValue("--debris").trim() || "#ffb454";
    COL.planetonly = CSS.getPropertyValue("--planetonly").trim() || "#c792ea";
    COL.quasar = CSS.getPropertyValue("--quasar").trim() || "#ff5c8a";
    COL.evolved = CSS.getPropertyValue("--evolved").trim() || "#e6be2e";
    COL.ink = CSS.getPropertyValue("--ink").trim() || "#e8ecf8";
    COL.dim = CSS.getPropertyValue("--dim").trim() || "#9aa7c7";
    COL.line = CSS.getPropertyValue("--line").trim() || "#2a3560";
    COL.sky = CSS.getPropertyValue("--sky").trim() || "#070b18";
    /* map overlay colors need different alphas per theme: the dark values
       are too faint to survive on a light background */
    const light = document.body && document.body.classList.contains("light");
    COL.grid = light ? "rgba(47,88,160,.22)" : "rgba(110,168,255,.14)";
    COL.gridlab2 = light ? "rgba(70,88,125,.7)" : "rgba(154,167,199,.6)";
    COL.constline = light ? "rgba(56,82,138,.40)" : "rgba(120,140,190,.30)";
    COL.constlab = light ? "rgba(50,74,126,.62)" : "rgba(140,160,210,.42)";
    COL.gal = light ? "rgba(60,100,190,.38)" : "rgba(160,190,255,.28)";
    COL.ecl = light ? "rgba(185,115,25,.40)" : "rgba(255,190,120,.20)";
    /* opaque variants so the on-curve labels stay legible (the lines are faint) */
    COL.gallab = light ? "rgba(52,92,180,.95)" : "rgba(178,202,255,.9)";
    COL.ecllab = light ? "rgba(170,105,20,.95)" : "rgba(255,200,140,.9)";
    COL.hover = light ? "#1c2438" : "#fff";
    COL.namelab = light ? "rgba(28,36,56,.92)" : "rgba(232,236,248,.85)";
  };

  let W = 0, H = 0, DPR = 1;
  /* optional ?fontscale=1.3 enlarges the map's canvas labels (print captures) */
  const FSCALE = parseFloat(new URLSearchParams(location.search).get("fontscale")) || 1;
  const fpx = n => Math.round(n * FSCALE * 10) / 10 + "px";
  const view = { ra0: 90, dec0: 5, ppd: 3, topInset: 0 };   // start loosely on Taurus/Ori side
  let minPPD = 1;
  const filters = { proto: true, debris: true, planetonly: true, quasar: true, evolved: true,
    refutedonly: true, planethost: false, hasimg: false, constellations: true,
    facilities: new Set(), instruments: new Set(), bands: new Set(), missing: new Set(),
    content: new Set(), surveys: new Set() };
  let visible = new Set(SYS.map(s => s.id));
  let hoverId = null, currentSys = null, curImg = 0, currentView = "sky";

  /* ---- URL-hash deep links ----------------------------------------------
     #s=<id>&i=<n>&v=matrix|tonight&cat=<off,cats>&ph=1&img=1&b=<bands>
       &miss=<...>&fac=<facilities>&instr=<instruments>
     Old links (#s=hl-tau, #s=hl-tau&i=3) keep working. Filter state is applied
     HERE — before the chips are built below, so they render "on" — while the
     view/system/image parts are applied at the end of boot (they need
     setView/goTo/showImg). syncHash() writes the whole state back on every
     filter/view/detail change, so the URL is always shareable. */
  let hashSys = null, hashImg = 0;         // detail card currently in the hash
  const CAT_KEYS = ["proto", "debris", "planetonly", "refutedonly", "quasar", "evolved"];
  const bootHash = (function () {
    const out = { sys: null, img: 0, view: null };
    const h = location.hash.replace(/^#/, "");
    if (!h) return out;
    for (const part of h.split("&")) {
      const eq = part.indexOf("="); if (eq < 0) continue;
      const k = part.slice(0, eq), v = part.slice(eq + 1);
      const toks = v.split(",").map(decodeURIComponent).filter(Boolean);
      if (k === "s") out.sys = v;
      else if (k === "i" && /^\d+$/.test(v)) out.img = +v;
      else if (k === "v" && (v === "matrix" || v === "tonight")) out.view = v;
      else if (k === "cat") toks.forEach(c => { if (CAT_KEYS.indexOf(c) >= 0) filters[c] = false; });
      else if (k === "ph") filters.planethost = v === "1";
      else if (k === "b") toks.forEach(x => filters.bands.add(x));
      else if (k === "cont") toks.forEach(x => filters.content.add(x));
      else if (k === "miss") toks.forEach(x => filters.missing.add(x));
      else if (k === "fac") toks.forEach(x => filters.facilities.add(x));
      else if (k === "instr") toks.forEach(x => filters.instruments.add(x));
      else if (k === "surv") toks.forEach(x => filters.surveys.add(x));
    }
    hashSys = out.sys; hashImg = out.img ? out.img - 1 : 0;
    return out;
  })();
  function syncHash() {
    if (!history.replaceState) return;
    const parts = [];
    if (hashSys) {
      parts.push("s=" + hashSys);
      if (hashImg) parts.push("i=" + (hashImg + 1));   // 1-based; omitted for the first image
    }
    if (currentView !== "sky") parts.push("v=" + currentView);
    const off = CAT_KEYS.filter(k => !filters[k]);
    if (off.length) parts.push("cat=" + off.join(","));
    if (filters.planethost) parts.push("ph=1");
    const setPart = (key, set) => {
      if (set.size) parts.push(key + "=" + [...set].map(encodeURIComponent).join(","));
    };
    setPart("b", filters.bands); setPart("cont", filters.content);
    setPart("miss", filters.missing);
    setPart("fac", filters.facilities); setPart("instr", filters.instruments);
    setPart("surv", filters.surveys);
    history.replaceState(null, "", parts.length ? "#" + parts.join("&") : "#");
  }

  /* background stars (seeded, fixed on sky) */
  function mulberry(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const BG = (() => {
    const r = mulberry(20260706), out = [];
    for (let i = 0; i < 1600; i++) {
      const ra = r() * 360, dec = Math.asin(2 * r() - 1) * R2D;
      out.push({ ra, dec, m: r() });
    }
    return out;
  })();

  function resize() {
    DPR = window.devicePixelRatio || 1;
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    view.topInset = topbarH();
    minPPD = Math.max(W / 360, (H - view.topInset) / 180);   // full sky fits below the header; Dec spans -90..+90
    view.ppd = Math.max(view.ppd, minPPD);
    draw();
  }

  function clampView() {
    view.ppd = Math.min(Math.max(view.ppd, minPPD), 1200);
    const half = (H - (view.topInset || 0)) / 2 / view.ppd;   // half of the visible height, in degrees
    // keep the Dec axis within [-90, +90] (no scrolling past the poles)
    view.dec0 = half >= 90 ? 0 : Math.min(90 - half, Math.max(-90 + half, view.dec0));
    view.ra0 = wrapRA(view.ra0);
  }

  function drawCurve(pts, color, dash) {
    ctx.strokeStyle = color; ctx.lineWidth = 1;
    ctx.setLineDash(dash || []);
    ctx.beginPath();
    let prev = null;
    for (const p of pts) {
      const q = project(p.ra, p.dec, view, W, H);
      if (prev && Math.abs(q.x - prev.x) > W / 2) { ctx.moveTo(q.x, q.y); }
      else if (prev) ctx.lineTo(q.x, q.y);
      else ctx.moveTo(q.x, q.y);
      prev = q;
    }
    ctx.stroke(); ctx.setLineDash([]);
  }
  /* write a curve's name (galactic plane / ecliptic) along its own tangent, at
     the flattest on-screen stretch so the rotated label stays readable. */
  function labelCurve(pts, color, text) {
    if (!text) return;
    ctx.font = fpx(11) + " system-ui";
    const tw = ctx.measureText(text).width;
    let best = null, bestScore = Infinity;
    for (let i = 2; i < pts.length - 2; i++) {
      const q = project(pts[i].ra, pts[i].dec, view, W, H);
      /* stay clear of the header (top) and the legend + RA labels (bottom) */
      if (q.x < 64 || q.x > W - tw - 28 || q.y < topbarH() + 26 || q.y > H - 54) continue;
      let a = project(pts[i - 2].ra, pts[i - 2].dec, view, W, H);
      let b = project(pts[i + 2].ra, pts[i + 2].dec, view, W, H);
      if (Math.abs(b.x - a.x) > W / 2) continue;        // skip the RA-wrap seam
      if (a.x > b.x) { const s = a; a = b; b = s; }      // left→right so text isn't upside down
      const slope = Math.abs((b.y - a.y) / ((b.x - a.x) || 1));
      /* rotated text handles slope, so weight it lightly; prefer a spot a little
         left of centre and near the vertical middle (away from both edges) */
      const score = slope * 70 + Math.abs(q.x - W * 0.30) + Math.abs(q.y - H * 0.42) * 0.8;
      if (score < bestScore) { bestScore = score; best = { q, a, b }; }
    }
    if (!best) return;
    ctx.save();
    ctx.translate(best.q.x, best.q.y);
    ctx.rotate(Math.atan2(best.b.y - best.a.y, best.b.x - best.a.x));
    ctx.fillStyle = color;
    ctx.font = fpx(11) + " system-ui";
    ctx.textBaseline = "bottom";
    ctx.fillText(text, 5, -3);                            // sits just above the line
    ctx.restore();
  }

  const GAL = []; for (let l = 0; l <= 360; l += 2) GAL.push(galToEq(l, 0));
  const ECL = []; for (let l = 0; l <= 360; l += 2) ECL.push(eclToEq(l));

  function drawGrid() {
    ctx.strokeStyle = COL.grid; ctx.fillStyle = COL.dim;
    ctx.lineWidth = 1; ctx.font = fpx(11) + " system-ui";
    const stepOpts = [ [60,30],[30,15],[15,10],[10,5],[5,2],[2,1],[1,.5] ];
    let raStep = 60, decStep = 30;
    for (const [rs, ds] of stepOpts) { if (view.ppd * rs > 90) { raStep = rs; decStep = ds; } }
    for (let ra = 0; ra < 360; ra += raStep) {
      const a = project(ra, 0, view, W, H);
      if (a.x < -20 || a.x > W + 20) continue;
      ctx.beginPath(); ctx.moveTo(a.x, 0); ctx.lineTo(a.x, H); ctx.stroke();
      const hrs = ra / 15;
      const lab = (raStep >= 15 ? hrs.toFixed(0) + "h" : hrs.toFixed(1) + "h");
      ctx.fillStyle = COL.ink;
      ctx.fillText(lab, a.x + 3, H - 8);          // x-axis labels along the BOTTOM
      ctx.fillStyle = COL.gridlab2;
      ctx.fillText(lab, a.x + 3, topbarH() + 14); // faint duplicates under the header
      ctx.fillStyle = COL.dim;
    }
    for (let dec = -90; dec <= 90; dec += decStep) {
      const a = project(view.ra0, dec, view, W, H);
      if (a.y < topbarH() - 1 || a.y > H) continue;
      ctx.beginPath(); ctx.moveTo(0, a.y); ctx.lineTo(W, a.y); ctx.stroke();
      ctx.fillStyle = COL.ink;
      ctx.fillText((dec > 0 ? "+" : "") + dec + "°", 6, Math.max(a.y - 3, topbarH() + 12));
      ctx.fillStyle = COL.dim;
    }
  }

  function topbarH() {
    const tb = document.getElementById("topbar");
    return tb ? tb.getBoundingClientRect().height : 48;
  }

  const CONST = (typeof window !== "undefined" && window.CONSTELLATIONS) || null;
  function drawConstellations() {
    if (!CONST || !filters.constellations) return;
    ctx.strokeStyle = COL.constline;
    ctx.lineWidth = 1;
    for (const seg of CONST.lines) {
      ctx.beginPath();
      let prev = null;
      for (const pt of seg) {
        const p = project(pt[0], pt[1], view, W, H);
        if (prev && Math.abs(p.x - prev.x) > W / 2) ctx.moveTo(p.x, p.y);
        else if (prev) ctx.lineTo(p.x, p.y);
        else ctx.moveTo(p.x, p.y);
        prev = p;
      }
      ctx.stroke();
    }
    if (view.ppd > 2.2) {
      ctx.fillStyle = COL.constlab;
      ctx.font = "italic " + fpx(11) + " system-ui";
      const CN = (typeof window !== "undefined" && window.I18N_CONST && window.I18N_CONST[lang]) || null;
      for (const n of CONST.names) {
        const p = project(n.ra, n.dec, view, W, H);
        if (p.x < 0 || p.x > W || p.y < topbarH() || p.y > H) continue;
        ctx.fillText((CN && CN[n.name]) || n.name, p.x, p.y);
      }
      ctx.font = fpx(11) + " system-ui";
    }
  }

  /* draw a category-specific shape (path only; caller fills/strokes) */
  function drawShape(key, x, y, r) {
    ctx.beginPath();
    const sh = sysShape(key);
    if (sh === "square") { const a = r * 0.92; ctx.rect(x - a, y - a, 2 * a, 2 * a); }
    else if (sh === "diamond") { const a = r * 1.28; ctx.moveTo(x, y - a); ctx.lineTo(x + a, y); ctx.lineTo(x, y + a); ctx.lineTo(x - a, y); ctx.closePath(); }
    else if (sh === "triangle") { const a = r * 1.32; ctx.moveTo(x, y - a); ctx.lineTo(x + a * 0.87, y + a * 0.6); ctx.lineTo(x - a * 0.87, y + a * 0.6); ctx.closePath(); }
    else if (sh === "hexagon") { const a = r * 1.16; for (let i = 0; i < 6; i++) { const ang = -Math.PI / 2 + i * Math.PI / 3; const px = x + a * Math.cos(ang), py = y + a * Math.sin(ang); i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); } ctx.closePath(); }
    else { ctx.arc(x, y, r, 0, 7); }
  }
  /* 5-pointed star path (for imaged-planet hosts) */
  function starPath(x, y, R) {
    const inner = R * 0.44;
    ctx.beginPath();
    for (let i = 0; i < 10; i++) {
      const a = -Math.PI / 2 + i * Math.PI / 5;
      const rad = i % 2 === 0 ? R : inner;
      const px = x + Math.cos(a) * rad, py = y + Math.sin(a) * rad;
      i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    }
    ctx.closePath();
  }

  function draw() {
    clampView();
    ctx.fillStyle = COL.sky;
    ctx.fillRect(0, 0, W, H);
    drawConstellations();
    drawCurve(GAL, COL.gal);
    drawCurve(ECL, COL.ecl, [5, 5]);
    drawGrid();
    labelCurve(GAL, COL.gallab, t("map_galactic"));
    labelCurve(ECL, COL.ecllab, t("map_ecliptic"));

    const zs = Math.min(1.6, 0.9 + view.ppd / 60);
    for (const s of PLOT()) {
      const p = project(s.ra_deg, s.dec_deg, view, W, H);
      if (p.x < -12 || p.x > W + 12 || p.y < -12 || p.y > H + 12) continue;
      const nimg = (s.images || []).filter(i => i.file).length;
      const r = 5 * zs;   // uniform size per marker type (image count no longer scales the marker; it only sets fill opacity below)
      const key = sysColorKey(s);
      const col = COL[key];
      ctx.globalAlpha = nimg ? 0.95 : 0.55;
      drawShape(key, p.x, p.y, r);
      if (key === "planetonly" && sysRefutedOnly(s)) {
        /* hollow ◆: only a refuted companion claim (FW Tau, YSES-2) */
        ctx.strokeStyle = col; ctx.lineWidth = 1.6; ctx.stroke();
      } else { ctx.fillStyle = col; ctx.fill(); }
      ctx.globalAlpha = 1;
      if (sysHasImagedPlanet(s)) {
        starPath(p.x, p.y, r + 4.5);
        ctx.strokeStyle = COL.ink; ctx.lineWidth = 1.3; ctx.stroke();
      }
      if (s.id === hoverId || (currentSys && s.id === currentSys.id)) {
        ctx.beginPath(); ctx.arc(p.x, p.y, r + 7.5, 0, 7);
        ctx.strokeStyle = COL.hover; ctx.lineWidth = 1.5; ctx.stroke();
      }
      if (view.ppd > 26) {
        ctx.fillStyle = COL.namelab; ctx.font = fpx(11) + " system-ui";
        ctx.fillText(s.name, p.x + r + 4, p.y + 4);
      }
    }
    const st = A.stats || {};
    /* the "N local images" token is only informative when some records lack a
       local panel — since 2026-07 every record ships one, so skip the stutter */
    const localTok = st.with_local_image === st.image_records ? "" :
      " · " + (st.with_local_image || 0) + " " + t("word_local");
    document.getElementById("statsline").textContent =
      (st.systems || SYS.length) + " " + t("word_systems") + " · " + (st.image_records || "?") +
      " " + t("word_records") + localTok +
      " · " + t("word_updated") + " " + (A.generated || "?").slice(0, 10);
    /* literature-exploration progress bar (paper-finder ledgers, baked in at build time) */
    if (st.papers_known) {
      let wrap = document.getElementById("litbar");
      if (!wrap) {
        wrap = document.createElement("span"); wrap.id = "litbar";
        const pctE = Math.round(100 * st.papers_explored / st.papers_known);
        const pctI = Math.round(100 * st.papers_in_atlas / st.papers_known);
        /* collapsed behind an (i) icon: hover (or tap) reveals numbers + bar.
           Language-independent scaffolding only; text is set below so it
           re-localises when draw() re-runs after a language switch. */
        wrap.innerHTML = '<span class="liticon">ⓘ</span>' +
          '<span class="litdetail"><span class="litlabel"></span>' +
          '<span class="littrack"><span class="litseg exp" style="width:' + pctE +
          '%"></span><span class="litseg ing" style="width:' + pctI + '%"></span></span></span>';
        wrap.onclick = () => wrap.classList.toggle("open");
        document.getElementById("statsline").after(wrap);
      }
      wrap.title = t("lit_title").replace("{k}", st.papers_known)
        .replace("{e}", st.papers_explored).replace("{i}", st.papers_in_atlas);
      /* exploration is saturated (explored == known) in maintenance mode — the
         middle number is then redundant, so show "in atlas / known"; the full
         three-number form returns whenever a fresh-papers digest is pending */
      wrap.querySelector(".litlabel").textContent = t("lit_label") + " " +
        st.papers_in_atlas + "/" +
        (st.papers_explored === st.papers_known ? st.papers_known :
          st.papers_explored + "/" + st.papers_known);
    }
  }

  function hitTest(mx, my) {
    let best = null, bd = 14 * 14;
    for (const s of PLOT()) {
      const p = project(s.ra_deg, s.dec_deg, view, W, H);
      const d = (p.x - mx) * (p.x - mx) + (p.y - my) * (p.y - my);
      if (d < bd) { bd = d; best = s; }
    }
    return best;
  }

  /* ---------- interactions ---------- */
  let dragging = false, moved = false, lx = 0, ly = 0;
  canvas.addEventListener("mousedown", e => { stopMomentum(); dragging = true; moved = false; lx = e.clientX; ly = e.clientY; canvas.classList.add("dragging"); });
  window.addEventListener("mouseup", () => { dragging = false; canvas.classList.remove("dragging"); });
  window.addEventListener("mousemove", e => {
    if (dragging) {
      const dx = e.clientX - lx, dy = e.clientY - ly; lx = e.clientX; ly = e.clientY;
      if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      view.ra0 = wrapRA(view.ra0 + dx / view.ppd);
      view.dec0 += dy / view.ppd;
      draw();
      return;
    }
    if (e.target !== canvas) { tooltip.hidden = true; return; }
    const s = hitTest(e.clientX, e.clientY);
    hoverId = s ? s.id : null;
    if (s) {
      tooltip.hidden = false;
      tooltip.style.left = Math.min(e.clientX + 14, window.innerWidth - 270) + "px";
      tooltip.style.top = (e.clientY + 12) + "px";
      const nimg = (s.images || []).filter(i => i.file).length;
      const nImg = activePlanets(s).filter(p => planetMethod(p) !== "transit").length;
      const nTra = activePlanets(s).length - nImg;
      tooltip.innerHTML = '<div class="nm">' + esc(s.name) + '</div>' +
        '<div class="meta">' + (s.categories || []).map(catLabel).join(" + ") +
        (nImg ? " · " + t("tag_imaged") : "") +
        (nTra ? " · " + t("tag_transiting") : "") + "<br>" +
        (s.images || []).length + " " + t("word_records") + " · " + nimg + " " + t("word_local") +
        (s.region ? " · " + esc(s.region) : "") + "</div>";
    } else tooltip.hidden = true;
    draw();
  });
  canvas.addEventListener("click", e => {
    if (moved) return;                                 // a pan, not a click
    const s = hitTest(e.clientX, e.clientY);
    if (s) openDetail(s);                              // clicked a target → open it
    else if (!detail.hidden) closeDetail();            // clicked empty sky → dismiss the open card
  });
  canvas.addEventListener("dblclick", e => {
    const c = unproject(e.clientX, e.clientY, view, W, H);
    view.ra0 = c.ra; view.dec0 = c.dec; view.ppd *= 2; draw();
  });
  canvas.addEventListener("wheel", e => {
    e.preventDefault();
    const f = Math.exp(-e.deltaY * 0.0016);
    const before = unproject(e.clientX, e.clientY, view, W, H);
    view.ppd *= f; clampView();
    const after = unproject(e.clientX, e.clientY, view, W, H);
    view.ra0 = wrapRA(view.ra0 + (before.ra - after.ra));
    view.dec0 += before.dec - after.dec;
    draw();
  }, { passive: false });

  /* ---- touch (iPhone/iPad/Android): one-finger pan, two-finger pinch zoom
     anchored at the finger midpoint, double-tap = 2x zoom (parity with the
     desktop dblclick). Taps still synthesise clicks, so tap-to-open-details
     keeps working; touch-action:none on #sky stops Safari's native gestures. */
  let pinchD = 0, lastTap = 0, lastTapX = 0, lastTapY = 0;
  /* flick-to-glide momentum after a one-finger pan (deceleration, like map apps) */
  let momRAF = 0, momVx = 0, momVy = 0, momT = 0;
  function stopMomentum() { cancelAnimationFrame(momRAF); momRAF = 0; }
  function startMomentum() {
    if (Math.hypot(momVx, momVy) < 0.25) return;      // only on a real flick
    let last = performance.now();
    (function step(now) {
      const dt = Math.min(now - last, 40); last = now;
      view.ra0 = wrapRA(view.ra0 + momVx * dt / view.ppd);
      view.dec0 += momVy * dt / view.ppd;
      clampView(); draw();
      const decay = Math.pow(0.9, dt / 16);
      momVx *= decay; momVy *= decay;
      momRAF = Math.hypot(momVx, momVy) > 0.01 ? requestAnimationFrame(step) : 0;
    })(last);
  }
  canvas.addEventListener("touchstart", e => {
    stopMomentum();
    if (e.touches.length === 1) {
      dragging = true; moved = false;
      lx = e.touches[0].clientX; ly = e.touches[0].clientY;
      momVx = momVy = 0; momT = performance.now();
    } else if (e.touches.length === 2) {
      dragging = false; moved = true;            // pinch, not a tap
      const t0 = e.touches[0], t1 = e.touches[1];
      pinchD = Math.hypot(t1.clientX - t0.clientX, t1.clientY - t0.clientY);
    }
  }, { passive: true });
  canvas.addEventListener("touchmove", e => {
    e.preventDefault();                          // no page scroll/zoom while on the map
    if (e.touches.length === 1 && dragging) {
      const t = e.touches[0];
      const dx = t.clientX - lx, dy = t.clientY - ly; lx = t.clientX; ly = t.clientY;
      if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      const now = performance.now(), dt = now - momT; momT = now;
      if (dt > 0) { momVx = dx / dt; momVy = dy / dt; }   // px/ms, for momentum
      view.ra0 = wrapRA(view.ra0 + dx / view.ppd);
      view.dec0 += dy / view.ppd;
      clampView(); draw();
    } else if (e.touches.length === 2) {
      const t0 = e.touches[0], t1 = e.touches[1];
      const d = Math.hypot(t1.clientX - t0.clientX, t1.clientY - t0.clientY);
      const cx = (t0.clientX + t1.clientX) / 2, cy = (t0.clientY + t1.clientY) / 2;
      if (pinchD > 0 && d > 0) {
        const before = unproject(cx, cy, view, W, H);
        view.ppd *= d / pinchD; clampView();
        const after = unproject(cx, cy, view, W, H);
        view.ra0 = wrapRA(view.ra0 + (before.ra - after.ra));
        view.dec0 += before.dec - after.dec;
        draw();
      }
      pinchD = d; moved = true;
    }
  }, { passive: false });
  canvas.addEventListener("touchend", e => {
    if (e.touches.length === 1) {                // pinch -> one finger left: resume pan
      dragging = true;
      lx = e.touches[0].clientX; ly = e.touches[0].clientY;
      pinchD = 0;
      return;
    }
    if (e.touches.length === 0) {
      dragging = false; pinchD = 0;
      /* double-tap = zoom in 2x on the tapped point */
      if (!moved && e.changedTouches.length === 1) {
        const t = e.changedTouches[0], now = Date.now();
        if (now - lastTap < 300 && Math.abs(t.clientX - lastTapX) < 30 &&
            Math.abs(t.clientY - lastTapY) < 30) {
          e.preventDefault();                    // swallow the second synthetic click
          const c = unproject(t.clientX, t.clientY, view, W, H);
          view.ra0 = c.ra; view.dec0 = c.dec; view.ppd *= 2; clampView(); draw();
          lastTap = 0;
          return;
        }
        lastTap = now; lastTapX = t.clientX; lastTapY = t.clientY;
      } else if (moved && performance.now() - momT < 60) {
        startMomentum();                    // released a moving pan → glide (skip if the finger paused)
      }
    }
  }, { passive: false });

  window.addEventListener("keydown", e => {
    if (e.key === "Escape") { closeDetail(); listEl.hidden = true; }
    if (!detail.hidden) {
      if (e.key === "ArrowLeft") showImg(curImg - 1, -1);
      if (e.key === "ArrowRight") showImg(curImg + 1, 1);
    }
  });

  /* ---------- filters & search ---------- */
  const FDEF = [
    ["proto", "cat_proto", "proto"],
    ["debris", "cat_debris", "debris"],
    ["planetonly", "cat_planetonly", "planet"],
    ["refutedonly", "leg_refuted", "planet"],   // hollow-◆ population; shares the legend label
    ["quasar", "cat_quasar", "quasar"],
    ["evolved", "cat_evolved", "evolved"],
    ["planethost", "f_planethost", ""],
    /* "has local image" chip retired 2026-07-12: every record now carries a
       local crop (2292/2292), so the filter selected everything; the
       filterSystems() hasimg logic stays for API/test compatibility */
    ["constellations", "f_constellations", ""]
  ];
  const fbar = document.getElementById("filters");
  /* Every category chip carries its map symbol (the same .mk icons the legend
     and matrix use) so header row, legend, and sky markers cross-reference
     each other; ★ marks the hosts-imaged-companion FILTER, and the two
     easily-confused companion chips additionally explain themselves on hover.
     Glyphs + tooltips sit OUTSIDE the translated label (inner data-i18n
     span), so applyStaticI18n() can't wipe them on a language switch. */
  const CHIP_GLYPH = {
    proto: '<i class="mk proto"></i>', debris: '<i class="mk debris"></i>',
    planetonly: '<i class="mk planetonly"></i>', quasar: '<i class="mk quasar"></i>',
    evolved: '<i class="mk evolved"></i>', refutedonly: '<i class="mk planetonly hollow"></i>',
    planethost: '<span class="mk-star">★</span>'
  };
  for (const [key, i18nKey, cls] of FDEF) {
    const el = document.createElement("span");
    el.className = "chip " + cls + (filters[key] ? " on" : "");
    el.dataset.fkey = key;
    if (CHIP_GLYPH[key]) {
      el.innerHTML = CHIP_GLYPH[key] + '<span data-i18n="' + i18nKey + '"></span>';
      el.querySelector("[data-i18n]").textContent = t(i18nKey);
      if (key === "planetonly" || key === "planethost") {
        el.dataset.i18nTitle = key === "planetonly" ? "tip_planetonly" : "tip_planethost";
        el.title = t(el.dataset.i18nTitle);
      }
    } else { el.dataset.i18n = i18nKey; el.textContent = t(i18nKey); }
    el.onclick = () => { filters[key] = !filters[key]; el.classList.toggle("on"); refilter(); };
    fbar.appendChild(el);
  }
  /* "clear categories": turn every category chip off -> blank map (constellations
     stay). Parallels "clear facets"; the two together give a full blank slate. */
  const catClear = document.createElement("span");
  catClear.className = "chip reset";
  catClear.dataset.i18n = "cat_clear"; catClear.textContent = t("cat_clear");
  catClear.onclick = () => {
    CAT_KEYS.forEach(k => { filters[k] = false; });
    fbar.querySelectorAll("[data-fkey]").forEach(el => {
      if (CAT_KEYS.indexOf(el.dataset.fkey) >= 0) el.classList.remove("on");
    });
    refilter();
  };
  fbar.appendChild(catClear);
  function refilter() {
    visible = new Set(filterSystems(SYS, filters, "").map(s => s.id));
    syncHash();
    draw();
    if (currentView === "matrix") buildMatrix();
    if (currentView === "tonight") computeTonight();
  }
  refilter();

  searchEl.addEventListener("input", () => {
    const q = searchEl.value.trim();
    if (!q) { listEl.hidden = true; return; }
    const res = filterSystems(SYS, { proto: 1, debris: 1, planetonly: 1 }, q).slice(0, 30);
    listEl.innerHTML = res.length ? "" : '<div class="nores">no match</div>';
    const ql = q.toLowerCase();
    for (const s of res) {
      const row = document.createElement("div");
      row.className = "row";
      /* if the query matched a recorded paper (not the name), show that paper —
         this is how a user confirms "paper X is already in the atlas, here" */
      const nameHit = [s.name, s.id, ...(s.alt_names || [])].some(x => String(x).toLowerCase().includes(ql));
      const surv = nameHit ? null : matchedSurvey(s, ql);       // priority: name > survey > paper
      const pap = (nameHit || surv) ? null : matchedPaper(s, ql);
      const meta = surv
        ? "🔭 " + esc(surv)                                     // survey tag, verbatim (not translated)
        : pap
        ? "📄 " + esc((pap.first_author || "?") + " " + (pap.year || ""))
        : (s.categories || []).map(c => c[0]).join("+") +
          ((s.images || []).some(i => i.file) ? " 🖼" : "") +
          (sysHasPlanet(s) ? " ● pl" : "");
      row.innerHTML = "<b>" + esc(s.name) + "</b><span class='meta'>" + meta + "</span>";
      const prefer = surv ? { survey: surv } : pap ? { paper: pap } : null;   // open on the matched image
      row.onclick = () => { listEl.hidden = true; searchEl.value = s.name; goTo(s, prefer); };
      listEl.appendChild(row);
    }
    /* anchor right under the search box (front layer over the facet chips) with
       header-relative offsets: the list lives inside the fixed #topbar, so a
       phone keyboard or focus zoom shifting the visual viewport moves both
       together and can never park the list on top of the input */
    listEl.hidden = false;
    const hdrW = (searchEl.offsetParent || document.body).clientWidth;
    listEl.style.left = Math.max(8, Math.min(searchEl.offsetLeft, hdrW - listEl.offsetWidth - 8)) + "px";
    listEl.style.top = (searchEl.offsetTop + searchEl.offsetHeight + 4) + "px";
  });
  /* keyboard navigation of the search dropdown: Up/Down move the highlight
     (wrapping), Enter opens the highlighted result (or the first one) */
  searchEl.addEventListener("keydown", e => {
    if (listEl.hidden) return;
    const rows = Array.prototype.slice.call(listEl.querySelectorAll(".row"));
    if (!rows.length) return;
    const cur = rows.findIndex(r => r.classList.contains("active"));
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const dir = e.key === "ArrowDown" ? 1 : -1;
      const next = cur < 0 ? (dir === 1 ? 0 : rows.length - 1)
                           : (cur + dir + rows.length) % rows.length;
      rows.forEach(r => r.classList.remove("active"));
      rows[next].classList.add("active");
      rows[next].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter") {
      e.preventDefault();
      (cur >= 0 ? rows[cur] : rows[0]).click();
    }
  });
  document.addEventListener("click", e => {
    if (e.target !== searchEl && !listEl.contains(e.target)) listEl.hidden = true;
  });

  function goTo(s, prefer) {
    if (s.ra_deg != null) {
      view.ra0 = s.ra_deg; view.dec0 = s.dec_deg;
      view.ppd = Math.max(view.ppd, 40);
    }
    openDetail(s, prefer);   // prefer: {survey} | {paper} — open on the matching image
  }

  /* ---------- detail panel ---------- */
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  function sortedImages(s) {
    return (s.images || []).slice().sort((a, b) =>
      (a.wavelength_um || 0) - (b.wavelength_um || 0));
  }

  function openDetail(s, prefer) {
    currentSys = s; curImg = 0;
    document.getElementById("d_name").textContent = s.name;
    const bits = [];
    for (const c of (s.categories || []))
      bits.push('<span class="tag ' + (c === "protoplanetary" ? "proto" :
        c === "quasar" ? "quasar" : c === "evolved" ? "evolved" : "debris") + '">' + esc(catLabel(c)) + "</span>");
    const nImgP = activePlanets(s).filter(p => planetMethod(p) !== "transit").length;
    const nTraP = activePlanets(s).length - nImgP;
    if (nImgP) bits.push('<span class="tag pl">' + nImgP + " " + esc(t("tag_imaged")) + "</span>");
    if (nTraP) bits.push('<span class="tag pl">' + nTraP + " " + esc(t("tag_transiting")) + "</span>");
    const meta = [];
    if (s.sptype) meta.push(esc(s.sptype));
    if (s.redshift != null) meta.push("z = " + s.redshift);
    else if (s.dist_pc) meta.push(s.dist_pc + " pc" +
      (s.plx_mas ? " (π " + s.plx_mas.toFixed(2) + " mas)" : ""));
    if (s.region) meta.push(esc(s.region));
    if (s.ra_deg != null) meta.push("RA " + s.ra_deg.toFixed(4) + "°, Dec " + s.dec_deg.toFixed(4) + "°");
    if (s.alt_names && s.alt_names.length) meta.push("= " + s.alt_names.map(esc).join(", "));
    let magrow = "";
    if (s.mags) {
      const order = ["U","B","V","G","R","I","J","H","K"];
      const parts = order.filter(b => s.mags[b] != null)
        .map(b => b + " " + s.mags[b].toFixed(2));
      if (parts.length) magrow = "<br>mag: " + parts.join(" · ");
    }
    /* simbad === null (explicit) => object absent from SIMBAD: link a coordinate
       search instead so the click still lands somewhere useful. */
    const simUrl = (s.simbad === null && s.ra_deg != null)
      ? "https://simbad.cds.unistra.fr/simbad/sim-coo?Coord=" +
        encodeURIComponent(s.ra_deg.toFixed(5) + " " + s.dec_deg.toFixed(5)) +
        "&Radius=10&Radius.unit=arcsec"
      : "https://simbad.cds.unistra.fr/simbad/sim-basic?Ident=" +
        encodeURIComponent(s.simbad || s.name) + "&submit=SIMBAD+search";
    magrow += (magrow ? " · " : "<br>") +
      '<a class="simlink" href="' + simUrl + '" target="_blank" rel="noopener">SIMBAD ↗</a>' +
      ' <span class="src">' + esc(t("d_simbadsrc")) + '</span>';
    document.getElementById("d_sub").innerHTML =
      bits.join("") + "<br>" + meta.join(" · ") + magrow;
    const pl = document.getElementById("d_planets");
    function compName(sysName, plName) {
      // "HD 135344 A" + "Ab" -> "HD 135344 Ab"; "eps Ind A"+"Ab" likewise.
      const m = sysName.match(/^(.*)\s([A-D])$/);
      if (m && plName.charAt(0) === m[2]) return m[1] + " " + plName;
      return sysName + " " + plName;
    }
    const citeIdx = citeIndex(s);
    if (sysHasPlanet(s)) {
      pl.innerHTML = '<div class="ph">' + esc(t("d_companions")) + "</div>" + s.planets.map(p => {
        const pp = p.paper || null;
        const links = [];
        if (pp) {
          const au = arxivUrl(pp), ad = adsUrl(pp);
          if (au) links.push('<a href="' + au + '" target="_blank" rel="noopener">arXiv</a>');
          if (ad) links.push('<a href="' + ad + '" target="_blank" rel="noopener">SciX</a>');
        }
        return '<div class="pl"><b>' + esc(compName(s.name, p.name)) + "</b>" +
          '<span class="st ' + esc(p.status || "confirmed") + '">' + esc(p.status || "confirmed") + "</span>" +
          '<span class="st">' + esc(planetMethod(p)) + "</span>" +
          (pp ? ' <span class="pref">' + esc((pp.first_author || "") +
            (pp.year ? " et al. " + pp.year : "")) + " " + links.join(" ") + "</span>" : "") +
          (p.extra_papers || []).map(ep => {
            const l = [];
            const eau = arxivUrl(ep), ead = adsUrl(ep);
            if (eau) l.push('<a href="' + eau + '" target="_blank" rel="noopener">arXiv</a>');
            if (ead) l.push('<a href="' + ead + '" target="_blank" rel="noopener">SciX</a>');
            return ' <span class="pref">' + esc((ep.label ? ep.label + ": " : "") +
              (ep.first_author || "") + (ep.year ? " et al. " + ep.year : "")) +
              " " + l.join(" ") + "</span>";
          }).join("") +
          (p.note ? "<br>" + linkifyCitations(esc(p.note), citeIdx) : "") + "</div>";
      }).join("");
    } else pl.innerHTML = "";
    document.getElementById("d_notes").innerHTML = linkifyCitations(esc(s.notes || ""), citeIdx) +
      (s.last_updated ? '<div class="lastupd">' + esc(t("d_updated")) + " " +
        esc(s.last_updated) + "</div>" : "");
    buildSlider(s);
    /* with instrument/facility facets active, open on the first image from the
       selection instead of the sequence start; instrument (more specific) wins.
       Matching mirrors the filter rules: instrument parent⊇children (SPHERE
       finds SPHERE/IRDIS…), facility VLT also counts VLTI records. */
    let first = 0;
    const ims = sortedImages(s);
    /* a survey/author SEARCH hit, or an active survey facet, opens on the
       matching image (highest priority); else instrument > facility facet. */
    const prefSurvey = (prefer && prefer.survey) ||
      (filters.surveys && [...filters.surveys].find(v => (s.images || []).some(im => im.survey === v)));
    let idx = -1;
    if (prefer && prefer.paper) {
      const key = paperTokens(prefer.paper);
      idx = ims.findIndex(im => im.paper && paperTokens(im.paper) === key);
    } else if (prefSurvey) {
      idx = ims.findIndex(im => im.survey === prefSurvey);
    }
    if (idx >= 0) first = idx;
    else if (filters.instruments && filters.instruments.size) {
      const sel = [...filters.instruments];
      const j = ims.findIndex(im => im.instr_key &&
        sel.some(x => im.instr_key === x || (!x.includes("/") && im.instr_key.startsWith(x + "/"))));
      if (j >= 0) first = j;
    } else if (filters.facilities && filters.facilities.size) {
      const sel = [...filters.facilities];
      const j = ims.findIndex(im => sel.some(x => (im.fac_keys || []).indexOf(x) >= 0 ||
        (x === "VLT" && (im.fac_keys || []).indexOf("VLTI") >= 0)));
      if (j >= 0) first = j;
    }
    showImg(first);
    detail.style.transition = ""; detail.style.transform = "";   // clear any leftover dismiss drag
    detail.hidden = false;
    if (detail._placeResize) detail._placeResize();   // position the resize handle
    draw();
  }
  function closeDetail() {
    detail.hidden = true; currentSys = null;
    hashSys = null; hashImg = 0; syncHash();
    draw();
  }
  document.getElementById("closebtn").onclick = closeDetail;
  document.getElementById("d_prev").onclick = () => showImg(curImg - 1, -1);
  document.getElementById("d_next").onclick = () => showImg(curImg + 1, 1);
  /* touch gestures on the detail image:
       · pinch (2 fingers) / double-tap → zoom (1×–5×), drag → pan when zoomed
       · swipe left/right (when not zoomed) → previous/next image
     #d_imgbox touch-action toggles pan-y (not zoomed: browser scrolls vertically,
     we own the h-swipe) → none (zoomed: we own both axes). Reset on image change. */
  let resetImgZoom = null;
  (function imgGestures() {
    const box = document.getElementById("d_imgbox");
    if (!box) return;
    let scale = 1, tx = 0, ty = 0, mode = null, sx = 0, sy = 0, lx = 0, ly = 0, pd0 = 0, s0 = 1, swiping = false, track = null, swVx = 0, swT = 0, swLastX = 0;
    const img = () => box.querySelector("img");
    const W = () => box.clientWidth || 380;
    function apply() {
      const im = img();
      if (im) im.style.transform = "translate(" + tx.toFixed(1) + "px," + ty.toFixed(1) + "px) scale(" + scale.toFixed(3) + ")";
      box.style.touchAction = scale > 1 ? "none" : "pan-y";
    }
    function clampPan() {
      const im = img(); if (!im) return;
      const ex = Math.max(0, (im.clientWidth * scale - box.clientWidth) / 2);
      const ey = Math.max(0, (im.clientHeight * scale - box.clientHeight) / 2);
      tx = Math.max(-ex, Math.min(ex, tx)); ty = Math.max(-ey, Math.min(ey, ty));
    }
    /* build a 3-slide carousel [prev · current · next] so the neighbour you swipe
       toward is already on screen (no blank gap); the track is torn back down to a
       single <img> by showImg() once the swipe settles. */
    function buildTrack() {
      const ims = currentSys ? sortedImages(currentSys) : [];
      if (ims.length < 2) return null;
      const n = ims.length, at = o => ims[(curImg + o + n) % n];
      const slide = im => {
        const s = document.createElement("div"); s.className = "d_slide";
        if (im.file) { const g = new Image(); g.alt = ""; g.decoding = "async"; g.src = im.file; s.appendChild(g); }
        else s.innerHTML = '<div class="placeholder"><span class="big">⏳</span>' + esc(t("d_pending1")) + "</div>";
        return s;
      };
      /* the current slide MOVES the live <img> instead of rebuilding it: the finger
         went down on that node, and destroying the touch target mid-gesture makes
         iOS/Android stop delivering the rest of the touchmove/touchend stream */
      const cur = document.createElement("div"); cur.className = "d_slide";
      while (box.firstChild) cur.appendChild(box.firstChild);
      const tr = document.createElement("div"); tr.className = "d_track";
      tr.appendChild(slide(at(-1))); tr.appendChild(cur); tr.appendChild(slide(at(1)));
      box.appendChild(tr);
      tr.style.transform = "translateX(" + (-W()) + "px)";   // centre the current slide
      return tr;
    }
    function slideTrack(tr, x, done) {      // animate the track then hand off to showImg
      tr.style.transition = "transform .2s ease";
      tr.style.transform = "translateX(" + x + "px)";
      let ran = false;
      const fin = () => { if (ran) return; ran = true; if (done) done(); };
      tr.addEventListener("transitionend", fin, { once: true });
      setTimeout(fin, 260);                 // fallback if transitionend doesn't fire
    }
    resetImgZoom = () => { scale = 1; tx = 0; ty = 0; swiping = false; track = null; apply(); };
    box.addEventListener("touchstart", e => {
      const im0 = img(); if (im0) im0.style.transition = "";   // cancel any in-flight slide
      if (e.touches.length === 1) {
        const t = e.touches[0]; sx = lx = swLastX = t.clientX; sy = ly = t.clientY; swiping = false;
        swVx = 0; swT = performance.now();
        mode = scale > 1 ? "pan" : "swipe";
      } else if (e.touches.length === 2) {
        mode = "pinch";
        const a = e.touches[0], b = e.touches[1];
        pd0 = Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY); s0 = scale;
      }
    }, { passive: true });
    box.addEventListener("touchmove", e => {
      if (mode === "pinch" && e.touches.length === 2) {
        e.preventDefault();
        const a = e.touches[0], b = e.touches[1];
        const d = Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY);
        if (pd0 > 0) scale = Math.max(1, Math.min(5, s0 * d / pd0));
        if (scale === 1) { tx = 0; ty = 0; }
        clampPan(); apply();
      } else if (mode === "pan" && e.touches.length === 1) {
        e.preventDefault();
        const t = e.touches[0];
        tx += t.clientX - lx; ty += t.clientY - ly; lx = t.clientX; ly = t.clientY;
        clampPan(); apply();
      } else if (mode === "swipe" && e.touches.length === 1) {
        const t = e.touches[0], dx = t.clientX - sx, dy = t.clientY - sy;
        if (!swiping && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) {
          swiping = true; track = buildTrack();          // bring the neighbours on screen
        }
        if (swiping && track) {                            // the carousel tracks the finger
          e.preventDefault();
          track.style.transition = "";
          track.style.transform = "translateX(" + (-W() + dx) + "px)";
          const now = performance.now(), dt = now - swT;    // running velocity for flick detection
          if (dt > 0) swVx = (t.clientX - swLastX) / dt;
          swLastX = t.clientX; swT = now;
        }
      }
    }, { passive: false });
    box.addEventListener("touchend", e => {
      if (e.touches.length >= 1) {                        // a finger is still down
        if (e.touches.length === 1) {                     // pinch → pan/swipe with the remaining finger
          const t = e.touches[0]; sx = lx = t.clientX; sy = ly = t.clientY;
          mode = scale > 1 ? "pan" : "swipe";
        }
        return;
      }
      const t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (mode === "swipe" && swiping && track) {           // resolve the carousel swipe
        const tr = track; track = null;
        const flick = Math.abs(swVx) > 0.35 && performance.now() - swT < 120;   // a recent quick flick (px/ms) commits even if short; a paused finger doesn't
        const commit = Math.abs(dx) > W() * 0.22 || (flick && Math.abs(dx) > 12);
        if (commit) {                                       // commit to the neighbour
          const dir = dx < 0 ? 1 : -1;                      // direction from total travel: left = next, right = prev
          slideTrack(tr, dir > 0 ? -2 * W() : 0, () => showImg(curImg + dir));   // settle, then swap to single img
        } else {
          slideTrack(tr, -W(), () => showImg(curImg));      // snap back to the current
        }
        swiping = false; mode = null; return;
      }
      /* no double-tap zoom on the image: rapid ‹/› taps to flip through images
         must never trigger a zoom (pinch is the only zoom gesture) */
      swiping = false; mode = null;
    }, { passive: true });
    box.addEventListener("touchcancel", () => {           // browser stole the gesture → settle back
      if (track) { const tr = track; track = null; slideTrack(tr, -W(), () => showImg(curImg)); }
      swiping = false; mode = null;
    }, { passive: true });
  })();
  /* drag the card DOWN to dismiss it (iPhone-app style): it follows the finger,
     then either flings off the bottom and closes, or springs back. Armed only when
     scrolled to the top (else a down-drag just scrolls) and not on a zoomed image. */
  (function panelDismiss() {
    const detail = document.getElementById("detail");
    if (!detail) return;
    let y0 = 0, x0 = 0, armed = false, engaged = false;
    detail.addEventListener("touchstart", e => {
      engaged = false;
      if (e.touches.length !== 1) { armed = false; return; }
      const t = e.touches[0]; y0 = t.clientY; x0 = t.clientX;
      const box = document.getElementById("d_imgbox");
      const onZoomedImg = box && box.contains(e.target) && getComputedStyle(box).touchAction === "none";
      armed = detail.scrollTop <= 0 && !onZoomedImg;
      detail.style.transition = "";
    }, { passive: true });
    detail.addEventListener("touchmove", e => {
      if (!armed || e.touches.length !== 1) return;
      const t = e.touches[0], dy = t.clientY - y0, dx = t.clientX - x0;
      if (!engaged) {
        if (dy > 6 && dy > Math.abs(dx)) engaged = true;                 // downward + vertical → drag the card
        else if (Math.abs(dx) > 8 || dy < -4) { armed = false; return; } // horizontal / upward → not a dismiss
      }
      if (engaged) {
        e.preventDefault();
        detail.style.transform = "translateY(" + Math.max(0, dy) + "px)";  // resist upward past 0
      }
    }, { passive: false });
    function settle(close) {
      detail.style.transition = "transform .25s cubic-bezier(.4,0,.2,1)";
      if (close) {
        detail.style.transform = "translateY(100%)";                    // fling off the bottom, then close
        let ran = false;
        const fin = () => { if (ran) return; ran = true; closeDetail(); detail.style.transition = ""; detail.style.transform = ""; };
        detail.addEventListener("transitionend", fin, { once: true });
        setTimeout(fin, 300);
      } else {
        detail.style.transform = "translateY(0)";                       // spring back into place
        setTimeout(() => { detail.style.transition = ""; detail.style.transform = ""; }, 280);
      }
    }
    detail.addEventListener("touchend", e => {
      if (!armed || !engaged) { armed = false; engaged = false; return; }
      armed = false; engaged = false;
      const dy = e.changedTouches[0].clientY - y0;
      settle(dy > 110);   // past threshold → dismiss, else spring back
    }, { passive: true });
  })();

  function shortFac(f) { return (f || "?").replace("VLT-", "").replace("Gemini-", "").replace("Subaru-", ""); }

  /* The OBSERVATION epoch (im.epoch) is the meaningful disambiguator. It is only
     shown as a bare year. The publication year is NOT an observation epoch, so when
     the obs epoch is not (yet) recorded we show the pub year in parentheses to make
     the distinction explicit — "2015" = observed 2015, "(2018)" = published 2018. */
  function imgYearTag(im) {
    if (im.epoch) { const m = String(im.epoch).match(/(19|20)\d\d/); if (m) return { y: m[0], obs: true }; }
    const py = im.paper && im.paper.year ? String(im.paper.year) : "";
    return py ? { y: py, obs: false } : null;
  }
  function buildSlider(s) {
    const sl = document.getElementById("d_slider");
    sl.innerHTML = "";
    sortedImages(s).forEach((im, i) => {
      const t = document.createElement("span");
      t.className = "tick";
      const yt = imgYearTag(im);
      t.innerHTML = '<span class="wl">' + fmtWl(im.wavelength_um) + "</span> "
        + esc((im.instr_key && im.instr_key !== "other") ? im.instr_key : shortFac(im.facility))
        + (yt ? ' <span class="yr' + (yt.obs ? "" : " pub") + '">' + (yt.obs ? esc(yt.y) : "(" + esc(yt.y) + ")") + "</span>" : "");
      t.title = yt ? (yt.obs ? (/^\d{4}-\d{4}$/.test(String(im.epoch))
                                  ? "observations span " + im.epoch + " (combined data)"
                                  : "observation epoch " + im.epoch)
                             : "published " + yt.y + " (observation epoch not recorded)") : "";
      t.onclick = () => showImg(i);
      sl.appendChild(t);
    });
  }

  function showImg(i, dir) {
    const s = currentSys; if (!s) return;
    const ims = sortedImages(s);
    if (!ims.length) {
      document.getElementById("d_imgbox").innerHTML =
        '<div class="placeholder"><span class="big">✴</span>' + esc(t("d_noimg")) + "</div>";
      document.getElementById("d_caption").innerHTML = "";
      document.getElementById("d_prev").disabled = document.getElementById("d_next").disabled = true;
      hashSys = s.id; hashImg = 0; syncHash();
      return;
    }
    curImg = (i + ims.length) % ims.length;
    /* deep link: #s=<id>&i=<n> — share/restore the exact image (n omitted for the first) */
    hashSys = s.id; hashImg = curImg; syncHash();
    const im = ims[curImg];
    const box = document.getElementById("d_imgbox");
    const prevImg = dir ? box.querySelector("img") : null;   // outgoing image, grabbed before the swap
    if (im.file) {
      box.innerHTML = '<img alt="' +
        esc(s.name + " — " + (im.wavelength_label || fmtWl(im.wavelength_um))) +
        '" decoding="async" src="' + esc(im.file) + '">';
      /* a 404 (stale cached data.js after an id rename, offline copy missing a file)
         must not leave a broken-image icon — swap in a translated notice */
      box.querySelector("img").onerror = () => {
        box.innerHTML = '<div class="placeholder"><span class="big">⚠</span>' +
          esc(t("d_imgerr")) + "</div>";
      };
    } else {
      box.innerHTML = '<div class="placeholder"><span class="big">⏳</span>' +
        esc(t("d_pending1")) + "<br>" + esc(t("d_pending2")) + "</div>";
    }
    if (resetImgZoom) resetImgZoom();   // clear any pinch-zoom from the previous image
    if (dir) {                          // carousel slide: incoming and outgoing images move together
      const w = box.clientWidth || 380;
      const enter = box.querySelector("img");
      if (enter) {                      // incoming image slides in from the entering side
        enter.style.transition = "none";
        enter.style.transform = "translate(" + (dir > 0 ? w : -w) + "px,0)";
        void enter.offsetWidth;         // reflow to lock the start position
        enter.style.transition = "transform .2s ease";
        enter.style.transform = "translate(0px,0)";
        setTimeout(() => { enter.style.transition = ""; }, 240);
      }
      if (prevImg) {                    // outgoing image slides out the opposite side, then is dropped
        prevImg.style.transition = "none";
        prevImg.style.transform = "";
        const ov = document.createElement("div"); ov.className = "d_slideout";
        ov.appendChild(prevImg);
        box.appendChild(ov);
        void ov.offsetWidth;
        ov.style.transition = "transform .2s ease";
        ov.style.transform = "translateX(" + (dir > 0 ? -w : w) + "px)";
        const drop = () => ov.remove();
        ov.addEventListener("transitionend", drop, { once: true });
        setTimeout(drop, 260);
      }
    }
    document.querySelectorAll("#d_slider .tick").forEach((el, k) =>
      el.classList.toggle("on", k === curImg));
    if (ims.length > 1) [-1, 1].forEach(o => {   // warm the neighbours so a swipe shows them instantly
      const nb = ims[(curImg + o + ims.length) % ims.length];
      if (nb && nb.file) { const pre = new Image(); pre.src = nb.file; }
    });
    const p = im.paper || {};
    const links = [];
    const au = arxivUrl(p), ad = adsUrl(p);
    if (au) links.push('<a href="' + au + '" target="_blank" rel="noopener">arXiv</a>');
    if (ad) links.push('<a href="' + ad + '" target="_blank" rel="noopener">SciX</a>');
    if (im.hires_url) links.push('<a href="' + esc(im.hires_url) + '" target="_blank" rel="noopener">' + esc(t("d_hires")) + ' ↗</a>');
    else if (au) links.push('<a href="' + au.replace("/abs/", "/pdf/") + '" target="_blank" rel="noopener">' + esc(t("d_hirespdf")) + '</a>');
    document.getElementById("d_caption").innerHTML =
      '<div class="row1">' + esc(im.facility || "?") + " · " + esc(im.instrument || "") +
      " · " + esc(im.wavelength_label || fmtWl(im.wavelength_um)) + "</div>" +
      '<div class="row2">' + esc(im.technique || "") +
      (im.survey ? " · survey: " + esc(im.survey) : "") +
      (im.credit ? " · " + esc(im.credit) : "") +
      " · " + esc(t("d_image")) + " " + (curImg + 1) + "/" + ims.length + "</div>" +
      '<div class="cite">' + esc(citeStr(p)) +
      (p.title ? '<br><span class="ttl">' + esc(p.title) + "</span>" : "") +
      '<br><span class="links">' + (links.join(" ") || esc(t("d_nolinks"))) + "</span></div>" +
      (!im.file ? '<div class="pending">' + esc(t("d_pendingnote")) + "</div>" : "");
    document.getElementById("d_prev").disabled = ims.length < 2;
    document.getElementById("d_next").disabled = ims.length < 2;
  }

  /* ---------- facets ---------- */
  const facetsBar = document.getElementById("facets");
  const ALL_FAC = [...new Set(SYS.flatMap(s => (s.images || []).flatMap(i => i.fac_keys || [])))]
    .filter(Boolean).sort((a, b) => a.localeCompare(b));
  /* facility <-> instrument relation, derived ONLY from single-facility records:
     joint A+B composites (e.g. a SPHERE+ALMA side-by-side figure) would otherwise
     wrongly pair an instrument with every facility in the composite. */
  const FAC2INSTR = {}, INSTR2FAC = {}, instrSet = new Set();
  SYS.forEach(s => (s.images || []).forEach(i => {
    if (!i.instr_key) return;
    instrSet.add(i.instr_key);
    if ((i.fac_keys || []).length !== 1) return;
    const k = i.fac_keys[0];
    (FAC2INSTR[k] = FAC2INSTR[k] || new Set()).add(i.instr_key);
    (INSTR2FAC[i.instr_key] = INSTR2FAC[i.instr_key] || new Set()).add(k);
  }));
  const ALL_INSTR = [...instrSet].sort((a, b) => a.localeCompare(b));
  /* curated major programs for the SURVEY facet — recognizable named surveys
     with a single clean tag; the fragmented/internal tags (SPHERE-Ks-RDI,
     STIS-Ren, the split Taurus-Long*) stay search-only. Only those actually
     present in the data get a chip; alphabetical (case-insensitive). */
  const MAJOR_SURVEYS = ["AGE-PRO", "ALICE", "ARKS", "DARTTS-S", "DESTINYS-Orion",
    "DSHARP", "eDisk", "exoALMA", "Gemini-LIGHTS", "GPIES-debris", "MAPS",
    "ODISEA", "REASONS", "SEEDS", "SONS", "SPHERE-debris-2025"];
  const presentSurveys = new Set(SYS.flatMap(s => (s.images || []).map(i => i.survey).filter(Boolean)));
  const ALL_SURVEYS = MAJOR_SURVEYS.filter(v => presentSurveys.has(v))
    .sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
  function chipGroup(parent, titleKey, entries, set, exclusive) {
    const wrap = document.createElement("div"); wrap.className = "fgroup";
    const lbl = document.createElement("span"); lbl.className = "flabel";
    lbl.dataset.i18n = titleKey; lbl.textContent = t(titleKey); wrap.appendChild(lbl);
    for (const [val, key, literal] of entries) {
      const c = document.createElement("span");
      c.className = "chip sm" + (set.has(val) ? " on" : "");
      c.dataset.val = val; c.dataset.group = titleKey;
      if (key) { c.dataset.i18n = key; c.textContent = t(key); } else c.textContent = literal;
      c.onclick = (e) => {
        if (exclusive && !(e.shiftKey || e.ctrlKey || e.metaKey)) {
          /* plain click: a new facility/instrument selection replaces the previous one */
          const wasOn = set.has(val);
          filters.facilities.clear(); filters.instruments.clear();
          facetsBar.querySelectorAll('.chip[data-group="facet_facility"].on, .chip[data-group="facet_instrument"].on')
            .forEach(x => x.classList.remove("on"));
          if (!wasOn) { set.add(val); c.classList.add("on"); }
        } else {
          /* shift/ctrl-click on facility/instrument: COMBINE — the system must have
             ALL of the selected facilities/instruments (e.g. VLT AND ALMA) */
          set.has(val) ? set.delete(val) : set.add(val); c.classList.toggle("on");
        }
        refilter(); updateRelHighlights();
      };
      wrap.appendChild(c);
    }
    parent.appendChild(wrap);
  }
  /* When facilities are selected, brighten the instruments they host (and vice
     versa) so users can see which instrument lives on which telescope. */
  function updateRelHighlights() {
    const relInstr = new Set(), relFac = new Set();
    for (const f of filters.facilities) {
      (FAC2INSTR[f] || []).forEach(i => relInstr.add(i));
      if (f === "VLT") (FAC2INSTR["VLTI"] || []).forEach(i => relInstr.add(i));
    }
    for (const i of filters.instruments) {
      (INSTR2FAC[i] || []).forEach(f => relFac.add(f));
      /* a selected PARENT instrument (e.g. "SPHERE") also lights up its own
         sub-instruments (SPHERE/IRDIS, .../ZIMPOL, .../IFS) in the instrument
         row, and relates to their facilities (VLT) too */
      if (!i.includes("/")) ALL_INSTR.forEach(k => {
        if (k.startsWith(i + "/")) { relInstr.add(k); (INSTR2FAC[k] || []).forEach(f => relFac.add(f)); }
      });
    }
    facetsBar.querySelectorAll('.chip[data-group="facet_instrument"]').forEach(c =>
      c.classList.toggle("rel", relInstr.has(c.dataset.val) && !c.classList.contains("on")));
    facetsBar.querySelectorAll('.chip[data-group="facet_facility"]').forEach(c =>
      c.classList.toggle("rel", relFac.has(c.dataset.val) && !c.classList.contains("on")));
  }
  if (facetsBar) {
    const bandEntries = WL_BANDS.map(b => [b.key, "band_" + b.key, b.label]).concat([["planet", "band_planet", "planet"]]);
    chipGroup(facetsBar, "facet_band", bandEntries, filters.bands);
    chipGroup(facetsBar, "facet_content", [["continuum", "content_cont", "continuum"], ["line", "content_line", "line"]], filters.content);
    chipGroup(facetsBar, "facet_missing", [["mm", "miss_mm", "mm"], ["nir", "miss_nir", "scat-light"], ["planet", "miss_planet", "imaged planet"]], filters.missing);
    chipGroup(facetsBar, "facet_facility", ALL_FAC.map(f => [f, null, f]), filters.facilities, true);
    chipGroup(facetsBar, "facet_instrument", ALL_INSTR.map(f => [f, null, f]), filters.instruments, true);
    /* SURVEY: verbatim tags (scientific data, never translated), additive union */
    if (ALL_SURVEYS.length) chipGroup(facetsBar, "facet_survey", ALL_SURVEYS.map(v => [v, null, v]), filters.surveys);
    const hint = document.createElement("span"); hint.className = "flabel fhint";
    hint.dataset.i18n = "facet_hint"; hint.textContent = t("facet_hint");
    facetsBar.appendChild(hint);
    const reset = document.createElement("span"); reset.className = "chip sm reset";
    reset.dataset.i18n = "facet_clear"; reset.textContent = t("facet_clear");
    reset.onclick = () => {
      filters.bands.clear(); filters.content.clear(); filters.missing.clear();
      filters.facilities.clear(); filters.instruments.clear(); filters.surveys.clear();
      facetsBar.querySelectorAll(".chip.on").forEach(c => c.classList.remove("on"));
      facetsBar.querySelectorAll(".chip.rel").forEach(c => c.classList.remove("rel")); refilter();
    };
    facetsBar.appendChild(reset);
  }

  /* ---------- view switcher ---------- */
  const matrixEl = document.getElementById("matrix");
  const tonightEl = document.getElementById("tonight");
  const tabsEl = document.getElementById("viewtabs");
  const legendEl = document.getElementById("legend");
  const VIEWS = [["sky", "🌌", "tab_sky"], ["matrix", "▦", "tab_matrix"], ["tonight", "🔭", "tab_tonight"]];
  if (tabsEl) for (const [v, ico, key] of VIEWS) {
    const tb = document.createElement("button");
    tb.className = "vtab" + (v === "sky" ? " on" : ""); tb.dataset.v = v;
    tb.innerHTML = '<span class="ico">' + ico + '</span> <span data-i18n="' + key + '"></span>' +
      /* disclosure chevron on Sky: signals that clicking it folds the filter rows */
      (v === "sky" ? ' <span class="foldchev" aria-hidden="true">▾</span>' : '');
    if (v === "sky") tb.dataset.i18nTitle = "fold_filters";
    tb.onclick = () => setView(v); tabsEl.appendChild(tb);
  }
  /* language selector */
  const langSel = document.getElementById("lang");
  if (langSel) {
    for (const [code, label] of (window.I18N_LANGS || [["en", "English"]])) {
      const o = document.createElement("option"); o.value = code; o.textContent = label;
      if (code === lang) o.selected = true; langSel.appendChild(o);
    }
    langSel.onchange = () => setLang(langSel.value);
  }
  /* logo = "back to start": reload to the clean URL. localStorage keeps
     language / theme / panel width; the transient view (open card, filters,
     facets, sky pan/zoom, search, matrix/tonight) resets to the default
     frontpage on boot — so users don't have to undo what they were viewing. */
  const logoEl = document.getElementById("logo");
  if (logoEl) {
    const goHome = () => {
      history.replaceState(null, "", location.pathname + location.search);   // drop the hash
      location.reload();
    };
    logoEl.onclick = goHome;
    logoEl.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); goHome(); } };
  }
  /* legend (built here so it carries symbols + translatable labels) */
  const legendKeys = [["proto", "cat_proto"], ["debris", "cat_debris"], ["evolved", "cat_evolved"], ["planetonly", "leg_planetonly"], ["quasar", "leg_quasar"]];
  if (legendEl) {
    let lh = "";
    for (const [k, key] of legendKeys)
      lh += '<span><i class="mk ' + k + '"></i><span data-i18n="' + key + '"></span></span>';
    lh += '<span><i class="mk planetonly hollow"></i><span data-i18n="leg_refuted"></span></span>';
    lh += '<span><span class="mk-star">★</span><span data-i18n="leg_imaged"></span></span>';
    /* touch devices have no wheel/hover — show the pinch/tap hint instead */
    const touch = typeof window !== "undefined" && window.matchMedia &&
      window.matchMedia("(hover: none), (pointer: coarse)").matches;
    lh += '<span class="hint" data-i18n="' + (touch ? "leg_hint_touch" : "leg_hint") + '"></span>';
    legendEl.innerHTML = lh;
  }
  /* phones start with the facet rows collapsed so the sky map isn't buried under
     dozens of facility/instrument chips (same 640px breakpoint as the CSS);
     tapping the Sky tab expands them as usual */
  let facetsCollapsed = !!(window.matchMedia && window.matchMedia("(max-width: 640px)").matches);
  /* BAND / MISSING / FACILITY / INSTRUMENT rows: Sky-tab only, and collapsible by
     clicking the Sky tab again (bigger map). Category chips stay everywhere. */
  function updateFacetVisibility() {
    const show = currentView === "sky" && !facetsCollapsed;
    /* hide the whole facets row (incl. its border-top separator), not just the
       chips inside, so no empty strip is left under the header */
    if (facetsBar) facetsBar.style.display = show ? "" : "none";
    ["facet_band", "facet_missing", "facet_facility", "facet_instrument"].forEach(k => {
      const lbl = facetsBar && facetsBar.querySelector('.flabel[data-i18n="' + k + '"]');
      if (lbl && lbl.closest(".fgroup")) lbl.closest(".fgroup").style.display = show ? "" : "none";
    });
    const hint = facetsBar && facetsBar.querySelector(".fhint");
    if (hint) hint.style.display = show ? "" : "none";
    const reset = facetsBar && facetsBar.querySelector(".chip.reset");
    if (reset) reset.style.display = show ? "" : "none";
    /* Sky-tab chevron: ▾ when the filters are open, ▸ when folded (hidden when
       not on the Sky view; visibility keeps the tab width stable) */
    const chev = tabsEl && tabsEl.querySelector('.vtab[data-v="sky"] .foldchev');
    if (chev) {
      chev.style.visibility = currentView === "sky" ? "visible" : "hidden";
      chev.textContent = facetsCollapsed ? "▸" : "▾";
    }
  }
  updateFacetVisibility();   /* apply the initial (mobile-collapsed) state at boot */
  function setView(v) {
    if (v === "sky" && currentView === "sky") facetsCollapsed = !facetsCollapsed;
    /* re-clicking the active Coverage/Tonight tab returns to the Sky view */
    if (v !== "sky" && v === currentView) v = "sky";
    currentView = v;
    syncHash();
    document.querySelectorAll(".vtab").forEach(t => t.classList.toggle("on", t.dataset.v === v));
    canvas.style.display = v === "sky" ? "" : "none";
    if (legendEl) legendEl.style.display = v === "sky" ? "" : "none";
    if (matrixEl) matrixEl.hidden = v !== "matrix";
    if (tonightEl) tonightEl.hidden = v !== "tonight";
    updateFacetVisibility();
    const el = v === "matrix" ? matrixEl : v === "tonight" ? tonightEl : null;
    if (el) el.style.paddingTop = (topbarH() + 10) + "px";
    if (v === "matrix") buildMatrix();
    else if (v === "tonight") buildTonight();
    else { resize(); draw(); }
  }
  window.addEventListener("resize", () => {
    if (currentView === "sky") return;
    const el = currentView === "matrix" ? matrixEl : tonightEl;
    if (el) el.style.paddingTop = (topbarH() + 10) + "px";
  });

  /* ---------- shared: category down-selection chips (matrix + tonight) ---------- */
  const CAT_DEFS = [["proto", "cat_proto"], ["debris", "cat_debris"], ["evolved", "cat_evolved"],
                    ["planetonly", "cat_planetonly"], ["quasar", "cat_quasar"]];
  function catChipsHTML() {
    return '<span class="catsel">' + CAT_DEFS.map(([k, ik]) =>
      '<span class="chip sm catchip' + (filters[k] ? " on" : "") + '" data-cat="' + k +
      '"><i class="mk ' + k + '"></i> ' + esc(t(ik)) + "</span>").join("") + "</span>" +
      /* content (continuum|line) down-select — the same facet the Sky view has */
      '<span class="catsel">' + [["continuum", "content_cont"], ["line", "content_line"]].map(([v, ik]) =>
      '<span class="chip sm contchip' + (filters.content.has(v) ? " on" : "") + '" data-content="' + v +
      '">' + esc(t(ik)) + "</span>").join("") + "</span>";
  }
  function wireCatChips(container) {
    container.querySelectorAll(".catchip").forEach(ch => ch.onclick = () => {
      /* drive the global header chip so all views + header stay in sync
         (the label key may sit on an inner span when the chip carries a
         map-symbol glyph — see the FDEF builder) */
      const hdr = [...document.querySelectorAll("#filters .chip")]
        .find(e => {
          const inner = e.querySelector("[data-i18n]");
          return (e.dataset.i18n || (inner && inner.dataset.i18n)) === "cat_" + ch.dataset.cat;
        });
      if (hdr) hdr.click();
      else { filters[ch.dataset.cat] = !filters[ch.dataset.cat]; refilter(); }
    });
    container.querySelectorAll(".contchip").forEach(ch => ch.onclick = () => {
      const v = ch.dataset.content;
      filters.content.has(v) ? filters.content.delete(v) : filters.content.add(v);
      /* keep the Sky-view facet chip in sync (it is built once at boot) */
      const fc = facetsBar && facetsBar.querySelector('.chip[data-group="facet_content"][data-val="' + v + '"]');
      if (fc) fc.classList.toggle("on", filters.content.has(v));
      refilter();
    });
  }
  function fmtDec(d) { return (d >= 0 ? "+" : "\u2212") + Math.abs(d).toFixed(1) + "\u00b0"; }

  /* ---------- coverage matrix ---------- */
  const MCOLS = [["opt", "col_optical", "<1μm"], ["nir", "col_nir", "1–5μm"], ["mir", "col_mir", "5–300μm"],
    ["mm", "col_mm", ">0.3mm"], ["planet", "col_planet", "imaged"]];
  let matrixSort = { key: "name", dir: 1 };
  function matrixRows() {
    const rows = filterSystems(SYS, filters, "").map(s => {
      const cells = {}; MCOLS.forEach(c => cells[c[0]] = { n: 0, local: 0 });
      /* non-exclusive: every record counts in its wavelength band, and a companion
         detection (type==="planet") ALSO counts in the planet column — a record can be
         both (e.g. TWA 7's MIR disk-ring image that also shows an imaged companion). */
      for (const im of (s.images || [])) {
        const band = wlBand(im.wavelength_um);
        if (cells[band]) { cells[band].n++; if (im.file) cells[band].local++; }
        if (im.type === "planet" && cells.planet) { cells.planet.n++; if (im.file) cells.planet.local++; }
      }
      return { s, cells };
    });
    const k = matrixSort.key, d = matrixSort.dir, txt = (k === "name" || k === "region" || k === "cat" || k === "ra" || k === "dec");
    rows.sort((a, b) => {
      let va, vb;
      if (k === "name") { va = a.s.name.toLowerCase(); vb = b.s.name.toLowerCase(); }
      else if (k === "cat") { va = sysColorKey(a.s); vb = sysColorKey(b.s); }
      else if (k === "ra") { va = a.s.ra_deg; vb = b.s.ra_deg; }
      else if (k === "dec") { va = a.s.dec_deg; vb = b.s.dec_deg; }
      else if (k === "region") { va = (a.s.region || "~~").toLowerCase(); vb = (b.s.region || "~~").toLowerCase(); }
      else { va = a.cells[k].n; vb = b.cells[k].n; }
      return va < vb ? -d : va > vb ? d : (txt ? 0 : a.s.name.localeCompare(b.s.name));
    });
    return rows;
  }
  function buildMatrix() {
    if (!matrixEl) return;
    const rows = matrixRows();
    let h = '<div class="mhint">' + t("mtx_hint").replace("{n}", rows.length) + catChipsHTML() + "</div>";
    h += '<div class="mscroll"><table class="mtx"><thead><tr>' +
      '<th class="sticky sortable" data-k="name">' + esc(t("col_system")) + ' ▲▼</th>' +
      '<th class="sortable" data-k="cat">' + esc(t("col_type")) + '</th>' +
      '<th class="sortable numcol" data-k="ra">' + esc(t("t_col_ra")) + '</th>' +
      '<th class="sortable numcol" data-k="dec">' + esc(t("t_col_dec")) + '</th>' +
      '<th class="sortable" data-k="region">' + esc(t("col_region")) + '</th>';
    /* the Planet column counts IMAGE RECORDS (like the band columns), not
       imaged planets — its sub-label says "images" (translated) to avoid
       misreading; the band columns keep their language-neutral μm ranges */
    for (const c of MCOLS) h += '<th class="sortable numcol" data-k="' + c[0] + '">' + esc(t(c[1])) + '<span class="sub">' + (c[0] === "planet" ? esc(t("col_planet_sub")) : c[2]) + "</span></th>";
    h += "</tr></thead><tbody>";
    for (const { s, cells } of rows) {
      h += '<tr><td class="sticky nm" data-id="' + s.id + '" title="' + esc(s.name) + '">' + esc(s.name) + "</td>" +
        '<td class="typecell"><i class="mk ' + mkClass(s) + '"></i> ' + esc(t("cat_" + sysColorKey(s))) +
        (sysHasImagedPlanet(s) ? ' <span class="phost" title="' + esc(t("f_planethost")) + '">★</span>' : "") + "</td>" +
        "<td class='numcol'>" + (s.ra_deg != null ? fmtRA(s.ra_deg) : "–") + "</td>" +
        "<td class='numcol'>" + (s.dec_deg != null ? fmtDec(s.dec_deg) : "–") + "</td>" +
        '<td class="rg" title="' + esc(s.region || "") + '">' + esc(s.region || "") + "</td>";
      for (const c of MCOLS) {
        const cell = cells[c[0]], cls = cell.local ? "has" : cell.n ? "meta" : "gap";
        h += '<td class="cell ' + cls + '"' + (cell.n ? ' data-id="' + s.id + '" data-col="' + c[0] + '"' : "") +
          ">" + (cell.n || "") + "</td>";
      }
      h += "</tr>";
    }
    h += "</tbody></table></div>";
    matrixEl.innerHTML = h;
    wireCatChips(matrixEl);
    matrixEl.querySelectorAll("th.sortable").forEach(th => th.onclick = () => {
      const k = th.dataset.k;
      matrixSort.dir = matrixSort.key === k ? -matrixSort.dir : (k === "name" || k === "region" || k === "cat" ? 1 : -1);
      matrixSort.key = k; buildMatrix();
    });
    matrixEl.querySelectorAll("td.cell[data-id]").forEach(td => td.onclick = () => {
      const s = SYS.find(x => x.id === td.dataset.id); if (!s) return;
      openDetail(s);
      const col = td.dataset.col;
      const idx = sortedImages(s).findIndex(im =>
        col === "planet" ? im.type === "planet" : wlBand(im.wavelength_um) === col);
      if (idx >= 0) showImg(idx);
    });
    matrixEl.querySelectorAll("td.nm").forEach(td => td.onclick = () => {
      const s = SYS.find(x => x.id === td.dataset.id); if (s) openDetail(s);
    });
  }

  /* ---------- tonight / observability planner ---------- */
  /* 4th field: airmass.org observatory id (https://airmass.org obsid) so each
     row can link to a full night chart there instead of us computing it. */
  const SITES = [
    ["Cerro Paranal — VLT", -24.6275, -70.4044, "paranal"],
    ["Chajnantor — ALMA", -23.0294, -67.7548, "alma"],
    ["Mauna Kea — Keck/Subaru/Gemini-N", 19.8261, -155.4747, "keck2"],
    ["Cerro Pachón — Gemini-S/Rubin", -30.2408, -70.7367, "gems"],
    ["La Silla — ESO", -29.2584, -70.7345, "lasilla"],
    ["Las Campanas — Magellan", -29.0089, -70.6920, "lco"],
    ["Roque de los Muchachos — La Palma", 28.7606, -17.8814, "wht"],
    ["Kitt Peak", 31.9583, -111.5967, "kpno"]
  ];
  function airmassOrgUrl(s) {
    const v = document.getElementById("t_site").value;
    if (v === "custom") return null;                       // airmass.org needs an obsid
    const dstr = document.getElementById("t_date").value;
    if (!dstr || s.ra_deg == null) return null;
    return "https://airmass.org/chart/obsid:" + SITES[+v][3] + "/date:" + dstr +
      "/object:" + encodeURIComponent(s.name) +
      "/ra:" + s.ra_deg.toFixed(6) + "/dec:" + s.dec_deg.toFixed(6);
  }
  let tonightData = [];
  let tonightSort = { key: "alt", dir: -1 };   // default: highest first
  function fmtRA(deg) {
    const h = deg / 15, hh = Math.floor(h), mm = Math.round((h - hh) * 60);
    return String(hh).padStart(2, "0") + "h" + String(mm).padStart(2, "0") + "m";
  }
  function julianDay(ms) { return ms / 86400000 + 2440587.5; }
  function gmstDeg(jd) { return ((280.46061837 + 360.98564736629 * (jd - 2451545.0)) % 360 + 360) % 360; }
  function siteLatLon() {
    const v = document.getElementById("t_site").value;
    if (v === "custom") return [parseFloat(document.getElementById("t_lat").value) || 0,
      parseFloat(document.getElementById("t_lon").value) || 0];
    return [SITES[+v][1], SITES[+v][2]];
  }
  function buildTonight() {
    if (!tonightEl) return;
    if (!tonightEl.dataset.init) {
      tonightEl.innerHTML =
        '<div class="tctl">' +
        '<label><span data-i18n="t_site"></span> <select id="t_site">' +
        SITES.map((s, i) => '<option value="' + i + '">' + s[0] + "</option>").join("") +
        '<option value="custom">Custom…</option></select></label>' +
        '<span id="t_custom" hidden><span data-i18n="t_lat"></span> <input id="t_lat" type="number" step="0.01" style="width:5em"> <span data-i18n="t_lon"></span> <input id="t_lon" type="number" step="0.01" style="width:5em"></span>' +
        '<label><span data-i18n="t_night"></span> <input type="date" id="t_date"></label>' +
        '<label><span data-i18n="t_minalt"></span> <input type="number" id="t_alt" value="30" min="0" max="85" style="width:5em">°</label>' +
        '<button id="t_go" data-i18n="t_compute"></button><button id="t_csv" data-i18n="t_csv"></button></div><div id="t_out"></div>';
      tonightEl.dataset.init = "1";
      applyStaticI18n();
      document.getElementById("t_date").value = new Date().toISOString().slice(0, 10);
      document.getElementById("t_site").onchange = e =>
        document.getElementById("t_custom").hidden = e.target.value !== "custom";
      document.getElementById("t_go").onclick = computeTonight;
      document.getElementById("t_csv").onclick = exportTonightCSV;
    }
    computeTonight();
  }
  function computeTonight() {
    if (!tonightEl || !tonightEl.dataset.init) return;
    const [lat, lon] = siteLatLon();
    const minAlt = parseFloat(document.getElementById("t_alt").value) || 30;
    const dstr = document.getElementById("t_date").value;
    if (!dstr) return;
    /* local midnight following the selected evening ≈ 00:00 local of (date + 1 day) */
    const midnightUTms = Date.parse(dstr + "T00:00:00Z") - (lon / 15) * 3600000 + 86400000;
    const lst = (gmstDeg(julianDay(midnightUTms)) + lon) % 360;
    const latR = lat * D2R;
    const rows = filterSystems(SYS, filters, "").filter(s => s.ra_deg != null).map(s => {
      const ha = ((lst - s.ra_deg + 540) % 360) - 180;                 // -180..180°
      const decR = s.dec_deg * D2R, haR = ha * D2R;
      const alt = Math.asin(Math.sin(latR) * Math.sin(decR) +
        Math.cos(latR) * Math.cos(decR) * Math.cos(haR)) * R2D;
      const transAlt = 90 - Math.abs(lat - s.dec_deg);
      const am = alt > 3 ? 1 / Math.cos((90 - alt) * D2R) : null;
      return { s, alt, transAlt, am, hrs: -ha / 15, chart: airmassOrgUrl(s) };
    });
    tonightData = rows.filter(r => r.alt >= minAlt);
    renderTonight(lat, lon, minAlt);
  }
  function renderTonight(lat, lon, minAlt) {
    const out = document.getElementById("t_out");
    const K = tonightSort.key, D = tonightSort.dir;
    const keyFn = {
      name: r => r.s.name.toLowerCase(), type: r => sysColorKey(r.s),
      ra: r => r.s.ra_deg, alt: r => r.alt, airmass: r => (r.am == null ? 99 : r.am),
      transalt: r => r.transAlt, hrs: r => r.hrs, region: r => (r.s.region || "").toLowerCase()
    }[K];
    tonightData.sort((a, b) => {
      const x = keyFn(a), y = keyFn(b);
      return (x < y ? -1 : x > y ? 1 : 0) * D;
    });
    const arrow = k => K === k ? (D === 1 ? " ▲" : " ▼") : "";
    const TH = (k, label, cls) => '<th class="' + (cls || "") + ' sortable" data-sort="' + k + '">' +
      esc(label) + arrow(k) + "</th>";
    let h = '<div class="mhint">' + t("t_hint").replace("{n}", tonightData.length)
      .replace("{a}", minAlt).replace("{lat}", lat.toFixed(2)).replace("{lon}", lon.toFixed(2)) +
      catChipsHTML() + "</div>";
    h += '<div class="mscroll"><table class="mtx"><thead><tr>' +
      TH("name", t("col_system"), "sticky") +
      "<th>" + esc(t("t_col_obs")) + "</th>" +
      TH("type", t("col_type")) +
      TH("ra", t("t_col_ra"), "numcol") +
      TH("alt", t("t_col_alt"), "numcol") +
      TH("airmass", t("t_col_airmass"), "numcol") +
      TH("transalt", t("t_col_transalt"), "numcol") +
      TH("hrs", t("t_col_htransit"), "numcol") +
      TH("region", t("col_region")) + "</tr></thead><tbody>";
    for (const r of tonightData) {
      h += '<tr><td class="sticky nm" data-id="' + r.s.id + '">' + esc(r.s.name) + "</td>" +
        "<td>" + (r.chart ? '<a href="' + r.chart +
          '" target="_blank" rel="noopener">' + esc(t("t_airmass_view")) + "</a>" : "–") + "</td>" +
        '<td class="typecell"><i class="mk ' + mkClass(r.s) + '"></i> ' +
        esc(t("cat_" + sysColorKey(r.s))) +
        (sysHasImagedPlanet(r.s) ? ' <span class="phost" title="' + esc(t("f_planethost")) + '">★</span>' : "") +
        "</td>" +
        "<td class='numcol'>" + fmtRA(r.s.ra_deg) + "</td>" +
        "<td class='numcol'>" + r.alt.toFixed(0) + "</td><td class='numcol'>" + (r.am ? r.am.toFixed(2) : "–") +
        "</td><td class='numcol'>" + r.transAlt.toFixed(0) + "</td><td class='numcol'>" + r.hrs.toFixed(1) +
        '</td><td class="rg" title="' + esc(r.s.region || "") + '">' + esc(r.s.region || "") + "</td></tr>";
    }
    h += "</tbody></table></div>";
    out.innerHTML = h;
    wireCatChips(out);
    out.querySelectorAll("td.nm").forEach(td => td.onclick = () => {
      const s = SYS.find(x => x.id === td.dataset.id); if (s) openDetail(s);
    });
    out.querySelectorAll("th.sortable").forEach(th => th.onclick = () => {
      const k = th.dataset.sort;
      if (tonightSort.key === k) tonightSort.dir *= -1;
      else tonightSort = { key: k, dir: (k === "name" || k === "type" || k === "region" || k === "ra" || k === "airmass") ? 1 : -1 };
      renderTonight(lat, lon, minAlt);
    });
  }
  function exportTonightCSV() {
    if (!tonightData.length) { alert(t("t_nothing")); return; }
    const hdr = ["name", "id", "category", "imaged_planet_host", "ra_deg", "dec_deg",
      "alt_deg", "airmass", "transit_alt_deg", "hours_from_transit", "region"];
    const lines = [hdr.join(",")].concat(tonightData.map(r => [
      '"' + r.s.name.replace(/"/g, '""') + '"', r.s.id,
      t("cat_" + sysColorKey(r.s)), sysHasImagedPlanet(r.s) ? "yes" : "no",
      r.s.ra_deg.toFixed(4), r.s.dec_deg.toFixed(4), r.alt.toFixed(1),
      r.am ? r.am.toFixed(2) : "", r.transAlt.toFixed(1), r.hrs.toFixed(2),
      '"' + (r.s.region || "").replace(/"/g, '""') + '"'].join(",")));
    const blob = new Blob([lines.join("\n")], { type: "text/csv" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
    a.download = "diskatlas_tonight.csv"; document.body.appendChild(a); a.click();
    a.remove(); URL.revokeObjectURL(a.href);
  }

  /* ---------- boot ---------- */
  (function initTheme() {
    if (localStorage.getItem("atlas_theme") === "light") document.body.classList.add("light");
    refreshCOL();
    const btn = document.createElement("button");
    btn.id = "themetoggle";
    btn.title = "light / dark";
    /* icon shows the CURRENT theme (sun in light, moon in dark);
       the button chrome follows the theme via CSS vars */
    btn.textContent = document.body.classList.contains("light") ? "☀️" : "🌙";
    const lang = document.getElementById("lang");
    lang.parentNode.insertBefore(btn, lang.nextSibling);
    btn.onclick = () => {
      const light = document.body.classList.toggle("light");
      localStorage.setItem("atlas_theme", light ? "light" : "dark");
      btn.textContent = light ? "☀️" : "🌙";
      refreshCOL();
      resize();                       // redraw sky with new palette
    };
  })();
  /* ---------- resizable detail panel ----------
     drag the handle on the panel's inner edge to widen/narrow it (bigger panel =
     bigger images); width persists in localStorage. Hidden on phones (full-width). */
  (function detailResize() {
    const detail = document.getElementById("detail");
    const handle = document.getElementById("d_resize");
    if (!detail || !handle) return;
    const KEY = "atlas_detail_w";
    const isMobile = () => window.matchMedia && window.matchMedia("(max-width: 640px)").matches;
    const rtl = () => document.documentElement.dir === "rtl";
    const clampW = w => Math.max(340, Math.min(w, Math.min(window.innerWidth - 40, 1100)));
    function applyStored() {
      if (isMobile()) { detail.style.width = ""; return; }
      const w = parseInt(localStorage.getItem(KEY), 10);
      if (w) detail.style.width = clampW(w) + "px";
    }
    function place() {
      if (detail.hidden || isMobile()) { handle.style.display = "none"; return; }
      handle.style.display = "";
      const r = detail.getBoundingClientRect();
      handle.style.left = (rtl() ? r.right - 5 : r.left - 5) + "px";   // sit on the inner edge
    }
    let dragging = false;
    handle.addEventListener("pointerdown", e => {
      if (isMobile()) return;
      dragging = true; handle.classList.add("drag");
      try { handle.setPointerCapture(e.pointerId); } catch (_) {}
      e.preventDefault();
    });
    handle.addEventListener("pointermove", e => {
      if (!dragging) return;
      detail.style.width = clampW(rtl() ? e.clientX : window.innerWidth - e.clientX) + "px";
      place();
    });
    const end = () => {
      if (!dragging) return; dragging = false; handle.classList.remove("drag");
      localStorage.setItem(KEY, parseInt(detail.style.width, 10) || "");
    };
    handle.addEventListener("pointerup", end);
    handle.addEventListener("pointercancel", end);
    window.addEventListener("resize", () => { applyStored(); place(); });
    detail._placeResize = place;                 // openDetail calls this after showing
    applyStored();
  })();
  applyStaticI18n();
  window.addEventListener("resize", resize);
  resize();
  if (!SYS.length) {
    document.getElementById("statsline").textContent =
      "data.js missing/empty — run backend-data/build.py";
  }
  /* service-worker freshness: sw.js posts {type:'atlas-updated'} when its
     background revalidation fetched a NEWER data.js than the one this page
     was served from — offer a one-tap localized reload */
  if ("serviceWorker" in navigator) {
    let toasted = false;
    navigator.serviceWorker.addEventListener("message", (e) => {
      if (toasted || !e.data || e.data.type !== "atlas-updated") return;
      toasted = true;
      const b = document.createElement("button");
      b.id = "swtoast"; b.type = "button"; b.textContent = t("sw_fresh");
      b.onclick = () => location.reload();
      document.body.appendChild(b);
      setTimeout(() => b.classList.add("show"), 30);
    });
  }
  /* apply the deep-linked view / system / image parsed at the top of boot */
  if (bootHash.view) setView(bootHash.view);
  if (bootHash.sys) {
    const s = SYS.find(x => x.id === bootHash.sys);
    if (s) { goTo(s); if (bootHash.img) showImg(bootHash.img - 1); }   // restore the deep-linked image
  }
})();
