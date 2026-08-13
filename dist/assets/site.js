/* ============================================================
   ISIDE SYSTEMS — shared behaviour
   Deliberately quiet: nothing loops. Figures draw once, then hold.
   ============================================================ */
"use strict";

const DPR = Math.min(window.devicePixelRatio || 1, 2);
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const easeOut = t => 1 - Math.pow(1 - t, 3);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* seeded PRNG — figures must look identical on every visit */
function rng(seed){
  let a = seed >>> 0;
  return function(){
    a += 0x6D2B79F5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---------------- palette from CSS ---------------- */
const PAL = {};
function readPal(){
  const c = getComputedStyle(document.documentElement);
  ["ink","dim","acc","acc2","bg"].forEach(k => PAL[k] = c.getPropertyValue("--" + k).trim());
  PAL.inkRgb = c.getPropertyValue("--ink-rgb").trim();
}
readPal();

/* ---------------- theme ---------------- */
(function theme(){
  const btn = document.getElementById("themeBtn");
  const apply = t => {
    document.documentElement.setAttribute("data-theme", t);
    if (btn) btn.textContent = t === "dark" ? "Light" : "Dark";
    readPal();
    document.dispatchEvent(new CustomEvent("themechange"));
  };
  let saved = null;
  try { saved = localStorage.getItem("iside-theme"); } catch(e){}
  apply(saved || "light");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    try { localStorage.setItem("iside-theme", next); } catch(e){}
    apply(next);
  });
})();

/* ---------------- reveal on scroll ---------------- */
(function reveal(){
  const els = document.querySelectorAll(".rv");
  if (!els.length) return;
  if (reduced){ els.forEach(e => e.classList.add("in")); return; }
  const io = new IntersectionObserver((ents) => {
    ents.forEach(e => { if (e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: .18 });
  els.forEach(e => io.observe(e));
  // failsafe: never leave content hidden if the observer misbehaves
  setTimeout(() => els.forEach(e => e.classList.add("in")), 2500);
})();

/* ============================================================
   HERO FIGURE — a fixed geometric construction.
   Drawn once with a left-to-right wipe, then still. No loop.
   ============================================================ */
(function figure(){
  const c = document.getElementById("figure");
  if (!c) return;
  const x = c.getContext("2d");
  let W = 0, H = 0, drawn = false;

  function geometry(){
    const r = rng(20260813);
    const S = Math.min(W, H);
    const cx = W * 0.5, cy = H * 0.5;
    const R = S * 0.36;
    const nodes = [];
    // 9 nodes on two concentric rings — fixed angles, no jitter
    for (let i = 0; i < 5; i++){
      const a = -Math.PI/2 + i * (Math.PI * 2 / 5);
      nodes.push({ x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R, r: 4.5, lab: "N" + i });
    }
    for (let i = 0; i < 4; i++){
      const a = -Math.PI/2 + Math.PI/4 + i * (Math.PI * 2 / 4);
      nodes.push({ x: cx + Math.cos(a) * R * 0.52, y: cy + Math.sin(a) * R * 0.52, r: 3.2, lab: "" });
    }
    // deterministic edge set
    const edges = [];
    for (let i = 0; i < nodes.length; i++)
      for (let j = i + 1; j < nodes.length; j++)
        if (r() < 0.42) edges.push([i, j]);
    return { cx, cy, R, S, nodes, edges };
  }

  function paint(p){                       // p = wipe progress 0..1
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
    x.clearRect(0, 0, W, H);
    const g = geometry();
    x.save();
    x.beginPath(); x.rect(0, 0, W * p, H); x.clip();

    // 1. base module grid
    const step = g.S / 16;
    x.strokeStyle = `rgba(${PAL.inkRgb},.07)`;
    x.lineWidth = 1;
    for (let i = 0; i <= 16; i++){
      const o = i * step + (W - g.S) / 2, o2 = i * step + (H - g.S) / 2;
      x.beginPath(); x.moveTo(o, (H - g.S) / 2); x.lineTo(o, (H + g.S) / 2); x.stroke();
      x.beginPath(); x.moveTo((W - g.S) / 2, o2); x.lineTo((W + g.S) / 2, o2); x.stroke();
    }

    // 2. outer square + inscribed circle + rotated square
    x.strokeStyle = `rgba(${PAL.inkRgb},.30)`;
    x.strokeRect((W - g.S * .84) / 2, (H - g.S * .84) / 2, g.S * .84, g.S * .84);
    x.beginPath(); x.arc(g.cx, g.cy, g.R, 0, Math.PI * 2); x.stroke();
    x.beginPath();
    for (let i = 0; i < 4; i++){
      const a = -Math.PI / 2 + i * Math.PI / 2;
      const px = g.cx + Math.cos(a) * g.R, py = g.cy + Math.sin(a) * g.R;
      i ? x.lineTo(px, py) : x.moveTo(px, py);
    }
    x.closePath(); x.stroke();

    // 3. tick ring
    x.strokeStyle = `rgba(${PAL.inkRgb},.35)`;
    for (let d = 0; d < 360; d += 5){
      const a = d * Math.PI / 180;
      const len = d % 45 === 0 ? 11 : 5;
      x.beginPath();
      x.moveTo(g.cx + Math.cos(a) * (g.R + 6), g.cy + Math.sin(a) * (g.R + 6));
      x.lineTo(g.cx + Math.cos(a) * (g.R + 6 + len), g.cy + Math.sin(a) * (g.R + 6 + len));
      x.stroke();
    }

    // 4. graph edges
    x.strokeStyle = `rgba(${PAL.inkRgb},.42)`;
    g.edges.forEach(([i, j]) => {
      x.beginPath();
      x.moveTo(g.nodes[i].x, g.nodes[i].y);
      x.lineTo(g.nodes[j].x, g.nodes[j].y);
      x.stroke();
    });

    // 5. nodes
    g.nodes.forEach((n, i) => {
      x.fillStyle = i === 0 ? PAL.acc : PAL.ink;
      x.beginPath(); x.arc(n.x, n.y, n.r, 0, Math.PI * 2); x.fill();
      if (n.lab){
        x.fillStyle = PAL.dim;
        x.font = `9px ${getComputedStyle(document.body).getPropertyValue("--mono")}`;
        x.textAlign = "center"; x.textBaseline = "middle";
        x.fillText(n.lab, n.x, n.y - 13);
      }
    });

    // 6. axes + corner marks
    x.strokeStyle = PAL.acc; x.lineWidth = 1;
    x.beginPath();
    x.moveTo((W - g.S * .84) / 2, g.cy); x.lineTo((W + g.S * .84) / 2, g.cy);
    x.stroke();
    x.setLineDash([2, 4]);
    x.strokeStyle = `rgba(${PAL.inkRgb},.28)`;
    x.beginPath(); x.moveTo(g.cx, (H - g.S * .84) / 2); x.lineTo(g.cx, (H + g.S * .84) / 2); x.stroke();
    x.setLineDash([]);
    x.restore();
  }

  function size(){
    const r = c.getBoundingClientRect();
    W = r.width; H = r.height;
    c.width = W * DPR; c.height = H * DPR;
  }

  function drawIn(){
    size();
    if (reduced){ paint(1); drawn = true; return; }
    const t0 = performance.now();
    (function step(){
      const p = clamp((performance.now() - t0) / 1200, 0, 1);
      paint(easeOut(p));
      if (p < 1) requestAnimationFrame(step); else drawn = true;
    })();
  }

  let rt;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { size(); paint(1); }, 180); });
  document.addEventListener("themechange", () => { if (drawn){ size(); paint(1); } });
  drawIn();
})();

/* ============================================================
   MEASUREMENT MATRIX — channels x funnel stages.
   Draws once when it enters view, then holds. No loop.
   ============================================================ */
(function matrix(){
  const c = document.getElementById("matrix");
  if (!c) return;
  const x = c.getContext("2d");
  const CH = ["GOOGLE ADS", "META", "LINKEDIN", "TIKTOK"];
  const ST = ["AWARENESS", "CONSIDERATION", "INTENT", "CONVERSION", "RETENTION"];
  // planned weight per channel/stage, 0..1 — illustrative, not client data
  const W8 = [
    [0.35, 0.55, 0.85, 1.00, 0.30],
    [0.90, 0.75, 0.45, 0.35, 0.55],
    [0.45, 0.80, 0.70, 0.40, 0.25],
    [1.00, 0.60, 0.25, 0.15, 0.20],
  ];
  let W = 0, H = 0, done = false;

  function size(){
    const r = c.getBoundingClientRect();
    W = r.width; H = W < 620 ? Math.max(300, Math.min(360, W * 0.95)) : Math.max(300, Math.min(430, W * 0.56));
    c.style.height = H + "px";
    c.width = W * DPR; c.height = H * DPR;
  }

  function paint(p){
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
    x.clearRect(0, 0, W, H);
    const mono = getComputedStyle(document.body).getPropertyValue("--mono");
    const fs = W < 420 ? 7 : W < 620 ? 8 : 9;
    x.font = `${fs}px ${mono}`;
    x.textBaseline = "middle";

    // pad the left gutter to whatever the channel labels actually measure
    const chW = Math.max(...CH.map(c2 => x.measureText(c2).width));
    const padL = Math.min(Math.round(chW) + 20, W * 0.34);
    const padR = 12, padT = 38, padB = 30;
    const cw = (W - padL - padR) / ST.length;
    const rh = (H - padT - padB) / CH.length;

    // stage headings: full word, else 4 letters, else 3 — whatever fits the column
    x.fillStyle = PAL.dim;
    x.textAlign = "center";
    ST.forEach((s2, j) => {
      let label = s2;
      if (x.measureText(label).width > cw - 6) label = s2.slice(0, 4);
      if (x.measureText(label).width > cw - 6) label = s2.slice(0, 3);
      x.fillText(label, padL + cw * (j + .5), padT - 17);
    });

    // grid
    x.strokeStyle = `rgba(${PAL.inkRgb},.14)`;
    for (let j = 0; j <= ST.length; j++){
      const px = padL + cw * j;
      x.beginPath(); x.moveTo(px, padT - 6); x.lineTo(px, H - padB); x.stroke();
    }
    for (let i = 0; i <= CH.length; i++){
      const py = padT + rh * i;
      x.beginPath(); x.moveTo(padL, py); x.lineTo(W - padR, py); x.stroke();
    }

    CH.forEach((ch, i) => {
      x.fillStyle = PAL.dim; x.textAlign = "right";
      x.fillText(ch, padL - 12, padT + rh * (i + .5));

      ST.forEach((s2, j) => {
        const target = W8[i][j];
        const e = easeOut(clamp((p - (i * ST.length + j) * 0.028) * 2.2, 0, 1));
        const v = target * e;
        const cx0 = padL + cw * j, cy0 = padT + rh * i;
        // weight drawn as a stack of ticks filling the cell from the bottom
        const inner = Math.max(4, Math.min(9, cw * 0.12)), ticks = 7;
        const filled = Math.round(v * ticks);
        for (let k = 0; k < ticks; k++){
          const on = k < filled;
          x.fillStyle = on
            ? (target >= .85 ? PAL.acc : PAL.ink)
            : `rgba(${PAL.inkRgb},.10)`;
          const ty = cy0 + rh - inner - k * ((rh - inner * 2) / ticks);
          x.fillRect(cx0 + inner, ty, cw - inner * 2, 2);
        }
      });
    });

    // captions, only if both actually fit side by side
    const legend = (c.dataset.legend || "").toUpperCase();
    const plan = (c.dataset.plan || "").toUpperCase();
    const room = W - padL - padR;
    x.fillStyle = PAL.dim; x.textAlign = "left";
    x.fillText(legend, padL, H - 12);
    if (x.measureText(legend).width + x.measureText(plan).width + 24 < room){
      x.fillStyle = PAL.acc; x.textAlign = "right";
      x.fillText(plan, W - padR, H - 12);
    }
  }

  function run(){
    size();
    if (reduced){ paint(1); done = true; return; }
    const t0 = performance.now();
    (function step(){
      const p = clamp((performance.now() - t0) / 1400, 0, 1);
      paint(p);
      if (p < 1) requestAnimationFrame(step); else done = true;
    })();
  }

  new IntersectionObserver((ents, obs) => {
    if (ents.some(e => e.isIntersecting)){ run(); obs.disconnect(); }
  }, { threshold: .3 }).observe(c);

  let rt;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (done){ size(); paint(1); } }, 180); });
  document.addEventListener("themechange", () => { if (done){ size(); paint(1); } });
})();

/* ============================================================
   PROJECT THUMBNAILS — deterministic geometric placeholders.
   Gently animated: only while on screen, ~15fps, tiny amplitude.
   Replace <canvas class="thumb"> with <img> once real art exists.
   ============================================================ */
(function thumbs(){
  const list = [...document.querySelectorAll("canvas.thumb")];
  if (!list.length) return;
  const visible = new Set();

  function paint(c, t){
    const x = c.getContext("2d");
    const r = c.getBoundingClientRect();
    const W = r.width, H = r.height;
    if (!W) return;
    if (c.width !== Math.round(W * DPR)){ c.width = W * DPR; c.height = H * DPR; }
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
    x.clearRect(0, 0, W, H);
    const seed = parseInt(c.dataset.seed || "1", 10);
    const kind = seed % 4;
    const ph = seed * 1.7;                       // per-tile phase, keeps the grid from pulsing in unison
    const slow = t * 0.00016;                    // one cycle ≈ 40s

    x.lineWidth = 1;

    if (kind === 0){                             // nested squares, breathing
      const live = 3 + Math.round(1.5 + 1.5 * Math.sin(slow * 1.6 + ph));
      for (let i = 0; i < 7; i++){
        const drift = Math.sin(slow * 2 + ph + i * 0.5) * 1.6;
        const m = 10 + i * (Math.min(W, H) * .045) + drift;
        x.strokeStyle = i === live ? PAL.acc : `rgba(${PAL.inkRgb},.28)`;
        x.strokeRect(m, m, W - m * 2, H - m * 2);
      }
    } else if (kind === 1){                      // dot matrix, threshold drifting
      const rand = rng(seed * 7919);
      const bias = 0.06 * Math.sin(slow * 1.4 + ph);
      for (let yy = 12; yy < H - 6; yy += 9)
        for (let xx = 12; xx < W - 6; xx += 9){
          const d = xx / W;
          if (rand() < d * .9 + .05 + bias){
            x.fillStyle = d > .82 ? PAL.acc : `rgba(${PAL.inkRgb},.42)`;
            x.fillRect(xx, yy, 2.4, 2.4);
          }
        }
    } else if (kind === 2){                      // step profile, heights easing
      const rand = rng(seed * 7919);
      const n = 9, step = (W - 28) / n;
      for (let i = 0; i < n; i++){
        const base = .14 + rand() * .72;
        const h = H * (base + 0.05 * Math.sin(slow * 2.2 + ph + i * 0.8));
        x.strokeStyle = i === n - 1 ? PAL.acc : `rgba(${PAL.inkRgb},.34)`;
        x.beginPath();
        x.moveTo(14 + i * step, H - 12);
        x.lineTo(14 + i * step, H - 12 - h);
        x.lineTo(14 + (i + 1) * step, H - 12 - h);
        x.stroke();
      }
    } else {                                     // radial spokes, slow rotation
      const rand = rng(seed * 7919);
      const cx = W / 2, cy = H / 2, R = Math.min(W, H) * .36;
      const rot = slow * 0.5 + ph;
      x.strokeStyle = `rgba(${PAL.inkRgb},.30)`;
      x.beginPath(); x.arc(cx, cy, R, 0, Math.PI * 2); x.stroke();
      for (let d = 0; d < 360; d += 12){
        const a = d * Math.PI / 180 + rot;
        const l = R * (.35 + rand() * .62) * (1 + 0.05 * Math.sin(slow * 3 + d));
        x.strokeStyle = d === 0 ? PAL.acc : `rgba(${PAL.inkRgb},.32)`;
        x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx + Math.cos(a) * l, cy + Math.sin(a) * l); x.stroke();
      }
    }
  }

  const io = new IntersectionObserver(ents => {
    ents.forEach(e => e.isIntersecting ? visible.add(e.target) : visible.delete(e.target));
  }, { rootMargin: "80px" });
  list.forEach(c => io.observe(c));

  if (reduced){ list.forEach(c => paint(c, 0)); return; }

  let last = 0;
  (function loop(now){
    if (now - last > 66){                        // ~15fps is plenty for this amplitude
      last = now;
      visible.forEach(c => paint(c, now));
    }
    requestAnimationFrame(loop);
  })(0);

  document.addEventListener("themechange", () => list.forEach(c => paint(c, performance.now())));
})();

/* ============================================================
   PROJECT FILTERS
   ============================================================ */
(function filters(){
  const btns = document.querySelectorAll("[data-filter]");
  const rows = document.querySelectorAll("[data-cat]");
  if (!btns.length || !rows.length) return;
  const count = document.getElementById("pcount");
  function apply(f){
    let n = 0;
    rows.forEach(r => {
      const on = f === "all" || r.dataset.cat.split(" ").includes(f);
      r.classList.toggle("off", !on);
      if (on) n++;
    });
    if (count) count.textContent = String(n).padStart(2, "0");
  }
  btns.forEach(b => b.addEventListener("click", () => {
    btns.forEach(o => o.setAttribute("aria-pressed", String(o === b)));
    apply(b.dataset.filter);
  }));
  apply("all");
})();

/* ============================================================
   CONTACT FORM — client-side only in this demo build.
   Point `action` at a real endpoint (Formspree, own handler) to send.
   ============================================================ */
(function contact(){
  const form = document.querySelector("form.contact");
  if (!form) return;
  const note = form.querySelector(".formnote");
  form.addEventListener("submit", e => {
    e.preventDefault();
    const d = new FormData(form);
    if (!d.get("name") || !d.get("email") || !d.get("message")){
      note.textContent = form.dataset.msgRequired || "";
      note.classList.remove("ok");
      return;
    }
    const body = [
      d.get("message"), "", "—",
      d.get("name"),
      d.get("organisation") || "",
      d.get("email"),
    ].filter(Boolean).join("\n");
    const href = "mailto:" + (form.dataset.mailto || "alessandro@iside.systems")
      + "?subject=" + encodeURIComponent(d.get("topic") || "")
      + "&body=" + encodeURIComponent(body);
    note.textContent = form.dataset.msgOk || "";
    note.classList.add("ok");
    window.location.href = href;
  });
})();

/* ============================================================
   COOKIE BAR — Consent Mode v2. The default in the page <head>
   is "denied"; this only records a choice and updates it.
   ============================================================ */
(function consent(){
  const bar = document.getElementById("cookiebar");
  if (!bar) return;
  const KEY = "iside-consent";

  const read = () => { try { return localStorage.getItem(KEY); } catch(e){ return null; } };
  const save = v => { try { localStorage.setItem(KEY, v); } catch(e){} };

  function update(state){
    const g = window.gtag || function(){ (window.dataLayer = window.dataLayer || []).push(arguments); };
    g("consent", "update", {
      ad_storage: state, ad_user_data: state, ad_personalization: state, analytics_storage: state
    });
    (window.dataLayer = window.dataLayer || []).push({
      event: state === "granted" ? "cookie_consent_granted" : "cookie_consent_denied"
    });
  }

  if (read()){ return; }                       // already answered, stay quiet

  bar.hidden = false;
  requestAnimationFrame(() => bar.classList.add("in"));

  bar.querySelectorAll("[data-consent]").forEach(b => {
    b.addEventListener("click", () => {
      const state = b.dataset.consent;
      save(state);
      update(state);
      bar.classList.remove("in");
      setTimeout(() => { bar.hidden = true; }, 450);
    });
  });
})();
