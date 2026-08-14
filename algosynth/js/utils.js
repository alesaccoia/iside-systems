// Tiny deterministic PRNG (Mulberry32)
export function prng(seed) {
  let s = seed ?? Math.floor(Math.random() * 0x7fffffff);
  return function next() {
    s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

