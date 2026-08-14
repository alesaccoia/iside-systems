/* ============================================================
   Internal voice — added for the web version.

   The original AlgoSynth only speaks MIDI, which means silence for anyone
   without a synth plugged in. This module renders the same note events with
   Web Audio so the page makes sound on its own; MIDI still goes out in
   parallel when a device is selected.

   Percussion tracks land on channel 9 by convention, so their notes are read
   as drums; everything else is played by a short subtractive voice.
   ============================================================ */

const DRUMS = {
  36: "kick", 35: "kick",
  38: "snare", 40: "snare",
  42: "hat", 44: "hat", 46: "openhat",
  37: "rim", 39: "clap",
  41: "tom", 43: "tom", 45: "tom", 47: "tom", 48: "tom", 50: "tom",
  49: "cymbal", 51: "cymbal",
};

export function initAudio(ctx){
  const out = ctx.createGain();
  out.gain.value = 0.9;

  // a touch of glue, so the drums and the voice sit in the same room
  const comp = ctx.createDynamicsCompressor();
  comp.threshold.value = -14;
  comp.knee.value = 12;
  comp.ratio.value = 3;
  comp.attack.value = 0.004;
  comp.release.value = 0.18;
  out.connect(comp).connect(ctx.destination);

  let noiseBuffer = null;
  function noise(){
    if (!noiseBuffer){
      const len = Math.floor(ctx.sampleRate * 0.5);
      noiseBuffer = ctx.createBuffer(1, len, ctx.sampleRate);
      const data = noiseBuffer.getChannelData(0);
      for (let i = 0; i < len; i++) data[i] = Math.random() * 2 - 1;
    }
    const src = ctx.createBufferSource();
    src.buffer = noiseBuffer;
    src.loop = true;
    return src;
  }

  const freq = note => 440 * Math.pow(2, (note - 69) / 12);

  function env(param, t, peak, attack, decay){
    param.cancelScheduledValues(t);
    param.setValueAtTime(0.0001, t);
    param.exponentialRampToValueAtTime(Math.max(peak, 0.0002), t + attack);
    param.exponentialRampToValueAtTime(0.0001, t + attack + decay);
  }

  function drum(kind, t, velocity){
    const g = ctx.createGain();
    g.connect(out);
    const v = velocity / 127;

    if (kind === "kick"){
      const o = ctx.createOscillator();
      o.type = "sine";
      o.frequency.setValueAtTime(160, t);
      o.frequency.exponentialRampToValueAtTime(46, t + 0.11);
      env(g.gain, t, 0.9 * v, 0.002, 0.30);
      o.connect(g); o.start(t); o.stop(t + 0.4);
      return;
    }
    if (kind === "snare" || kind === "clap" || kind === "rim"){
      const n = noise();
      const bp = ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.frequency.value = kind === "rim" ? 2400 : 1750;
      bp.Q.value = kind === "clap" ? 1.2 : 0.8;
      env(g.gain, t, 0.5 * v, 0.002, kind === "rim" ? 0.06 : 0.16);
      n.connect(bp).connect(g); n.start(t); n.stop(t + 0.4);
      if (kind === "snare"){
        const o = ctx.createOscillator();
        const og = ctx.createGain();
        o.type = "triangle";
        o.frequency.setValueAtTime(190, t);
        env(og.gain, t, 0.28 * v, 0.002, 0.11);
        o.connect(og).connect(out); o.start(t); o.stop(t + 0.3);
      }
      return;
    }
    if (kind === "hat" || kind === "openhat" || kind === "cymbal"){
      const n = noise();
      const hp = ctx.createBiquadFilter();
      hp.type = "highpass";
      hp.frequency.value = kind === "cymbal" ? 5200 : 7200;
      const decay = kind === "hat" ? 0.045 : kind === "openhat" ? 0.28 : 0.6;
      env(g.gain, t, 0.28 * v, 0.001, decay);
      n.connect(hp).connect(g); n.start(t); n.stop(t + decay + 0.2);
      return;
    }
    // toms and anything else percussive
    const o = ctx.createOscillator();
    o.type = "sine";
    o.frequency.setValueAtTime(220, t);
    o.frequency.exponentialRampToValueAtTime(90, t + 0.18);
    env(g.gain, t, 0.6 * v, 0.003, 0.22);
    o.connect(g); o.start(t); o.stop(t + 0.5);
  }

  const held = new Map();   // note+channel -> stop function

  function voiceOn(note, t, velocity, channel){
    const g = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.Q.value = 6;
    const f = freq(note);
    filter.frequency.setValueAtTime(Math.min(f * 8, 9000), t);
    filter.frequency.exponentialRampToValueAtTime(Math.max(f * 2.2, 220), t + 0.5);

    const a = ctx.createOscillator();
    const b = ctx.createOscillator();
    a.type = "sawtooth"; b.type = "square";
    a.frequency.setValueAtTime(f, t);
    b.frequency.setValueAtTime(f, t);
    b.detune.setValueAtTime(7, t);          // a hair of movement between them

    const v = (velocity / 127) * 0.22;
    g.gain.cancelScheduledValues(t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(v, t + 0.012);
    g.gain.exponentialRampToValueAtTime(v * 0.55, t + 0.22);

    a.connect(filter); b.connect(filter);
    filter.connect(g).connect(out);
    a.start(t); b.start(t);

    const key = `${channel}:${note}`;
    const previous = held.get(key);
    if (previous) previous(t);
    held.set(key, stopAt => {
      const s = Math.max(stopAt, ctx.currentTime);
      g.gain.cancelScheduledValues(s);
      g.gain.setValueAtTime(Math.max(g.gain.value, 0.0002), s);
      g.gain.exponentialRampToValueAtTime(0.0001, s + 0.12);
      a.stop(s + 0.2); b.stop(s + 0.2);
      held.delete(key);
    });
  }

  function voiceOff(note, t, channel){
    const stop = held.get(`${channel}:${note}`);
    if (stop) stop(t);
  }

  return {
    /** The app schedules with performance.now(); convert to the audio clock. */
    at(whenMs){
      if (typeof whenMs !== "number") return ctx.currentTime;
      return Math.max(ctx.currentTime, ctx.currentTime + (whenMs - performance.now()) / 1000);
    },
    noteOn(note, velocity, channel, whenMs){
      const t = this.at(whenMs);
      if (channel === 9) drum(DRUMS[note] || "tom", t, velocity);
      else voiceOn(note, t, velocity, channel);
    },
    noteOff(note, channel, whenMs){
      if (channel === 9) return;             // percussion rings out on its own
      voiceOff(note, this.at(whenMs), channel);
    },
    allNotesOff(){
      held.forEach(stop => stop(ctx.currentTime));
      held.clear();
    },
    get gain(){ return out.gain; },
  };
}
