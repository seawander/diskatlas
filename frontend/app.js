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
/* Turn "Mesa+2023", "Kenworthy et al. 2025", "Smith & Terrile 1984" citation
   mentions inside already-HTML-escaped free text into SciX search links. */
function linkifyCitations(escapedText) {
  if (!escapedText) return "";
  const link = (m, name, year) => {
    const q = encodeURIComponent('author:"' + name + '" year:' + year);
    return '<a href="https://scixplorer.org/search?q=' + q +
           '&sort=score+desc" target="_blank" rel="noopener">' + m + "</a>";
  };
  return escapedText
    .replace(/\b((?:(?:De|Del|Van|Von|Le|La|Di|Da|Mac|Mc|O')\s+)?[A-Z][A-Za-z'-]+)\+((?:19|20)\d{2}[a-z]?)\b/g,
             (m, n, y) => link(m, n, y.replace(/[a-z]$/, "")))
    .replace(/\b((?:(?:De|Del|Van|Von|Le|La|Di|Da|Mac|Mc|O')\s+)?[A-Z][A-Za-z'-]+)(?:\s*(?:&amp;|&)\s*[A-Z][A-Za-z'-]+)?\s+et al\.?,?\s+\(?((?:19|20)\d{2})\)?/g,
             (m, n, y) => link(m, n, y))
    .replace(/\b([A-Z][A-Za-z'-]+)\s*(?:&amp;|&)\s*[A-Z][A-Za-z'-]+\s+\(?((?:19|20)\d{2})\)?/g,
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
function sysHasImage(s) { return (s.images || []).some(i => i.file); }
function sysColorKey(s) {
  const c = s.categories || [];
  if (c.includes("quasar")) return "quasar";
  if (c.includes("protoplanetary")) return "proto";
  if (c.includes("debris")) return "debris";
  return "planetonly";
}
/* distinct SHAPE per category (colorblind + B/W-print friendly): circle/triangle/diamond/square */
const SYS_SHAPE = { proto: "circle", debris: "triangle", planetonly: "diamond", quasar: "square" };
const SYS_GLYPH = { proto: "●", debris: "▲", planetonly: "◆", quasar: "■" };
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

function filterSystems(systems, f, q) {
  q = (q || "").trim().toLowerCase();
  const facSet = f.facilities && f.facilities.size ? f.facilities : null;
  const instSet = f.instruments && f.instruments.size ? f.instruments : null;
  const bandSet = f.bands && f.bands.size ? f.bands : null;
  const missSet = f.missing && f.missing.size ? f.missing : null;
  return systems.filter(s => {
    const key = sysColorKey(s);
    if (key === "proto" && !f.proto) return false;
    if (key === "debris" && !f.debris) return false;
    if (key === "planetonly" && !f.planetonly) return false;
    if (key === "quasar" && f.quasar === false) return false;
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
      const is = new Set((s.images || []).map(i => i.instr_key).filter(Boolean));
      if (![...instSet].every(x => is.has(x))) return false;
    }
    if (bandSet) {
      const bs = new Set((s.images || []).map(imgCol));
      if (![...bandSet].some(x => bs.has(x))) return false;
    }
    if (missSet) {
      if (missSet.has("mm") && sysHasMm(s)) return false;
      if (missSet.has("nir") && sysHasNir(s)) return false;
      if (missSet.has("planet") && sysHasImagedPlanet(s)) return false;
    }
    if (q) {
      const hay = [s.name, s.id, ...(s.alt_names || [])].join(" ").toLowerCase();
      if (!hay.includes(q)) return false;
    }
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
    document.title = t("title");
    document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
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
  const CAT_KEY = { protoplanetary: "cat_proto", debris: "cat_debris", quasar: "cat_quasar" };
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
    COL.ink = CSS.getPropertyValue("--ink").trim() || "#e8ecf8";
    COL.dim = CSS.getPropertyValue("--dim").trim() || "#9aa7c7";
    COL.line = CSS.getPropertyValue("--line").trim() || "#2a3560";
    COL.sky = CSS.getPropertyValue("--sky").trim() || "#070b18";
  };

  let W = 0, H = 0, DPR = 1;
  const view = { ra0: 90, dec0: 5, ppd: 3, topInset: 0 };   // start loosely on Taurus/Ori side
  let minPPD = 1;
  const filters = { proto: true, debris: true, planetonly: true, quasar: true,
    planethost: false, hasimg: false, constellations: true,
    facilities: new Set(), instruments: new Set(), bands: new Set(), missing: new Set() };
  let visible = new Set(SYS.map(s => s.id));
  let hoverId = null, currentSys = null, curImg = 0, currentView = "sky";

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

  const GAL = []; for (let l = 0; l <= 360; l += 2) GAL.push(galToEq(l, 0));
  const ECL = []; for (let l = 0; l <= 360; l += 2) ECL.push(eclToEq(l));

  function drawGrid() {
    ctx.strokeStyle = "rgba(110,168,255,.14)"; ctx.fillStyle = COL.dim;
    ctx.lineWidth = 1; ctx.font = "11px system-ui";
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
      ctx.fillStyle = "rgba(154,167,199,.6)";
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
    ctx.strokeStyle = "rgba(120,140,190,.30)";
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
      ctx.fillStyle = "rgba(140,160,210,.42)";
      ctx.font = "italic 11px system-ui";
      for (const n of CONST.names) {
        const p = project(n.ra, n.dec, view, W, H);
        if (p.x < 0 || p.x > W || p.y < topbarH() || p.y > H) continue;
        ctx.fillText(n.name, p.x, p.y);
      }
      ctx.font = "11px system-ui";
    }
  }

  /* draw a category-specific shape (path only; caller fills/strokes) */
  function drawShape(key, x, y, r) {
    ctx.beginPath();
    const sh = sysShape(key);
    if (sh === "square") { const a = r * 0.92; ctx.rect(x - a, y - a, 2 * a, 2 * a); }
    else if (sh === "diamond") { const a = r * 1.28; ctx.moveTo(x, y - a); ctx.lineTo(x + a, y); ctx.lineTo(x, y + a); ctx.lineTo(x - a, y); ctx.closePath(); }
    else if (sh === "triangle") { const a = r * 1.32; ctx.moveTo(x, y - a); ctx.lineTo(x + a * 0.87, y + a * 0.6); ctx.lineTo(x - a * 0.87, y + a * 0.6); ctx.closePath(); }
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
    drawCurve(GAL, "rgba(160,190,255,.28)");
    drawCurve(ECL, "rgba(255,190,120,.20)", [5, 5]);
    drawGrid();

    const zs = Math.min(1.6, 0.9 + view.ppd / 60);
    for (const s of PLOT()) {
      const p = project(s.ra_deg, s.dec_deg, view, W, H);
      if (p.x < -12 || p.x > W + 12 || p.y < -12 || p.y > H + 12) continue;
      const nimg = (s.images || []).filter(i => i.file).length;
      const r = 5 * zs;   // uniform size per marker type (image count no longer scales the marker; it only sets fill opacity below)
      const key = sysColorKey(s);
      const col = COL[key];
      ctx.fillStyle = col; ctx.globalAlpha = nimg ? 0.95 : 0.55;
      drawShape(key, p.x, p.y, r); ctx.fill(); ctx.globalAlpha = 1;
      if (sysHasImagedPlanet(s)) {
        starPath(p.x, p.y, r + 4.5);
        ctx.strokeStyle = COL.ink; ctx.lineWidth = 1.3; ctx.stroke();
      }
      if (s.id === hoverId || (currentSys && s.id === currentSys.id)) {
        ctx.beginPath(); ctx.arc(p.x, p.y, r + 7.5, 0, 7);
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.stroke();
      }
      if (view.ppd > 26) {
        ctx.fillStyle = "rgba(232,236,248,.85)"; ctx.font = "11px system-ui";
        ctx.fillText(s.name, p.x + r + 4, p.y + 4);
      }
    }
    const st = A.stats || {};
    document.getElementById("statsline").textContent =
      (st.systems || SYS.length) + " " + t("word_systems") + " · " + (st.image_records || "?") +
      " " + t("word_records") + " · " + (st.with_local_image || 0) + " " + t("word_local") +
      " · " + t("word_built") + " " + (A.generated || "?").slice(0, 10);
    /* literature-exploration progress bar (paper-finder ledgers, baked in at build time) */
    if (st.papers_known && !document.getElementById("litbar")) {
      const wrap = document.createElement("span"); wrap.id = "litbar";
      const pctE = Math.round(100 * st.papers_explored / st.papers_known);
      const pctI = Math.round(100 * st.papers_in_atlas / st.papers_known);
      wrap.title = t("lit_title").replace("{k}", st.papers_known)
        .replace("{e}", st.papers_explored).replace("{i}", st.papers_in_atlas);
      /* collapsed behind an (i) icon: hover (or tap) reveals numbers + bar */
      wrap.innerHTML = '<span class="liticon">ⓘ</span>' +
        '<span class="litdetail"><span class="litlabel">' + t("lit_label") + " " +
        st.papers_in_atlas + "/" + st.papers_explored + "/" + st.papers_known + "</span>" +
        '<span class="littrack"><span class="litseg exp" style="width:' + pctE +
        '%"></span><span class="litseg ing" style="width:' + pctI + '%"></span></span></span>';
      wrap.onclick = () => wrap.classList.toggle("open");
      document.getElementById("statsline").after(wrap);
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
  canvas.addEventListener("mousedown", e => { dragging = true; moved = false; lx = e.clientX; ly = e.clientY; canvas.classList.add("dragging"); });
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
    if (moved) return;
    const s = hitTest(e.clientX, e.clientY);
    if (s) openDetail(s);
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

  window.addEventListener("keydown", e => {
    if (e.key === "Escape") { closeDetail(); listEl.hidden = true; }
    if (!detail.hidden) {
      if (e.key === "ArrowLeft") showImg(curImg - 1);
      if (e.key === "ArrowRight") showImg(curImg + 1);
    }
  });

  /* ---------- filters & search ---------- */
  const FDEF = [
    ["proto", "cat_proto", "proto"],
    ["debris", "cat_debris", "debris"],
    ["planetonly", "cat_planetonly", "planet"],
    ["quasar", "cat_quasar", "quasar"],
    ["planethost", "f_planethost", ""],
    ["hasimg", "f_hasimg", ""],
    ["constellations", "f_constellations", ""]
  ];
  const fbar = document.getElementById("filters");
  for (const [key, i18nKey, cls] of FDEF) {
    const el = document.createElement("span");
    el.className = "chip " + cls + (filters[key] ? " on" : "");
    el.dataset.i18n = i18nKey; el.textContent = t(i18nKey);
    el.onclick = () => { filters[key] = !filters[key]; el.classList.toggle("on"); refilter(); };
    fbar.appendChild(el);
  }
  function refilter() {
    visible = new Set(filterSystems(SYS, filters, "").map(s => s.id));
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
    for (const s of res) {
      const row = document.createElement("div");
      row.className = "row";
      row.innerHTML = "<b>" + esc(s.name) + "</b><span class='meta'>" +
        (s.categories || []).map(c => c[0]).join("+") +
        ((s.images || []).some(i => i.file) ? " 🖼" : "") +
        (sysHasPlanet(s) ? " ● pl" : "") + "</span>";
      row.onclick = () => { listEl.hidden = true; searchEl.value = s.name; goTo(s); };
      listEl.appendChild(row);
    }
    const r = searchEl.getBoundingClientRect();
    listEl.style.left = r.left + "px";
    /* anchor right under the search box and overlay the facet chips (front layer),
       instead of below the whole (tall) header */
    listEl.style.top = (r.bottom + 4) + "px";
    listEl.hidden = false;
  });
  document.addEventListener("click", e => {
    if (e.target !== searchEl && !listEl.contains(e.target)) listEl.hidden = true;
  });

  function goTo(s) {
    if (s.ra_deg != null) {
      view.ra0 = s.ra_deg; view.dec0 = s.dec_deg;
      view.ppd = Math.max(view.ppd, 40);
    }
    openDetail(s);
  }

  /* ---------- detail panel ---------- */
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  function sortedImages(s) {
    return (s.images || []).slice().sort((a, b) =>
      (a.wavelength_um || 0) - (b.wavelength_um || 0));
  }

  function openDetail(s) {
    currentSys = s; curImg = 0;
    document.getElementById("d_name").textContent = s.name;
    const bits = [];
    for (const c of (s.categories || []))
      bits.push('<span class="tag ' + (c === "protoplanetary" ? "proto" :
        c === "quasar" ? "quasar" : "debris") + '">' + esc(catLabel(c)) + "</span>");
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
          (p.note ? "<br>" + linkifyCitations(esc(p.note)) : "") + "</div>";
      }).join("");
    } else pl.innerHTML = "";
    document.getElementById("d_notes").innerHTML = linkifyCitations(esc(s.notes || "")) +
      (s.last_updated ? '<div class="lastupd">' + esc(t("d_updated")) + " " +
        esc(s.last_updated) + "</div>" : "");
    buildSlider(s);
    showImg(0);
    detail.hidden = false;
    if (history.replaceState) history.replaceState(null, "", "#s=" + s.id);
    draw();
  }
  function closeDetail() {
    detail.hidden = true; currentSys = null;
    if (history.replaceState) history.replaceState(null, "", "#");
    draw();
  }
  document.getElementById("closebtn").onclick = closeDetail;
  document.getElementById("d_prev").onclick = () => showImg(curImg - 1);
  document.getElementById("d_next").onclick = () => showImg(curImg + 1);

  function shortFac(f) { return (f || "?").replace("VLT-", "").replace("Gemini-", "").replace("Subaru-", ""); }

  function buildSlider(s) {
    const sl = document.getElementById("d_slider");
    sl.innerHTML = "";
    sortedImages(s).forEach((im, i) => {
      const t = document.createElement("span");
      t.className = "tick";
      t.innerHTML = '<span class="wl">' + fmtWl(im.wavelength_um) + "</span> " + esc((im.instr_key && im.instr_key !== "other") ? im.instr_key : shortFac(im.facility));
      t.onclick = () => showImg(i);
      sl.appendChild(t);
    });
  }

  function showImg(i) {
    const s = currentSys; if (!s) return;
    const ims = sortedImages(s);
    if (!ims.length) {
      document.getElementById("d_imgbox").innerHTML =
        '<div class="placeholder"><span class="big">✴</span>' + esc(t("d_noimg")) + "</div>";
      document.getElementById("d_caption").innerHTML = "";
      document.getElementById("d_prev").disabled = document.getElementById("d_next").disabled = true;
      return;
    }
    curImg = (i + ims.length) % ims.length;
    const im = ims[curImg];
    const box = document.getElementById("d_imgbox");
    if (im.file) {
      box.innerHTML = '<img alt="" src="' + esc(im.file) + '">';
    } else {
      box.innerHTML = '<div class="placeholder"><span class="big">⏳</span>' +
        esc(t("d_pending1")) + "<br>" + esc(t("d_pending2")) + "</div>";
    }
    document.querySelectorAll("#d_slider .tick").forEach((el, k) =>
      el.classList.toggle("on", k === curImg));
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
    for (const i of filters.instruments) (INSTR2FAC[i] || []).forEach(f => relFac.add(f));
    facetsBar.querySelectorAll('.chip[data-group="facet_instrument"]').forEach(c =>
      c.classList.toggle("rel", relInstr.has(c.dataset.val) && !c.classList.contains("on")));
    facetsBar.querySelectorAll('.chip[data-group="facet_facility"]').forEach(c =>
      c.classList.toggle("rel", relFac.has(c.dataset.val) && !c.classList.contains("on")));
  }
  if (facetsBar) {
    const bandEntries = WL_BANDS.map(b => [b.key, "band_" + b.key, b.label]).concat([["planet", "band_planet", "planet"]]);
    chipGroup(facetsBar, "facet_band", bandEntries, filters.bands);
    chipGroup(facetsBar, "facet_missing", [["mm", "miss_mm", "mm"], ["nir", "miss_nir", "scat-light"], ["planet", "miss_planet", "imaged planet"]], filters.missing);
    chipGroup(facetsBar, "facet_facility", ALL_FAC.map(f => [f, null, f]), filters.facilities, true);
    chipGroup(facetsBar, "facet_instrument", ALL_INSTR.map(f => [f, null, f]), filters.instruments, true);
    const hint = document.createElement("span"); hint.className = "flabel fhint";
    hint.dataset.i18n = "facet_hint"; hint.textContent = t("facet_hint");
    facetsBar.appendChild(hint);
    const reset = document.createElement("span"); reset.className = "chip sm reset";
    reset.dataset.i18n = "facet_clear"; reset.textContent = t("facet_clear");
    reset.onclick = () => {
      filters.bands.clear(); filters.missing.clear(); filters.facilities.clear(); filters.instruments.clear();
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
    tb.innerHTML = '<span class="ico">' + ico + '</span> <span data-i18n="' + key + '"></span>';
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
  /* legend (built here so it carries symbols + translatable labels) */
  const legendKeys = [["proto", "cat_proto"], ["debris", "cat_debris"], ["planetonly", "leg_planetonly"], ["quasar", "leg_quasar"]];
  if (legendEl) {
    let lh = "";
    for (const [k, key] of legendKeys)
      lh += '<span><i class="mk ' + k + '"></i><span data-i18n="' + key + '"></span></span>';
    lh += '<span><span class="mk-star">★</span><span data-i18n="leg_imaged"></span></span>';
    lh += '<span class="hint" data-i18n="leg_hint"></span>';
    legendEl.innerHTML = lh;
  }
  let facetsCollapsed = false;
  /* BAND / MISSING / FACILITY / INSTRUMENT rows: Sky-tab only, and collapsible by
     clicking the Sky tab again (bigger map). Category chips stay everywhere. */
  function updateFacetVisibility() {
    const show = currentView === "sky" && !facetsCollapsed;
    ["facet_band", "facet_missing", "facet_facility", "facet_instrument"].forEach(k => {
      const lbl = facetsBar && facetsBar.querySelector('.flabel[data-i18n="' + k + '"]');
      if (lbl && lbl.closest(".fgroup")) lbl.closest(".fgroup").style.display = show ? "" : "none";
    });
    const hint = facetsBar && facetsBar.querySelector(".fhint");
    if (hint) hint.style.display = show ? "" : "none";
    const reset = facetsBar && facetsBar.querySelector(".chip.reset");
    if (reset) reset.style.display = show ? "" : "none";
  }
  function setView(v) {
    if (v === "sky" && currentView === "sky") facetsCollapsed = !facetsCollapsed;
    currentView = v;
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
  const CAT_DEFS = [["proto", "cat_proto"], ["debris", "cat_debris"],
                    ["planetonly", "cat_planetonly"], ["quasar", "cat_quasar"]];
  function catChipsHTML() {
    return '<span class="catsel">' + CAT_DEFS.map(([k, ik]) =>
      '<span class="chip sm catchip' + (filters[k] ? " on" : "") + '" data-cat="' + k +
      '"><i class="mk ' + k + '"></i> ' + esc(t(ik)) + "</span>").join("") + "</span>";
  }
  function wireCatChips(container) {
    container.querySelectorAll(".catchip").forEach(ch => ch.onclick = () => {
      /* drive the global header chip so all views + header stay in sync */
      const hdr = [...document.querySelectorAll("#filters .chip")]
        .find(e => e.dataset.i18n === "cat_" + ch.dataset.cat);
      if (hdr) hdr.click();
      else { filters[ch.dataset.cat] = !filters[ch.dataset.cat]; refilter(); }
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
      for (const im of (s.images || [])) { const k = imgCol(im); if (cells[k]) { cells[k].n++; if (im.file) cells[k].local++; } }
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
    for (const c of MCOLS) h += '<th class="sortable numcol" data-k="' + c[0] + '">' + esc(t(c[1])) + '<span class="sub">' + c[2] + "</span></th>";
    h += "</tr></thead><tbody>";
    for (const { s, cells } of rows) {
      h += '<tr><td class="sticky nm" data-id="' + s.id + '" title="' + esc(s.name) + '">' + esc(s.name) + "</td>" +
        '<td class="typecell"><i class="mk ' + sysColorKey(s) + '"></i> ' + esc(t("cat_" + sysColorKey(s))) +
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
      const idx = sortedImages(s).findIndex(im => imgCol(im) === td.dataset.col);
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
        '<label><span data-i18n="t_minalt"></span> <input type="number" id="t_alt" value="30" min="0" max="85" style="width:3.4em">°</label>' +
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
        '<td class="typecell"><i class="mk ' + sysColorKey(r.s) + '"></i> ' +
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
  applyStaticI18n();
  window.addEventListener("resize", resize);
  resize();
  if (!SYS.length) {
    document.getElementById("statsline").textContent =
      "data.js missing/empty — run backend/build.py";
  }
  const m = location.hash.match(/#s=([a-z0-9-]+)/);
  if (m) {
    const s = SYS.find(x => x.id === m[1]);
    if (s) goTo(s);
  }
})();
