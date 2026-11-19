"""'Animated illustration' Short (like the Monroe-doctrine reference): one illustrated scene per sentence.
Each scene uses clips/NN.mp4 (animated in Grok from the picture) if present, else images/NN.(png|jpg) with a slow
push-in and gentle sway. Cuts come in with a short zoom-blur. Yellow condensed captions, 2 words at a time.
Music: synthesized sombre piano/strings; the last scenes play the Ode to Joy melody (public-domain composition,
our own rendition). Usage: python3 build.py [--preview]"""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


HERE = os.path.abspath(sys.argv[1]); NAME = os.path.basename(HERE)   # usage: build_one.py <video dir>
sys.path.insert(0, HERE)
PREVIEW = "--preview" in sys.argv
from script import SCENES
NOMUSIC = os.environ.get("MUSIC", "0") != "1"   # daily shorts: voice only, no music bed
W, H = (540, 960) if PREVIEW else (1080, 1920)
FPS, SR, GAP = 30, 48000, 0.15
FONT = ImageFont.truetype(f"{os.path.dirname(os.path.abspath(__file__))}/../fonts/Oswald-Bold.ttf", int(W * 0.082))
ODE_FROM = int(os.environ.get("ODE_FROM", "0"))     # scene where the Ode to Joy melody starts
rng = np.random.default_rng(3)

def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR

rows, t = [], 0.3
for n, *_ in SCENES:
    a, lead = trim(pcm(f"{HERE}/vo/{n:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{n:02d}.mp3.json"))
    words = [(t + w["s"] - lead, t + w["s"] - lead + w["d"], w["w"]) for w in meta["words"]]
    rows.append({"n": n, "t0": t, "a": a, "words": words}); t += len(a) / SR + GAP
TOTAL = t + 1.0
for i, r in enumerate(rows): r["t1"] = rows[i + 1]["t0"] if i + 1 < len(rows) else TOTAL

# ---------- music ----------
def tone(f, L, v, bright=0.35):
    x = np.arange(int(L * SR)) / SR
    y = (np.sin(2 * np.pi * f * x) + bright * np.sin(4 * np.pi * f * x) + 0.12 * np.sin(6 * np.pi * f * x)) * np.exp(-x * 2.2) * v
    return y

def music():
    n = int(TOTAL * SR); out = np.zeros((n, 2), np.float32); tt = np.arange(n) / SR
    ode_t = next((r["t0"] for r in rows if r["n"] == ODE_FROM), TOTAL + 1)
    # sombre part: D minor pad + slow low piano arpeggios
    chords = [(146.8, 174.6, 220.0), (116.5, 146.8, 174.6), (130.8, 164.8, 196.0), (110.0, 138.6, 164.8)]
    bar = 2.8
    for k in range(int(ode_t / bar) + 1):
        s = int(k * bar * SR); e = min(n, int((k + 1) * bar * SR + SR * 0.6), int(ode_t * SR) + SR // 2)
        if s >= e: break
        x = np.arange(e - s) / SR; env = np.minimum(1, x / 0.8) * np.minimum(1, (e - s) / SR - x + 0.01)
        for f in chords[k % 4]:
            out[s:e, 0] += np.sin(2 * np.pi * f * x) * env * 0.016; out[s:e, 1] += np.sin(2 * np.pi * (f + 0.4) * x) * env * 0.016
        for j, f in enumerate(chords[k % 4] + (chords[k % 4][0] * 2,)):
            p = s + int(j * bar / 4 * SR); y = tone(f, 2.0, 0.05)
            if p + len(y) < n: out[p:p + len(y)] += y[:, None]
    # Ode to Joy (D major): F# F# G A | A G F# E | D D E F# | F# E E ; then repeat ending E D D
    D4, E4, F4, G4, A4 = 293.7, 329.6, 370.0, 392.0, 440.0
    mel = [F4, F4, G4, A4, A4, G4, F4, E4, D4, D4, E4, F4, F4, E4, E4, None,
           F4, F4, G4, A4, A4, G4, F4, E4, D4, D4, E4, F4, E4, D4, D4, None]
    durs = [1] * 12 + [1.5, .5, 2, 0] + [1] * 12 + [1.5, .5, 2, 0]
    beat = 0.42; p = ode_t + 0.2
    for f, d in zip(mel, durs):
        if f and p < TOTAL - 0.5:
            y = tone(f, max(0.6, d * beat * 1.6), 0.085, 0.5); s = int(p * SR); L = min(len(y), n - s); out[s:s + L] += y[:L, None]
            b = tone(f / 2, d * beat * 1.4, 0.03); L = min(len(b), n - s); out[s:s + L] += b[:L, None]
        p += d * beat
    if ode_t > TOTAL: return out * (np.minimum(1, tt / 1.0) * np.minimum(1, (TOTAL - tt) / 1.6))[:, None]
    pad_e = n; x = np.arange(pad_e - int(ode_t * SR)) / SR; s = int(ode_t * SR)
    for f in (146.8, 185.0, 220.0):
        out[s:, 0] += np.sin(2 * np.pi * f * x) * np.minimum(1, x / 1.5) * 0.014; out[s:, 1] += np.sin(2 * np.pi * (f + .3) * x) * np.minimum(1, x / 1.5) * 0.014
    fade = np.minimum(1, tt / 1.0) * np.minimum(1, (TOTAL - tt) / 1.6); return out * fade[:, None]

def whoosh(L=0.35):
    x = np.arange(int(L * SR)) / SR; y = np.convolve(rng.standard_normal(len(x)), np.ones(14) / 14, "same")
    return y * np.exp(-((x - L * .6) / (L * .2)) ** 2) * 0.16

def mix():
    m = music(); m = m * 0 if NOMUSIC else m; n = len(m); vo = np.zeros(n, np.float32)
    for r in rows: s = int(r["t0"] * SR); vo[s:s + len(r["a"])] += r["a"][: n - s] * 1.15
    env = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), "same")
    out = m * (1 - 0.5 * np.clip(env * 12, 0, 1))[:, None] + vo[:, None]; wh = whoosh()
    for r in rows[1:]:
        s = int((r["t0"] - 0.2) * SR); out[s:s + len(wh)] += wh[:, None]
    out /= max(1, np.abs(out).max() / .95); os.makedirs(f"{HERE}/out", exist_ok=True); p = f"{HERE}/out/mix.wav"
    with wave.open(p, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
    return p

# ---------- pictures / clips ----------
class Clip:
    def __init__(self, path, dur):
        self.frames = []; raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
        k = W * H * 3; self.frames = [raw[i:i + k] for i in range(0, len(raw) - k + 1, k)]
        self.speed = max(0.5, min(1.0, len(self.frames) / max(1, dur * FPS)))   # slow down if the clip is short
    def at(self, dt):
        i = int(dt * FPS * self.speed)
        n = len(self.frames); i = i % (2 * n - 2) if n > 1 else 0; i = i if i < n else 2 * n - 2 - i   # ping-pong if too short
        return Image.frombytes("RGB", (W, H), self.frames[i])

class Still:
    def __init__(self, path, k):
        src = Image.open(path).convert("RGB"); cw, ch = int(W * 1.12), int(H * 1.12); ar = src.width / src.height
        if abs(ar - W / H) < 0.12: self.im = ImageOps.fit(src, (cw, ch), Image.LANCZOS)
        else:
            bg = ImageOps.fit(src, (cw, ch), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
            bg = Image.fromarray((np.asarray(bg).astype(np.float32) * 0.55).astype(np.uint8))
            fw = cw if ar > W / H else int(ch * 0.82 * ar); fh = int(fw / ar)
            if fh > ch * 0.82: fh = int(ch * 0.82); fw = int(fh * ar)
            fg = src.resize((fw, fh), Image.LANCZOS); bg.paste(fg, ((cw - fw) // 2, int((ch - fh) * 0.42))); self.im = bg
        self.k = k
    def at(self, dt):
        z = 1 + 0.035 * dt; sx = np.sin(dt * 0.9 + self.k) * W * 0.008; cw, ch = W * 1.0 / z, H * 1.0 / z
        x0 = (self.im.width - cw) / 2 + sx; y0 = (self.im.height - ch) / 2 + np.cos(dt * 0.7) * H * 0.004
        return self.im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)

def source(r, k):
    n = r["n"]
    for ext in ("mp4", "mov"):
        p = f"{HERE}/clips/{n:02d}.{ext}"
        if os.path.exists(p): return Clip(p, r["t1"] - r["t0"])
    for ext in ("png", "jpg", "jpeg"):
        p = f"{HERE}/images/{n:02d}.{ext}"
        if os.path.exists(p): return Still(p, k)
    im = Image.new("RGB", (W, H), (40 + 9 * n, 60, 70)); ImageDraw.Draw(im).text((W // 2, H // 3), f"{n:02d}", font=FONT, anchor="mm", fill="white")
    return Still.__new__(Still) if False else type("P", (), {"at": lambda self, dt, im=im: im})()

def zoomblur(im, s):    # s 1 -> 0 : entrance blur + slight zoom
    if s <= 0.02: return im
    z = 1 + 0.12 * s; cw, ch = W / z, H / z; x0, y0 = (W - cw) / 2, (H - ch) / 2
    im = im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BILINEAR)
    return im.filter(ImageFilter.GaussianBlur(W / 45 * s))

def chunks(words):
    out = []
    for i in range(0, len(words), 2):
        g = words[i:i + 2]; txt = " ".join(w for _, _, w in g).upper().strip(" ,.:;!?«»—").replace("«", "").replace("»", "")
        out.append((g[0][0], g[-1][1], txt))
    return out

def caption(im, t, chs):
    cur = None
    for j, (s, e, txt) in enumerate(chs):
        nxt = chs[j + 1][0] if j + 1 < len(chs) else e + 0.4
        if s <= t < max(nxt, s + 0.3) and t < e + 0.6: cur = txt
    if not cur: return im
    d = ImageDraw.Draw(im)
    d.text((W // 2, int(H * 0.775)), cur, font=FONT, anchor="mm", fill=(255, 226, 40), stroke_width=max(4, W // 150), stroke_fill=(10, 10, 10))
    return im

def main():
    audio = mix(); chs = chunks([w for r in rows for w in r["words"]])
    out = f"{HERE}/out/{NAME}{'_preview' if PREVIEW else ''}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", audio, "-c:v", "libx264", "-preset", "veryfast" if PREVIEW else "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    yy, xx = np.mgrid[0:H, 0:W]; vig = (1 - 0.30 * (((xx - W / 2) / (W / 1.2)) ** 2 + ((yy - H / 2) / (H / 1.2)) ** 2))[..., None]
    cur_i, src = -1, None
    for f in range(int(TOTAL * FPS)):
        t = f / FPS; i = max([k for k, r in enumerate(rows) if r["t0"] <= t] or [0])
        if i != cur_i: src = source(rows[i], i); cur_i = i
        dt = max(0, t - rows[i]["t0"]); im = src.at(dt)
        if i > 0 and dt < 0.28: im = zoomblur(im, 1 - dt / 0.28)
        im = Image.fromarray((np.asarray(im).astype(np.float32) * vig).clip(0, 255).astype(np.uint8))
        im = caption(im, t, chs)
        fade = min(1, t / 0.3, (TOTAL - t) / 0.8)
        if fade < 1: im = Image.blend(Image.new("RGB", (W, H)), im, max(0, fade))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait(); print(out, round(TOTAL, 2), "s")

main()
