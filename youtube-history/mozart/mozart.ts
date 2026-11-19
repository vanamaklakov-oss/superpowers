import { Gfx, rng, type Ctx, type Env, type Medium, type P } from "./core";
import type { Film } from "./film";
import { G, letter, width } from "./drafting";
import { blob, fillShape, hatchRuns, inside } from "./gallery";
import timing from "./mozart-timing.json";

// MOZART AND THE SECRET MISERERE · chalkboard history short, 9x16 (anidoodle engine, chalk after explainer/moonPhases).
// Each chapter is written in the order a teacher works and wiped off left to right by the felt eraser.
// Chapter frames come from the narration (mozart-timing.json, written by build.py); narration, captions and music are added after render.

// ---------------------------------------------------------------- Cyrillic capitals for the draftsman's hand (y down, cap height 6)
const S5: P[] = [[0, 3], [2.6, 3], [3.7, 3.8], [3.7, 5.1], [2.7, 6], [0, 6]];
const CYR: Record<string, { l?: P[][]; c?: P[][]; w?: number }> = {
  А: G.A, В: G.B, Е: G.E, К: G.K, М: G.M, Н: G.H, О: G.O, Р: G.P, С: G.C, Т: G.T, Х: G.X,
  Б: { l: [[[3.6, 0], [0, 0], [0, 6]]], c: [S5], w: 3.8 },
  Г: { l: [[[3.6, 0], [0, 0], [0, 6]]], w: 3.8 },
  Д: { l: [[[1, 0], [0.5, 5]], [[1, 0], [3.6, 0], [3.6, 5]], [[-0.2, 6.6], [-0.2, 5], [4.3, 5], [4.3, 6.6]]], w: 4.4 },
  Ж: { l: [[[2.5, 0], [2.5, 6]], [[0, 0], [2.5, 3.1], [5, 0]], [[0, 6], [2.5, 3.1], [5, 6]]], w: 5 },
  З: { c: [[[0.3, 0.9], [1.3, 0.1], [2.8, 0.1], [3.5, 1], [3.5, 2.1], [2.6, 3], [1.5, 3]], [[2.6, 3], [3.7, 3.8], [3.7, 5.1], [2.8, 5.9], [1.2, 5.9], [0.3, 5.1]]], w: 3.9 },
  И: { l: [[[0, 0], [0, 6], [4, 0], [4, 6]]] },
  Й: { l: [[[0, 0], [0, 6], [4, 0], [4, 6]]], c: [[[1.2, -1.3], [2, -0.6], [2.8, -1.3]]] },
  Л: { l: [[[0, 6], [1.6, 0], [4, 0], [4, 6]]] },
  П: { l: [[[0, 6], [0, 0], [4, 0], [4, 6]]] },
  У: { l: [[[0, 0], [2, 3.4]], [[4, 0], [1.2, 6]]] },
  Ф: { l: [[[2.4, -0.3], [2.4, 6.3]]], c: [[[2.4, 1], [0.9, 1], [0.1, 2], [0.1, 3.4], [0.9, 4.3], [2.4, 4.3], [3.9, 4.3], [4.7, 3.4], [4.7, 2], [3.9, 1], [2.4, 1]]], w: 4.8 },
  Ц: { l: [[[0, 0], [0, 5.6], [3.8, 5.6], [3.8, 0]], [[3.8, 5.6], [4.4, 5.6], [4.4, 7]]], w: 4.4 },
  Ч: { l: [[[0, 0], [0, 2.4]], [[3.8, 0], [3.8, 6]]], c: [[[0, 2.4], [0.8, 3.3], [3.8, 3.3]]], w: 3.9 },
  Ш: { l: [[[0, 0], [0, 6], [5, 6], [5, 0]], [[2.5, 0], [2.5, 6]]], w: 5 },
  Щ: { l: [[[0, 0], [0, 6], [5, 6], [5, 0]], [[2.5, 0], [2.5, 6]], [[5, 6], [5.6, 6], [5.6, 7.3]]], w: 5.6 },
  Ъ: { l: [[[0, 0], [1.2, 0], [1.2, 6]]], c: [[[1.2, 3], [3.3, 3], [4.3, 3.8], [4.3, 5.1], [3.3, 6], [1.2, 6]]], w: 4.4 },
  Ы: { l: [[[0, 0], [0, 6]], [[4.6, 0], [4.6, 6]]], c: [[[0, 3], [1.9, 3], [2.9, 3.8], [2.9, 5.1], [1.9, 6], [0, 6]]], w: 4.6 },
  Ь: { l: [[[0, 0], [0, 6]]], c: [S5], w: 3.8 },
  Э: { c: [[[0.2, 1.2], [1.2, 0.1], [2.7, 0.1], [3.8, 1.3], [3.8, 4.7], [2.7, 5.9], [1.2, 5.9], [0.2, 4.8]]], l: [[[1.4, 3], [3.8, 3]]] },
  Ю: { l: [[[0, 0], [0, 6]], [[0, 3], [1.4, 3]]], c: [[[3.2, 0.1], [2.1, 0.4], [1.4, 1.6], [1.4, 4.4], [2.1, 5.6], [3.2, 5.9], [4.3, 5.6], [5, 4.4], [5, 1.6], [4.3, 0.4], [3.2, 0.1]]], w: 5 },
  Я: { l: [[[3.7, 0], [3.7, 6]], [[1.9, 3.3], [0, 6]]], c: [[[3.7, 0], [1, 0], [0, 0.9], [0, 2.4], [1, 3.3], [3.7, 3.3]]], w: 3.8 },
  Ё: { l: [[[3.6, 0], [0, 0], [0, 6], [3.7, 6]], [[0, 3], [2.8, 3]], [[1, -1.3], [1.1, -0.8]], [[2.6, -1.3], [2.7, -0.8]]] },
};
Object.entries(CYR).forEach(([k, v]) => { if (!G[k]) G[k] = v; });

const FPS = 30, BPM = 120;
const CHALK = "#f4f0e6", YEL = "#f6e6a4", BLUE = "#a9d3e8", PINK = "#f3c1cf", RED = "#f08f86";
const CHALK_M: Medium = { nib: 2.1, taper: 0.55, pressure: 0.95, retrace: true, wobble: 1.4, rough: 1.2 };
const W = 1080, H = 1920, B0 = 34, B1 = 1046, TOP = 34, LEDGE = 1780;
const clamp = (v: number) => Math.max(0, Math.min(1, v));

const chalk = (g: Gfx, draw: (dust: boolean) => void, dustAlpha = 0.2) => {
  g.group("plain", () => draw(true), { blur: 3.2, alpha: dustAlpha });
  g.group("plain", () => draw(false), { textures: ["pencilTooth", "risoSpeck"] });
};
const line = (g: Gfx, dust: boolean, pts: P[], w: number, color: string, seed: number, progress = 1, op = 0.92, wob = 1) => {
  if (progress <= 0) return;
  g.pen(pts, { w: dust ? w * 2.6 : w, color, seed, wobble: wob, boil: 0, opacity: op, retrace: !dust, taper: 1, progress });
};
// straight-edged polyline: each segment drawn on its own so the pen's smoothing cannot round the corners
const lineS = (g: Gfx, dust: boolean, pts: P[], w: number, color: string, seed: number, progress = 1, op = 0.92) => {
  const n = pts.length - 1;
  for (let i = 0; i < n; i++) line(g, dust, [pts[i], pts[i + 1]], w, color, seed + i * 7, clamp(progress * n - i), op);
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
const star = (cx: number, cy: number, r0: number, r1: number, n = 5): P[] => Array.from({ length: n * 2 + 1 }, (_, i) => { const a = -Math.PI / 2 + (i / (n * 2)) * Math.PI * 2, rr = i % 2 ? r0 : r1; return [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr] as P; });

// writes text centred at (x, y), shrinking the cap height so the line fits the board
const T = (g: Gfx, text: string, x: number, y: number, cap: number, color: string, seed: number, p: number, w?: number) => {
  const fit = Math.min(cap, (940 / width(text, 1)));
  letter(g, text, x, y, { cap: fit, color, seed, align: "center", opacity: 0.95, progress: p, slant: 0.08, w: w ?? Math.max(4, fit * 0.075) });
};
// a music staff with notes written one by one
const staff = (g: Gfx, d: boolean, x0: number, y0: number, w: number, seed: number, p: number, notes: number[]) => {
  for (let i = 0; i < 5; i++) line(g, d, [[x0, y0 + i * 26], [x0 + w, y0 + i * 26 - 3]], 3, CHALK, seed + i, clamp(p * 3 - i * 0.2), 0.75);
  notes.forEach((nv, k) => {
    const pk = clamp(p * (notes.length + 3) - 3 - k); if (pk <= 0) return;
    const x = x0 + 70 + k * ((w - 120) / Math.max(1, notes.length - 1)), y = y0 + 104 - nv * 13;
    if (!d) scumble(g, d, circle(x, y, 17, 12, 0, 1, 20), YEL, seed + 20 + k, pk, 0.85);
    line(g, d, circle(x, y, 17, 12, 0, 1.05, 24), 3, YEL, seed + 40 + k, pk);
    line(g, d, [[x + 16, y], [x + 16, y - 80]], 4, YEL, seed + 60 + k, clamp(pk * 2 - 1));
  });
};

// ---------------------------------------------------------------- chapters (frames from the narration)
type Ck = (id: string) => number;
type Chapter = { id: string; a: number; b: number; marks: [string, number][]; draw: (g: Gfx, ck: Ck) => void };
const WIPE = 12;
const TM = timing as { n: number; a: number; b: number }[];
const N = TM[TM.length - 1].b;
const at = (i: number) => ({ a: TM[i].a, b: TM[i].b });

const CH: Chapter[] = [
  { id: "hook", ...at(0), marks: [["name", 30], ["u", 10], ["age", 22], ["note", 30], ["vat", 24]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "МОЦАРТ", 540, 230, 190, CHALK, 11, ck("name"), 13); line(g, d, [[170, 470], [910, 460]], 6, YEL, 12, ck("u")); });
    chalk(g, (d) => { if (!d) T(g, "14 ЛЕТ", 540, 560, 130, YEL, 13, ck("age"), 10);
      line(g, d, circle(470, 1180, 80, 58, 0, 1.05, 30), 7, CHALK, 14, ck("note")); scumble(g, d, circle(470, 1180, 80, 58, 0, 1, 30), CHALK, 15, clamp(ck("note") * 2 - 0.6), 0.5);
      line(g, d, [[548, 1170], [548, 840]], 8, CHALK, 16, clamp(ck("note") * 2 - 1)); line(g, d, [[548, 840], [640, 900], [660, 1000]], 7, CHALK, 17, clamp(ck("note") * 3 - 2));
      if (!d) T(g, "ПРОТИВ ВАТИКАНА", 540, 1400, 64, PINK, 18, ck("vat"), 6); });
  } },
  { id: "chapel", ...at(1), marks: [["t1", 22], ["t2", 18], ["walls", 24], ["roof", 16], ["win", 18], ["mis", 26], ["all", 18]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "СИКСТИНСКАЯ", 540, 140, 80, CHALK, 21, ck("t1"), 7); T(g, "КАПЕЛЛА", 540, 260, 80, CHALK, 22, ck("t2"), 7); }
      lineS(g, d, rect(260, 560, 560, 420), 6, CHALK, 23, ck("walls")); line(g, d, [[230, 570], [540, 410], [850, 570]], 6, CHALK, 24, ck("roof"));
      [340, 470, 600, 730].forEach((x, i) => line(g, d, [[x - 30, 900], [x - 30, 700], ...circle(x, 700, 30, 40, Math.PI, 0.5, 10), [x + 30, 900]], 4, BLUE, 25 + i, clamp(ck("win") * 4 - i))); });
    chalk(g, (d) => { if (!d) { T(g, "MISERERE", 540, 1100, 120, YEL, 31, ck("mis"), 10); T(g, "АЛЛЕГРИ, 1630-Е", 540, 1310, 62, CHALK, 32, ck("all"), 6); } });
  } },
  { id: "secret", ...at(2), marks: [["lock", 26], ["shk", 14], ["key", 10], ["sec", 20], ["ban", 22], ["box", 12], ["leg", 18]], draw: (g, ck) => {
    chalk(g, (d) => { lineS(g, d, rect(380, 380, 320, 260), 7, CHALK, 41, ck("lock")); scumble(g, d, rect(380, 380, 320, 260), CHALK, 42, ck("lock"), 0.2);
      line(g, d, [[440, 380], [440, 290], ...circle(540, 290, 100, 100, Math.PI, 0.5, 16), [640, 380]], 7, CHALK, 43, ck("shk"));
      line(g, d, circle(540, 490, 26, 26), 5, YEL, 44, ck("key")); line(g, d, [[540, 516], [540, 580]], 6, YEL, 45, ck("key"));
      if (!d) T(g, "ТАЙНА", 540, 760, 140, YEL, 46, ck("sec"), 11); });
    chalk(g, (d) => { if (!d) T(g, "ЗАПРЕЩЕНО", 540, 1060, 96, RED, 47, ck("ban"), 8); lineS(g, d, rect(150, 1030, 780, 160), 5, RED, 48, ck("box")); if (!d) T(g, "ПО ЛЕГЕНДЕ", 540, 1290, 56, CHALK, 49, ck("leg"), 5); });
  } },
  { id: "rome", ...at(3), marks: [["yr", 30], ["rim", 22], ["dome", 30], ["lan", 12], ["arr", 14]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "1770", 540, 160, 260, YEL, 51, ck("yr"), 18); if (!d) T(g, "РИМ", 540, 620, 150, CHALK, 52, ck("rim"), 12); });
    chalk(g, (d) => { line(g, d, [[230, 1420], [850, 1420]], 6, CHALK, 53, ck("dome")); lineS(g, d, rect(300, 1220, 480, 200), 5, CHALK, 54, ck("dome"));
      line(g, d, circle(540, 1220, 220, 200, Math.PI, 0.5, 30), 6, CHALK, 55, ck("dome")); scumble(g, d, [...circle(540, 1220, 220, 200, Math.PI, 0.5, 30), [760, 1220], [320, 1220]], BLUE, 56, ck("dome"), 0.25);
      lineS(g, d, rect(515, 960, 50, 70), 4, CHALK, 57, ck("lan")); line(g, d, [[540, 960], [540, 910]], 4, YEL, 58, ck("lan"));
      arrow([140, 850], [300, 1000]).forEach((s, i) => line(g, d, s, 5, PINK, 59 + i, clamp(ck("arr") * 3 - i))); });
  } },
  { id: "memory", ...at(4), marks: [["hear", 22], ["ear", 22], ["arr", 12], ["staff", 40], ["wrote", 20], ["mem", 22]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "УСЛЫШАЛ", 540, 140, 100, CHALK, 61, ck("hear"), 9);
      line(g, d, [...circle(540, 470, 110, 150, -Math.PI * 0.9, 0.62, 26), [600, 560], [560, 600]], 7, CHALK, 62, ck("ear")); line(g, d, circle(530, 460, 40, 60, -Math.PI * 0.8, 0.6, 14), 5, CHALK, 63, ck("ear"));
      arrow([540, 680], [540, 820]).forEach((s, i) => line(g, d, s, 6, PINK, 64 + i, clamp(ck("arr") * 3 - i))); });
    chalk(g, (d) => { staff(g, d, 140, 880, 800, 70, ck("staff"), [2, 3, 4, 3, 5, 4, 2]); if (!d) { T(g, "ЗАПИСАЛ", 540, 1140, 100, CHALK, 71, ck("wrote"), 9); T(g, "ПО ПАМЯТИ", 540, 1310, 110, YEL, 72, ck("mem"), 10); } });
  } },
  { id: "letter", ...at(5), marks: [["env", 28], ["flap", 14], ["seal", 12], ["who", 22], ["date", 26]], draw: (g, ck) => {
    chalk(g, (d) => { lineS(g, d, rect(250, 300, 580, 380), 6, CHALK, 81, ck("env")); line(g, d, [[250, 300], [540, 520], [830, 300]], 6, CHALK, 82, ck("flap"));
      scumble(g, d, circle(540, 530, 46, 46, 0, 1, 24), RED, 83, ck("seal"), 0.75); });
    chalk(g, (d) => { if (!d) { T(g, "ПИСЬМО ОТЦА", 540, 820, 80, CHALK, 84, ck("who"), 7); T(g, "ЛЕОПОЛЬД МОЦАРТ", 540, 960, 64, BLUE, 85, ck("who"), 6); T(g, "14 АПРЕЛЯ 1770", 540, 1180, 84, YEL, 86, ck("date"), 7); } });
  } },
  { id: "doubt", ...at(6), marks: [["one", 26], ["src", 20], ["q", 24], ["dis", 24]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "1", 540, 120, 330, YEL, 91, ck("one"), 20); T(g, "ИСТОЧНИК", 540, 620, 110, CHALK, 92, ck("src"), 9); } line(g, d, circle(540, 290, 220, 230), 5, YEL, 93, ck("one")); });
    chalk(g, (d) => { if (!d) { T(g, "?", 540, 880, 260, RED, 94, ck("q"), 18); T(g, "ИСТОРИКИ СПОРЯТ", 540, 1330, 70, CHALK, 95, ck("dis"), 6); } });
  } },
  { id: "spur", ...at(7), marks: [["pun", 24], ["x", 10], ["ord", 34], ["gold", 22], ["spur", 18], ["pope", 18]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) T(g, "НАКАЗАНИЕ", 540, 140, 100, CHALK, 101, ck("pun"), 9); line(g, d, [[150, 230], [930, 180]], 9, RED, 102, ck("x")); });
    chalk(g, (d) => { const cx = 540, cy = 640;
      for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + Math.PI / 4, b = 0.38; const p: P[] = [[cx, cy], [cx + Math.cos(a - b) * 230, cy + Math.sin(a - b) * 230], [cx + Math.cos(a) * 170, cy + Math.sin(a) * 170], [cx + Math.cos(a + b) * 230, cy + Math.sin(a + b) * 230], [cx, cy]];
        line(g, d, p, 6, YEL, 103 + i, clamp(ck("ord") * 4 - i)); scumble(g, d, p, YEL, 110 + i, clamp(ck("ord") * 4 - i - 0.5), 0.3); }
      line(g, d, circle(cx, cy, 60), 6, CHALK, 115, clamp(ck("ord") * 2 - 1));
      if (!d) { T(g, "ЗОЛОТАЯ", 540, 960, 110, YEL, 116, ck("gold"), 9); T(g, "ШПОРА", 540, 1110, 110, YEL, 117, ck("spur"), 9); T(g, "ОТ ПАПЫ РИМСКОГО", 540, 1330, 60, CHALK, 118, ck("pope"), 5); } });
  } },
  { id: "london", ...at(8), marks: [["yr", 26], ["lon", 20], ["page", 22], ["staff", 30]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "1771", 540, 140, 230, YEL, 121, ck("yr"), 16); T(g, "ЛОНДОН", 540, 560, 130, CHALK, 122, ck("lon"), 11); } });
    chalk(g, (d) => { lineS(g, d, rect(170, 800, 740, 560), 5, CHALK, 123, ck("page")); staff(g, d, 220, 880, 640, 130, ck("staff"), [1, 3, 2, 4]); staff(g, d, 220, 1110, 640, 150, clamp(ck("staff") * 1.4 - 0.4), [4, 3, 5, 2]); });
  } },
  { id: "end", ...at(9), marks: [["num", 30], ["yrs", 22], ["lock", 30], ["note", 24]], draw: (g, ck) => {
    chalk(g, (d) => { if (!d) { T(g, "130+", 540, 150, 230, YEL, 131, ck("num"), 16); T(g, "ЛЕТ ТАЙНЫ", 540, 560, 110, CHALK, 132, ck("yrs"), 9); } });
    chalk(g, (d) => { lineS(g, d, rect(360, 1000, 300, 240), 7, CHALK, 133, ck("lock"));   // the padlock, open now
      line(g, d, [[420, 1000], [420, 900], ...circle(520, 900, 100, 100, Math.PI, 0.5, 16), [620, 830]], 7, CHALK, 134, ck("lock"));
      line(g, d, circle(820, 1120, 42, 30, 0, 1.05, 24), 6, YEL, 135, ck("note")); line(g, d, [[860, 1115], [860, 920], [930, 970]], 6, YEL, 136, ck("note")); });
  } },
];

const clockFor = (c: Chapter, local: number): Ck => {
  const total = c.marks.reduce((s, m) => s + m[1], 0), room = Math.max(10, (c.b - c.a - WIPE) * 0.82), k = Math.min(1, room / total);
  const tbl = new Map<string, [number, number]>(); let t = WIPE;
  for (const [id, len] of c.marks) { tbl.set(id, [t, t + len * k]); t += len * k; }
  return (id) => { const s = tbl.get(id); if (!s) return 1; return clamp((local - s[0]) / (s[1] - s[0])); };
};

const board = (g: Gfx, ctx: Ctx) => {
  const gr = ctx.createRadialGradient(540, 820, 80, 540, 820, 1200);
  gr.addColorStop(0, "#35493f"); gr.addColorStop(0.62, "#27352f"); gr.addColorStop(1, "#1b2622");
  ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
  g.paper("coldpress", 0.3);
  g.group("plain", () => {
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
    for (let i = 0; i < 160; i++) { const x = B0 + r() * (B1 - B0), y = LEDGE + 2 + r() * 20; fillShape(g, blob(x, y, 0.8 + r() * 1.8, 0.6 + r(), 110 + i, 0.3, 6), CHALK, 0.25 + r() * 0.45); }
    fillShape(g, [[690, LEDGE + 2], [790, LEDGE - 6], [794, LEDGE + 10], [694, LEDGE + 18]], CHALK);
    const ex = eraserX < 0 ? 320 : eraserX, ey = eraserX < 0 ? LEDGE - 2 : 900;
    fillShape(g, [[ex - 70, ey - 40], [ex + 70, ey - 46], [ex + 76, ey + 30], [ex - 64, ey + 36]], "#a0714a");
    fillShape(g, [[ex - 68, ey + 8], [ex + 74, ey + 2], [ex + 76, ey + 30], [ex - 64, ey + 36]], "#8e8a86");
  });
};

const draw = (ctx: Ctx, f: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, CHALK_M);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  board(g, ctx);
  const k = Math.max(0, CH.findIndex((c) => f >= c.a && f < c.b)), c = CH[k], local = f - c.a;
  let eraserX = -1;
  if (k > 0 && local < WIPE) {
    const wx = 40 + (local / WIPE) * 1040, prev = CH[k - 1], cut = (fn: () => void, left: boolean) => { const cc = g.cur; cc.save(); cc.beginPath(); if (left) cc.rect(0, 0, wx, H); else cc.rect(wx, 0, W - wx, H); cc.clip(); fn(); cc.restore(); };
    g.group("plain", () => cut(() => prev.draw(g, () => 1), true), { blur: 6, alpha: 0.12 });
    cut(() => prev.draw(g, () => 1), false);
    eraserX = wx;
  }
  c.draw(g, clockFor(c, local));
  frame(g, eraserX);
};

export const mozart: Film = {
  meta: { title: "Mozart and the secret Miserere · chalkboard", W, H, fps: FPS, bpm: BPM, durationFrames: N },
  assets: { images: {} },
  shots: [{ id: "lesson", start: 0, end: N, draw }],
};
