import { rng, type Ctx, type Env } from "./core";
import type { Film } from "./film";

// CAN YOUR PC RUN GTA 6? · neon breakdown, 9x16. The PS5 as the benchmark, part by part, each card
// popping in on the word that names it. Our own synthwave sunset city as the backdrop: no game
// footage, no product photos; every icon is drawn here. Narration and captions are added after
// render (pcspecs/vo), timed to the chapter table and the cue frames below.

const W = 1080, H = 1920, FPS = 30, N = 1425;
const CH = [0, 170, 415, 715, 840, 1030, 1140, 1275, N];          // chapter boundaries, frames
const CUE = { ps5: 94, ryzen: 308, gpuEq: 508, r3060: 643, hdd: 943, nvme: 976, m1: 1044, r4070: 1200, ram32: 1242, specs: 1384 };
const CYAN = "#5ef2ff", PINK = "#ff4fd8", GREEN = "#7dff8a", YEL = "#ffd84d", ORANGE = "#ffa24d", RED = "#ff5a5a", WHITE = "#f5f2ff";
const F = (px: number, w = 900) => `${w} ${px}px "Inter Display", Inter, sans-serif`;
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const easeOut = (t: number) => 1 - Math.pow(1 - clamp(t), 3);
const back = (t: number) => { t = clamp(t); const s = 1.7; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };

// ---------------------------------------------------------------- backdrop: a synthwave dusk over our own city
const backdrop = (c: Ctx, f: number) => {
  const sky = c.createLinearGradient(0, 0, 0, 1180);
  sky.addColorStop(0, "#0b0620"); sky.addColorStop(0.55, "#2a0b45"); sky.addColorStop(1, "#5a1450");
  c.fillStyle = sky; c.fillRect(0, 0, W, H);
  const r = rng(3);   // stars
  for (let i = 0; i < 120; i++) { const x = r() * W, y = r() * 900, tw = 0.35 + 0.65 * Math.abs(Math.sin(f * 0.05 + i)); c.globalAlpha = 0.25 * tw; c.fillStyle = WHITE; c.fillRect(x, y, 2.2, 2.2); }
  c.globalAlpha = 1;
  // the sun, striped, sinking very slowly
  const sy = 1050 + f * 0.02, sr = 300, sg = c.createLinearGradient(0, sy - sr, 0, sy + sr);
  sg.addColorStop(0, "#ffd84d"); sg.addColorStop(0.5, "#ff6a8a"); sg.addColorStop(1, "#c42fd1");
  c.save(); c.beginPath(); c.arc(540, sy, sr, 0, Math.PI * 2); c.clip(); c.fillStyle = sg; c.fillRect(240, sy - sr, 600, sr * 2);
  c.fillStyle = "#2a0b45"; for (let i = 0; i < 9; i++) { const yy = sy - 20 + i * 34, h = 3 + i * 2.4; c.fillRect(240, yy, 600, h); }
  c.restore();
  // skyline: blocks with lit windows, then palms
  const sk = rng(9); c.fillStyle = "#14082a";
  let x = -20; const blocks: [number, number, number][] = [];
  while (x < W + 20) { const bw = 50 + sk() * 90, bh = 120 + sk() * 330; blocks.push([x, bw, bh]); c.fillRect(x, 1180 - bh, bw, bh); x += bw + 4; }
  blocks.forEach(([bx, bw, bh], i) => { const wr = rng(100 + i); for (let yy = 1180 - bh + 14; yy < 1170; yy += 22) for (let xx = bx + 8; xx < bx + bw - 10; xx += 16) if (wr() < 0.28) { c.globalAlpha = 0.5 + 0.4 * Math.sin(f * 0.02 + xx); c.fillStyle = wr() < 0.5 ? "#ff9bd8" : "#9bf1ff"; c.fillRect(xx, yy, 6, 9); } });
  c.globalAlpha = 1;
  const palm = (px: number, s: number) => { c.save(); c.translate(px, 1185); c.scale(s, s); c.strokeStyle = "#0a0418"; c.fillStyle = "#0a0418"; c.lineWidth = 16; c.lineCap = "round"; c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(30, -200, 10, -420); c.stroke();
    for (let k = 0; k < 7; k++) { const a = -Math.PI / 2 + (k - 3) * 0.48 + Math.sin(f * 0.03 + k) * 0.03; c.beginPath(); c.moveTo(10, -420); c.quadraticCurveTo(10 + Math.cos(a - 0.4) * 140, -420 + Math.sin(a - 0.4) * 140, 10 + Math.cos(a) * 250, -420 + Math.sin(a) * 250 + 60); c.lineWidth = 12; c.stroke(); } c.restore(); };
  palm(70, 1.05); palm(1010, 0.9);
  // the grid floor, rushing toward the viewer
  const fl = c.createLinearGradient(0, 1180, 0, H); fl.addColorStop(0, "#1a0630"); fl.addColorStop(1, "#05020d");
  c.fillStyle = fl; c.fillRect(0, 1180, W, H - 1180);
  c.strokeStyle = PINK; c.lineWidth = 2;
  for (let i = -14; i <= 14; i++) { c.globalAlpha = 0.45; c.beginPath(); c.moveTo(540 + i * 30, 1180); c.lineTo(540 + i * 260, H); c.stroke(); }
  const ph = (f % 30) / 30;
  for (let k = 0; k < 14; k++) { const z = (k + ph) / 14, y = 1180 + Math.pow(z, 2.2) * (H - 1180); c.globalAlpha = 0.15 + 0.5 * z; c.beginPath(); c.moveTo(0, y); c.lineTo(W, y); c.stroke(); }
  c.globalAlpha = 1;
  // a veil so the cards read
  c.fillStyle = "rgba(6,2,16,0.45)"; c.fillRect(0, 0, W, H);
};

// ---------------------------------------------------------------- text and pieces
const glowText = (c: Ctx, s: string, x: number, y: number, px: number, col: string, a = 1, sc = 1, align: CanvasTextAlign = "center") => {
  if (a <= 0) return;
  c.save(); c.translate(x, y); c.scale(sc, sc); c.globalAlpha = a; c.font = F(px); c.textAlign = align; c.textBaseline = "middle";
  c.shadowColor = col; c.shadowBlur = px * 0.35; c.fillStyle = col; c.fillText(s, 0, 0);
  c.shadowBlur = 0; c.lineWidth = Math.max(2, px * 0.03); c.strokeStyle = "rgba(255,255,255,0.35)"; c.strokeText(s, 0, 0); c.restore();
};
const rrect = (c: Ctx, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); };
const card = (c: Ctx, x: number, y: number, w: number, h: number, col: string, t: number) => {
  if (t <= 0) return; const s = back(t);
  c.save(); c.translate(x + w / 2, y + h / 2); c.scale(s, s); c.translate(-(x + w / 2), -(y + h / 2)); c.globalAlpha = clamp(t * 3);
  rrect(c, x, y, w, h, 34); c.fillStyle = "rgba(14,6,34,0.82)"; c.fill();
  c.shadowColor = col; c.shadowBlur = 26; c.lineWidth = 5; c.strokeStyle = col; c.stroke(); c.restore();
};
const pill = (c: Ctx, s: string, x: number, y: number, px: number, bg: string, fg: string, t: number) => {
  if (t <= 0) return; c.save(); c.font = F(px); const tw = c.measureText(s).width, w = tw + px * 1.3, h = px * 1.55, sc = back(t);
  c.translate(x, y); c.scale(sc, sc); c.globalAlpha = clamp(t * 3); rrect(c, -w / 2, -h / 2, w, h, h / 2); c.shadowColor = bg; c.shadowBlur = 22; c.fillStyle = bg; c.fill();
  c.shadowBlur = 0; c.fillStyle = fg; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(s, 0, px * 0.04); c.restore();
};
const tick = (c: Ctx, x: number, y: number, s: number, col: string, t: number) => { if (t <= 0) return; c.save(); c.strokeStyle = col; c.lineWidth = 12 * s; c.lineCap = "round"; c.shadowColor = col; c.shadowBlur = 18; const p = clamp(t * 1.5);
  c.beginPath(); c.moveTo(x - 30 * s, y); c.lineTo(x - 30 * s + 22 * s * clamp(p * 2), y + 24 * s * clamp(p * 2)); if (p > 0.5) c.lineTo(x - 8 * s + 50 * s * clamp(p * 2 - 1), y + 24 * s - 56 * s * clamp(p * 2 - 1)); c.stroke(); c.restore(); };
const cross = (c: Ctx, x: number, y: number, s: number, t: number) => { if (t <= 0) return; c.save(); c.strokeStyle = RED; c.lineWidth = 14; c.lineCap = "round"; c.shadowColor = RED; c.shadowBlur = 20; const p = clamp(t * 1.4);
  c.beginPath(); c.moveTo(x - s, y - s); c.lineTo(x - s + 2 * s * clamp(p * 2), y - s + 2 * s * clamp(p * 2)); if (p > 0.5) { c.moveTo(x + s, y - s); c.lineTo(x + s - 2 * s * clamp(p * 2 - 1), y - s + 2 * s * clamp(p * 2 - 1)); } c.stroke(); c.restore(); };

// icons, drawn here
const pop = (c: Ctx, x: number, y: number, t: number, fn: () => void) => { if (t <= 0) return; const s = back(t); c.save(); c.translate(x, y); c.scale(s, s); c.globalAlpha = clamp(t * 3); fn(); c.restore(); };
const chip = (c: Ctx, col: string) => { c.lineWidth = 6; c.strokeStyle = col; c.shadowColor = col; c.shadowBlur = 16; rrect(c, -80, -80, 160, 160, 18); c.stroke(); rrect(c, -46, -46, 92, 92, 10); c.stroke();
  for (let i = -3; i <= 3; i++) { const o = i * 20; [[o, -80, o, -104], [o, 80, o, 104], [-80, o, -104, o], [80, o, 104, o]].forEach(([a, b, d, e]) => { c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.stroke(); }); } };
const gpu = (c: Ctx, col: string, f: number) => { c.lineWidth = 6; c.strokeStyle = col; c.shadowColor = col; c.shadowBlur = 16; rrect(c, -190, -70, 380, 140, 20); c.stroke();
  [-90, 90].forEach((fx) => { c.beginPath(); c.arc(fx, 0, 52, 0, Math.PI * 2); c.stroke(); for (let b = 0; b < 7; b++) { const a = f * 0.25 + (b / 7) * Math.PI * 2; c.beginPath(); c.moveTo(fx, 0); c.quadraticCurveTo(fx + Math.cos(a) * 30, Math.sin(a) * 30 - 10, fx + Math.cos(a + 0.5) * 46, Math.sin(a + 0.5) * 46); c.stroke(); } });
  c.beginPath(); c.moveTo(-170, 70); c.lineTo(-170, 96); c.lineTo(60, 96); c.lineTo(60, 70); c.stroke(); };
const ram = (c: Ctx, col: string) => { c.lineWidth = 6; c.strokeStyle = col; c.shadowColor = col; c.shadowBlur = 16; rrect(c, -220, -45, 440, 90, 10); c.stroke();
  for (let i = 0; i < 6; i++) { rrect(c, -195 + i * 66, -28, 46, 40, 5); c.stroke(); } c.beginPath(); for (let i = 0; i < 24; i++) { c.moveTo(-205 + i * 18, 45); c.lineTo(-205 + i * 18, 58); } c.stroke(); };
const m2 = (c: Ctx, col: string) => { c.lineWidth = 6; c.strokeStyle = col; c.shadowColor = col; c.shadowBlur = 16; rrect(c, -220, -36, 440, 72, 8); c.stroke(); rrect(c, -150, -20, 90, 40, 4); c.stroke(); rrect(c, -30, -20, 90, 40, 4); c.stroke();
  c.beginPath(); c.arc(200, 0, 12, 0, Math.PI * 2); c.stroke(); };
const hdd = (c: Ctx, col: string, f: number) => { c.lineWidth = 6; c.strokeStyle = col; c.shadowColor = col; c.shadowBlur = 12; rrect(c, -110, -140, 220, 280, 16); c.stroke(); c.beginPath(); c.arc(0, -20, 80, 0, Math.PI * 2); c.stroke(); c.beginPath(); c.arc(0, -20, 14, 0, Math.PI * 2); c.stroke();
  c.save(); c.translate(70, 90); c.rotate(-0.9 + Math.sin(f * 0.2) * 0.05); c.beginPath(); c.moveTo(0, 0); c.lineTo(-10, -110); c.stroke(); c.restore(); };
const consoleIcon = (c: Ctx) => {   // a generic white tower, labelled; not a likeness of any product
  c.save(); c.shadowColor = "#bfe8ff"; c.shadowBlur = 30; c.fillStyle = "#f2f6ff"; c.beginPath(); c.moveTo(-70, -240); c.quadraticCurveTo(-120, -60, -80, 240); c.lineTo(80, 240); c.quadraticCurveTo(120, -60, 70, -240); c.closePath(); c.fill();
  c.shadowBlur = 0; c.fillStyle = "#151024"; c.fillRect(-26, -240, 52, 480); c.fillStyle = CYAN; c.fillRect(-26, -200, 6, 380); c.fillRect(20, -200, 6, 380);
  c.fillStyle = "#1a1230"; c.fillRect(-130, 240, 260, 24); c.restore(); };

const badge = (c: Ctx, f: number) => pill(c, "PS5 HARDWARE ESTIMATE", 540, 90, 30, YEL, "#1a0b00", clamp((f - CH[1]) / 10));
const header = (c: Ctx, s: string, local: number, col = CYAN, y = 205, px = 108) => glowText(c, s, 540, y, px, col, clamp(local / 6), back(local / 9));
const count = (to: number, dec: number, t: number) => (to * easeOut(t)).toFixed(dec);

// ---------------------------------------------------------------- chapters
const draw = (ctx: Ctx, f: number, env: Env) => {
  const c = ctx; ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  backdrop(c, f);
  const k = CH.findIndex((b, i) => f >= b && f < CH[i + 1]), local = f - CH[k], since = (cue: number) => (f - cue) / 9;
  if (k >= 1) badge(c, f);
  switch (k) {
    case 0: {
      glowText(c, "CAN YOUR PC", 540, 250, 104, WHITE, clamp(local / 6), back(local / 9));
      glowText(c, "RUN GTA 6?", 540, 380, 132, YEL, clamp((local - 6) / 6), back((local - 6) / 9));
      pop(c, 540, 820, since(CUE.ps5), () => consoleIcon(c));
      if (f >= CUE.ps5) { glowText(c, "PS5", 540, 1140, 84, WHITE, clamp(since(CUE.ps5))); pill(c, "THE BENCHMARK", 540, 1250, 40, CYAN, "#05101a", since(CUE.ps5 + 12)); }
      break;
    }
    case 1: {
      header(c, "CPU", local);
      card(c, 110, 300, 860, 470, CYAN, (local - 4) / 10);
      if (local > 6) { const t = (local - 6) / 30; glowText(c, "PS5 CPU", 540, 360, 34, CYAN, clamp(t * 4));
        glowText(c, `${Math.round(8 * easeOut(t))} CORES`, 540, 470, 104, GREEN, clamp(t * 4)); glowText(c, "ZEN 2", 540, 590, 96, GREEN, clamp(t * 4 - 0.6)); glowText(c, "UP TO 3.5 GHZ", 540, 700, 72, GREEN, clamp(t * 4 - 1.2)); }
      pop(c, 300, 1010, since(CUE.ryzen), () => chip(c, ORANGE));
      pill(c, "= RYZEN 7 3700X", 650, 1010, 46, ORANGE, "#1a0b00", since(CUE.ryzen + 4));
      glowText(c, "ON PC, ABOUT", 650, 920, 36, WHITE, clamp(since(CUE.ryzen + 4)));
      break;
    }
    case 2: {
      header(c, "GPU", local);
      card(c, 110, 300, 860, 360, PINK, (local - 4) / 10);
      if (local > 6) { const t = (local - 6) / 30; glowText(c, "PS5 GPU", 540, 360, 34, PINK, clamp(t * 4)); glowText(c, count(10.3, 1, t), 540, 480, 150, GREEN, clamp(t * 4)); glowText(c, "TERAFLOPS", 540, 600, 60, GREEN, clamp(t * 4 - 0.6)); }
      pop(c, 540, 820, since(CUE.gpuEq), () => gpu(c, PINK, f));
      pill(c, "RX 6700", 330, 1010, 44, PINK, "#1a0010", since(CUE.gpuEq + 6)); pill(c, "RTX 2070 SUPER", 700, 1010, 44, PINK, "#1a0010", since(CUE.gpuEq + 12));
      pill(c, "RTX 3060", 470, 1140, 52, GREEN, "#001a05", since(CUE.r3060)); tick(c, 680, 1132, 1.1, GREEN, since(CUE.r3060 + 6));
      glowText(c, "SAME LEAGUE", 540, 1240, 40, WHITE, clamp(since(CUE.r3060 + 10)));
      break;
    }
    case 3: {
      header(c, "MEMORY", local, YEL);
      card(c, 110, 300, 860, 380, YEL, (local - 4) / 10);
      if (local > 6) { const t = (local - 6) / 24; glowText(c, "PS5 · SHARED GDDR6", 540, 360, 34, YEL, clamp(t * 4)); glowText(c, `${Math.round(16 * easeOut(t))} GB`, 540, 500, 170, GREEN, clamp(t * 4)); }
      pop(c, 540, 840, (local - 40) / 9, () => ram(c, YEL));
      pill(c, "GET 16 GB RAM", 540, 1010, 54, YEL, "#1a0b00", (local - 60) / 9);
      break;
    }
    case 4: {
      header(c, "STORAGE", local, CYAN);
      card(c, 110, 300, 860, 360, CYAN, (local - 4) / 10);
      if (local > 6) { const t = (local - 6) / 26; glowText(c, "PS5 SSD READS", 540, 360, 34, CYAN, clamp(t * 4)); glowText(c, count(5.5, 1, t), 540, 480, 150, GREEN, clamp(t * 4)); glowText(c, "GB PER SECOND", 540, 600, 56, GREEN, clamp(t * 4 - 0.6)); }
      pop(c, 300, 900, since(CUE.hdd), () => hdd(c, "#b9a9d6", f)); cross(c, 300, 880, 120, since(CUE.hdd + 6));
      glowText(c, "HDD", 300, 1090, 44, RED, clamp(since(CUE.hdd + 6)));
      pop(c, 730, 880, since(CUE.nvme), () => { c.rotate(-0.25); c.scale(0.75, 0.75); m2(c, GREEN); });
      pill(c, "NVME SSD", 730, 1010, 50, GREEN, "#001a05", since(CUE.nvme + 5));
      break;
    }
    case 5: {
      header(c, "MINIMUM", local, YEL);
      pill(c, "1080P · ~30 FPS", 540, 330, 42, YEL, "#1a0b00", (local - 4) / 9);
      const rows: [string, string, string][] = [["CPU", "RYZEN 7 3700X", ORANGE], ["GPU", "RTX 3060 / RX 6700", PINK], ["RAM", "16 GB", YEL], ["SSD", "NVME", GREEN]];
      rows.forEach(([a, b, col], i) => { const t = (local - 10 - i * 8) / 9; if (t <= 0) return; const y = 470 + i * 150, sx = 1 - easeOut(t);
        c.save(); c.translate(sx * -600, 0); c.globalAlpha = clamp(t * 2); rrect(c, 110, y - 55, 860, 110, 22); c.fillStyle = "rgba(14,6,34,0.85)"; c.fill(); c.shadowColor = col; c.shadowBlur = 18; c.lineWidth = 4; c.strokeStyle = col; c.stroke(); c.restore();
        pill(c, a, 210, y, 34, col, "#0b0418", t); glowText(c, b, 300, y, 50, WHITE, clamp(t * 2), 1, "left"); });
      break;
    }
    case 6: {
      header(c, "WANT 60 FPS?", local, GREEN, 210, 112);
      pop(c, 540, 600, since(CUE.r4070), () => { c.scale(1.4, 1.4); gpu(c, GREEN, f); });
      pill(c, "RTX 4070", 540, 850, 64, GREEN, "#001a05", since(CUE.r4070 + 6));
      pop(c, 540, 1040, since(CUE.ram32), () => ram(c, YEL)); pill(c, "32 GB RAM", 540, 1170, 54, YEL, "#1a0b00", since(CUE.ram32 + 5));
      break;
    }
    case 7: {
      header(c, "ESTIMATES ONLY", local, ORANGE, 230, 96);
      card(c, 110, 340, 860, 300, ORANGE, (local - 4) / 10);
      glowText(c, "NO PC VERSION", 540, 440, 72, WHITE, clamp((local - 8) / 6)); glowText(c, "ANNOUNCED YET", 540, 540, 72, WHITE, clamp((local - 12) / 6));
      glowText(c, "DROP YOUR SPECS", 540, 860, 80, YEL, clamp(since(CUE.specs)), back(since(CUE.specs)));
      if (f >= CUE.specs) { const b = Math.sin((f - CUE.specs) * 0.3) * 14; c.save(); c.strokeStyle = YEL; c.lineWidth = 12; c.lineCap = "round"; c.shadowColor = YEL; c.shadowBlur = 18; c.beginPath(); c.moveTo(540, 960 + b); c.lineTo(540, 1110 + b); c.moveTo(480, 1050 + b); c.lineTo(540, 1110 + b); c.lineTo(600, 1050 + b); c.stroke(); c.restore(); }
      break;
    }
  }
};

export const pcspecs: Film = {
  meta: { title: "Can your PC run GTA 6? · neon breakdown", W, H, fps: FPS, bpm: 120, durationFrames: N },
  assets: { images: {} },
  shots: [{ id: "breakdown", start: 0, end: N, draw }],
};
