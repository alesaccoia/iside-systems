/* ============================================================
   Page shell for AlgoSynth: the guide, and the desktop floor.
   Loaded alongside the sequencer, which it does not touch.
   ============================================================ */
"use strict";

const LANG = document.documentElement.lang === "en" ? "en" : "it";

const T = {
  it: {
    gTitle: "AlgoSynth — sequencer algoritmico",
    gIntro: "Un sequencer in cui i pattern non si disegnano nota per nota: si generano da regole "
      + "e poi si piegano. L'ispirazione è Acroyear degli Autechre — imposti un processo, lo "
      + "ascolti, e intervieni sui parametri mentre suona. Il suono esce dal browser; se hai un "
      + "sintetizzatore collegato, esce anche in MIDI.",
    gHow: "Come si usa",
    steps: [
      ["Premi Play", "Il browser blocca l'audio finché non lo chiedi tu: il primo <b>Play</b> "
        + "sblocca il suono. Da lì cambi <b>BPM</b>, <b>Swing</b> e numero di <b>Step</b> mentre gira."],
      ["Accendi gli step", "Ogni traccia ha la sua griglia: clicca una casella per accenderla o "
        + "spegnerla. <b>Tasto destro</b> su una casella per darle una probabilità (0–1) e una "
        + "condizione: <b>always</b>, <b>1:2</b>, <b>fill</b>… È lì che il pattern smette di "
        + "ripetersi uguale."],
      ["Lascia generare", "Sulle tracce ritmiche, <b>Euclid</b> distribuisce N colpi su M step nel "
        + "modo più uniforme possibile — la base di quasi tutti i ritmi del mondo — e <b>Density</b> "
        + "decide quanto spesso il generatore aggiunge o toglie. Le tracce melodiche pescano da una "
        + "scala: scegli scala, nota radice, estensione e quanto spesso costruire accordi."],
      ["Componi", "Salva lo stato corrente come <b>Pattern</b>, poi accodane altri: in modalità "
        + "<b>Song</b> si susseguono con le ripetizioni che decidi. <b>Queue Next</b> cambia pattern "
        + "al giro successivo, senza interrompere."],
    ],
    gMidi: "MIDI",
    gMidiText: "Con Chrome o Edge su https, i dispositivi collegati compaiono in <b>MIDI Out</b>. "
      + "Le tracce ritmiche escono sul canale 10 (percussioni), le melodiche sul canale che scegli. "
      + "<b>Panic</b> spegne tutte le note se qualcosa resta appeso.",
    gClose: "Ho capito, suona",
    guide: "Guida",
    smallTitle: "Serve uno schermo più grande.",
    smallText: "AlgoSynth affianca la libreria dei pattern alle griglie delle tracce: su uno "
      + "schermo stretto le caselle diventano impossibili da colpire. È pensato per desktop.",
    smallReq: "Larghezza minima 900 px",
    smallBack: "← Torna al sito",
  },
  en: {
    gTitle: "AlgoSynth — algorithmic sequencer",
    gIntro: "A sequencer where patterns are not drawn note by note: they are generated from rules "
      + "and then bent. The inspiration is Autechre's Acroyear — you set a process running, listen, "
      + "and work the parameters while it plays. Sound comes out of the browser; if you have a "
      + "synth attached, it goes out over MIDI as well.",
    gHow: "How to use it",
    steps: [
      ["Press Play", "Browsers hold audio until you ask for it: the first <b>Play</b> unlocks the "
        + "sound. From there change <b>BPM</b>, <b>Swing</b> and the number of <b>Steps</b> while it "
        + "runs."],
      ["Switch steps on", "Each track has its own grid: click a cell to turn it on or off. "
        + "<b>Right-click</b> a cell to give it a probability (0–1) and a condition: <b>always</b>, "
        + "<b>1:2</b>, <b>fill</b>… That is where the pattern stops repeating itself."],
      ["Let it generate", "On rhythmic tracks, <b>Euclid</b> spreads N hits across M steps as "
        + "evenly as possible — the backbone of most rhythms in the world — and <b>Density</b> "
        + "decides how often the generator adds or drops one. Melodic tracks draw from a scale: "
        + "pick the scale, root, range, and how often to build chords."],
      ["Arrange", "Save the current state as a <b>Pattern</b>, then queue more: in <b>Song</b> mode "
        + "they follow one another with the repeats you set. <b>Queue Next</b> switches pattern at "
        + "the next loop, without interrupting."],
    ],
    gMidi: "MIDI",
    gMidiText: "In Chrome or Edge over https, attached devices appear under <b>MIDI Out</b>. "
      + "Rhythmic tracks go out on channel 10 (percussion), melodic ones on the channel you choose. "
      + "<b>Panic</b> silences every note if something hangs.",
    gClose: "Got it, play",
    guide: "Guide",
    smallTitle: "This needs a bigger screen.",
    smallText: "AlgoSynth puts the pattern library beside the track grids: on a narrow screen the "
      + "step cells become impossible to hit. It is built for the desktop.",
    smallReq: "Minimum width 900 px",
    smallBack: "← Back to the site",
  },
}[LANG];

/* four small drawings, in the same hand as the site's figures */
const SVG = [
  // transport: play mark and a tempo ruler
  '<path d="M40 30 l0 24 l20 -12 z" fill="var(--acc)"/>'
  + '<line x1="72" y1="42" x2="120" y2="42" stroke="currentColor" opacity=".45"/>'
  + '<line x1="72" y1="34" x2="72" y2="50" stroke="currentColor" opacity=".7"/>'
  + '<line x1="88" y1="36" x2="88" y2="48" stroke="currentColor" opacity=".45"/>'
  + '<line x1="104" y1="36" x2="104" y2="48" stroke="currentColor" opacity=".45"/>'
  + '<line x1="120" y1="34" x2="120" y2="50" stroke="currentColor" opacity=".7"/>',
  // a step row, some on, one under the playhead
  '<g fill="none" stroke="currentColor" opacity=".5">'
  + '<rect x="20" y="34" width="16" height="16"/><rect x="40" y="34" width="16" height="16"/>'
  + '<rect x="60" y="34" width="16" height="16"/><rect x="80" y="34" width="16" height="16"/>'
  + '<rect x="100" y="34" width="16" height="16"/><rect x="120" y="34" width="16" height="16"/></g>'
  + '<rect x="20" y="34" width="16" height="16" fill="currentColor" opacity=".55"/>'
  + '<rect x="60" y="34" width="16" height="16" fill="currentColor" opacity=".55"/>'
  + '<rect x="100" y="34" width="16" height="16" fill="var(--acc)"/>',
  // euclidean spread around a circle
  '<circle cx="75" cy="42" r="26" fill="none" stroke="currentColor" opacity=".4"/>'
  + '<circle cx="75" cy="16" r="4" fill="var(--acc)"/>'
  + '<circle cx="97" cy="55" r="4" fill="var(--acc)"/>'
  + '<circle cx="53" cy="55" r="4" fill="var(--acc)"/>'
  + '<circle cx="101" cy="30" r="3" fill="currentColor" opacity=".45"/>'
  + '<circle cx="49" cy="30" r="3" fill="currentColor" opacity=".45"/>',
  // patterns chained into a song
  '<rect x="16" y="30" width="30" height="24" fill="none" stroke="currentColor" opacity=".5"/>'
  + '<rect x="56" y="30" width="30" height="24" fill="none" stroke="var(--acc)"/>'
  + '<rect x="96" y="30" width="30" height="24" fill="none" stroke="currentColor" opacity=".5"/>'
  + '<line x1="46" y1="42" x2="56" y2="42" stroke="currentColor" opacity=".5"/>'
  + '<line x1="86" y1="42" x2="96" y2="42" stroke="currentColor" opacity=".5"/>'
  + '<text x="66" y="46" font-size="10" font-family="monospace" fill="var(--acc)">x4</text>',
];

const guide = document.getElementById("guide");
if (guide){
  guide.innerHTML = `<div class="sheet">
      <h2>${T.gTitle}</h2>
      <p class="intro">${T.gIntro}</p>
      <h3>${T.gHow}</h3>
      ${T.steps.map(([t, b], i) => `
        <div class="step-row">
          <svg viewBox="0 0 150 84" xmlns="http://www.w3.org/2000/svg">${SVG[i]}</svg>
          <p><b>${t}.</b> ${b}</p>
        </div>`).join("")}
      <h3>${T.gMidi}</h3>
      <p class="intro">${T.gMidiText}</p>
      <button class="close" id="gclose">${T.gClose}</button>
    </div>`;

  const open = () => { guide.hidden = false; requestAnimationFrame(() => guide.classList.add("in")); };
  const close = () => {
    guide.classList.remove("in");
    setTimeout(() => { guide.hidden = true; }, 350);
    try { localStorage.setItem("algosynth-seen-guide", "1"); } catch (e) {}
  };
  guide.addEventListener("click", e => { if (e.target === guide) close(); });
  document.getElementById("gclose").addEventListener("click", close);
  const btn = document.getElementById("guideBtn");
  if (btn) btn.addEventListener("click", open);
  addEventListener("keydown", e => { if (e.key === "Escape" && !guide.hidden) close(); });
  try {
    if (!localStorage.getItem("algosynth-seen-guide") && innerWidth > 900) open();
  } catch (e) {}
}

const small = document.querySelector(".asmall .in");
if (small){
  small.innerHTML = `<h2>${T.smallTitle}</h2><p>${T.smallText}</p>`
    + `<p class="req">${T.smallReq}</p>`
    + `<a class="back" href="${LANG === "en" ? "/en" : "/"}">${T.smallBack}</a>`;
}
