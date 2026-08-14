// Pattern and Song management

export class PatternBank {
  constructor(trackManager) {
    this.tm = trackManager;
    this.patterns = [];
    this.currentId = null;
    this.queuedId = null;
    this.song = []; // [{patternId, repeats}]
    this.songIndex = 0;
    this.songRepeatLeft = 0;
    this.mode = 'pattern'; // 'pattern' | 'song'
    this.onSelected = null; // optional callback: (pattern) => void
  }

  create(name = this.defaultName()) {
    const id = crypto.randomUUID();
    const data = this.tm.serialize();
    const pat = { id, name, data };
    this.patterns.push(pat);
    this.currentId = id;
    return pat;
  }

  duplicate(id) {
    const src = this.patterns.find(p => p.id === id);
    if (!src) return null;
    const copy = JSON.parse(JSON.stringify(src));
    copy.id = crypto.randomUUID();
    copy.name = this.defaultName(src.name + ' copy');
    this.patterns.push(copy);
    return copy;
  }

  rename(id, name) {
    const p = this.patterns.find(p => p.id === id);
    if (p) p.name = name || p.name;
  }

  remove(id) {
    const idx = this.patterns.findIndex(p => p.id === id);
    if (idx >= 0) {
      const removedCurrent = this.currentId === id;
      this.patterns.splice(idx, 1);
      // remove from song chain
      this.song = this.song.filter(entry => entry.patternId !== id);
      if (removedCurrent) {
        this.currentId = this.patterns[0]?.id ?? null;
        if (this.currentId) this.select(this.currentId);
      }
    }
  }

  select(id) {
    const p = this.patterns.find(p => p.id === id);
    if (!p) return;
    this.currentId = id;
    this.tm.load(p.data);
    // keep transport steps in sync with pattern
    const steps = p.data?.steps ?? 16;
    this.tm.transport?.setSteps?.(steps);
    // Force refresh all track step displays
    this.tm.tracks.forEach(track => {
      if (track.redrawSteps) track.redrawSteps();
    });
    this.onSelected?.(p);
  }

  queue(id) {
    this.queuedId = id;
  }

  onPatternEnd() {
    // apply any queued pattern switch
    if (this.mode === 'pattern') {
      if (this.queuedId) {
        this.select(this.queuedId);
        this.queuedId = null;
      }
      return;
    }
    // song mode
    if (this.song.length === 0) return;
    if (this.songRepeatLeft > 0) {
      this.songRepeatLeft -= 1;
      return;
    }
    this.songIndex = (this.songIndex + 1) % this.song.length;
    const entry = this.song[this.songIndex];
    this.songRepeatLeft = Math.max(0, (entry.repeats ?? 1) - 1);
    this.select(entry.patternId);
  }

  addToSong(patternId, repeats = 1) {
    this.song.push({ patternId, repeats: Math.max(1, repeats | 0) });
  }

  clearSong() { this.song = []; this.songIndex = 0; this.songRepeatLeft = 0; }

  setMode(mode) { this.mode = mode; }

  defaultName(prefix = 'Pattern') { return `${prefix} ${this.patterns.length + 1}`; }

  captureIntoCurrent() {
    if (!this.currentId) return;
    const p = this.patterns.find(pp => pp.id === this.currentId);
    if (!p) return;
    p.data = this.tm.serialize();
  }

  serialize() {
    return {
      patterns: this.patterns,
      currentId: this.currentId,
      queuedId: this.queuedId,
      song: this.song,
      songIndex: this.songIndex,
      songRepeatLeft: this.songRepeatLeft,
      mode: this.mode,
    };
  }

  load(data, autoSelect = true) {
    this.patterns = data.patterns || [];
    this.currentId = data.currentId || this.patterns[0]?.id || null;
    this.queuedId = data.queuedId || null;
    this.song = data.song || [];
    this.songIndex = data.songIndex || 0;
    this.songRepeatLeft = data.songRepeatLeft || 0;
    this.mode = data.mode || 'pattern';
    if (this.currentId && autoSelect) {
      const pat = this.patterns.find(p => p.id === this.currentId);
      if (pat) {
        this.tm.load(pat.data);
        const steps = pat.data?.steps ?? 16;
        this.tm.transport?.setSteps?.(steps);
        this.onSelected?.(pat);
      }
    }
  }
}

