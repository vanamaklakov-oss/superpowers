"""Assemble «Да Винчи — История за минуту» from images/NN.png + vo/NN.mp3 (+ word timings).
Look: slow push-in on each picture, white light-flash cuts, torn-paper cuts around the title card,
rain on dark scenes, one word on screen at a time, synthesized music and whooshes.
Usage: python3 build.py [--preview]   (preview = 540x960, fast)"""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from script import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
PREVIEW = "--preview" in sys.argv
W, H = (540, 960) if PREVIEW else (1080, 1920)
FPS, SR, GAP = 30, 48000, 0.12
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
RAIN = set()                 # scenes with falling rain/snow
TORN = {1, 2}                         # torn-paper cut INTO this scene's successor... see cut_kind
TITLE_WORD = "История"                # title card appears on this word of scene 1
rng = np.random.default_rng(7)

# ---------- audio: trim each narration, place on a timeline ----------
def pcm(path):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR

rows, t = [], 0.35
for n, _, kw, k1, k2, yr in SCENES:
    a, lead = trim(pcm(f"{HERE}/vo/{n:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{n:02d}.mp3.json"))
    words = [{"w": w["w"], "s": t + w["s"] - lead, "e": t + w["s"] - lead + w["d"]} for w in meta["words"]]
    kt = next((w["s"] for w in words if w["w"].lower().strip(".,?!:").startswith(kw)), t + 0.5)
    rows.append({"n": n, "t0": t, "audio": a, "words": words, "kt": kt, "k1": k1, "k2": k2, "yr": yr}); t += len(a) / SR + GAP
TOTAL = t + 0.9
for i, r in enumerate(rows): r["t1"] = rows[i + 1]["t0"] if i + 1 < len(rows) else TOTAL
title_t = next(w["s"] for w in rows[0]["words"] if w["w"].strip(".,").lower() == TITLE_WORD.lower())
title_end = rows[0]["t1"]

def music(total):
    n = int(total * SR); tt = np.arange(n) / SR; out = np.zeros((n, 2), np.float32)
    bpm = 84; beat = 60 / bpm
    # minor progression (Dm - Bb - F - C), slow string pad with a little detune
    prog = [(146.83, 174.61, 220.0), (116.54, 146.83, 174.61), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0)]
    bar = beat * 4
    for k in range(int(total / bar) + 1):
        s = int(k * bar * SR); e = min(n, int((k + 1) * bar * SR) + SR // 2)
        if s >= n: break
        x = np.arange(e - s) / SR; env = np.minimum(1, x / 0.6) * np.exp(-np.maximum(0, x - bar) * 4)
        for f in prog[k % 4]:
            for dt, pan in [(-0.6, 0.3), (0.7, 0.7)]:
                w = (np.sin(2 * np.pi * (f + dt) * x) + 0.35 * np.sin(4 * np.pi * (f + dt) * x)) * env * 0.022
                out[s:e, 0] += w * (1 - pan); out[s:e, 1] += w * pan
        bass = np.sin(2 * np.pi * prog[k % 4][0] / 2 * x) * env * 0.05; out[s:e] += bass[:, None]
    # war drums: low tom on beats 1 and 3, faster hits in the second half
    for k in range(int(total / beat)):
        t0 = k * beat; hits = [0] if k % 2 else [0]
        if t0 > total * 0.35 and k % 4 == 3: hits += [beat / 2]
        for h in hits:
            s = int((t0 + h) * SR); L = int(0.5 * SR)
            if s + L >= n: continue
            x = np.arange(L) / SR; f = 70 * np.exp(-x * 6) + 45
            d = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 7) * (0.22 if k % 2 == 0 else 0.13)
            out[s:s + L] += d[:, None]
    fade = np.minimum(1, tt / 1.0) * np.minimum(1, (total - tt) / 1.5); return out * fade[:, None]

def whoosh(L=0.45):
    x = np.arange(int(L * SR)) / SR; noise = rng.standard_normal(len(x))
    k = np.exp(-((x - L * 0.55) / (L * 0.22)) ** 2); y = np.convolve(noise, np.ones(18) / 18, "same") * k * 0.25
    return y

def mix(cuts):
    m = music(TOTAL); n = len(m); voice = np.zeros(n, np.float32)
    for r in rows:
        s = int(r["t0"] * SR); voice[s:s + len(r["audio"])] += r["audio"][: n - s] * 1.15
    env = np.convolve(np.abs(voice), np.ones(SR // 10) / (SR // 10), "same"); duck = 1 - 0.55 * np.clip(env * 12, 0, 1)
    out = m * duck[:, None] + voice[:, None]
    wh = whoosh()
    for c in cuts:
        s = int((c - 0.28) * SR)
        if 0 <= s and s + len(wh) < n: out[s:s + len(wh)] += wh[:, None]
    out /= max(1.0, np.abs(out).max() / 0.95)
    p = f"{HERE}/out/mix.wav"
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
    return p

# ---------- pictures ----------
def load(n):
    p = f"{HERE}/images/{n:02d}.png"
    if not os.path.exists(p):
        p2 = p.replace(".png", ".jpg"); p = p2 if os.path.exists(p2) else None
    if p is None:   # placeholder until the real picture arrives
        im = Image.new("RGB", (W, H), tuple(int(v) for v in rng.integers(40, 160, 3)))
        ImageDraw.Draw(im).text((W // 2, H // 2), f"{n:02d}", font=ImageFont.truetype(FONT, W // 4), anchor="mm", fill="white"); return im
    return ImageOps.fit(Image.open(p).convert("RGB"), (W, H), Image.LANCZOS)

def kenburns(im, p, k):
    z = 1.04 + 0.10 * p; dx = (0.5 + 0.06 * np.sin(k * 1.7) * (p - 0.5)) ; dy = 0.5 - 0.03 * p * (1 if k % 2 else -1)
    cw, ch = W / z, H / z; x0 = (W - cw) * dx; y0 = (H - ch) * dy
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)

PX = 4   # pixel-font block size at 1080 wide
def ptext(im, cx, cy, lines, size):
    """Draw lines [(text, rgb)] as chunky pixel text centred at (cx, cy); size = cap height in output px."""
    k = max(2, round(PX * W / 1080)); f = ImageFont.truetype(FONT, max(6, int(size / k)))
    small = [(f.getbbox(t), t, c) for t, c in lines]; lw = max(b[2] - b[0] for b, _, _ in small) + 4; lh = int(size / k * 1.15)
    lay = Image.new("RGBA", (lw + 4, lh * len(lines) + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for j, (b, t, c) in enumerate(small):
        d.text(((lw + 4) // 2, 2 + lh * j + lh // 2), t, font=f, anchor="mm", fill=c + (255,), stroke_width=1, stroke_fill=(15, 10, 10, 255))
    lay = lay.resize((lay.width * k, lay.height * k), Image.NEAREST)
    if lay.width > W * 0.94: r = W * 0.94 / lay.width; lay = lay.resize((int(lay.width * r), int(lay.height * r)), Image.NEAREST)
    im.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay); return im

def title_card(base):
    m = f"{HERE}/images/mascot.png"
    if not os.path.exists(m): m = m.replace(".png", ".jpg")
    if os.path.exists(m): g = ImageOps.fit(Image.open(m).convert("RGB"), (W, H), Image.LANCZOS)
    else: g = Image.blend(ImageOps.grayscale(base).convert("RGB"), Image.new("RGB", (W, H), (10, 10, 10)), 0.35)
    return ptext(g, W / 2, H * 0.36, [("ИСТОРИЯ", (255, 255, 255)), ("ЗА МИНУТУ", (220, 30, 30))], W * 0.12)

def torn(a, b, p, seed):
    """b tears in from the left over a; ragged paper edge between them."""
    r = np.random.default_rng(seed); edge = np.cumsum(r.normal(0, W * 0.006, H)); edge -= edge.mean()
    x = (p * 1.2 - 0.1) * W + edge
    cols = np.arange(W)[None, :]; mask = cols < x[:, None]
    paper = (cols >= x[:, None]) & (cols < x[:, None] + W * 0.025)
    A, B = np.asarray(a), np.asarray(b); out = np.where(mask[..., None], B, A).copy()
    out[paper] = (238, 234, 225); shade = (cols >= x[:, None] + W * 0.025) & (cols < x[:, None] + W * 0.04)
    out[shade] = (out[shade] * 0.6).astype(np.uint8); return Image.fromarray(out)

def flash(im, s):   # s in 0..1, 1 = full white
    if s <= 0: return im
    glow = im.filter(ImageFilter.GaussianBlur(W / 60)); im = Image.blend(im, glow, min(1, s * 1.5))
    return Image.blend(im, Image.new("RGB", (W, H), (255, 246, 225)), s)

drops = rng.random((140, 3))
def rain(im, t):
    d = ImageDraw.Draw(im, "RGBA"); L = H * 0.035
    for x, y, v in drops:
        yy = (y * H + t * H * (1.3 + v)) % (H + L) - L; xx = (x * W - t * W * 0.12) % W
        d.line([(xx, yy), (xx - L * 0.15, yy + L)], fill=(220, 230, 255, int(70 + 70 * v)), width=max(1, W // 540))
    return im

def word_at(t):
    for r in rows:
        for w in r["words"]:
            if w["s"] <= t < max(w["e"], w["s"] + 0.12): return w["w"]
    return None

FS = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", int(W * 0.042))
def caption(im, t, r):
    # small running line at the top: the 3-word chunk holding the current word
    ws = r["words"]
    cur = next((k for k, w in enumerate(ws) if w["s"] <= t < (ws[k + 1]["s"] if k + 1 < len(ws) else w["e"] + 0.3)), None)
    if cur is not None and t < ws[cur]["e"] + 0.6:
        c0 = cur - cur % 3; txt = " ".join(w["w"] for w in ws[c0:c0 + 3])
        ImageDraw.Draw(im).text((W // 2, int(H * 0.065)), txt, font=FS, anchor="mm", fill=(245, 245, 245), stroke_width=max(2, W // 360), stroke_fill=(10, 10, 10))
    if r["yr"] and t < r["t0"] + 2.2: ptext(im, W / 2, H * 0.16, [(r["yr"], (205, 205, 205))], W * 0.2)
    if t >= r["kt"] and t < r["t1"] - 0.05:
        lines = [(r["k1"], (255, 255, 255))] + ([(r["k2"], (225, 35, 35))] if r["k2"] else [])
        ptext(im, W / 2, H * 0.6, lines, W * 0.075)
    return im

def spin(im, s):   # rotational whip blur, s 0..1
    if s <= 0.02: return im
    acc = np.zeros((H, W, 3), np.float32); n = 6
    for j in range(n): acc += np.asarray(im.rotate(s * 28 * (j / (n - 1) - 0.3), resample=Image.BILINEAR, expand=False).resize((W, H)), np.float32)
    out = Image.fromarray((acc / n).astype(np.uint8)); return out.filter(ImageFilter.GaussianBlur(W / 200 * s))

def grade(im):   # warm, slightly crunchy pixel look + vignette
    a = np.asarray(im).astype(np.float32); yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.35 * (((xx - W / 2) / (W / 1.3)) ** 2 + ((yy - H / 2) / (H / 1.3)) ** 2); return Image.fromarray(np.clip(a * v[..., None], 0, 255).astype(np.uint8))
VIG = None

def main():
    global VIG
    os.makedirs(f"{HERE}/out", exist_ok=True)
    imgs = {r["n"]: load(r["n"]) for r in rows}; tc = title_card(imgs[1])
    yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.32 * (((xx - W / 2) / (W / 1.25)) ** 2 + ((yy - H / 2) / (H / 1.25)) ** 2))[..., None]
    cuts = [r["t0"] for r in rows[1:]] + [title_t]
    audio = mix(cuts)
    out = f"{HERE}/out/cleopatra{'_preview' if PREVIEW else ''}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", audio, "-c:v", "libx264", "-preset", "veryfast" if PREVIEW else "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    TR = 0.35
    def scene_frame(i, t):
        r = rows[i]; p = (t - r["t0"]) / (r["t1"] - r["t0"] + TR); im = kenburns(imgs[r["n"]], np.clip(p, 0, 1), i)
        if r["n"] == 1 and t >= title_t: im = kenburns(tc, np.clip((t - title_t) / (title_end - title_t + TR), 0, 1) * 0.5, 0)
        if r["n"] in RAIN: im = rain(im, t)
        return im
    for f in range(int(TOTAL * FPS)):
        t = f / FPS; i = max(k for k, r in enumerate(rows) if r["t0"] <= t) if t >= rows[0]["t0"] else 0
        im = scene_frame(i, t)
        # incoming cut: torn paper around the title card, light flash elsewhere
        if rows[0]["t0"] <= title_t <= t < title_t + TR:            # scene 1 -> title card
            im = torn(scene_frame(0, title_t - 0.01), im, (t - title_t) / TR, 1)
        elif i == 1 and t < rows[1]["t0"] + TR:                       # title card -> scene 2
            im = torn(scene_frame(0, rows[1]["t0"] - 0.01), im, (t - rows[1]["t0"]) / TR, 2)
        elif i == len(rows) - 1 and t < rows[i]["t0"] + TR:          # final statue: torn paper too
            im = torn(scene_frame(i - 1, rows[i]["t0"] - 0.01), im, (t - rows[i]["t0"]) / TR, 3)
        elif i >= 1:
            d = t - rows[i]["t0"]
            if d < 0.3: im = flash(im, 1 - d / 0.3) if i % 2 else spin(im, 1 - d / 0.3)
        if i + 1 < len(rows) and i + 1 not in (1, len(rows) - 1):
            d = rows[i + 1]["t0"] - t
            if d < 0.22: im = flash(im, 1 - d / 0.22) if (i + 1) % 2 else spin(im, 1 - d / 0.22)
        a = (np.asarray(im).astype(np.float32) * VIG).clip(0, 255).astype(np.uint8); im = Image.fromarray(a)
        if t < TOTAL - 0.6 and not (title_t <= t < rows[1]["t0"]): im = caption(im, t, rows[i])
        fade = min(1, t / 0.25, (TOTAL - t) / 0.5)
        if fade < 1: im = Image.blend(Image.new("RGB", (W, H)), im, max(0, fade))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait(); print(out, round(TOTAL, 2), "s")

main()
