import { rng, type Ctx, type Env } from "./core";
import type { Film } from "./film";

// BREAKDOWN · a data-driven explainer in a colourful sticker style, 9x16. Organic backdrop (drifting
// colour blobs, doodles that boil like stop-motion, paper grain), white sticker cards with a fat
// outline and a hard coloured shadow, everything popping in on the word that names it. One spec per
// video (bd-*.json, written from the narration's word timings); narration and captions added after.

export type Item =
  | { t: "head"; text: string; cue: number; color?: string; size?: number }
  | { t: "big"; text: string; sub?: string; cue: number; color?: string; count?: number; dec?: number; suffix?: string }
  | { t: "pills"; pills: { text: string; cue: number; color?: string; mark?: "check" | "cross" }[]; size?: number }
  | { t: "icon"; name: string; cue: number; color?: string; mark?: "cross" | "check"; markCue?: number; scale?: number }
  | { t: "text"; text: string; cue: number; size?: number; color?: string }
  | { t: "list"; rows: { label: string; text: string; cue: number; color?: string; mark?: "check" | "cross" }[] }
  | { t: "arrow"; cue: number; color?: string };
export type Scene = { a: number; b: number; items: Item[] };
export type Spec = { title: string; N: number; pal: { bg: [string, string]; blobs: string[]; accent: string[] }; scenes: Scene[] };

const W = 1080, H = 1920, INK = "#1d1433", PAPER = "#fffaf0";
const F = (px: number) => `900 ${px}px "Inter Display", Inter, sans-serif`;
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const back = (t: number) => { t = clamp(t); const s = 2.2; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };
const easeOut = (t: number) => 1 - Math.pow(1 - clamp(t), 3);
const POP = 10;   // frames an item takes to pop

// ---------------------------------------------------------------- backdrop
const backdrop = (c: Ctx, f: number, s: Spec, scene: number) => {
  const g = c.createLinearGradient(0, 0, W * 0.3, H); g.addColorStop(0, s.pal.bg[0]); g.addColorStop(1, s.pal.bg[1]);
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  s.pal.blobs.forEach((col, i) => {   // big soft blobs drifting on slow, different orbits
    const r = rng(40 + i), ph = r() * 6.28, sp = 0.004 + r() * 0.004;
    const x = W * (0.2 + 0.6 * r()) + Math.sin(f * sp + ph) * 220, y = H * (0.15 + 0.7 * r()) + Math.cos(f * sp * 1.3 + ph) * 260, rad = 380 + r() * 260;
    const rg = c.createRadialGradient(x, y, 0, x, y, rad); rg.addColorStop(0, col + "ee"); rg.addColorStop(0.55, col + "77"); rg.addColorStop(1, col + "00");
    c.fillStyle = rg; c.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  });
  const boil = Math.floor(f / 4);   // stop-motion boil: doodles redraw every 4 frames with a new wobble
  const dr = rng(900 + scene * 13);
  for (let i = 0; i < 9; i++) {
    const x = dr() < 0.5 ? 40 + dr() * 200 : 840 + dr() * 200, y = 120 + dr() * 1650, kind = Math.floor(dr() * 4), col = s.pal.accent[i % s.pal.accent.length], sz = 26 + dr() * 34, rot = dr() * 6;
    const w = rng(boil * 31 + i), j = () => (w() - 0.5) * 4;
    c.save(); c.translate(x, y); c.rotate(rot + Math.sin(f * 0.02 + i) * 0.15); c.strokeStyle = col; c.fillStyle = col; c.lineWidth = 7; c.lineCap = "round"; c.lineJoin = "round"; c.globalAlpha = 0.85;
    c.beginPath();
    if (kind === 0) { for (let k = 0; k <= 10; k++) { const a = -Math.PI / 2 + (k / 10) * Math.PI * 2, rr = k % 2 ? sz * 0.42 : sz; k ? c.lineTo(Math.cos(a) * rr + j(), Math.sin(a) * rr + j()) : c.moveTo(Math.cos(a) * rr + j(), Math.sin(a) * rr + j()); } c.closePath(); c.stroke(); }
    else if (kind === 1) { c.moveTo(-sz, 0); for (let k = 1; k <= 6; k++) c.quadraticCurveTo(-sz + (k - 0.5) * sz / 3, (k % 2 ? -1 : 1) * sz * 0.4 + j(), -sz + k * sz / 3, j()); c.stroke(); }
    else if (kind === 2) { c.arc(j(), j(), sz * 0.55, 0, Math.PI * 2); c.stroke(); }
    else { c.moveTo(-sz * 0.6 + j(), j()); c.lineTo(sz * 0.6 + j(), j()); c.moveTo(j(), -sz * 0.6 + j()); c.lineTo(j(), sz * 0.6 + j()); c.stroke(); }
    c.restore();
  }
  const pr = rng(7); c.fillStyle = "#000"; for (let i = 0; i < 2400; i++) { c.globalAlpha = 0.035; c.fillRect(pr() * W, pr() * H, 2, 2); } c.globalAlpha = 1;   // paper grain
};

// ---------------------------------------------------------------- stickers
const rrect = (c: Ctx, x: number, y: number, w: number, h: number, r: number) => { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); };
const sticker = (c: Ctx, cx: number, cy: number, w: number, h: number, shadow: string, fill = PAPER, r = 30) => {
  rrect(c, cx - w / 2 + 10, cy - h / 2 + 12, w, h, r); c.fillStyle = shadow; c.fill();
  rrect(c, cx - w / 2, cy - h / 2, w, h, r); c.fillStyle = fill; c.fill(); c.lineWidth = 7; c.strokeStyle = INK; c.stroke();
};
const popAt = (c: Ctx, f: number, cue: number, cx: number, cy: number, tilt: number, fn: () => void) => {
  const t = (f - cue) / POP; if (t <= 0) return false;
  const s = back(t), sq = 1 + Math.sin(clamp(t) * Math.PI) * 0.06;
  c.save(); c.translate(cx, cy); c.rotate(tilt * (1 - 0.3 * Math.sin(f * 0.05))); c.scale(s * sq, s / sq); c.globalAlpha = clamp(t * 3); fn(); c.restore(); return true;
};
const textW = (c: Ctx, s: string, px: number) => { c.font = F(px); return c.measureText(s).width; };
const inkText = (c: Ctx, s: string, x: number, y: number, px: number, col = INK) => { c.font = F(px); c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = col; c.fillText(s, x, y + px * 0.04); };
const outlined = (c: Ctx, s: string, x: number, y: number, px: number, fill: string, shadow: string) => {
  c.font = F(px); c.textAlign = "center"; c.textBaseline = "middle"; c.lineJoin = "round";
  c.lineWidth = px * 0.22; c.strokeStyle = shadow; c.strokeText(s, x + 8, y + 10); c.fillStyle = shadow; c.fillText(s, x + 8, y + 10);
  c.lineWidth = px * 0.22; c.strokeStyle = INK; c.strokeText(s, x, y); c.fillStyle = fill; c.fillText(s, x, y);
};
const mark = (c: Ctx, kind: "check" | "cross", x: number, y: number, s: number, t: number) => {
  if (t <= 0) return; const p = clamp(t);
  c.save(); c.translate(x, y); c.lineCap = "round"; c.lineJoin = "round";
  const col = kind === "check" ? "#2bd46b" : "#ff4d4d";
  for (const [lw, st] of [[s * 0.34, INK], [s * 0.2, col]] as [number, string][]) {
    c.lineWidth = lw; c.strokeStyle = st; c.beginPath();
    if (kind === "check") { c.moveTo(-s * 0.5, 0); const a = clamp(p * 2), b = clamp(p * 2 - 1); c.lineTo(-s * 0.5 + s * 0.35 * a, s * 0.35 * a); if (b > 0) c.lineTo(-s * 0.15 + s * 0.65 * b, s * 0.35 - s * 0.8 * b); }
    else { const a = clamp(p * 2), b = clamp(p * 2 - 1); c.moveTo(-s * 0.5, -s * 0.5); c.lineTo(-s * 0.5 + s * a, -s * 0.5 + s * a); if (b > 0) { c.moveTo(s * 0.5, -s * 0.5); c.lineTo(s * 0.5 - s * b, -s * 0.5 + s * b); } }
    c.stroke();
  }
  c.restore();
};

// ---------------------------------------------------------------- icons: fat ink outline, flat colour
const ink = (c: Ctx, fill: string, path: () => void, lw = 8) => { c.beginPath(); path(); c.fillStyle = fill; c.fill(); c.lineWidth = lw; c.strokeStyle = INK; c.lineJoin = "round"; c.stroke(); };
const ICONS: Record<string, (c: Ctx, col: string, f: number) => void> = {
  chip: (c, col) => { for (let i = -3; i <= 3; i++) { const o = i * 22; [[o, -95, o, -125], [o, 95, o, 125], [-95, o, -125, o], [95, o, 125, o]].forEach(([a, b, d, e]) => { c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.lineWidth = 10; c.strokeStyle = INK; c.lineCap = "round"; c.stroke(); }); }
    ink(c, col, () => rrect(c, -100, -100, 200, 200, 22)); ink(c, PAPER, () => rrect(c, -55, -55, 110, 110, 12)); },
  gpu: (c, col, f) => { ink(c, col, () => rrect(c, -210, -85, 420, 170, 24)); [-100, 100].forEach((fx) => { ink(c, PAPER, () => c.arc(fx, 0, 62, 0, Math.PI * 2)); for (let b = 0; b < 6; b++) { const a = f * 0.3 + (b / 6) * Math.PI * 2; ink(c, col, () => { c.moveTo(fx, 0); c.quadraticCurveTo(fx + Math.cos(a - 0.6) * 50, Math.sin(a - 0.6) * 50, fx + Math.cos(a) * 54, Math.sin(a) * 54); c.lineTo(fx + Math.cos(a + 0.35) * 30, Math.sin(a + 0.35) * 30); c.closePath(); }, 5); } ink(c, INK, () => c.arc(fx, 0, 12, 0, Math.PI * 2), 2); });
    ink(c, "#ffd84d", () => c.rect(-180, 85, 230, 22), 6); },
  ram: (c, col) => { ink(c, col, () => rrect(c, -240, -60, 480, 120, 14)); for (let i = 0; i < 6; i++) ink(c, INK, () => rrect(c, -205 + i * 70, -34, 48, 52, 6), 2); ink(c, "#ffd84d", () => c.rect(-220, 60, 440, 20), 6); },
  ssd: (c, col) => { ink(c, col, () => rrect(c, -240, -48, 480, 96, 12)); ink(c, INK, () => rrect(c, -170, -26, 100, 52, 6), 2); ink(c, INK, () => rrect(c, -40, -26, 100, 52, 6), 2); ink(c, "#ffd84d", () => c.arc(205, 0, 16, 0, Math.PI * 2), 5); },
  hdd: (c, col, f) => { ink(c, col, () => rrect(c, -125, -160, 250, 320, 20)); ink(c, PAPER, () => c.arc(0, -25, 92, 0, Math.PI * 2)); ink(c, INK, () => c.arc(0, -25, 16, 0, Math.PI * 2), 2); c.save(); c.translate(80, 105); c.rotate(-0.9 + Math.sin(f * 0.25) * 0.06); ink(c, "#ffd84d", () => rrect(c, -12, -120, 24, 130, 10), 6); c.restore(); },
  console: (c, col) => { ink(c, PAPER, () => { c.moveTo(-80, -230); c.quadraticCurveTo(-135, -40, -90, 230); c.lineTo(90, 230); c.quadraticCurveTo(135, -40, 80, -230); c.closePath(); }); ink(c, INK, () => c.rect(-26, -230, 52, 460), 2); ink(c, col, () => c.rect(-8, -190, 16, 380), 3); },
  calendar: (c, col) => { ink(c, PAPER, () => rrect(c, -170, -150, 340, 320, 26)); ink(c, col, () => rrect(c, -170, -150, 340, 95, 26)); for (let i = 0; i < 2; i++) ink(c, INK, () => rrect(c, -95 + i * 160 - 12, -185, 24, 70, 10), 2);
    for (let r = 0; r < 3; r++) for (let k = 0; k < 4; k++) ink(c, r === 2 && k === 2 ? "#ff4d4d" : "#e9e2d0", () => c.arc(-110 + k * 73, -5 + r * 62, 20, 0, Math.PI * 2), 4); },
  eye: (c, col, f) => { const bl = Math.abs(Math.sin(f * 0.04)) > 0.97 ? 0.15 : 1; ink(c, PAPER, () => { c.moveTo(-210, 0); c.quadraticCurveTo(0, -170 * bl, 210, 0); c.quadraticCurveTo(0, 170 * bl, -210, 0); }); if (bl > 0.5) { ink(c, col, () => c.arc(0, 0, 70, 0, Math.PI * 2)); ink(c, INK, () => c.arc(0, 0, 30, 0, Math.PI * 2), 2); ink(c, PAPER, () => c.arc(-14, -16, 10, 0, Math.PI * 2), 2); } },
  clock: (c, col, f) => { ink(c, PAPER, () => c.arc(0, 0, 170, 0, Math.PI * 2)); ink(c, col, () => c.arc(0, 0, 150, 0, Math.PI * 2), 4); ink(c, PAPER, () => c.arc(0, 0, 128, 0, Math.PI * 2), 4);
    const a = f * 0.08, b = f * 0.008; [[a, 105, 10], [b, 70, 14]].forEach(([ang, L, w]) => { c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.sin(ang) * L, -Math.cos(ang) * L); c.lineWidth = w; c.strokeStyle = INK; c.lineCap = "round"; c.stroke(); }); ink(c, "#ff4d4d", () => c.arc(0, 0, 14, 0, Math.PI * 2), 4); },
  play: (c, col) => { ink(c, col, () => rrect(c, -210, -140, 420, 280, 60)); ink(c, PAPER, () => { c.moveTo(-50, -75); c.lineTo(85, 0); c.lineTo(-50, 75); c.closePath(); }); },
  pin: (c, col, f) => { const bob = Math.sin(f * 0.12) * 10; ink(c, "#00000033", () => c.ellipse(0, 170, 90, 22, 0, 0, Math.PI * 2), 0); ink(c, col, () => { c.moveTo(0, 160 + bob - 10); c.bezierCurveTo(-160, -20 + bob, -110, -190 + bob, 0, -190 + bob); c.bezierCurveTo(110, -190 + bob, 160, -20 + bob, 0, 160 + bob - 10); }); ink(c, PAPER, () => c.arc(0, -85 + bob, 48, 0, Math.PI * 2)); },
  alien: (c, col, f) => { const t = Math.sin(f * 0.1) * 8; ink(c, col, () => { c.moveTo(0, -200); c.bezierCurveTo(170, -200, 170, 40, 0, 190); c.bezierCurveTo(-170, 40, -170, -200, 0, -200); });
    [-1, 1].forEach((s) => { c.save(); c.translate(s * 62, -20); c.rotate(s * 0.45); ink(c, INK, () => c.ellipse(0, 0, 42, 66, 0, 0, Math.PI * 2), 2); ink(c, PAPER, () => c.ellipse(-8 + t * 0.5, -22, 10, 14, 0, 0, Math.PI * 2), 2); c.restore(); }); c.beginPath(); c.moveTo(-30, 110); c.quadraticCurveTo(0, 130, 30, 110); c.lineWidth = 8; c.strokeStyle = INK; c.stroke(); },
  phone: (c, col, f) => { ink(c, INK, () => rrect(c, -120, -220, 240, 440, 40), 2); ink(c, col, () => rrect(c, -100, -190, 200, 380, 24)); ink(c, PAPER, () => { c.moveTo(-30, -40); c.lineTo(45, 0); c.lineTo(-30, 40); c.closePath(); }); const h = (f % 40) / 40; ink(c, "#ff4d4d", () => c.arc(70, -150 - h * 30, 16 * (1 - h) + 4, 0, Math.PI * 2), 3); },
  capitol: (c, col) => { ink(c, PAPER, () => { c.rect(-220, 40, 440, 140); }); for (let i = 0; i < 7; i++) ink(c, col, () => c.rect(-200 + i * 64, 60, 26, 110), 5); ink(c, PAPER, () => { c.moveTo(-150, 40); c.quadraticCurveTo(-150, -150, 0, -160); c.quadraticCurveTo(150, -150, 150, 40); c.closePath(); }); ink(c, col, () => c.rect(-12, -230, 24, 75), 5); ink(c, INK, () => c.rect(-240, 180, 480, 22), 2); },
  controller: (c, col) => { ink(c, col, () => { c.moveTo(-230, -40); c.quadraticCurveTo(-200, -120, -100, -110); c.lineTo(100, -110); c.quadraticCurveTo(200, -120, 230, -40); c.quadraticCurveTo(270, 120, 190, 130); c.quadraticCurveTo(140, 130, 100, 60); c.lineTo(-100, 60); c.quadraticCurveTo(-140, 130, -190, 130); c.quadraticCurveTo(-270, 120, -230, -40); });
    ink(c, PAPER, () => { c.rect(-160, -40, 70, 22); c.rect(-136, -64, 22, 70); }, 5); ["#ff4d4d", "#2bd46b", "#4da3ff", "#ffd84d"].forEach((cc, i) => ink(c, cc, () => c.arc(130 + [0, 30, 0, -30][i], -30 + [-30, 0, 30, 0][i], 15, 0, Math.PI * 2), 5)); },
  grave: (c, col) => { ink(c, "#b9b3c9", () => { c.moveTo(-150, 200); c.lineTo(-150, -60); c.quadraticCurveTo(-150, -210, 0, -210); c.quadraticCurveTo(150, -210, 150, -60); c.lineTo(150, 200); c.closePath(); }); inkText(c, "RIP", 0, -60, 90); ink(c, col, () => { c.rect(-260, 190, 520, 30); }, 6); },
};

// ---------------------------------------------------------------- layout and drawing of a scene
const HS = 1.22;
const heights = (it: Item) => it.t === "head" ? (it.size ?? 110) * HS * 1.25 : it.t === "big" ? (it.sub ? 400 : 300) : it.t === "pills" ? (it.size ?? 52) * HS * 2.1 : it.t === "icon" ? (({ console: 620, phone: 560, alien: 500, hdd: 420, pin: 470, grave: 520, capitol: 520 } as Record<string, number>)[it.name] ?? 420) * (it.scale ?? 1) : it.t === "text" ? (it.size ?? 60) * HS * 1.9 : it.t === "list" ? it.rows.length * 150 : 200;
const drawScene = (c: Ctx, f: number, s: Spec, sc: Scene, si: number) => {
  const total = sc.items.reduce((a, it) => a + heights(it) + 40, -40), TOP = 190, AVAIL = 1270, k = Math.min(1, AVAIL / total);
  c.save(); c.translate(540, TOP + AVAIL / 2); c.scale(k, k); c.translate(-540, -(TOP + AVAIL / 2));
  let y = TOP + (AVAIL - total) / 2;
  const tiltR = rng(500 + si);
  sc.items.forEach((it, ii) => {
    const h = heights(it), cy = y + h / 2, tilt = (tiltR() - 0.5) * 0.08, acc = (k: number) => s.pal.accent[(ii + k) % s.pal.accent.length];
    if (it.t === "head") { const px = (it.size ?? 110) * HS; popAt(c, f, it.cue, 540, cy, tilt * 0.5, () => outlined(c, it.text, 0, 0, Math.min(px, (960 / textW(c, it.text, px)) * px), it.color ?? PAPER, acc(0))); }
    else if (it.t === "big") popAt(c, f, it.cue, 540, cy, tilt, () => {
      const px = 190, raw = it.count !== undefined ? (it.count * easeOut((f - it.cue) / 24)).toFixed(it.dec ?? 0).replace(".", ",") + (it.suffix ?? "") : it.text;
      const shown = it.count !== undefined ? raw : it.text, w = Math.max(textW(c, it.text, px), it.sub ? textW(c, it.sub, 64) : 0) + 120;
      const cw = Math.min(980, w), fit = Math.min(1, 900 / textW(c, it.text, px));
      sticker(c, 0, 0, cw, h - 20, acc(0), PAPER, 40);
      inkText(c, shown, 0, it.sub ? -60 : 0, px * fit, it.color ?? INK); if (it.sub) inkText(c, it.sub, 0, 110, 64 * Math.min(1, 860 / textW(c, it.sub, 64)));
    });
    else if (it.t === "pills") {
      const px = (it.size ?? 52) * HS, ws = it.pills.map((p) => textW(c, p.text, px) + px * 1.4 + (p.mark ? px * 1.3 : 0)), gap = 26, sum = ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1), sca = Math.min(1, 980 / sum);
      let x = 540 - (sum * sca) / 2;
      it.pills.forEach((p, k) => { const w = ws[k] * sca, cx = x + w / 2; x += w + gap * sca;
        popAt(c, f, p.cue, cx, cy, (tiltR() - 0.5) * 0.1, () => { c.scale(sca, sca); const fill = p.color ?? acc(k + 1); sticker(c, 0, 0, ws[k], px * 1.7, INK, fill, px * 0.85); inkText(c, p.text, p.mark ? -px * 0.55 : 0, 0, px); if (p.mark) mark(c, p.mark, ws[k] / 2 - px * 0.85, p.mark === "check" ? -6 : 0, px * 0.9, (f - p.cue - 6) / 8); }); });
    }
    else if (it.t === "icon") popAt(c, f, it.cue, 540, cy, tilt, () => { c.scale((it.scale ?? 1) * 1.2, (it.scale ?? 1) * 1.2); (ICONS[it.name] ?? ICONS.chip)(c, it.color ?? acc(0), f); if (it.mark) mark(c, it.mark, 0, 0, 260, (f - (it.markCue ?? it.cue + 10)) / 8); });
    else if (it.t === "text") popAt(c, f, it.cue, 540, cy, tilt, () => { const px = (it.size ?? 60) * HS, fit = Math.min(px, (900 / textW(c, it.text, px)) * px); sticker(c, 0, 0, Math.min(1000, textW(c, it.text, fit) + 90), fit * 1.7, acc(0), it.color ?? PAPER, 26); inkText(c, it.text, 0, 0, fit); });
    else if (it.t === "list") it.rows.forEach((r, k) => { const ry = y + 70 + k * 150, t = (f - r.cue) / POP; if (t <= 0) return; const sx = (1 - easeOut(t)) * -700;
      c.save(); c.translate(sx, 0); c.globalAlpha = clamp(t * 2); sticker(c, 540, ry, 940, 122, r.color ?? acc(k), PAPER, 26);
      const lw = textW(c, r.label, 40) + 50; sticker(c, 100 + lw / 2, ry, lw, 72, INK, r.color ?? acc(k), 36); inkText(c, r.label, 100 + lw / 2, ry, 40);
      c.font = F(58); c.textAlign = "left"; c.textBaseline = "middle"; c.fillStyle = INK; const maxw = 760 - lw - (r.mark ? 60 : 0); const fs = Math.min(58, 58 * maxw / c.measureText(r.text).width); c.font = F(fs); c.fillText(r.text, 130 + lw, ry + 2);
      if (r.mark) mark(c, r.mark, 950, ry, 66, (f - r.cue - 8) / 8); c.restore(); });
    else if (it.t === "arrow") popAt(c, f, it.cue, 540, cy, 0, () => { c.scale(1.3, 1.3); const b = Math.sin((f - it.cue) * 0.3) * 16; c.translate(0, b); for (const [lw, st] of [[30, INK], [16, it.color ?? acc(0)]] as [number, string][]) { c.beginPath(); c.moveTo(0, -70); c.lineTo(0, 60); c.moveTo(-55, 10); c.lineTo(0, 65); c.lineTo(55, 10); c.lineWidth = lw; c.strokeStyle = st; c.lineCap = "round"; c.lineJoin = "round"; c.stroke(); } });
    y += h + 40;
  });
  c.restore();
};

export const makeFilm = (s: Spec): Film => ({
  meta: { title: s.title, W, H, fps: 30, bpm: 120, durationFrames: s.N },
  assets: { images: {} },
  shots: [{ id: "bd", start: 0, end: s.N, draw: (ctx: Ctx, f: number, env: Env) => {
    ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
    const si = Math.max(0, s.scenes.findIndex((sc) => f >= sc.a && f < sc.b)), sc = s.scenes[si], local = f - sc.a;
    backdrop(ctx, f, s, si);
    const z = 1 + 0.035 * (local / Math.max(1, sc.b - sc.a)), enter = 1 - easeOut(local / 8);   // slow push-in; each scene slides up into place
    ctx.save(); ctx.translate(540, 960 + enter * 120); ctx.scale(z, z); ctx.translate(-540, -960);
    drawScene(ctx, f, s, sc, si);
    ctx.restore();
  } }],
});
