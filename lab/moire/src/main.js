import { VisualEngine } from "./visual.js";
import { AudioEngine } from "./audio.js";

const canvas = document.getElementById("visual-canvas");
const visualEngine = new VisualEngine(canvas);
const audioEngine = new AudioEngine();

const ui = {
  pattern: document.getElementById("pattern"),
  density: document.getElementById("density"),
  angleDelta: document.getElementById("angleDelta"),
  scaleDelta: document.getElementById("scaleDelta"),
  rotationSpeed: document.getElementById("rotationSpeed"),
  invert: document.getElementById("invert"),
  animate: document.getElementById("animate"),
  carrierFreq: document.getElementById("carrierFreq"),
  modIndex: document.getElementById("modIndex"),
  sync: document.getElementById("sync"),
  mute: document.getElementById("mute"),
  play: document.getElementById("play"),
  pause: document.getElementById("pause"),
  snapshot: document.getElementById("snapshot"),
  fullscreen: document.getElementById("fullscreen"),
};

const outputSpans = {
  density: document.querySelector('[data-out="density"]'),
  angleDelta: document.querySelector('[data-out="angleDelta"]'),
  scaleDelta: document.querySelector('[data-out="scaleDelta"]'),
  rotationSpeed: document.querySelector('[data-out="rotationSpeed"]'),
  carrierFreq: document.querySelector('[data-out="carrierFreq"]'),
  modIndex: document.querySelector('[data-out="modIndex"]'),
};

function updateOutputs() {
  outputSpans.density.textContent = ui.density.value;
  outputSpans.angleDelta.textContent = ui.angleDelta.value;
  outputSpans.scaleDelta.textContent = ui.scaleDelta.value;
  outputSpans.rotationSpeed.textContent = ui.rotationSpeed.value;
  outputSpans.carrierFreq.textContent = ui.carrierFreq.value;
  outputSpans.modIndex.textContent = ui.modIndex.value;
}

function currentVisualParams() {
  return {
    pattern: ui.pattern.value,
    density: Number(ui.density.value),
    angleDeltaDegrees: Number(ui.angleDelta.value),
    scaleDelta: Number(ui.scaleDelta.value),
    rotationSpeed: Number(ui.rotationSpeed.value),
    invert: ui.invert.checked,
    animate: ui.animate.checked,
  };
}

function currentAudioParams() {
  return {
    carrierFrequencyHz: Number(ui.carrierFreq.value),
    modulationFrequencyHz: deriveModulatorFrequency(
      Number(ui.carrierFreq.value),
      Number(ui.rotationSpeed.value)
    ),
    modulationIndex: Number(ui.modIndex.value),
    muted: ui.mute.checked,
  };
}

function syncAudioWithVisuals() {
  const v = currentVisualParams();

  const spatialToPitch = Math.max(40, Math.min(1600, v.density * 4));
  const modFreq = deriveModulatorFrequency(spatialToPitch, v.rotationSpeed);
  const modIndex = Math.max(0, Math.min(2000, Math.abs(v.rotationSpeed) * 900 + Math.abs(v.scaleDelta) * 12000));

  audioEngine.setParameters({
    carrierFrequencyHz: spatialToPitch,
    modulationFrequencyHz: modFreq,
    modulationIndex: modIndex,
  });
}

function applyVisualParams() {
  visualEngine.setParameters(currentVisualParams());
  if (ui.sync.checked) syncAudioWithVisuals();
}

function applyAudioParams() {
  audioEngine.setParameters(currentAudioParams());
}

function isFullscreenActive() {
  return !!(document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement);
}

function enterFullscreen() {
  const el = document.documentElement;
  if (el.requestFullscreen) return el.requestFullscreen();
  if (el.webkitRequestFullscreen) return el.webkitRequestFullscreen();
  if (el.msRequestFullscreen) return el.msRequestFullscreen();
}

function exitFullscreen() {
  if (document.exitFullscreen) return document.exitFullscreen();
  if (document.webkitExitFullscreen) return document.webkitExitFullscreen();
  if (document.msExitFullscreen) return document.msExitFullscreen();
}

function updateFullscreenButton() {
  if (!ui.fullscreen) return;
  ui.fullscreen.textContent = isFullscreenActive() ? "Exit Fullscreen" : "Fullscreen";
}

function deriveModulatorFrequency(carrierHz, rotationSpeed) {
  const degreesPerSecond = Math.abs(rotationSpeed) * 20;
  const differenceHz = Math.max(0, Math.min(2000, degreesPerSecond * 5));
  const modFreq = carrierHz + differenceHz;
  return Math.max(0.1, Math.min(20000, modFreq));
}

// Wire UI
[
  ui.pattern,
  ui.density,
  ui.angleDelta,
  ui.scaleDelta,
  ui.rotationSpeed,
  ui.invert,
  ui.animate,
].forEach((el) => {
  el.addEventListener("input", () => {
    updateOutputs();
    applyVisualParams();
    if (!ui.sync.checked) {
      applyAudioParams();
    }
  });
});

[
  ui.carrierFreq,
  ui.modIndex,
  ui.mute,
].forEach((el) => {
  el.addEventListener("input", () => {
    updateOutputs();
    applyAudioParams();
  });
});

ui.sync.addEventListener("input", () => {
  if (ui.sync.checked) syncAudioWithVisuals();
});

ui.play.addEventListener("click", async () => {
  await audioEngine.resume();
  visualEngine.start();
});

ui.pause.addEventListener("click", () => {
  visualEngine.stop();
  audioEngine.suspend();
});

ui.snapshot.addEventListener("click", () => {
  const url = canvas.toDataURL("image/png");
  const a = document.createElement("a");
  a.href = url;
  a.download = `moire_${Date.now()}.png`;
  a.click();
});

ui.fullscreen.addEventListener("click", async () => {
  try {
    if (isFullscreenActive()) {
      await exitFullscreen();
    } else {
      await enterFullscreen();
    }
  } finally {
    updateFullscreenButton();
    visualEngine.resize();
  }
});

document.addEventListener("fullscreenchange", () => {
  updateFullscreenButton();
  visualEngine.resize();
});
document.addEventListener("webkitfullscreenchange", () => {
  updateFullscreenButton();
  visualEngine.resize();
});
document.addEventListener("msfullscreenchange", () => {
  updateFullscreenButton();
  visualEngine.resize();
});

window.addEventListener("resize", () => visualEngine.resize());

// Initialize
updateOutputs();
applyVisualParams();
applyAudioParams();
visualEngine.start();
updateFullscreenButton();

// Keyboard shortcuts
window.addEventListener("keydown", async (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    if (visualEngine.isRunning()) {
      visualEngine.stop();
      audioEngine.suspend();
    } else {
      await audioEngine.resume();
      visualEngine.start();
    }
  }
});

