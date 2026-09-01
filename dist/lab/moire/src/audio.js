// A silent WAV, inlined so nothing extra loads over the network. Playing a
// real <audio> element, even an inaudible one, is what nudges iOS Safari's
// audio session out of the "ambient" category (which respects the hardware
// silent switch) and into "playback" (which does not) — WebAudio oscillators
// on their own stay ambient and can end up muted on an iPhone with the ring
// switch flipped, even though .resume() reports the context as running.
const SILENT_WAV = "data:audio/wav;base64,UklGRmQGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YUAGAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA";

export class AudioEngine {
  constructor() {
    this.context = null;
    this.nodes = null;
    this._unlockEl = null;
    this.parameters = {
      carrierFrequencyHz: 220,
      modulationFrequencyHz: 3,
      modulationIndex: 300,
      muted: false,
    };
  }

  _ensureUnlockElement() {
    if (this._unlockEl) return this._unlockEl;
    const el = document.createElement("audio");
    el.setAttribute("playsinline", "");
    el.loop = true;
    el.src = SILENT_WAV;
    el.style.display = "none";
    document.body.appendChild(el);
    this._unlockEl = el;
    return el;
  }

  _ensureContext() {
    if (this.context) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    this.context = new AudioCtx();

    const carrier = this.context.createOscillator();
    const modulator = this.context.createOscillator();
    const modGain = this.context.createGain();
    const outGain = this.context.createGain();

    carrier.type = "sine";
    modulator.type = "sine";

    // FM: modulator -> gain (index) -> carrier.frequency
    modulator.connect(modGain);
    modGain.connect(carrier.frequency);

    carrier.connect(outGain);
    outGain.connect(this.context.destination);

    carrier.start();
    modulator.start();

    this.nodes = { carrier, modulator, modGain, outGain };
    this._applyParameters();
  }

  async resume() {
    this._ensureContext();
    // Best-effort: browsers that don't need this (everything but iOS Safari)
    // just play two hundred milliseconds of silence and loop it, harmlessly.
    try {
      await this._ensureUnlockElement().play();
    } catch (_err) {
      // autoplay refused outside a user gesture, or no HTMLMediaElement
      // support worth worrying about — either way the oscillators still work
    }
    if (this.context.state === "suspended") {
      await this.context.resume();
    }
    this._applyParameters();
  }

  async suspend() {
    if (!this.context) return;
    if (this.context.state === "running") {
      await this.context.suspend();
    }
  }

  setParameters(next) {
    this.parameters = { ...this.parameters, ...next };
    this._applyParameters();
  }

  _applyParameters() {
    if (!this.context || !this.nodes) return;
    const now = this.context.currentTime;
    const p = this.parameters;
    const { carrier, modulator, modGain, outGain } = this.nodes;

    const timeConstant = 0.02;
    carrier.frequency.setTargetAtTime(p.carrierFrequencyHz, now, timeConstant);
    modulator.frequency.setTargetAtTime(p.modulationFrequencyHz, now, timeConstant);
    modGain.gain.setTargetAtTime(p.modulationIndex, now, timeConstant);
    outGain.gain.setTargetAtTime(p.muted ? 0 : 0.4, now, 0.02);
  }
}

