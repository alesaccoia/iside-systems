// Simple step transport with swing

export function initTransport({ onTick, onLoop }) {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  let isPlaying = false;
  let bpm = 120;
  let swing = 0.0; // 0..0.6
  let steps = 16;
  let stepIndex = 0;
  let timerId = null;
  let loopCount = 0;

  function msPerStep() {
    // 16th notes per step by default
    const beatsPerSecond = bpm / 60;
    const sixteenthPerSecond = beatsPerSecond * 4;
    return 1000 / sixteenthPerSecond;
  }

  function scheduleNext() {
    const base = msPerStep();
    const isOdd = stepIndex % 2 === 1;
    const swingOffset = isOdd ? base * swing * 0.5 : 0;
    const delay = base + swingOffset;
    const scheduledAt = performance.now() + delay;

    timerId = setTimeout(() => {
      const next = (stepIndex + 1);
      const wrapped = next % steps;
      if (wrapped === 0 && stepIndex !== 0) {
        loopCount += 1;
        onLoop?.(loopCount);
      }
      stepIndex = wrapped;
      onTick?.(stepIndex, scheduledAt);
      scheduleNext();
    }, delay);
  }

  async function start() {
    if (isPlaying) return;
    await ctx.resume();
    isPlaying = true;
    onTick?.(stepIndex, performance.now());
    scheduleNext();
  }

  function stop() {
    isPlaying = false;
    clearTimeout(timerId);
    timerId = null;
  }

  async function toggle() {
    if (isPlaying) stop(); else await start();
  }

  function setBpm(next) {
    bpm = Math.max(40, Math.min(300, Number(next) || 120));
  }

  function setSwing(next) {
    swing = Math.max(0, Math.min(0.6, Number(next) || 0));
  }

  function setSteps(next) {
    steps = Math.max(8, Math.min(64, Number(next) || 16));
    if (stepIndex >= steps) stepIndex = 0;
  }

  return {
    ctx,
    get isPlaying() { return isPlaying; },
    get bpm() { return bpm; },
    get swing() { return swing; },
    get steps() { return steps; },
    get loopCount() { return loopCount; },
    toggle,
    setBpm,
    setSwing,
    setSteps,
  };
}

