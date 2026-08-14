import { prng } from './utils.js';

export class TrackManager {
  constructor(containerEl, deps) {
    this.containerEl = containerEl;
    this.midi = deps.midi;
    this.visualizer = deps.visualizer;
    this.transport = deps.transport;
    this.tracks = [];
    this.steps = 16;
    this.onChanged = null;
    this.notifyChanged = () => { try { this.onChanged?.(); } catch (_) {} };
  }

  setSteps(count) {
    this.steps = count;
    for (const t of this.tracks) t.setSteps(count);
    this.notifyChanged();
  }

  addTrack(opts) {
    const { type, euclid } = opts;
    const id = crypto.randomUUID();
    // melodic tracks take scale, root, mode, motif… so pass the options through
    const track = type === 'percussion'
      ? new PercussionTrack(id, this, opts)
      : new MelodicTrack(id, this, opts);
    track.setSteps(this.steps);
    this.tracks.push(track);
    this.containerEl.appendChild(track.render());
    // a euclid spec passed at creation was stored but never applied, so a track
    // asked for 5-in-8 started empty and only the stochastic fills were heard
    if (euclid && track.applyEuclid) track.applyEuclid();
    this.notifyChanged();
    return track;
  }

  removeTrack(id) {
    const idx = this.tracks.findIndex(t => t.id === id);
    if (idx >= 0) {
      this.tracks[idx].destroy();
      this.tracks.splice(idx, 1);
      this.notifyChanged();
    }
  }

  onTick(stepIndex, stepTimeMs) {
    for (const t of this.tracks) {
      t.onTick(stepIndex, stepTimeMs);
    }
    this.updatePlayhead(stepIndex);
  }

  updatePlayhead(stepIndex) {
    for (const t of this.tracks) t.updatePlayhead(stepIndex);
  }

  serialize() {
    return {
      steps: this.steps,
      tracks: this.tracks.map(t => t.serialize()),
    };
  }

  load(data) {
    // clear
    for (const t of this.tracks) t.destroy();
    this.tracks = [];
    this.steps = data.steps || 16;
    for (const td of data.tracks || []) {
      const track = this.addTrack({ ...td });
      track.load?.(td);
    }
    // Ensure all tracks have the correct step count and redraw
    this.tracks.forEach(track => {
      track.setSteps(this.steps);
    });
  }

  clear() {
    // clear all tracks
    for (const t of this.tracks) t.destroy();
    this.tracks = [];
    this.steps = 16;
    this.notifyChanged();
  }
}

class BaseTrack {
  constructor(id, manager, opts) {
    this.id = id;
    this.manager = manager;
    this.midi = manager.midi;
    this.visualizer = manager.visualizer;
    this.transport = manager.transport;
    this.name = opts.name || (this.constructor.name.toUpperCase());
    this.channel = Number(opts.channel ?? 0);
    this.steps = 16;
    this.stepStates = [];
    this.rootEl = null;
    this.stepsEl = null;
  }

  setSteps(count) {
    this.steps = count;
    if (this.stepStates.length !== count) {
      const next = new Array(count).fill(false).map((_, i) => ({ on: false, prob: 1.0, cond: 'always' }));
      for (let i = 0; i < Math.min(count, this.stepStates.length); i++) next[i] = normalizeStep(this.stepStates[i]);
      this.stepStates = next;
      this.redrawSteps();
    }
  }

  render() {
    const el = document.createElement('div');
    el.className = 'track';
    el.innerHTML = `
      <div class="track-head">
        <div class="track-title">${this.name}</div>
        <div class="track-controls"></div>
      </div>
      <div class="steps"></div>
    `;
    this.rootEl = el;
    this.stepsEl = el.querySelector('.steps');
    this.renderControls(el.querySelector('.track-controls'));
    this.redrawSteps();
    return el;
  }

  redrawSteps() {
    if (!this.stepsEl) return;
    this.stepsEl.innerHTML = '';
    for (let i = 0; i < this.steps; i++) {
      const step = document.createElement('div');
      step.className = 'step';
      const s = normalizeStep(this.stepStates[i]);
      if (s.on) step.classList.add('active');
      step.title = `p=${s.prob.toFixed(2)} ${s.cond}`;
      step.addEventListener('click', () => {
        s.on = !s.on; this.stepStates[i] = s;
        step.classList.toggle('active');
        this.manager.notifyChanged();
      });
      step.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        const p = Number(prompt('Probability 0..1', String(s.prob)) || s.prob);
        s.prob = clamp(p, 0, 1);
        const cond = prompt('Condition: always, 1:2, 2:2, 1:3, 2:3, 3:3, fill', s.cond) || s.cond;
        s.cond = cond;
        this.stepStates[i] = s;
        step.title = `p=${s.prob.toFixed(2)} ${s.cond}`;
        this.manager.notifyChanged();
      });
      this.stepsEl.appendChild(step);
    }
  }

  updatePlayhead(stepIndex) {
    if (!this.stepsEl) return;
    const children = Array.from(this.stepsEl.children);
    children.forEach((c, i) => c.classList.toggle('playhead', i === stepIndex));
  }

  destroy() {
    this.rootEl?.remove();
  }

  serialize() {
    return {
      type: this.type,
      name: this.name,
      channel: this.channel,
      steps: this.steps,
      stepStates: this.stepStates,
    };
  }

  load(data) {
    this.name = data.name ?? this.name;
    this.channel = Number(data.channel ?? this.channel);
    this.setSteps(Number(data.steps ?? this.steps));
    if (Array.isArray(data.stepStates)) {
      const copy = new Array(this.steps).fill(false).map((_, i) => ({ on: false, prob: 1.0, cond: 'always' }));
      for (let i = 0; i < Math.min(copy.length, data.stepStates.length); i++) {
        copy[i] = normalizeStep(data.stepStates[i]);
      }
      this.stepStates = copy;
      this.redrawSteps();
    }
  }
}

class PercussionTrack extends BaseTrack {
  constructor(id, manager, opts) {
    super(id, manager, opts);
    this.type = 'percussion';
    this.midiNote = Number(opts.midiNote ?? 36);
    // density used to gate the written steps AND to sprinkle extra hits, so a
    // pattern never played what the grid showed. Split in two: the grid is
    // honoured, ghost notes are opt-in.
    this.density = Number(opts.density ?? 1);
    this.ghost = Number(opts.ghost ?? 0);
    this.euclid = opts.euclid || null; // { beats, steps, rotate }
    this.random = prng();
  }

  renderControls(container) {
    container.appendChild(makeNumber('Note', this.midiNote, v => { this.midiNote = clamp(v, 0, 127); this.manager.notifyChanged(); }, 0, 127, 1, 58));
    container.appendChild(makeNumber('Ch', this.channel, v => { this.channel = clamp(v, 0, 15); this.manager.notifyChanged(); }, 0, 15, 1, 48));
    container.appendChild(makeRange('Density', this.density, v => { this.density = clamp(v, 0, 1); this.manager.notifyChanged(); }, 0, 1, 0.01));
    container.appendChild(makeRange('Ghost', this.ghost, v => { this.ghost = clamp(v, 0, 1); this.manager.notifyChanged(); }, 0, 1, 0.01));

    // Euclid used to hide behind three prompt() dialogs; these apply as you type
    const e = this.euclid || { beats: 4, steps: this.steps, rotate: 0 };
    const push = () => { this.euclid = e; this.applyEuclid(); this.manager.notifyChanged(); };
    container.appendChild(makeNumber('Hits', e.beats, v => { e.beats = clamp(v, 0, 64); push(); }, 0, 64, 1, 48));
    container.appendChild(makeNumber('Of', e.steps, v => { e.steps = clamp(v, 1, 64); push(); }, 1, 64, 1, 48));
    container.appendChild(makeNumber('Rot', e.rotate, v => { e.rotate = clamp(v, 0, 64); push(); }, 0, 64, 1, 48));

    const rm = document.createElement('button');
    rm.className = 'btn subtle'; rm.textContent = this.manager.labels?.remove || 'Remove';
    rm.addEventListener('click', () => this.manager.removeTrack(this.id));
    container.appendChild(rm);
  }

  applyEuclid() {
    if (!this.euclid) return;
    const { beats, steps, rotate } = this.euclid;
    const pattern = bjorklund(beats, steps);
    this.stepStates = new Array(this.steps).fill(false);
    // tile the figure across the whole grid: a 5-in-8 asked on 16 steps used to
    // fill only the first bar and leave the second silent
    for (let i = 0; i < this.steps; i++) {
      const src = ((i - rotate) % steps + steps) % steps;
      if (pattern[src]) this.stepStates[i] = true;
    }
    this.redrawSteps();
  }

  onTick(stepIndex, stepTimeMs) {
    const s = normalizeStep(this.stepStates[stepIndex]);
    const should = stepCondition(s, this.transport.loopCount);
    if (!s.on || !should) {
      if (this.ghost && this.random() < this.ghost * 0.25) this.trigger(stepTimeMs, 62);
      return;
    }
    if (this.random() < this.density * s.prob) this.trigger(stepTimeMs);
  }

  trigger(whenMs, velocity = 110) {
    this.midi.noteOn(this.midiNote, velocity, this.channel, whenMs);
    this.midi.noteOff(this.midiNote, this.channel, whenMs + 25);
    this.visualizer.ping({ hue: 160, energy: 0.7, x: this.channel / 16 });
  }

  serialize() {
    const base = super.serialize();
    return { ...base, midiNote: this.midiNote, density: this.density, ghost: this.ghost,
             euclid: this.euclid };
  }

  load(data) {
    super.load(data);
    if (typeof data.midiNote === 'number') this.midiNote = data.midiNote;
    if (typeof data.density === 'number') this.density = data.density;
    if (typeof data.ghost === 'number') this.ghost = data.ghost;
    if (data.euclid) { this.euclid = data.euclid; this.applyEuclid(); }
  }
}

class MelodicTrack extends BaseTrack {
  constructor(id, manager, opts) {
    super(id, manager, opts);
    this.type = 'melodic';
    this.scale = opts.scale || 'minor';
    this.root = Number(opts.root ?? 48);              // C3
    this.octaves = Number(opts.octaves ?? 2);
    this.harmonicity = Number(opts.harmonicity ?? 0.2); // how often a degree becomes a chord
    this.density = Number(opts.density ?? 1);           // how often an active step speaks
    this.gate = Number(opts.gate ?? 1);                 // note length, in steps
    this.mode = opts.mode || 'motif';   // motif | up | down | updown | walk | random
    this.motifLen = Number(opts.motifLen ?? 8);
    this.mutate = Number(opts.mutate ?? 0.12);          // chance a degree is rewritten each loop
    this.euclid = opts.euclid || null;
    this.random = prng();
    this.cursor = 0;            // where the arpeggio or the walk has got to
    this.hitIndex = 0;          // which note of the motif comes next
    this.dir = 1;
    this.lastLoop = -1;
    this.motif = this.makeMotif();
  }

  /* A motif is a short list of scale degrees. Repeating it is what makes a
     phrase sound composed rather than sampled from noise; mutation keeps it
     from becoming wallpaper. */
  makeMotif() {
    const len = clamp(this.motifLen, 2, 32);
    const span = 7;
    const out = [];
    let d = 0;
    for (let i = 0; i < len; i++) {
      if (i === 0) { out.push(0); continue; }   // phrases start on the root
      // small intervals most of the time, an occasional leap
      const jump = this.random() < 0.22
        ? Math.round((this.random() * 4) - 2) * 2
        : Math.round((this.random() * 2) - 1);
      d = clamp(d + jump, -span, span);
      out.push(d);
    }
    return out;
  }

  mutateMotif() {
    if (this.motif.length < 2) return;
    const i = 1 + Math.floor(this.random() * (this.motif.length - 1));
    const delta = this.random() < 0.5 ? -1 : 1;
    this.motif[i] = clamp(this.motif[i] + delta * (this.random() < 0.3 ? 2 : 1), -7, 7);
  }

  renderControls(container) {
    const changed = () => this.manager.notifyChanged();
    container.appendChild(makeNumber('Ch', this.channel, v => { this.channel = clamp(v, 0, 15); changed(); }, 0, 15, 1, 48));

    container.appendChild(makeSelect('Mode', this.mode,
      [['motif', 'Motif'], ['up', 'Arp up'], ['down', 'Arp down'], ['updown', 'Arp up/down'],
       ['walk', 'Walk'], ['random', 'Random']],
      v => { this.mode = v; this.cursor = 0; changed(); }));

    container.appendChild(makeSelect('Scale', this.scale,
      ['minor', 'major', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian', 'whole',
       'pentaMinor', 'pentaMajor'].map(k => [k, k]),
      v => { this.scale = v; changed(); }));

    // root as a note name, not a MIDI number nobody wants to convert in their head
    const names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
    const roots = [];
    for (let oct = 1; oct <= 5; oct++)
      for (let n = 0; n < 12; n++) roots.push([String(12 * (oct + 1) + n), `${names[n]}${oct}`]);
    container.appendChild(makeSelect('Root', String(this.root), roots,
      v => { this.root = Number(v); changed(); }));

    container.appendChild(makeNumber('Oct', this.octaves, v => { this.octaves = clamp(v, 1, 4); changed(); }, 1, 4, 1, 44));
    container.appendChild(makeNumber('Len', this.motifLen, v => {
      this.motifLen = clamp(v, 2, 32); this.motif = this.makeMotif(); changed();
    }, 2, 32, 1, 48));
    container.appendChild(makeRange('Mutate', this.mutate, v => { this.mutate = clamp(v, 0, 1); changed(); }, 0, 1, 0.01));
    container.appendChild(makeRange('Chord', this.harmonicity, v => { this.harmonicity = clamp(v, 0, 1); changed(); }, 0, 1, 0.01));
    container.appendChild(makeRange('Density', this.density, v => { this.density = clamp(v, 0, 1); changed(); }, 0, 1, 0.01));
    container.appendChild(makeRange('Gate', this.gate, v => { this.gate = clamp(v, 0.25, 4); changed(); }, 0.25, 4, 0.25));

    const e = this.euclid || { beats: 5, steps: this.steps, rotate: 0 };
    const push = () => { this.euclid = e; this.applyEuclid(); changed(); };
    container.appendChild(makeNumber('Hits', e.beats, v => { e.beats = clamp(v, 0, 64); push(); }, 0, 64, 1, 48));
    container.appendChild(makeNumber('Of', e.steps, v => { e.steps = clamp(v, 1, 64); push(); }, 1, 64, 1, 48));

    const gen = document.createElement('button');
    gen.className = 'btn';
    gen.textContent = this.manager.labels?.newMotif || 'New motif';
    gen.addEventListener('click', () => { this.random = prng(); this.motif = this.makeMotif(); changed(); });
    container.appendChild(gen);

    const rm = document.createElement('button');
    rm.className = 'btn subtle';
    rm.textContent = this.manager.labels?.remove || 'Remove';
    rm.addEventListener('click', () => this.manager.removeTrack(this.id));
    container.appendChild(rm);
  }

  /* Euclid fills the grid the same way it does for drums. */
  applyEuclid() {
    if (!this.euclid) return;
    const { beats, steps, rotate } = this.euclid;
    const pattern = bjorklund(beats, steps);
    this.stepStates = new Array(this.steps).fill(false);
    // tile the figure across the whole grid: a 5-in-8 asked on 16 steps used to
    // fill only the first bar and leave the second silent
    for (let i = 0; i < this.steps; i++) {
      const src = ((i - rotate) % steps + steps) % steps;
      if (pattern[src]) this.stepStates[i] = true;
    }
    this.redrawSteps();
  }

  degreeFor(stepIndex) {
    const len = this.motif.length || 1;
    switch (this.mode) {
      // indexed by hit order, not by step: the phrase starts on the root even
      // when the euclid figure puts its first hit off the downbeat
      case 'motif':  return this.motif[(this.hitIndex++) % len];
      case 'up':     return (this.cursor++) % 8;
      case 'down':   return 7 - ((this.cursor++) % 8);
      case 'updown': {
        const d = this.cursor;
        this.cursor += this.dir;
        if (this.cursor > 7) { this.cursor = 6; this.dir = -1; }
        if (this.cursor < 0) { this.cursor = 1; this.dir = 1; }
        return d;
      }
      case 'walk': {
        const step = this.random() < 0.5 ? -1 : 1;
        this.cursor = clamp(this.cursor + step * (this.random() < 0.25 ? 2 : 1), -7, 7);
        return this.cursor;
      }
      default:       return Math.floor(this.random() * 8);
    }
  }

  onTick(stepIndex, stepTimeMs) {
    // one mutation per loop, so a phrase drifts instead of being redrawn
    const loop = this.transport.loopCount;
    if (loop !== this.lastLoop) {
      this.lastLoop = loop;
      this.hitIndex = 0;
      if (this.mode !== 'motif' && this.mode !== 'walk') { this.cursor = 0; this.dir = 1; }
      if (this.mode === 'motif' && this.random() < this.mutate) this.mutateMotif();
    }

    const s = normalizeStep(this.stepStates[stepIndex]);
    if (!s.on || !stepCondition(s, loop)) return;
    if (this.random() > this.density * s.prob) return;

    const notes = this.notesFor(this.degreeFor(stepIndex));
    const stepMs = 60000 / (this.transport.bpm * 4);
    for (const n of notes) {
      const v = 74 + Math.floor(this.random() * 30);
      this.midi.noteOn(n, v, this.channel, stepTimeMs);
      this.midi.noteOff(n, this.channel, stepTimeMs + stepMs * this.gate * 0.92);
    }
    this.visualizer.ping({ hue: 0, energy: 0.8, x: this.channel / 16 });
  }

  notesFor(degree) {
    const intervals = getScale(this.scale);
    const size = intervals.length - 1;              // last entry is the octave
    const wrap = ((degree % size) + size) % size;
    const octave = Math.floor(degree / size);
    const top = this.root + this.octaves * 12;
    // fold into the declared range instead of letting a negative degree drop
    // an octave below the root
    const fold = n => {
      while (n > top) n -= 12;
      while (n < this.root) n += 12;
      return n;
    };
    const notes = [fold(this.root + intervals[wrap] + octave * 12)];
    if (this.random() < this.harmonicity) {
      notes.push(fold(this.root + intervals[(wrap + 2) % size] + octave * 12));
      notes.push(fold(this.root + intervals[(wrap + 4) % size] + octave * 12));
    }
    return notes.map(n => clamp(n, 0, 127));
  }

  serialize() {
    const base = super.serialize();
    return { ...base, scale: this.scale, root: this.root, octaves: this.octaves,
             harmonicity: this.harmonicity, density: this.density, gate: this.gate,
             mode: this.mode, motifLen: this.motifLen, mutate: this.mutate,
             motif: this.motif.slice(), euclid: this.euclid };
  }

  load(data) {
    super.load(data);
    if (data.scale) this.scale = data.scale;
    if (typeof data.root === 'number') this.root = data.root;
    if (typeof data.octaves === 'number') this.octaves = data.octaves;
    if (typeof data.harmonicity === 'number') this.harmonicity = data.harmonicity;
    if (typeof data.density === 'number') this.density = data.density;
    if (typeof data.gate === 'number') this.gate = data.gate;
    if (data.mode) this.mode = data.mode;
    if (typeof data.motifLen === 'number') this.motifLen = data.motifLen;
    if (typeof data.mutate === 'number') this.mutate = data.mutate;
    if (Array.isArray(data.motif)) this.motif = data.motif.slice();
    if (data.euclid) { this.euclid = data.euclid; this.applyEuclid(); }
  }
}

function makeNumber(label, value, onChange, min, max, step, width) {
  const input = document.createElement('input');
  input.type = 'number'; input.value = String(value);
  if (min !== undefined) input.min = String(min);
  if (max !== undefined) input.max = String(max);
  if (step !== undefined) input.step = String(step);
  if (width) input.style.width = width + 'px';
  input.addEventListener('input', () => onChange(Number(input.value)));
  return wrap(label, input);
}

function makeSelect(label, value, options, onChange) {
  const sel = document.createElement('select');
  options.forEach(([v, text]) => {
    const o = document.createElement('option');
    o.value = v; o.textContent = text;
    if (String(v) === String(value)) o.selected = true;
    sel.appendChild(o);
  });
  sel.addEventListener('change', () => onChange(sel.value));
  return wrap(label, sel);
}
function makeRange(label, value, onChange, min, max, step) {
  const input = document.createElement('input');
  input.type = 'range'; input.min = String(min); input.max = String(max); input.step = String(step || 0.01); input.value = String(value);
  input.addEventListener('input', () => onChange(Number(input.value)));
  return wrap(label, input);
}
function wrap(label, el) {
  const div = document.createElement('label'); div.className = 'control';
  const span = document.createElement('span'); span.textContent = label; div.appendChild(span);
  div.appendChild(el); return div;
}

function clamp(n, min, max) { return Math.max(min, Math.min(max, Number(n) || 0)); }

function normalizeStep(s) {
  if (typeof s === 'boolean') return { on: s, prob: 1.0, cond: 'always' };
  if (!s) return { on: false, prob: 1.0, cond: 'always' };
  if (s.on === undefined) s.on = !!s;
  if (s.prob === undefined) s.prob = 1.0;
  if (!s.cond) s.cond = 'always';
  return s;
}

function stepCondition(step, loopCount) {
  const cond = (step.cond || 'always').trim();
  if (cond === 'always') return true;
  if (cond === 'fill') return loopCount % 4 === 3; // simple fill every 4 bars
  const m = cond.match(/^(\d+):(\d+)$/);
  if (m) {
    const a = Number(m[1]);
    const b = Number(m[2]);
    if (b <= 0) return true;
    return (loopCount % b) === (a - 1);
  }
  return true;
}

function getScale(name) {
  switch (name) {
    case 'minor': return [0,2,3,5,7,8,10,12];
    case 'major': return [0,2,4,5,7,9,11,12];
    case 'dorian': return [0,2,3,5,7,9,10,12];
    case 'phrygian': return [0,1,3,5,7,8,10,12];
    case 'lydian': return [0,2,4,6,7,9,11,12];
    case 'mixolydian': return [0,2,4,5,7,9,10,12];
    case 'locrian': return [0,1,3,5,6,8,10,12];
    case 'whole': return [0,2,4,6,8,10,12];
    case 'pentaMinor': return [0,3,5,7,10,12];
    case 'pentaMajor': return [0,2,4,7,9,12];
    default: return [0,2,3,5,7,8,10,12];
  }
}

// Euclidean rhythm generator (Bjorklund algorithm)
// Returns an array of length `steps` containing 0/1 with `pulses` ones distributed evenly
function bjorklund(pulses, steps) {
  const s = Math.max(1, Math.floor(steps));
  const p = Math.max(0, Math.min(s, Math.floor(pulses)));
  if (p === 0) return new Array(s).fill(0);
  if (p === s) return new Array(s).fill(1);
  let pattern = [];
  let counts = [];
  let remainders = [];
  let divisor = s - p;
  remainders.push(p);
  let level = 0;
  while (true) {
    counts.push(Math.floor(divisor / remainders[level]));
    remainders.push(divisor % remainders[level]);
    divisor = remainders[level];
    level += 1;
    if (remainders[level] <= 1) break;
  }
  counts.push(divisor);
  function build(level) {
    if (level === -1) {
      pattern.push(0);
    } else if (level === -2) {
      pattern.push(1);
    } else {
      for (let i = 0; i < counts[level]; i++) build(level - 1);
      if (remainders[level] !== 0) build(level - 2);
    }
  }
  build(level);
  return pattern;
}

