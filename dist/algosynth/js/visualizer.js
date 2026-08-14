export class Visualizer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    window.addEventListener('resize', () => this.resize());
    this.resize();
    requestAnimationFrame(() => this.draw());
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = Math.floor(window.innerWidth * dpr);
    this.canvas.height = Math.floor(window.innerHeight * dpr);
    this.canvas.style.width = window.innerWidth + 'px';
    this.canvas.style.height = window.innerHeight + 'px';
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  ping({ hue = 0, energy = 0.5, x = 0.5 }) {
    const cx = x * window.innerWidth;
    const cy = window.innerHeight * (0.4 + Math.random() * 0.4);
    const count = 6 + Math.floor(energy * 24);
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: cx + (Math.random() - 0.5) * 30,
        y: cy + (Math.random() - 0.5) * 20,
        vx: (Math.random() - 0.5) * 1.6,
        vy: -0.5 - Math.random() * 1.5,
        life: 1,
        hue,
      });
    }
  }

  draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
    // background grid
    ctx.strokeStyle = 'rgba(255,255,255,0.045)';
    ctx.lineWidth = 1;
    const grid = 24;
    for (let x = 0; x < window.innerWidth; x += grid) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, window.innerHeight); ctx.stroke();
    }
    for (let y = 0; y < window.innerHeight; y += grid) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(window.innerWidth, y); ctx.stroke();
    }

    // particles
    for (const p of this.particles) {
      ctx.fillStyle = `hsla(${p.hue}, 80%, 60%, ${p.life * 0.6})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2 + 3 * (1 - p.life), 0, Math.PI * 2);
      ctx.fill();
      p.x += p.vx; p.y += p.vy; p.vy += 0.02; p.life -= 0.02;
    }
    this.particles = this.particles.filter(p => p.life > 0);

    requestAnimationFrame(() => this.draw());
  }
}

