import { initTransport } from './transport.js';
import { initMidi } from './midi.js';
import { TrackManager } from './tracks.js';
import { Visualizer } from './visualizer.js';
import { PatternBank } from './patterns.js';
import { initAudio } from './audio.js';

const stateKey = 'algosynth-state-v1';

const playToggle = document.getElementById('playToggle');
const bpmInput = document.getElementById('bpm');
const swingInput = document.getElementById('swing');
const stepsInput = document.getElementById('steps');
const panicBtn = document.getElementById('panic');
const midiOutSelect = document.getElementById('midiOut');
const addPercBtn = document.getElementById('addPerc');
const addMelodicBtn = document.getElementById('addMelodic');
const saveBtn = document.getElementById('saveState');
const loadBtn = document.getElementById('loadState');
const clearBtn = document.getElementById('clearState');
const tracksContainer = document.getElementById('tracksContainer');
const newPatternBtn = document.getElementById('newPattern');
const dupPatternBtn = document.getElementById('dupPattern');
const renamePatternBtn = document.getElementById('renamePattern');
const deletePatternBtn = document.getElementById('deletePattern');
const patternList = document.getElementById('patternList');
const queueNextBtn = document.getElementById('queueNext');
const playModeSel = document.getElementById('playMode');
const addToSongBtn = document.getElementById('addToSong');
const songRepeatsInput = document.getElementById('songRepeats');
const songList = document.getElementById('songList');
const clearSongBtn = document.getElementById('clearSong');

const visualizer = new Visualizer(document.getElementById('viz'));
const transport = initTransport({ onTick: handleTick, onLoop: handleLoop });

const rawMidi = await initMidi(midiOutSelect);
const audio = initAudio(transport.ctx);

// The original app is MIDI-only, which is silence without a device attached.
// This tee keeps MIDI intact and plays the same events through Web Audio.
const audioToggle = document.getElementById('audioToggle');
let audioOn = true;
const midi = {
  noteOn(note, velocity = 100, channel = 0, whenMs){
    rawMidi.noteOn(note, velocity, channel, whenMs);
    if (audioOn) audio.noteOn(note, velocity, channel, whenMs);
  },
  noteOff(note, channel = 0, whenMs){
    rawMidi.noteOff(note, channel, whenMs);
    if (audioOn) audio.noteOff(note, channel, whenMs);
  },
  cc: (...a) => rawMidi.cc(...a),
  program: (...a) => rawMidi.program(...a),
  allNotesOff(){ rawMidi.allNotesOff(); audio.allNotesOff(); },
};
if (audioToggle){
  audioToggle.addEventListener('click', () => {
    audioOn = !audioOn;
    audioToggle.setAttribute('aria-pressed', String(audioOn));
    if (!audioOn) audio.allNotesOff();
  });
  audioToggle.setAttribute('aria-pressed', 'true');
}
const trackManager = new TrackManager(tracksContainer, { midi, visualizer, transport });
const patterns = new PatternBank(trackManager);
patterns.onSelected = () => {
  stepsInput.value = String(transport.steps);
  renderPatterns();
};
trackManager.onChanged = () => {
  patterns.captureIntoCurrent();
};

function handleTick(stepIndex, stepTimeMs) {
  trackManager.onTick(stepIndex, stepTimeMs);
}
function handleLoop(loopCount) {
  patterns.onPatternEnd();
}

function bindUI() {
  playToggle.addEventListener('click', async () => {
    await transport.toggle();
    playToggle.textContent = transport.isPlaying
      ? (playToggle.dataset.pause || 'Pause')
      : (playToggle.dataset.play || 'Play');
    playToggle.setAttribute('aria-pressed', String(transport.isPlaying));
  });

  bpmInput.addEventListener('input', () => {
    const bpm = Number(bpmInput.value) || 120;
    transport.setBpm(bpm);
  });
  swingInput.addEventListener('input', () => {
    const swing = Number(swingInput.value) || 0;
    transport.setSwing(swing);
  });
  stepsInput.addEventListener('input', () => {
    const steps = Math.max(8, Math.min(64, Number(stepsInput.value) || 16));
    transport.setSteps(steps);
    trackManager.setSteps(steps);
  });

  panicBtn.addEventListener('click', () => {
    midi.allNotesOff();
  });

  addPercBtn.addEventListener('click', () => {
    trackManager.addTrack({ type: 'percussion' });
  });

  addMelodicBtn.addEventListener('click', () => {
    trackManager.addTrack({ type: 'melodic' });
  });

  // Patterns
  newPatternBtn.addEventListener('click', () => {
    // capture current as new pattern
    const p = patterns.create();
    renderPatterns();
    selectPatternInList(p.id);
    // Clear the current scene for a fresh start
    trackManager.clear();
    stepsInput.value = String(transport.steps);
  });
  dupPatternBtn.addEventListener('click', () => {
    const sel = currentPatternIdFromList();
    if (!sel) return;
    // First capture current state into the selected pattern
    patterns.captureIntoCurrent();
    // Then duplicate it
    const p = patterns.duplicate(sel);
    if (p) { renderPatterns(); selectPatternInList(p.id); }
  });
  renamePatternBtn.addEventListener('click', () => {
    const sel = currentPatternIdFromList();
    if (!sel) return;
    const name = prompt('Pattern name', currentPatternName(sel));
    if (name) { patterns.rename(sel, name); renderPatterns(); selectPatternInList(sel); }
  });
  deletePatternBtn.addEventListener('click', () => {
    const sel = currentPatternIdFromList();
    if (!sel) return;
    patterns.remove(sel); renderPatterns(); renderSong();
  });
  patternList.addEventListener('change', () => {
    const id = currentPatternIdFromList();
    if (!id) return;
    patterns.select(id);
  });
  queueNextBtn.addEventListener('click', () => {
    const id = currentPatternIdFromList(); if (!id) return; patterns.queue(id);
  });

  // Song
  playModeSel.addEventListener('change', () => {
    patterns.setMode(playModeSel.value);
    if (playModeSel.value === 'song' && patterns.song.length > 0) {
      const entry = patterns.song[0];
      patterns.songIndex = 0;
      patterns.songRepeatLeft = Math.max(0, (entry.repeats ?? 1) - 1);
      patterns.select(entry.patternId);
      renderPatterns();
      renderSong();
    }
  });
  addToSongBtn.addEventListener('click', () => {
    const id = currentPatternIdFromList(); if (!id) return;
    const reps = Number(songRepeatsInput.value) || 1;
    patterns.addToSong(id, reps);
    renderSong();
  });
  clearSongBtn.addEventListener('click', () => { patterns.clearSong(); renderSong(); });

  saveBtn.addEventListener('click', () => {
    const data = {
      transport: { steps: transport.steps, bpm: transport.bpm, swing: transport.swing },
      scene: trackManager.serialize(),
      patterns: patterns.serialize(),
    };
    localStorage.setItem(stateKey, JSON.stringify(data));
    flash(saveBtn);
  });
  loadBtn.addEventListener('click', () => {
    const raw = localStorage.getItem(stateKey);
    if (raw) {
      const data = JSON.parse(raw);
      // Load patterns first, then scene
      if (data.patterns) {
        patterns.load(data.patterns, false); // Don't auto-select during load
        renderPatterns();
        renderSong();
      }
      // Load scene data
      trackManager.load(data.scene || data);
      // Update transport controls
      if (data.transport) {
        transport.setSteps(data.transport.steps ?? 16);
        transport.setBpm(data.transport.bpm ?? 120);
        transport.setSwing(data.transport.swing ?? 0);
        bpmInput.value = String(transport.bpm);
        swingInput.value = String(transport.swing);
      } else {
        transport.setSteps(data.steps ?? 16);
      }
      stepsInput.value = String(transport.steps);
      // Update play mode
      if (data.patterns?.mode) {
        playModeSel.value = data.patterns.mode;
      }
      flash(loadBtn);
    }
  });
  clearBtn.addEventListener('click', () => {
    localStorage.removeItem(stateKey);
    flash(clearBtn);
  });
}

function flash(el) {
  el.classList.remove('pulse');
  // force reflow
  void el.offsetWidth;
  el.classList.add('pulse');
}

// Initialize
bindUI();

// Default tracks for demo
trackManager.addTrack({ type: 'percussion', name: 'KICK', midiNote: 36, channel: 9, density: 0.4,
                        euclid: { beats: 4, steps: 16, rotate: 0 } });
trackManager.addTrack({ type: 'percussion', name: 'SNARE', midiNote: 38, channel: 9, density: 0.5,
                        euclid: { beats: 2, steps: 16, rotate: 4 } });
trackManager.addTrack({ type: 'percussion', name: 'HATS', midiNote: 42, channel: 9, density: 0.6,
                        euclid: { beats: 5, steps: 8, rotate: 0 } });
trackManager.addTrack({ type: 'melodic', name: 'MELO', channel: 0 });

// Setup initial pattern bank with one pattern
const firstPattern = patterns.create('Pattern 1');
renderPatterns();
selectPatternInList(firstPattern.id);

function renderPatterns() {
  patternList.innerHTML = '';
  for (const p of patterns.patterns) {
    const opt = document.createElement('option');
    opt.value = p.id; opt.textContent = p.name; if (p.id === patterns.currentId) opt.selected = true;
    patternList.appendChild(opt);
  }
}
function selectPatternInList(id) {
  for (const o of Array.from(patternList.options)) o.selected = (o.value === id);
}
function currentPatternIdFromList() {
  return patternList.value || (patternList.options[0]?.value ?? null);
}
function currentPatternName(id) {
  const p = patterns.patterns.find(p => p.id === id); return p?.name || 'Pattern';
}

function renderSong() {
  songList.innerHTML = '';
  patterns.song.forEach((entry, idx) => {
    const p = patterns.patterns.find(pp => pp.id === entry.patternId);
    const li = document.createElement('li');
    li.textContent = `${idx+1}. ${(p?.name)||'Unknown'} x${entry.repeats}`;
    songList.appendChild(li);
  });
}

