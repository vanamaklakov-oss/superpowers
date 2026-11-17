import { Gfx, rng, type Ctx, type Env, type Medium, type P } from "./core";
import type { Film } from "./film";
import { letter } from "./drafting";
import { blob, fillShape, hatchRuns, inside } from "./gallery";

// GTA 6 IN 40 SECONDS · chalkboard explainer, 9x16. A teacher's slate in portrait: each chapter is
// written on in the order a teacher works (headline, the big number, the diagram, the label), and the
// felt eraser sweeps it off left to right before the next one. Facts and sources: facts.json.
// Narration is added after render (vo/), timed to the chapter table below.

const FPS = 30, BPM = 120, N = 1170;                                  // 39 s; a beat is 15 frames, N % 15 === 0
const CHALK = "#f4f0e6", YEL = "#f6e6a4", BLUE = "#a9d3e8", PINK = "#f3c1cf", RED = "#f08f86";
const CHALK_M: Medium = { nib: 2.1, taper: 0.55, pressure: 0.95, retrace: true, wobble: 1.4, rough: 1.2 };
const W = 1080, H = 1920, B0 = 34, B1 = 1046, TOP = 34, LEDGE = 1780;
const clamp = (v: number) => Math.max(0, Math.min(1, v));

// ---------------------------------------------------------------- chalk primitives (after moonPhases.ts)
const chalk = (g: Gfx, draw: (dust: boolean) => void, dustAlpha = 0.2) => {
  g.group("plain", () => draw(true), { blur: 3.2, alpha: dustAlpha });
  g.group("plain", () => draw(false), { textures: ["pencilTooth", "risoSpeck"] });
};
const line = (g: Gfx, dust: boolean, pts: P[], w: number, color: string, seed: number, progress = 1, op = 0.92, wob = 1) => {
  if (progress <= 0) return;
  g.pen(pts, { w: dust ? w * 2.6 : w, color, seed, wobble: wob, boil: 0, opacity: op, retrace: !dust, taper: 1, progress });
};
const scumble = (g: Gfx, dust: boolean, region: P[], color: string, seed: number, progress: number, alpha = 0.4, angle = -0.8) => {
  if (progress <= 0) return;
  const r = rng(seed);
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; region.forEach(([x, y]) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); });
  const c = g.cur; g.touch(x0 - 12, y0 - 12, x1 + 12, y1 + 12);
  c.save(); c.lineCap = "round"; c.lineJoin = "round"; c.strokeStyle = color; c.lineWidth = dust ? 9 : 4.2;
  const runs = hatchRuns({ x0, y0, x1, y1 }, angle, 3.4, (x, y) => inside(region, x, y), 4, seed), upto = progress * runs.length;
  runs.forEach((run, i) => { if (i > upto) return; const pts = run.filter((_, k, a) => k % 2 === 0 || k === a.length - 1), m = i + 1 > upto ? Math.max(2, Math.ceil(pts.length * (upto - i))) : pts.length; c.globalAlpha = alpha * (0.86 + r() * 0.2); c.beginPath(); pts.slice(0, m).forEach(([x, y], k) => (k ? c.lineTo(x + (r() - 0.5) * 1.5, y + (r() - 0.5) * 1.5) : c.moveTo(x, y))); c.stroke(); });
  c.restore();
};
const circle = (cx: number, cy: number, rx: number, ry = rx, a0 = -Math.PI / 2, turns = 1.08, n = 40): P[] =>
  Array.from({ length: n + 1 }, (_, i) => { const a = a0 + (i / n) * Math.PI * 2 * turns; return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry] as P; });
const rect = (x: number, y: number, w: number, h: number): P[] => [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]];
const arrow = (a: P, b: P): P[][] => { const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = 34; return [[a, b], [b, [b[0] - Math.cos(ang - 0.45) * L, b[1] - Math.sin(ang - 0.45) * L]], [b, [b[0] - Math.cos(ang + 0.45) * L, b[1] - Math.sin(ang + 0.45) * L]]]; };

// ---------------------------------------------------------------- the clock: one cue table per chapter
// Each chapter lists its marks in drawing order with a length in frames; they are laid end to end
// from the chapter's start + WIPE, so a chapter is written mark by mark, never faded in.
type Ck = (id: string) => number;
type Chapter = { id: string; a: number; b: number; marks: [string, number][]; draw: (g: Gfx, ck: Ck) => void };
const WIPE = 14;

const T = (g: Gfx, text: string, x: number, y: number, cap: number, color: string, seed: number, p: number, w?: number) =>
  letter(g, text, x, y, { cap, color, seed, align: "center", opacity: 0.95, progress: p, slant: 0.08, ...(w ? { w } : {}) });

const CH: Chapter[] = [
  { id: "hook", a: 0, b: 140, marks: [["title", 26], ["u1", 5], ["u2", 5], ["date", 22], ["sub", 30]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "GTA 6", 540, 330, 190, CHALK, 11, ck("title"), 13); line(g, d, [[250, 600], [830, 590]], 6, YEL, 12, ck("u1")); line(g, d, [[280, 628], [800, 622]], 4, YEL, 13, ck("u2")); });
    chalk(g, (d) => { if (!d) { T(g, "NOV 19", 540, 760, 120, YEL, 14, ck("date"), 9); T(g, "EVERYTHING YOU", 540, 1060, 54, CHALK, 15, Math.min(1, ck("sub") * 2)); T(g, "NEED TO KNOW", 540, 1150, 54, CHALK, 16, Math.max(0, ck("sub") * 2 - 1)); } });
  } },
  { id: "years", a: 140, b: 270, marks: [["n13", 28], ["years", 16], ["t5", 16], ["arr", 10], ["t6", 16]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "13", 540, 300, 300, YEL, 21, ck("n13"), 18); T(g, "YEARS", 540, 690, 90, CHALK, 22, ck("years"), 8); } });
    chalk(g, (d) => { if (!d) { T(g, "GTA 5", 270, 940, 64, CHALK, 23, ck("t5")); T(g, "2013", 270, 1030, 56, BLUE, 24, ck("t5")); T(g, "GTA 6", 810, 940, 64, CHALK, 25, ck("t6")); T(g, "2026", 810, 1030, 56, BLUE, 26, ck("t6")); } arrow([430, 1000], [650, 1000]).forEach((s, i) => line(g, d, s, 5, CHALK, 27 + i, clamp(ck("arr") * 3 - i))); });
  } },
  { id: "delay", a: 270, b: 455, marks: [["head", 22], ["d1", 14], ["x1", 8], ["d2", 18], ["x2", 8], ["d3", 22], ["ring", 14]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "DELAYED TWICE", 540, 230, 78, CHALK, 31, ck("head"), 7); line(g, d, [[200, 340], [880, 335]], 4, YEL, 32, ck("head")); });
    chalk(g, (d) => {
      if (!d) { T(g, "2025", 540, 470, 110, CHALK, 33, ck("d1"), 9); T(g, "MAY 2026", 540, 720, 110, CHALK, 34, ck("d2"), 9); T(g, "NOV 19 2026", 540, 995, 86, YEL, 35, ck("d3"), 8); }
      line(g, d, [[350, 560], [730, 500]], 8, RED, 36, ck("x1")); line(g, d, [[230, 810], [850, 750]], 8, RED, 37, ck("x2"));
      line(g, d, circle(540, 1045, 420, 115, -2.6, 1.05), 5, YEL, 38, ck("ring"));
      [0, 1].forEach((i) => line(g, d, [[540, 600 + i * 260], [540, 650 + i * 260]], 4, BLUE, 39 + i, ck(i ? "d3" : "d2")));
    });
  } },
  { id: "where", a: 455, b: 640, marks: [["coast", 36], ["fill", 18], ["lab", 16], ["star", 10], ["vc", 14], ["p1", 18], ["p2", 18]], draw: (g, ck) => {
    // Leonida is Rockstar's fictional state; drawn here as an invented peninsula, not a traced map
    const coast: P[] = [[300, 170], [760, 160], [800, 230], [770, 330], [720, 420], [700, 520], [690, 640], [650, 760], [600, 830], [560, 840], [540, 780], [520, 650], [470, 560], [420, 470], [380, 360], [320, 300], [280, 230], [300, 170]];
    chalk(g, (d) => { scumble(g, d, coast, CHALK, 41, ck("fill"), 0.16); line(g, d, coast, 4, CHALK, 42, ck("coast")); });
    chalk(g, (d) => { if (!d) { T(g, "LEONIDA", 540, 230, 54, CHALK, 43, ck("lab"), 5); T(g, "VICE CITY", 600, 900, 50, PINK, 44, ck("vc"), 5); }
      const st: P[] = Array.from({ length: 11 }, (_, i) => { const a = -Math.PI / 2 + (i / 10) * Math.PI * 2, rr = i % 2 ? 11 : 26; return [645 + Math.cos(a) * rr, 700 + Math.sin(a) * rr] as P; }); line(g, d, st, 4, PINK, 45, ck("star")); });
    // two leads as chalk figures with name tags: stick people, not likenesses
    const fig = (cx: number, seed: number, p: number, name: string, col: string) => chalk(g, (d) => {
      line(g, d, circle(cx, 1030, 48), 5, col, seed, clamp(p * 4));
      line(g, d, [[cx, 1080], [cx, 1260]], 5, col, seed + 1, clamp(p * 4 - 1));
      line(g, d, [[cx - 80, 1150], [cx, 1110], [cx + 80, 1150]], 5, col, seed + 2, clamp(p * 4 - 1.6));
      line(g, d, [[cx - 60, 1370], [cx, 1260], [cx + 60, 1370]], 5, col, seed + 3, clamp(p * 4 - 2.2));
      if (!d) T(g, name, cx, 1410, 52, col, seed + 4, clamp(p * 4 - 3));
    });
    fig(370, 50, ck("p1"), "LUCIA", PINK); fig(710, 60, ck("p2"), "JASON", BLUE);
  } },
  { id: "where2play", a: 640, b: 790, marks: [["b1", 16], ["l1", 14], ["b2", 16], ["l2", 18], ["ok", 12], ["pc", 16], ["q", 10], ["ny", 14]], draw: (g, ck) => {
    chalk(g, (d) => {
      line(g, d, rect(160, 220, 330, 420), 5, CHALK, 61, ck("b1")); line(g, d, rect(590, 220, 330, 420), 5, CHALK, 62, ck("b2"));
      if (!d) { T(g, "PS5", 325, 390, 80, CHALK, 63, ck("l1"), 7); T(g, "XBOX", 755, 360, 64, CHALK, 64, ck("l2"), 6); T(g, "SERIES X/S", 755, 460, 40, CHALK, 65, ck("l2")); }
      [325, 755].forEach((x, i) => line(g, d, [[x - 50, 760], [x - 10, 800], [x + 60, 700]], 9, YEL, 66 + i, clamp(ck("ok") * 2 - i)));
    });
    chalk(g, (d) => { line(g, d, rect(375, 960, 330, 230), 5, CHALK, 70, ck("pc")); line(g, d, [[540, 1190], [540, 1250], [470, 1250], [610, 1250]], 5, CHALK, 71, ck("pc"));
      if (!d) { T(g, "PC", 540, 1030, 80, CHALK, 72, ck("pc"), 7); T(g, "?", 760, 960, 160, RED, 73, ck("q"), 12); T(g, "NOT YET", 540, 1330, 70, RED, 74, ck("ny"), 7); } });
  } },
  { id: "trailer", a: 790, b: 955, marks: [["eye", 22], ["num", 24], ["mil", 16], ["views", 20], ["rec", 18], ["star", 10]], draw: (g, ck) => {
    chalk(g, (d) => { line(g, d, [...circle(540, 330, 230, 110, Math.PI, 0.5), ...circle(540, 330, 230, 110, 0, 0.5)], 6, CHALK, 81, ck("eye")); scumble(g, d, circle(540, 330, 70, 70, 0, 1, 30), BLUE, 82, clamp(ck("eye") * 2 - 1), 0.5); });
    chalk(g, (d) => { if (!d) { T(g, "93", 540, 520, 260, YEL, 83, ck("num"), 16); T(g, "MILLION VIEWS", 540, 860, 66, CHALK, 84, ck("mil"), 6); T(g, "IN 24 HOURS", 540, 970, 66, CHALK, 85, ck("views"), 6); T(g, "A YOUTUBE RECORD", 540, 1230, 54, PINK, 86, ck("rec"), 5); } line(g, d, rect(170, 1200, 740, 150), 4, PINK, 87, ck("rec"));
      const st: P[] = Array.from({ length: 11 }, (_, i) => { const a = -Math.PI / 2 + (i / 10) * Math.PI * 2, rr = i % 2 ? 16 : 38; return [880 + Math.cos(a) * rr, 1180 + Math.sin(a) * rr] as P; }); line(g, d, st, 4, YEL, 88, ck("star")); });
  } },
  { id: "stream", a: 955, b: 1060, marks: [["clock", 20], ["hands", 10], ["h24", 16], ["live", 10], ["lab", 20]], draw: (g, ck) => {
    chalk(g, (d) => { line(g, d, circle(540, 520, 260), 6, CHALK, 91, ck("clock"));
      for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2; line(g, d, [[540 + Math.cos(a) * 225, 520 + Math.sin(a) * 225], [540 + Math.cos(a) * 250, 520 + Math.sin(a) * 250]], 4, CHALK, 92 + i, clamp(ck("clock") * 12 - i)); }
      line(g, d, [[540, 520], [540, 330]], 6, CHALK, 105, ck("hands")); line(g, d, [[540, 520], [680, 600]], 6, CHALK, 106, ck("hands"));
      if (!d) T(g, "24H", 540, 860, 150, YEL, 107, ck("h24"), 12); });
    chalk(g, (d) => { scumble(g, d, circle(330, 1150, 26, 26, 0, 1, 24), RED, 108, ck("live"), 0.8); if (!d) { T(g, "LIVE", 470, 1120, 70, RED, 109, ck("live"), 7); T(g, "LAUNCH DAY STREAM", 540, 1290, 56, CHALK, 110, ck("lab"), 5); } });
  } },
  { id: "ask", a: 1060, b: N, marks: [["q", 18], ["day", 22], ["arr", 12], ["c", 18]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "?", 540, 200, 380, YEL, 121, ck("q"), 22); T(g, "DAY ONE?", 540, 800, 120, CHALK, 122, ck("day"), 10); T(g, "COMMENT", 540, 1260, 70, PINK, 124, ck("c"), 7); }
      arrow([540, 1020], [540, 1200]).forEach((s, i) => line(g, d, s, 6, PINK, 123 + i * 7, clamp(ck("arr") * 3 - i))); });
  } },
];

((): void => {   // the checker runs at load: chapters tile the film, every chapter's marks finish inside it, all on the 5-frame grid
  let at = 0;
  for (const c of CH) {
    if (c.a !== at || c.a % 5 || c.b % 5 || c.b <= c.a) throw new Error(`explainer: chapter ${c.id} (${c.a}-${c.b}) leaves a gap or is off the grid`);
    const len = WIPE + c.marks.reduce((s, m) => s + m[1], 0);
    if (len > c.b - c.a) throw new Error(`explainer: chapter ${c.id} needs ${len} frames, has ${c.b - c.a}`);
    at = c.b;
  }
  if (at !== N || N % 15) throw new Error("explainer: chapters do not tile the film");
})();

const clockFor = (c: Chapter, local: number): Ck => {
  const tbl = new Map<string, [number, number]>(); let t = WIPE;
  for (const [id, len] of c.marks) { tbl.set(id, [t, t + len]); t += len; }
  return (id) => { const s = tbl.get(id); if (!s) return 1; return clamp((local - s[0]) / (s[1] - s[0])); };
};

// ---------------------------------------------------------------- the board and its frame
const board = (g: Gfx, ctx: Ctx) => {
  const gr = ctx.createRadialGradient(540, 820, 80, 540, 820, 1200);
  gr.addColorStop(0, "#35493f"); gr.addColorStop(0.62, "#27352f"); gr.addColorStop(1, "#1b2622");
  ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
  g.paper("coldpress", 0.3);
  g.group("plain", () => {   // ghosts of older lessons
    const r = rng(5);
    for (let i = 0; i < 12; i++) { const cx = 120 + r() * 840, cy = 120 + r() * 1500, rr = 140 + r() * 180, a0 = r() * 6; const pts: P[] = []; for (let k = 0; k <= 12; k++) { const a = a0 + (k / 12) * 2.2; pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.55]); } g.pen(pts, { w: 40 + r() * 30, color: CHALK, seed: 6 + i, wobble: 3, boil: 0, opacity: 0.05, retrace: false, taper: 0.4 }); }
  }, { blur: 9 });
};
const frame = (g: Gfx, eraserX: number) => {
  g.group("plain", () => {
    const wood = "#7b5231", r = rng(70);
    fillShape(g, [[0, 0], [W, 0], [W, TOP], [0, TOP]], wood); fillShape(g, [[0, 0], [B0, 0], [B0, H], [0, H]], wood); fillShape(g, [[B1, 0], [W, 0], [W, H], [B1, H]], wood);
    fillShape(g, [[0, LEDGE], [W, LEDGE], [W, H], [0, H]], "#6a4526");
    fillShape(g, [[B0 - 8, LEDGE - 4], [B1 + 8, LEDGE - 4], [B1 + 20, LEDGE + 24], [B0 - 20, LEDGE + 24]], "#8c6139");
    fillShape(g, [[B0, TOP], [B1, TOP], [B1 - 6, TOP + 8], [B0 + 8, TOP + 8], [B0 + 8, LEDGE - 4], [B0, LEDGE - 4]], "#0e1512", 0.55);
    for (let i = 0; i < 160; i++) { const x = B0 + r() * (B1 - B0), y = LEDGE + 2 + r() * 20; fillShape(g, blob(x, y, 0.8 + r() * 1.8, 0.6 + r(), 110 + i, 0.3, 6), CHALK, 0.25 + r() * 0.45); }
    const st: P[] = [[690, LEDGE + 2], [790, LEDGE - 6], [794, LEDGE + 10], [694, LEDGE + 18]]; fillShape(g, st, CHALK);
    // the felt eraser: resting on the ledge, or sweeping the board
    const ex = eraserX < 0 ? 320 : eraserX, ey = eraserX < 0 ? LEDGE - 2 : 900;
    const er: P[] = [[ex - 70, ey - 40], [ex + 70, ey - 46], [ex + 76, ey + 30], [ex - 64, ey + 36]];
    fillShape(g, er, "#a0714a"); fillShape(g, [[ex - 68, ey + 8], [ex + 74, ey + 2], [ex + 76, ey + 30], [ex - 64, ey + 36]], "#8e8a86");
  });
};

const draw = (ctx: Ctx, f: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, CHALK_M);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  board(g, ctx);
  const k = CH.findIndex((c) => f >= c.a && f < c.b), c = CH[k], local = f - c.a;
  let eraserX = -1;
  if (k > 0 && local < WIPE) {   // the previous chapter, wiped off left to right; its ghost stays behind the eraser
    const wx = 40 + (local / WIPE) * 1040, prev = CH[k - 1], cut = (fn: () => void, left: boolean) => { const cc = g.cur; cc.save(); cc.beginPath(); if (left) cc.rect(0, 0, wx, H); else cc.rect(wx, 0, W - wx, H); cc.clip(); fn(); cc.restore(); };
    g.group("plain", () => cut(() => prev.draw(g, () => 1), true), { blur: 6, alpha: 0.12 });
    cut(() => prev.draw(g, () => 1), false);
    eraserX = wx;
  }
  c.draw(g, clockFor(c, local));
  frame(g, eraserX);
};

export const explainer: Film = {
  meta: { title: "GTA 6 in 40 seconds · chalkboard", W, H, fps: FPS, bpm: BPM, durationFrames: N },
  assets: { images: {} },
  shots: [{ id: "lesson", start: 0, end: N, draw }],
};
