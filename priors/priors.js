/* ============================================================
   PRIORS — build and query small Bayesian networks in the browser.

   A plain-JavaScript rewrite of github.com/alesaccoia/priors: same model,
   same exact-inference-by-enumeration, no framework and no build step, so
   it drops into a static site as one page.

   Model
     node   { id, name, pos:{x,y}, states:[string], parents:[id], cpt }
     cpt    { "parentId:state|parentId:state": { state: probability } }
            root nodes use the single key "root"
     evidence { nodeId: state }
   ============================================================ */
"use strict";

const LANG = document.documentElement.lang === "en" ? "en" : "it";

const T = {
  it: {
    select: "Seleziona", node: "Nodo", connect: "Collega", comment: "Nota",
    examples: "Esempi", reset: "Svuota", exportF: "Esporta", importF: "Importa",
    nodeName: "Nome del nodo", states: "Stati", addState: "Aggiungi stato",
    cpt: "Probabilità condizionate", given: "Dati i genitori", del: "Elimina nodo",
    emptyPanel: "Nessun nodo selezionato. Clicca un nodo per modificarne stati e probabilità, "
      + "oppure clicca uno stato dentro un nodo per fissarlo come evidenza.",
    hintRoot: "Nodo senza genitori: una sola riga di probabilità a priori.",
    hintCpt: "Una riga per ogni combinazione degli stati dei genitori. Le righe vengono "
      + "normalizzate a 1 quando esci dal campo.",
    connectHint: "Clicca il nodo di partenza, poi quello di arrivo.",
    cycle: "Quel collegamento creerebbe un ciclo: una rete bayesiana deve restare aciclica.",
    exists: "Quel collegamento esiste già.",
    tooBig: "Rete troppo grande per l'inferenza esatta in tempo reale (oltre 200.000 combinazioni).",
    impossible: "Evidenza impossibile: nessuno scenario compatibile con queste osservazioni.",
    newNode: "Nuovo nodo", state: "Stato",
    cleared: "Evidenza rimossa.", loaded: "Rete caricata.", saved: "Rete esportata.",
    badFile: "File non valido.",
    obs: "osservato", removeEdge: "Scollega dai genitori",
    guide: "Guida",
    gTitle: "Priors — reti bayesiane",
    gIntro: "Una rete bayesiana descrive come le cause influenzano gli effetti in termini di "
      + "probabilità. Quando osservi qualcosa — un test positivo, un parere, un allarme — Priors "
      + "ricalcola all'istante quanto diventano probabili tutte le altre cose, anche a monte. "
      + "È il calcolo che quasi nessuno fa a mente correttamente.",
    gHow: "Come si usa",
    gSteps: [
      ["Crea un nodo", "Clicca <b>Nodo</b> e poi il punto della tela. Ogni nodo è una variabile con "
        + "i suoi stati — presente/assente, buono/medio/scarso. Trascinalo dove vuoi."],
      ["Collega le cause", "Clicca <b>Collega</b>, poi prima il nodo causa e poi quello effetto. "
        + "La freccia va dalla causa all'effetto. I cicli vengono rifiutati."],
      ["Metti i numeri", "Seleziona un nodo: nel pannello a destra compaiono gli stati e la tabella "
        + "delle probabilità, una riga per ogni combinazione degli stati dei genitori. Le righe si "
        + "normalizzano a 1 da sole."],
      ["Osserva e leggi", "Clicca uno stato dentro un nodo per fissarlo come <b>evidenza</b>: "
        + "diventa rosso e tutte le altre probabilità si aggiornano. Ricliccalo per toglierlo."],
    ],
    gTry: "Da dove partire",
    gTryText: "Apri un esempio dal menu in alto. Nel test diagnostico, fissa l'esito su «Positivo» "
      + "e guarda la probabilità di malattia: sale dal 20% al 43%, non al 90% come suggerisce "
      + "l'intuito. È l'errore di ragionamento più comune che esista.",
    gClose: "Ho capito, inizia",
    smallTitle: "Serve uno schermo più grande.",
    smallText: "Priors mette la tela e il pannello delle probabilità uno accanto all'altro: "
      + "impilarli su uno schermo stretto renderebbe lo strumento inutilizzabile. È pensato per "
      + "desktop.",
    smallReq: "Larghezza minima 900 px",
    smallBack: "← Torna al sito",
  },
  en: {
    select: "Select", node: "Node", connect: "Connect", comment: "Note",
    examples: "Examples", reset: "Clear", exportF: "Export", importF: "Import",
    nodeName: "Node name", states: "States", addState: "Add state",
    cpt: "Conditional probabilities", given: "Given the parents", del: "Delete node",
    emptyPanel: "No node selected. Click a node to edit its states and probabilities, or click a "
      + "state inside a node to set it as evidence.",
    hintRoot: "A node with no parents: a single row of prior probabilities.",
    hintCpt: "One row per combination of parent states. Rows are normalised to 1 when you leave "
      + "the field.",
    connectHint: "Click the parent node, then the child.",
    cycle: "That link would create a cycle: a Bayesian network has to stay acyclic.",
    exists: "That link already exists.",
    tooBig: "Network too large for real-time exact inference (over 200,000 combinations).",
    impossible: "Impossible evidence: no scenario is consistent with these observations.",
    newNode: "New node", state: "State",
    cleared: "Evidence cleared.", loaded: "Network loaded.", saved: "Network exported.",
    badFile: "Not a valid file.",
    obs: "observed", removeEdge: "Detach from parents",
    guide: "Guide",
    gTitle: "Priors — Bayesian networks",
    gIntro: "A Bayesian network describes how causes bear on effects in terms of probability. "
      + "When you observe something — a positive test, an opinion, an alarm — Priors immediately "
      + "recomputes how likely everything else becomes, including upstream. It is the calculation "
      + "almost nobody performs correctly in their head.",
    gHow: "How to use it",
    gSteps: [
      ["Create a node", "Click <b>Node</b>, then a point on the canvas. Each node is a variable "
        + "with its states — present/absent, good/moderate/poor. Drag it wherever you like."],
      ["Connect the causes", "Click <b>Connect</b>, then the cause node and then the effect. The "
        + "arrow runs from cause to effect. Cycles are refused."],
      ["Enter the numbers", "Select a node: the panel on the right shows its states and the "
        + "probability table, one row per combination of parent states. Rows normalise to 1 on "
        + "their own."],
      ["Observe and read", "Click a state inside a node to set it as <b>evidence</b>: it turns red "
        + "and every other probability updates. Click it again to release it."],
    ],
    gTry: "Where to start",
    gTryText: "Open an example from the menu above. In the diagnostic test, set the result to "
      + "«Positive» and watch the probability of disease: it rises from 20% to 43%, not to 90% as "
      + "intuition suggests. It is the most common reasoning error there is.",
    gClose: "Got it, start",
    smallTitle: "This needs a bigger screen.",
    smallText: "Priors puts the canvas and the probability panel side by side: stacking them on a "
      + "narrow screen would make the tool unusable. It is built for the desktop.",
    smallReq: "Minimum width 900 px",
    smallBack: "← Back to the site",
  },
}[LANG];

/* ---------------------------------------------------------------- examples */
const EXAMPLES = {
  it: {
    "Investimento": {
      nodes: [
        { id: "success", name: "Successo dell'impresa", pos: { x: 520, y: 90 },
          states: ["Successo", "Fallimento"], parents: [],
          cpt: { root: { "Successo": 0.2, "Fallimento": 0.8 } } },
        { id: "forecast", name: "Parere dell'esperto", pos: { x: 520, y: 330 },
          states: ["Buono", "Medio", "Scarso"], parents: ["success"],
          cpt: {
            "success:Successo": { "Buono": 0.4, "Medio": 0.4, "Scarso": 0.2 },
            "success:Fallimento": { "Buono": 0.1, "Medio": 0.3, "Scarso": 0.6 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 90 }, text:
        "Un investitore valuta una start-up. Solo il 20% delle start-up ha successo.\n\n"
        + "L'esperto consultato non è infallibile: fra quelle che avranno successo ne giudica "
        + "buone il 40%, medie il 40%, scarse il 20%. Fra quelle che falliranno, buone il 10%, "
        + "medie il 30%, scarse il 60%.\n\n"
        + "Domanda: se l'esperto dice «buono», qual è la probabilità di successo?\n"
        + "Fissa «Parere dell'esperto» su Buono e guarda il nodo sopra." }],
    },
    "Test diagnostico": {
      nodes: [
        { id: "disease", name: "Malattia", pos: { x: 470, y: 90 },
          states: ["Presente", "Assente"], parents: [],
          cpt: { root: { "Presente": 0.2, "Assente": 0.8 } } },
        { id: "test", name: "Esito del test", pos: { x: 470, y: 330 },
          states: ["Positivo", "Negativo"], parents: ["disease"],
          cpt: {
            "disease:Presente": { "Positivo": 0.9, "Negativo": 0.1 },
            "disease:Assente": { "Positivo": 0.3, "Negativo": 0.7 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 90 }, text:
        "Il 20% della popolazione esaminata ha la malattia.\n\n"
        + "Il test è positivo nel 90% dei malati, ma anche nel 30% dei sani.\n\n"
        + "Uno studente risulta positivo: qual è la probabilità che sia malato?\n"
        + "Fissa «Esito del test» su Positivo. La risposta sorprende quasi tutti." }],
    },
    "Allarme": {
      nodes: [
        { id: "burglary", name: "Furto", pos: { x: 330, y: 80 },
          states: ["Sì", "No"], parents: [], cpt: { root: { "Sì": 0.01, "No": 0.99 } } },
        { id: "quake", name: "Terremoto", pos: { x: 700, y: 80 },
          states: ["Sì", "No"], parents: [], cpt: { root: { "Sì": 0.02, "No": 0.98 } } },
        { id: "alarm", name: "Allarme", pos: { x: 515, y: 300 },
          states: ["Suona", "Muto"], parents: ["burglary", "quake"],
          cpt: {
            "burglary:Sì|quake:Sì": { "Suona": 0.95, "Muto": 0.05 },
            "burglary:Sì|quake:No": { "Suona": 0.94, "Muto": 0.06 },
            "burglary:No|quake:Sì": { "Suona": 0.29, "Muto": 0.71 },
            "burglary:No|quake:No": { "Suona": 0.001, "Muto": 0.999 },
          } },
        { id: "call", name: "Chiamata del vicino", pos: { x: 515, y: 540 },
          states: ["Sì", "No"], parents: ["alarm"],
          cpt: {
            "alarm:Suona": { "Sì": 0.9, "No": 0.1 },
            "alarm:Muto": { "Sì": 0.05, "No": 0.95 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 300 }, text:
        "L'esempio classico di Judea Pearl.\n\n"
        + "Il vicino chiama: probabilmente è un furto. Ma se poi scopri che c'è stato un "
        + "terremoto, la probabilità di furto crolla — il terremoto «spiega via» l'allarme.\n\n"
        + "Prova: fissa la chiamata su Sì, guarda Furto. Poi fissa anche Terremoto su Sì." }],
    },
  },
  en: {
    "Venture": {
      nodes: [
        { id: "success", name: "Venture success", pos: { x: 520, y: 90 },
          states: ["Success", "Failure"], parents: [],
          cpt: { root: { "Success": 0.2, "Failure": 0.8 } } },
        { id: "forecast", name: "Expert forecast", pos: { x: 520, y: 330 },
          states: ["Good", "Moderate", "Poor"], parents: ["success"],
          cpt: {
            "success:Success": { "Good": 0.4, "Moderate": 0.4, "Poor": 0.2 },
            "success:Failure": { "Good": 0.1, "Moderate": 0.3, "Poor": 0.6 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 90 }, text:
        "An investor is weighing a start-up. Only 20% of start-ups succeed.\n\n"
        + "The expert is not infallible: of those that will succeed he calls 40% good, 40% "
        + "moderate, 20% poor. Of those that will fail: 10% good, 30% moderate, 60% poor.\n\n"
        + "If the expert says «good», what is the probability of success?\n"
        + "Set «Expert forecast» to Good and watch the node above." }],
    },
    "Diagnostic test": {
      nodes: [
        { id: "disease", name: "Disease", pos: { x: 470, y: 90 },
          states: ["Present", "Absent"], parents: [],
          cpt: { root: { "Present": 0.2, "Absent": 0.8 } } },
        { id: "test", name: "Test result", pos: { x: 470, y: 330 },
          states: ["Positive", "Negative"], parents: ["disease"],
          cpt: {
            "disease:Present": { "Positive": 0.9, "Negative": 0.1 },
            "disease:Absent": { "Positive": 0.3, "Negative": 0.7 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 90 }, text:
        "20% of the screened population has the disease.\n\n"
        + "The test is positive in 90% of the sick — and in 30% of the healthy.\n\n"
        + "A student tests positive: how likely is it that they are ill?\n"
        + "Set «Test result» to Positive. The answer surprises most people." }],
    },
    "Alarm": {
      nodes: [
        { id: "burglary", name: "Burglary", pos: { x: 330, y: 80 },
          states: ["Yes", "No"], parents: [], cpt: { root: { "Yes": 0.01, "No": 0.99 } } },
        { id: "quake", name: "Earthquake", pos: { x: 700, y: 80 },
          states: ["Yes", "No"], parents: [], cpt: { root: { "Yes": 0.02, "No": 0.98 } } },
        { id: "alarm", name: "Alarm", pos: { x: 515, y: 300 },
          states: ["Ringing", "Silent"], parents: ["burglary", "quake"],
          cpt: {
            "burglary:Yes|quake:Yes": { "Ringing": 0.95, "Silent": 0.05 },
            "burglary:Yes|quake:No": { "Ringing": 0.94, "Silent": 0.06 },
            "burglary:No|quake:Yes": { "Ringing": 0.29, "Silent": 0.71 },
            "burglary:No|quake:No": { "Ringing": 0.001, "Silent": 0.999 },
          } },
        { id: "call", name: "Neighbour calls", pos: { x: 515, y: 540 },
          states: ["Yes", "No"], parents: ["alarm"],
          cpt: {
            "alarm:Ringing": { "Yes": 0.9, "No": 0.1 },
            "alarm:Silent": { "Yes": 0.05, "No": 0.95 },
          } },
      ],
      comments: [{ id: "c1", pos: { x: 60, y: 300 }, text:
        "Judea Pearl's classic.\n\n"
        + "The neighbour calls: probably a burglary. But learn that there was an earthquake and "
        + "the probability of burglary collapses — the quake explains the alarm away.\n\n"
        + "Try it: set the call to Yes and watch Burglary. Then set Earthquake to Yes too." }],
    },
  },
}[LANG];

/* ---------------------------------------------------------------- state */
const KEY = "priors-network-" + LANG;
let net = null;          // { nodes, comments }
let evidence = {};
let selected = null;     // node id or comment id
let mode = "select";
let connectFrom = null;

const $ = sel => document.querySelector(sel);
const world = $("#world");
const svg = $("#wires");
const panel = $("#panel");
const notice = $("#notice");

const uid = () => "n" + Math.random().toString(36).slice(2, 8);

function say(text){
  notice.textContent = text;
  notice.classList.add("in");
  clearTimeout(say._t);
  say._t = setTimeout(() => notice.classList.remove("in"), 3200);
}

/* ---------------------------------------------------------------- model */
function cptKey(node, assignment){
  if (!node.parents.length) return "root";
  return node.parents.map(pid => `${pid}:${assignment[pid]}`).join("|");
}

function parentCombos(node){
  const parents = node.parents.map(id => net.nodes.find(n => n.id === id)).filter(Boolean);
  if (!parents.length) return [{ key: "root", label: [] }];
  const out = [];
  (function walk(i, parts, labels){
    if (i === parents.length){ out.push({ key: parts.join("|"), label: labels.slice() }); return; }
    parents[i].states.forEach(s => {
      walk(i + 1, parts.concat(`${parents[i].id}:${s}`), labels.concat(`${parents[i].name}: ${s}`));
    });
  })(0, [], []);
  return out;
}

function normaliseCPT(node){
  const fresh = {};
  parentCombos(node).forEach(({ key }) => {
    const row = node.cpt[key] || {};
    const dist = {};
    let sum = 0;
    node.states.forEach(s => { const v = Number(row[s]); dist[s] = isFinite(v) && v >= 0 ? v : 0; sum += dist[s]; });
    if (sum <= 0) node.states.forEach(s => { dist[s] = 1 / node.states.length; });
    else node.states.forEach(s => { dist[s] = dist[s] / sum; });
    fresh[key] = dist;
  });
  node.cpt = fresh;
}

function wouldCycle(fromId, toId){
  // walking down from the child must never reach the parent
  const seen = new Set();
  const stack = [toId];
  while (stack.length){
    const id = stack.pop();
    if (id === fromId) return true;
    if (seen.has(id)) continue;
    seen.add(id);
    net.nodes.filter(n => n.parents.includes(id)).forEach(n => stack.push(n.id));
  }
  return false;
}

/* ---------------------------------------------------------------- inference */
function infer(){
  const nodes = net.nodes;
  const result = {};
  nodes.forEach(n => { result[n.id] = {}; n.states.forEach(s => result[n.id][s] = 0); });
  if (!nodes.length) return { result, ok: true };

  const worlds = nodes.reduce((acc, n) => acc * n.states.length, 1);
  if (worlds > 200000) return { result, ok: false, reason: "big" };

  const assignment = {};
  let mass = 0;

  (function walk(i){
    if (i === nodes.length){
      for (const [id, state] of Object.entries(evidence)){
        if (state && assignment[id] !== state) return;
      }
      let p = 1;
      for (const n of nodes){
        const row = n.cpt[cptKey(n, assignment)];
        const q = row ? row[assignment[n.id]] : 1 / n.states.length;
        p *= (typeof q === "number" ? q : 0);
        if (p === 0) break;
      }
      if (p > 0){
        mass += p;
        for (const n of nodes) result[n.id][assignment[n.id]] += p;
      }
      return;
    }
    const n = nodes[i];
    for (const s of n.states){ assignment[n.id] = s; walk(i + 1); }
  })(0);

  if (mass <= 0) return { result, ok: false, reason: "impossible" };
  nodes.forEach(n => n.states.forEach(s => { result[n.id][s] /= mass; }));
  return { result, ok: true };
}

/* ---------------------------------------------------------------- render */
function render(){
  const { result, ok, reason } = infer();
  if (!ok && reason === "big") say(T.tooBig);
  if (!ok && reason === "impossible") say(T.impossible);

  world.querySelectorAll(".pnode,.pcomment").forEach(el => el.remove());

  net.nodes.forEach(n => {
    const el = document.createElement("div");
    el.className = "pnode" + (selected === n.id ? " sel" : "") + (evidence[n.id] ? " hasev" : "");
    el.style.left = n.pos.x + "px";
    el.style.top = n.pos.y + "px";
    el.dataset.id = n.id;

    const head = document.createElement("h4");
    head.textContent = n.name;
    if (evidence[n.id]){
      const tag = document.createElement("em");
      tag.textContent = T.obs;
      head.appendChild(tag);
    }
    el.appendChild(head);

    n.states.forEach(s => {
      const p = ok ? (result[n.id][s] || 0) : 0;
      const row = document.createElement("div");
      row.className = "pstate" + (evidence[n.id] === s ? " obs" : "");
      row.dataset.state = s;
      row.innerHTML = '<span class="bar"></span>'
        + `<span class="lab">${escapeHtml(s)}</span>`
        + `<span class="val">${(p * 100).toFixed(1)}%</span>`;
      row.querySelector(".bar").style.width = Math.max(0, Math.min(100, p * 100)) + "%";
      el.appendChild(row);
    });
    world.appendChild(el);
  });

  net.comments.forEach(c => {
    const el = document.createElement("div");
    el.className = "pcomment" + (selected === c.id ? " sel" : "");
    el.style.left = c.pos.x + "px";
    el.style.top = c.pos.y + "px";
    el.dataset.id = c.id;
    el.dataset.comment = "1";
    el.textContent = c.text;
    world.appendChild(el);
  });

  drawEdges();
  renderPanel();
  save();
}

function escapeHtml(v){
  return String(v).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function nodeBox(id){
  const el = world.querySelector(`.pnode[data-id="${id}"]`);
  if (!el) return null;
  return { x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight };
}

function drawEdges(){
  svg.innerHTML = "";
  net.nodes.forEach(child => {
    child.parents.forEach(pid => {
      const a = nodeBox(pid), b = nodeBox(child.id);
      if (!a || !b) return;
      const x1 = a.x + a.w / 2, y1 = a.y + a.h;
      const x2 = b.x + b.w / 2, y2 = b.y;
      const my = (y1 + y2) / 2;
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("class", "pedge");
      path.setAttribute("d", `M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2 - 8}`);
      svg.appendChild(path);
      const head = document.createElementNS("http://www.w3.org/2000/svg", "path");
      head.setAttribute("class", "pedge-head");
      head.setAttribute("d", `M${x2},${y2} l-4,-8 l8,0 z`);
      svg.appendChild(head);
    });
  });
}

/* ---------------------------------------------------------------- panel */
function renderPanel(){
  const node = net.nodes.find(n => n.id === selected);
  if (!node){
    panel.innerHTML = `<h3>${T.cpt}</h3><p class="empty">${T.emptyPanel}</p>`;
    return;
  }

  const combos = parentCombos(node);
  const rows = combos.map(({ key, label }) => {
    const cells = node.states.map(s =>
      `<td><input type="number" step="0.01" min="0" max="1" data-key="${escapeHtml(key)}" `
      + `data-state="${escapeHtml(s)}" value="${(node.cpt[key]?.[s] ?? 0).toFixed(3)}"></td>`).join("");
    const cond = label.length ? `<td class="cond">${escapeHtml(label.join(" · "))}</td>` : "";
    return `<tr>${cond}${cells}</tr>`;
  }).join("");

  panel.innerHTML = `
    <h3>${T.nodeName}</h3>
    <div class="pfield"><input type="text" id="pname" value="${escapeHtml(node.name)}"></div>

    <h3>${T.states}</h3>
    <ul class="pstates" id="pstates">
      ${node.states.map((s, i) => `<li><input type="text" data-i="${i}" value="${escapeHtml(s)}">`
        + `<button class="x" data-del="${i}"${node.states.length < 3 ? " disabled" : ""}>×</button></li>`).join("")}
    </ul>
    <div class="prow"><button class="pb" id="paddstate">${T.addState}</button></div>

    <h3 style="margin-top:22px">${T.cpt}</h3>
    <table class="pcpt">
      <thead><tr>${node.parents.length ? `<th>${T.given}</th>` : ""}
        ${node.states.map(s => `<th>${escapeHtml(s)}</th>`).join("")}</tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <p class="phint">${node.parents.length ? T.hintCpt : T.hintRoot}</p>

    <div class="prow">
      ${node.parents.length ? `<button class="pb" id="pdetach">${T.removeEdge}</button>` : ""}
      <button class="pb danger" id="pdel">${T.del}</button>
    </div>`;

  $("#pname").addEventListener("input", e => { node.name = e.target.value; drawSoon(); });
  panel.querySelectorAll("#pstates input").forEach(inp => {
    inp.addEventListener("change", e => {
      const i = +e.target.dataset.i;
      const old = node.states[i];
      const val = e.target.value.trim() || `${T.state} ${i + 1}`;
      node.states[i] = val;
      Object.values(node.cpt).forEach(row => {
        if (old in row){ row[val] = row[old]; if (val !== old) delete row[old]; }
      });
      // children reference this node's states inside their CPT keys
      net.nodes.filter(c => c.parents.includes(node.id)).forEach(c => normaliseCPT(c));
      if (evidence[node.id] === old) evidence[node.id] = val;
      render();
    });
  });
  panel.querySelectorAll("[data-del]").forEach(b => b.addEventListener("click", () => {
    const i = +b.dataset.del;
    if (node.states.length < 3) return;
    const gone = node.states.splice(i, 1)[0];
    Object.values(node.cpt).forEach(row => delete row[gone]);
    normaliseCPT(node);
    net.nodes.filter(c => c.parents.includes(node.id)).forEach(c => normaliseCPT(c));
    if (evidence[node.id] === gone) delete evidence[node.id];
    render();
  }));
  $("#paddstate").addEventListener("click", () => {
    node.states.push(`${T.state} ${node.states.length + 1}`);
    normaliseCPT(node);
    net.nodes.filter(c => c.parents.includes(node.id)).forEach(c => normaliseCPT(c));
    render();
  });
  panel.querySelectorAll(".pcpt input").forEach(inp => {
    inp.addEventListener("change", e => {
      const { key, state } = e.target.dataset;
      node.cpt[key] = node.cpt[key] || {};
      node.cpt[key][state] = Math.max(0, Number(e.target.value) || 0);
      normaliseCPT(node);
      render();
    });
  });
  const detach = $("#pdetach");
  if (detach) detach.addEventListener("click", () => {
    node.parents = [];
    normaliseCPT(node);
    render();
  });
  $("#pdel").addEventListener("click", () => {
    net.nodes = net.nodes.filter(n => n.id !== node.id);
    net.nodes.forEach(n => {
      if (n.parents.includes(node.id)){
        n.parents = n.parents.filter(p => p !== node.id);
        normaliseCPT(n);
      }
    });
    delete evidence[node.id];
    selected = null;
    render();
  });
}

let drawTimer = null;
function drawSoon(){
  clearTimeout(drawTimer);
  drawTimer = setTimeout(render, 250);
}

/* ---------------------------------------------------------------- interaction */
world.addEventListener("pointerdown", e => {
  const card = e.target.closest(".pnode, .pcomment");

  if (mode === "node" && !card){
    const r = world.getBoundingClientRect();
    addNode(e.clientX - r.left - 105, e.clientY - r.top - 20);
    setMode("select");
    return;
  }
  if (mode === "comment" && !card){
    const r = world.getBoundingClientRect();
    net.comments.push({ id: uid(), pos: { x: e.clientX - r.left, y: e.clientY - r.top },
                        text: LANG === "it" ? "Nota…" : "Note…" });
    setMode("select");
    render();
    return;
  }
  if (!card){ selected = null; render(); return; }

  const id = card.dataset.id;

  if (mode === "connect" && !card.dataset.comment){
    if (!connectFrom){ connectFrom = id; selected = id; render(); say(T.connectHint); return; }
    if (connectFrom === id){ connectFrom = null; return; }
    const child = net.nodes.find(n => n.id === id);
    if (child.parents.includes(connectFrom)){ say(T.exists); }
    else if (wouldCycle(connectFrom, id)){ say(T.cycle); }
    else { child.parents.push(connectFrom); normaliseCPT(child); }
    connectFrom = null;
    setMode("select");
    render();
    return;
  }

  selected = id;

  // clicking a state toggles evidence
  const stateRow = e.target.closest(".pstate");
  if (stateRow && !card.dataset.comment){
    const s = stateRow.dataset.state;
    if (evidence[id] === s) { delete evidence[id]; say(T.cleared); }
    else evidence[id] = s;
    render();
    return;
  }

  // otherwise drag
  const item = card.dataset.comment
    ? net.comments.find(c => c.id === id)
    : net.nodes.find(n => n.id === id);
  const startX = e.clientX, startY = e.clientY;
  const origin = { x: item.pos.x, y: item.pos.y };
  card.classList.add("dragging");
  card.setPointerCapture(e.pointerId);

  const move = ev => {
    item.pos.x = Math.max(0, origin.x + (ev.clientX - startX));
    item.pos.y = Math.max(0, origin.y + (ev.clientY - startY));
    card.style.left = item.pos.x + "px";
    card.style.top = item.pos.y + "px";
    drawEdges();
  };
  const up = () => {
    card.classList.remove("dragging");
    card.removeEventListener("pointermove", move);
    card.removeEventListener("pointerup", up);
    render();
  };
  card.addEventListener("pointermove", move);
  card.addEventListener("pointerup", up);
  render();
});

world.addEventListener("dblclick", e => {
  const c = e.target.closest(".pcomment");
  if (!c) return;
  const item = net.comments.find(x => x.id === c.dataset.id);
  const text = prompt(LANG === "it" ? "Testo della nota" : "Note text", item.text);
  if (text !== null){ item.text = text; render(); }
});

function addNode(x, y){
  const n = { id: uid(), name: T.newNode, pos: { x: Math.max(0, x), y: Math.max(0, y) },
              states: [`${T.state} 1`, `${T.state} 2`], parents: [], cpt: {} };
  normaliseCPT(n);
  net.nodes.push(n);
  selected = n.id;
  render();
}

function setMode(m){
  mode = m;
  connectFrom = null;
  document.querySelectorAll("[data-mode]").forEach(b =>
    b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
  if (m === "connect") say(T.connectHint);
}

/* ---------------------------------------------------------------- storage */
function save(){
  try { localStorage.setItem(KEY, JSON.stringify({ net, evidence })); } catch (e) {}
}
function load(){
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (!data || !data.net || !Array.isArray(data.net.nodes)) return false;
    net = data.net;
    net.comments = net.comments || [];
    evidence = data.evidence || {};
    return true;
  } catch (e) { return false; }
}

function loadExample(name){
  const src = EXAMPLES[name];
  net = JSON.parse(JSON.stringify(src));
  net.comments = net.comments || [];
  evidence = {};
  selected = null;
  render();
}

/* ---------------------------------------------------------------- toolbar */
document.querySelectorAll("[data-mode]").forEach(b =>
  b.addEventListener("click", () => setMode(b.dataset.mode)));

$("#pexamples").innerHTML = Object.keys(EXAMPLES)
  .map(k => `<option value="${escapeHtml(k)}">${escapeHtml(k)}</option>`).join("");
$("#pexamples").addEventListener("change", e => { if (e.target.value) loadExample(e.target.value); });

$("#preset").addEventListener("click", () => {
  net = { nodes: [], comments: [] };
  evidence = {};
  selected = null;
  render();
});

$("#pclearev").addEventListener("click", () => { evidence = {}; say(T.cleared); render(); });

$("#pexport").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify({ net, evidence }, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "priors-network.json";
  a.click();
  URL.revokeObjectURL(a.href);
  say(T.saved);
});

$("#pimport").addEventListener("click", () => $("#pfile").click());
$("#pfile").addEventListener("change", e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      const candidate = data.net || data;
      if (!candidate || !Array.isArray(candidate.nodes)) throw new Error("shape");
      net = candidate;
      net.comments = net.comments || [];
      evidence = data.evidence || {};
      selected = null;
      render();
      say(T.loaded);
    } catch (err) { say(T.badFile); }
  };
  reader.readAsText(file);
  e.target.value = "";
});

/* ---------------------------------------------------------------- start */
if (!load()) loadExample(Object.keys(EXAMPLES)[0]);
else render();
setMode("select");

/* ---------------------------------------------------------------- guide */
const GUIDE_SVG = [
  // 1. a node card with its states
  '<rect x="34" y="14" width="82" height="56" fill="none" stroke="currentColor" opacity=".55"/>'
  + '<line x1="34" y1="30" x2="116" y2="30" stroke="currentColor" opacity=".55"/>'
  + '<rect x="40" y="38" width="46" height="6" fill="currentColor" opacity=".35"/>'
  + '<rect x="40" y="52" width="26" height="6" fill="currentColor" opacity=".35"/>',
  // 2. two nodes and the arrow between them
  '<rect x="46" y="8" width="58" height="24" fill="none" stroke="currentColor" opacity=".55"/>'
  + '<rect x="46" y="52" width="58" height="24" fill="none" stroke="currentColor" opacity=".55"/>'
  + '<line x1="75" y1="32" x2="75" y2="46" stroke="var(--acc)"/>'
  + '<path d="M75 52 l-4 -7 l8 0 z" fill="var(--acc)"/>',
  // 3. the probability table
  '<rect x="24" y="16" width="102" height="52" fill="none" stroke="currentColor" opacity=".45"/>'
  + '<line x1="24" y1="30" x2="126" y2="30" stroke="currentColor" opacity=".45"/>'
  + '<line x1="66" y1="16" x2="66" y2="68" stroke="currentColor" opacity=".45"/>'
  + '<line x1="96" y1="16" x2="96" y2="68" stroke="currentColor" opacity=".45"/>'
  + '<text x="75" y="45" font-size="9" fill="var(--acc)" font-family="monospace">0.9</text>'
  + '<text x="105" y="45" font-size="9" fill="currentColor" opacity=".6" font-family="monospace">0.1</text>'
  + '<text x="75" y="61" font-size="9" fill="currentColor" opacity=".6" font-family="monospace">0.3</text>'
  + '<text x="105" y="61" font-size="9" fill="currentColor" opacity=".6" font-family="monospace">0.7</text>',
  // 4. evidence set on one state
  '<rect x="34" y="14" width="82" height="56" fill="none" stroke="var(--acc)"/>'
  + '<line x1="34" y1="30" x2="116" y2="30" stroke="var(--acc)" opacity=".6"/>'
  + '<rect x="34" y="36" width="82" height="12" fill="var(--acc)" opacity=".3"/>'
  + '<rect x="40" y="56" width="18" height="6" fill="currentColor" opacity=".3"/>'
  + '<path d="M92 44 l0 12 l4 -3 l3 6 l3 -1 l-3 -6 l5 -1 z" fill="var(--acc)"/>',
];

function buildGuide(){
  const box = document.getElementById("guide");
  if (!box) return;
  const steps = T.gSteps.map(([title, body], i) => `
    <div class="step">
      <svg viewBox="0 0 150 84" xmlns="http://www.w3.org/2000/svg">${GUIDE_SVG[i]}</svg>
      <p><b>${title}.</b> ${body}</p>
    </div>`).join("");
  box.innerHTML = `<div class="sheet">
      <h2>${T.gTitle}</h2>
      <p class="intro">${T.gIntro}</p>
      <h3>${T.gHow}</h3>
      ${steps}
      <h3>${T.gTry}</h3>
      <p class="intro">${T.gTryText}</p>
      <button class="close" id="gclose">${T.gClose}</button>
    </div>`;
  box.addEventListener("click", e => { if (e.target === box) closeGuide(); });
  document.getElementById("gclose").addEventListener("click", closeGuide);
}

function openGuide(){
  const box = document.getElementById("guide");
  box.hidden = false;
  requestAnimationFrame(() => box.classList.add("in"));
}
function closeGuide(){
  const box = document.getElementById("guide");
  box.classList.remove("in");
  setTimeout(() => { box.hidden = true; }, 350);
  try { localStorage.setItem("priors-seen-guide", "1"); } catch (e) {}
}

function buildSmall(){
  const box = document.querySelector(".psmall .in");
  if (!box) return;
  box.innerHTML = `<h2>${T.smallTitle}</h2><p>${T.smallText}</p>`
    + `<p class="req">${T.smallReq}</p>`
    + `<a class="back" href="${LANG === "en" ? "/en" : "/"}">${T.smallBack}</a>`;
}

buildGuide();
buildSmall();
const guideBtn = document.getElementById("pguide");
if (guideBtn) guideBtn.addEventListener("click", openGuide);
addEventListener("keydown", e => { if (e.key === "Escape") closeGuide(); });
try {
  if (!localStorage.getItem("priors-seen-guide") && innerWidth > 900) openGuide();
} catch (e) {}
