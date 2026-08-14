export async function initMidi(outputSelectEl) {
  let midiAccess = null;
  let output = null;
  let outputs = [];

  async function request() {
    try {
      midiAccess = await navigator.requestMIDIAccess();
      refreshOutputs();
    } catch (e) {
      console.warn('WebMIDI not available', e);
    }
  }

  function refreshOutputs() {
    outputs = [];
    outputSelectEl.innerHTML = '';
    if (!midiAccess) return;
    midiAccess.outputs.forEach((out) => {
      outputs.push(out);
    });
    outputs.forEach((out, idx) => {
      const opt = document.createElement('option');
      opt.value = String(idx);
      opt.textContent = out.name || `OUT ${idx}`;
      outputSelectEl.appendChild(opt);
    });
    output = outputs[0] || null;
    outputSelectEl.addEventListener('change', () => {
      const idx = Number(outputSelectEl.value);
      output = outputs[idx] || null;
    });
  }

  function send(message, timestampMs) {
    if (!output) return;
    output.send(message, timestampMs);
  }

  function noteOn(note, velocity = 100, channel = 0, whenMs) {
    const status = 0x90 + (channel & 0x0f);
    send([status, note & 0x7f, velocity & 0x7f], whenMs);
  }
  function noteOff(note, channel = 0, whenMs) {
    const status = 0x80 + (channel & 0x0f);
    send([status, note & 0x7f, 0x00], whenMs);
  }
  function cc(controller, value, channel = 0, whenMs) {
    const status = 0xB0 + (channel & 0x0f);
    send([status, controller & 0x7f, value & 0x7f], whenMs);
  }
  function program(number, channel = 0, whenMs) {
    const status = 0xC0 + (channel & 0x0f);
    send([status, number & 0x7f], whenMs);
  }
  function allNotesOff() {
    for (let ch = 0; ch < 16; ch++) {
      cc(123, 0, ch);
    }
  }

  await request();

  return { noteOn, noteOff, cc, program, allNotesOff };
}

