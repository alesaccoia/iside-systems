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

  addTrack({ type, name, midiNote, channel, density, euclid }) {
    const id = crypto.randomUUID();
    const track = type === 'percussion'
      ? new PercussionTrack(id, this, { name, midiNote, channel, density, euclid })
      : new MelodicTrack(id, this, { name, channel });
    track.setSteps(this.steps);
    this.tracks.push(track);
    this.containerEl.appendChild(track.render());
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
      const track = this.addTrack({
        type: td.type,
        name: td.name,
        midiNote: td.midiNote,
        channel: td.channel,
        density: td.density,
        euclid: td.euclid
      });
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
    this.density = Number(opts.density ?? 0.5);
    this.euclid = opts.euclid || null; // { beats, steps, rotate }
    this.random = prng();
  }

  renderControls(container) {
    container.appendChild(makeNumber('Note', this.midiNote, v => { this.midiNote = clamp(v, 0, 127); this.manager.notifyChanged(); }));
    container.appendChild(makeNumber('Ch', this.channel, v => { this.channel = clamp(v, 0, 15); this.manager.notifyChanged(); }));
    container.appendChild(makeRange('Density', this.density, v => { this.density = clamp(v, 0, 1); this.manager.notifyChanged(); }, 0, 1, 0.01));
    const btn = document.createElement('button');
    btn.className = 'btn subtle';
    btn.textContent = 'Euclid';
    btn.addEventListener('click', () => {
      const beats = Number(prompt('Beats?', String(this.euclid?.beats ?? 5)) || 0);
      const steps = Number(prompt('Steps?', String(this.euclid?.steps ?? this.steps)) || 0);
      const rotate = Number(prompt('Rotate?', String(this.euclid?.rotate ?? 0)) || 0);
      this.euclid = { beats: clamp(beats, 0, 64), steps: clamp(steps, 1, 64), rotate: clamp(rotate, 0, 64) };
      this.applyEuclid();
      this.manager.notifyChanged();
    });
    container.appendChild(btn);
    const rm = document.createElement('button');
    rm.className = 'btn subtle'; rm.textContent = 'Remove';
    rm.addEventListener('click', () => this.manager.removeTrack(this.id));
    container.appendChild(rm);
  }

  applyEuclid() {
    if (!this.euclid) return;
    const { beats, steps, rotate } = this.euclid;
    const pattern = bjorklund(beats, steps);
    this.stepStates = new Array(this.steps).fill(false);
    for (let i = 0; i < steps; i++) {
      const idx = (i + rotate) % steps;
      if (pattern[i]) this.stepStates[idx] = true;
    }
    this.redrawSteps();
  }

  onTick(stepIndex, stepTimeMs) {
    const s = normalizeStep(this.stepStates[stepIndex]);
    const should = stepCondition(s, this.transport.loopCount);
    if (!s.on || !should) {
      // stochastic fill
      if (this.random() < this.density * 0.15) this.trigger(stepTimeMs);
      return;
    }
    if (this.random() < this.density * s.prob) this.trigger(stepTimeMs);
  }

  trigger(whenMs) {
    this.midi.noteOn(this.midiNote, 110, this.channel, whenMs);
    this.midi.noteOff(this.midiNote, this.channel, whenMs + 25);
    this.visualizer.ping({ hue: 160, energy: 0.7, x: this.channel / 16 });
  }

  serialize() {
    const base = super.serialize();
    return { ...base, midiNote: this.midiNote, density: this.density, euclid: this.euclid };
  }

  load(data) {
    super.load(data);
    if (typeof data.midiNote === 'number') this.midiNote = data.midiNote;
    if (typeof data.density === 'number') this.density = data.density;
    if (data.euclid) { this.euclid = data.euclid; this.applyEuclid(); }
  }
}

class MelodicTrack extends BaseTrack {
  constructor(id, manager, opts) {
    super(id, manager, opts);
    this.type = 'melodic';
    this.scale = 'minor';
    this.root = 48; // C3
    this.range = 24; // two octaves
    this.harmonicity = 0.5; // chord probability
    this.random = prng();
  }

  renderControls(container) {
    container.appendChild(makeNumber('Ch', this.channel, v => { this.channel = clamp(v, 0, 15); this.manager.notifyChanged(); }));
    const sel = document.createElement('select'); sel.className = '';
    ;['minor','major','dorian','phrygian','lydian','mixolydian','locrian','whole'].forEach(k => {
      const o = document.createElement('option'); o.value = k; o.textContent = k; if (k===this.scale) o.selected = true; sel.appendChild(o);
    });
    sel.addEventListener('change', () => { this.scale = sel.value; this.manager.notifyChanged(); });
    container.appendChild(wrap('Scale', sel));
    container.appendChild(makeNumber('Root', this.root, v => { this.root = clamp(v, 0, 120); this.manager.notifyChanged(); }));
    container.appendChild(makeNumber('Range', this.range, v => { this.range = clamp(v, 12, 72); this.manager.notifyChanged(); }));
    container.appendChild(makeRange('Chord', this.harmonicity, v => { this.harmonicity = clamp(v, 0, 1); this.manager.notifyChanged(); }, 0, 1, 0.01));
    const rm = document.createElement('button'); rm.className = 'btn subtle'; rm.textContent = 'Remove';
    rm.addEventListener('click', () => this.manager.removeTrack(this.id)); container.appendChild(rm);
  }

  onTick(stepIndex, stepTimeMs) {
    const s = normalizeStep(this.stepStates[stepIndex]);
    const should = stepCondition(s, this.transport.loopCount);
    if ((!s.on || !should) && this.random() > 0.05) return;
    const notes = this.generateNotes();
    for (const n of notes) {
      const v = 80 + Math.floor(this.random()*40);
      const off = stepTimeMs + 140 + Math.floor(this.random()*220);
      this.midi.noteOn(n, v, this.channel, stepTimeMs);
      this.midi.noteOff(n, this.channel, off);
    }
    this.visualizer.ping({ hue: 0, energy: 0.8, x: this.channel / 16 });
  }

  generateNotes() {
    const scaleIntervals = getScale(this.scale);
    const stepsInScale = scaleIntervals.length;
    const baseDegree = Math.floor(this.random() * stepsInScale);
    const baseNote = this.root + scaleIntervals[baseDegree] + Math.floor(this.random()*this.range/12)*12;
    const notes = [baseNote];
    if (this.random() < this.harmonicity) {
      // simple chord: add a third and fifth within range
      const third = this.root + scaleIntervals[(baseDegree + 2) % stepsInScale] + 12 * Math.floor(this.random()*this.range/12);
      const fifth = this.root + scaleIntervals[(baseDegree + 4) % stepsInScale] + 12 * Math.floor(this.random()*this.range/12);
      if (third <= this.root + this.range) notes.push(third);
      if (fifth <= this.root + this.range) notes.push(fifth);
    }
    return notes;
  }

  serialize() {
    const base = super.serialize();
    return { ...base, scale: this.scale, root: this.root, range: this.range, harmonicity: this.harmonicity };
  }

  load(data) {
    super.load(data);
    if (data.scale) this.scale = data.scale;
    if (typeof data.root === 'number') this.root = data.root;
    if (typeof data.range === 'number') this.range = data.range;
    if (typeof data.harmonicity === 'number') this.harmonicity = data.harmonicity;
  }
}

function makeNumber(label, value, onChange) {
  const input = document.createElement('input');
  input.type = 'number'; input.value = String(value);
  input.addEventListener('input', () => onChange(Number(input.value)));
  return wrap(label, input);
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

