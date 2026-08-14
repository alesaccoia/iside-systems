export class VisualEngine {
  constructor(canvas) {
    this.canvas = canvas;
    this.offscreen = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { alpha: false });
    this.offCtx = this.offscreen.getContext("2d", { alpha: true });
    this.running = false;
    this.parameters = {
      pattern: "lines",
      density: 200,
      angleDeltaDegrees: 2,
      scaleDelta: 0.01,
      rotationSpeed: 0.2,
      invert: false,
      animate: true,
    };
    this.state = {
      rotationRadians: 0,
      lastTimestampMs: 0,
    };
    this.resize();
  }

  setParameters(newParams) {
    this.parameters = { ...this.parameters, ...newParams };
  }

  isRunning() {
    return this.running;
  }

  start() {
    if (this.running) return;
    this.running = true;
    this.state.lastTimestampMs = performance.now();
    const loop = (t) => {
      if (!this.running) return;
      const dt = Math.max(0, Math.min(0.05, (t - this.state.lastTimestampMs) / 1000));
      this.state.lastTimestampMs = t;
      this.update(dt);
      this.draw();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  stop() {
    this.running = false;
  }

  resize() {
    const dpr = Math.max(1, Math.min(3, window.devicePixelRatio || 1));
    const { innerWidth: w, innerHeight: h } = window;
    this.canvas.width = Math.floor(w * dpr);
    this.canvas.height = Math.floor(h * dpr);
    this.canvas.style.width = `${w}px`;
    this.canvas.style.height = `${h}px`;
    this.ctx.setTransform(1, 0, 0, 1, 0, 0);
    this.ctx.scale(dpr, dpr);
    this.offscreen.width = Math.max(512, Math.ceil(w * dpr));
    this.offscreen.height = Math.max(512, Math.ceil(h * dpr));
    // ensure crisp lines
    this.ctx.imageSmoothingEnabled = false;
    this.offCtx.imageSmoothingEnabled = false;
  }

  update(dtSeconds) {
    if (!this.parameters.animate) return;
    const degreesPerSecond = this.parameters.rotationSpeed * 20;
    this.state.rotationRadians += (degreesPerSecond * Math.PI / 180) * dtSeconds;
  }

  draw() {
    const ctx = this.ctx;
    const w = this.canvas.clientWidth;
    const h = this.canvas.clientHeight;
    const cx = w / 2;
    const cy = h / 2;

    const bg = this.parameters.invert ? "#fff" : "#000";
    const fg = this.parameters.invert ? "#000" : "#fff";
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // Prepare pattern
    const patternCanvas = this.offscreen;
    const pctx = this.offCtx;
    pctx.setTransform(1, 0, 0, 1, 0, 0);
    pctx.clearRect(0, 0, patternCanvas.width, patternCanvas.height);
    pctx.fillStyle = this.parameters.invert ? "#fff" : "#000";
    pctx.fillRect(0, 0, patternCanvas.width, patternCanvas.height);
    pctx.strokeStyle = fg;
    pctx.lineWidth = 1;
    pctx.globalCompositeOperation = "source-over";

    this._drawBasePattern(pctx, patternCanvas.width, patternCanvas.height, fg);

    // Draw two layers with slight transform offsets to produce moiré
    ctx.save();
    ctx.translate(cx, cy);

    const angleA = 0;
    const angleB = this.parameters.angleDeltaDegrees * Math.PI / 180 + this.state.rotationRadians;
    const scaleA = 1;
    const scaleB = 1 + this.parameters.scaleDelta;

    // Layer A
    ctx.save();
    ctx.rotate(angleA);
    ctx.scale(scaleA, scaleA);
    ctx.drawImage(
      patternCanvas,
      0,
      0,
      patternCanvas.width,
      patternCanvas.height,
      -w / 2,
      -h / 2,
      w,
      h
    );
    ctx.restore();

    // Layer B
    ctx.globalAlpha = 0.75;
    ctx.save();
    ctx.rotate(angleB);
    ctx.scale(scaleB, scaleB);
    ctx.drawImage(
      patternCanvas,
      0,
      0,
      patternCanvas.width,
      patternCanvas.height,
      -w / 2,
      -h / 2,
      w,
      h
    );
    ctx.restore();
    ctx.globalAlpha = 1;

    ctx.restore();
  }

  _drawBasePattern(pctx, w, h, fg) {
    const pattern = this.parameters.pattern;
    const density = this.parameters.density;
    if (pattern === "lines") {
      this._drawLines(pctx, w, h, density, fg);
    } else if (pattern === "grid") {
      this._drawGrid(pctx, w, h, density, fg);
    } else if (pattern === "circles") {
      this._drawCircles(pctx, w, h, density, fg);
    } else if (pattern === "radial") {
      this._drawRadial(pctx, w, h, density, fg);
    }
  }

  _drawLines(pctx, w, h, density, fg) {
    const spacing = Math.max(2, Math.min(200, Math.floor((w + h) / density)));
    pctx.beginPath();
    for (let y = 0; y < h; y += spacing) {
      pctx.moveTo(0, y + 0.5);
      pctx.lineTo(w, y + 0.5);
    }
    pctx.stroke();
  }

  _drawGrid(pctx, w, h, density, fg) {
    const spacing = Math.max(4, Math.min(200, Math.floor((w + h) / density)));
    pctx.beginPath();
    for (let y = 0; y < h; y += spacing) {
      pctx.moveTo(0, y + 0.5);
      pctx.lineTo(w, y + 0.5);
    }
    for (let x = 0; x < w; x += spacing) {
      pctx.moveTo(x + 0.5, 0);
      pctx.lineTo(x + 0.5, h);
    }
    pctx.stroke();
  }

  _drawCircles(pctx, w, h, density, fg) {
    const cx = w / 2;
    const cy = h / 2;
    const maxR = Math.sqrt(cx * cx + cy * cy);
    const spacing = Math.max(1.5, Math.min(80, Math.floor(maxR / (density / 2))));
    pctx.beginPath();
    for (let r = 4; r < maxR; r += spacing) {
      pctx.moveTo(cx + r, cy);
      pctx.arc(cx, cy, r, 0, Math.PI * 2);
    }
    pctx.stroke();
  }

  _drawRadial(pctx, w, h, density, fg) {
    const cx = w / 2;
    const cy = h / 2;
    const lines = Math.max(12, Math.min(2000, density));
    const radius = Math.sqrt(cx * cx + cy * cy) + 10;
    pctx.beginPath();
    for (let i = 0; i < lines; i++) {
      const a = (i / lines) * Math.PI * 2;
      const x = cx + Math.cos(a) * radius;
      const y = cy + Math.sin(a) * radius;
      pctx.moveTo(cx + 0.5, cy + 0.5);
      pctx.lineTo(x + 0.5, y + 0.5);
    }
    pctx.stroke();
  }
}

