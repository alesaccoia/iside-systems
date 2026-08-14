class GranularMorpher {
  constructor() {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    this.context = new AudioCtx();
    this.output = this.context.createGain();
    this.output.gain.value = 0.6;
    this.output.connect(this.context.destination);

    this.buffers = { A: null, B: null };
    this.params = {
      morph: 0.5,
      grainMs: 60,
      density: 30, // grains per second
      jitterMs: 50,
      pitchSt: 0,
      spreadSt: 2,
      scanSpeedNormPerSec: 0.1,
      freeze: false,
      volume: 0.6,
    };
    this.state = {
      positionNorm: 0,
      running: false,
      schedulerTimer: null,
      lookaheadMs: 30,
      scheduleAheadMs: 200,
      lastScheduleTime: 0,
    };
  }

  setParam(key, value) {
    this.params[key] = value;
    if (key === "volume") {
      this.output.gain.setTargetAtTime(value, this.context.currentTime, 0.02);
    }
  }

  async loadFileTo(slot, file) {
    const arrayBuf = await file.arrayBuffer();
    const audioBuf = await this.context.decodeAudioData(arrayBuf);
    this.buffers[slot] = audioBuf;
    return audioBuf;
  }

  resume() {
    if (this.context.state === "suspended") return this.context.resume();
  }

  start() {
    if (this.state.running) return;
    this.state.running = true;
    this.state.lastScheduleTime = this.context.currentTime;
    this._tick();
  }

  pause() {
    this.state.running = false;
    if (this.state.schedulerTimer) {
      clearTimeout(this.state.schedulerTimer);
      this.state.schedulerTimer = null;
    }
  }

  stop() {
    this.pause();
    this.state.positionNorm = 0;
  }

  _tick() {
    if (!this.state.running) return;
    const now = this.context.currentTime;
    const ahead = this.state.scheduleAheadMs / 1000;
    while (this.state.lastScheduleTime < now + ahead) {
      this._scheduleGrainAt(this.state.lastScheduleTime);
      const interval = 1 / Math.max(1, this.params.density);
      this.state.lastScheduleTime += interval;
    }

    const lookahead = this.state.lookaheadMs;
    this.state.schedulerTimer = setTimeout(() => this._tick(), lookahead);
  }

  _scheduleGrainAt(time) {
    const hasA = !!this.buffers.A;
    const hasB = !!this.buffers.B;
    if (!hasA && !hasB) return;

    const { morph, grainMs, jitterMs, pitchSt, spreadSt, scanSpeedNormPerSec, freeze } = this.params;
    const grainDur = Math.max(0.01, grainMs / 1000);

    let localPos = this.state.positionNorm;
    if (!freeze) {
      const dt = time - this.context.currentTime;
      localPos += Math.max(-1, Math.min(1, scanSpeedNormPerSec)) * dt;
      localPos = (localPos % 1 + 1) % 1;
      this.state.positionNorm = localPos;
    }

    const posA = localPos;
    const posB = localPos;

    const sr = this.context.sampleRate;
    const jitter = (Math.random() * 2 - 1) * (jitterMs / 1000);
    const when = Math.max(this.context.currentTime, time + jitter);

    const transposeSt = pitchSt + (Math.random() * 2 - 1) * spreadSt;
    const rate = Math.pow(2, transposeSt / 12);

    const voiceGain = this.context.createGain();
    voiceGain.gain.setValueAtTime(0, when);
    // Hann window envelope
    const a = 0.5;
    voiceGain.gain.linearRampToValueAtTime(1, when + grainDur * a);
    voiceGain.gain.linearRampToValueAtTime(0, when + grainDur);
    voiceGain.connect(this.output);

    const sources = [];
    if (hasA && morph < 1) {
      const srcA = this.context.createBufferSource();
      srcA.buffer = this.buffers.A;
      srcA.playbackRate.value = rate;
      srcA.connect(voiceGain);
      const startA = posA * Math.max(0, srcA.buffer.duration - grainDur);
      srcA.start(when, startA, grainDur);
      sources.push(srcA);
    }
    if (hasB && morph > 0) {
      const srcB = this.context.createBufferSource();
      srcB.buffer = this.buffers.B;
      srcB.playbackRate.value = rate;
      const gB = this.context.createGain();
      gB.gain.value = morph;
      srcB.connect(gB).connect(voiceGain);
      const startB = posB * Math.max(0, srcB.buffer.duration - grainDur);
      srcB.start(when, startB, grainDur);
      sources.push(srcB);
    }
    // if both present, attenuate A proportionally
    if (sources.length === 2) {
      const atten = this.context.createGain();
      atten.gain.value = 1 - morph;
      sources[0].disconnect();
      sources[0].connect(atten).connect(voiceGain);
    }
  }
}

const ui = {
  fileA: document.getElementById("fileA"),
  fileB: document.getElementById("fileB"),
  infoA: document.getElementById("infoA"),
  infoB: document.getElementById("infoB"),
  morph: document.getElementById("morph"),
  grainMs: document.getElementById("grainMs"),
  density: document.getElementById("density"),
  jitterMs: document.getElementById("jitterMs"),
  pitchSt: document.getElementById("pitchSt"),
  spreadSt: document.getElementById("spreadSt"),
  scan: document.getElementById("scan"),
  freeze: document.getElementById("freeze"),
  volume: document.getElementById("volume"),
  out: {
    morph: document.getElementById("out_morph"),
    grainMs: document.getElementById("out_grainMs"),
    density: document.getElementById("out_density"),
    jitterMs: document.getElementById("out_jitterMs"),
    pitchSt: document.getElementById("out_pitchSt"),
    spreadSt: document.getElementById("out_spreadSt"),
    scan: document.getElementById("out_scan"),
    volume: document.getElementById("out_volume"),
  },
  play: document.getElementById("play"),
  pause: document.getElementById("pause"),
  stop: document.getElementById("stop"),
};

const engine = new GranularMorpher();

function updateOutputs() {
  ui.out.morph.textContent = ui.morph.value;
  ui.out.grainMs.textContent = ui.grainMs.value;
  ui.out.density.textContent = ui.density.value;
  ui.out.jitterMs.textContent = ui.jitterMs.value;
  ui.out.pitchSt.textContent = ui.pitchSt.value;
  ui.out.spreadSt.textContent = ui.spreadSt.value;
  ui.out.scan.textContent = ui.scan.value;
  ui.out.volume.textContent = ui.volume.value;
}

ui.fileA.addEventListener("change", async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  await engine.resume();
  const buf = await engine.loadFileTo("A", f);
  ui.infoA.textContent = `${f.name} (${buf.duration.toFixed(2)}s)`;
});

ui.fileB.addEventListener("change", async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  await engine.resume();
  const buf = await engine.loadFileTo("B", f);
  ui.infoB.textContent = `${f.name} (${buf.duration.toFixed(2)}s)`;
});

[
  ["morph", (v) => engine.setParam("morph", Number(v))],
  ["grainMs", (v) => engine.setParam("grainMs", Number(v))],
  ["density", (v) => engine.setParam("density", Number(v))],
  ["jitterMs", (v) => engine.setParam("jitterMs", Number(v))],
  ["pitchSt", (v) => engine.setParam("pitchSt", Number(v))],
  ["spreadSt", (v) => engine.setParam("spreadSt", Number(v))],
  ["scan", (v) => engine.setParam("scanSpeedNormPerSec", Number(v))],
  ["freeze", (v) => engine.setParam("freeze", !!ui.freeze.checked)],
  ["volume", (v) => engine.setParam("volume", Number(v))],
].forEach(([key, setter]) => {
  const el = ui[key];
  el.addEventListener("input", () => {
    setter(el.value);
    updateOutputs();
  });
});

ui.play.addEventListener("click", async () => {
  await engine.resume();
  engine.start();
});

ui.pause.addEventListener("click", () => engine.pause());
ui.stop.addEventListener("click", () => engine.stop());

updateOutputs();

