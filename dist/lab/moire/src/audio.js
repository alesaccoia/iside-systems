export class AudioEngine {
  constructor() {
    this.context = null;
    this.nodes = null;
    this.parameters = {
      carrierFrequencyHz: 220,
      modulationFrequencyHz: 3,
      modulationIndex: 300,
      muted: false,
    };
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

