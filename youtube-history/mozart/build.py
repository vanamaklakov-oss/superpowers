"""Mozart chalkboard Short with the anidoodle engine.
1) narration timeline -> chapter frames (mozart-timing.json), 2) render the chalk film in the anidoodle studio,
3) add music, chalk-scratch sounds, narration and yellow 2-word captions.  Usage: python3 build.py [--skip-render]"""
import json, os, shutil, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import SCENES

HERE = os.path.dirname(os.path.abspath(__file__)); STUDIO = os.environ.get("STUDIO", "/home/user/studio")
W, H, FPS, SR, GAP = 1080, 1920, 30, 48000, 0.25
FONT = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 76)
rng = np.random.default_rng(5)

def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR

rows, t = [], 0.6          # the board's first marks start a little before the voice
for n, *_ in SCENES:
    a, lead = trim(pcm(f"{HERE}/vo/{n:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{n:02d}.mp3.json"))
    rows.append({"n": n, "t0": t, "a": a, "words": [(t + w["s"] - lead, t + w["s"] - lead + w["d"], w["w"]) for w in meta["words"]]})
    t += len(a) / SR + GAP
TOTAL = t + 1.0; NF = int(round(TOTAL * FPS))
fr = [0] + [int(round((r["t0"] - 0.35) * FPS)) for r in rows[1:]] + [NF]     # the eraser starts just before each sentence
timing = [{"n": r["n"], "a": fr[i], "b": fr[i + 1]} for i, r in enumerate(rows)]

def render():
    cc = f"{STUDIO}/src/canvas-core"
    json.dump(timing, open(f"{cc}/mozart-timing.json", "w"))
    shutil.copy(f"{HERE}/mozart.ts", f"{cc}/mozart.ts")
    open(f"{STUDIO}/src/hosts/page-mozart.ts", "w").write('import { mozart } from "../canvas-core/mozart";\nimport { mountFilm } from "./page";\nmountFilm(mozart);\n')
    subprocess.run(["node", "tools/render.mjs", "mozart", "--out", "out/mozart.mp4"], cwd=STUDIO, check=True)

def tone(f, L, v, bright=0.35):
    x = np.arange(int(L * SR)) / SR
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(4 * np.pi * f * x) + 0.12 * np.sin(6 * np.pi * f * x)) * np.exp(-x * 2.0) * v

def music():
    n = int(TOTAL * SR); out = np.zeros((n, 2), np.float32); tt = np.arange(n) / SR
    # a quiet G-minor harpsichord-ish walk (our own notes), 72 bpm, with a sustained organ pad: a chapel mood
    chords = [(196.0, 233.1, 293.7), (174.6, 220.0, 261.6), (155.6, 196.0, 233.1), (146.8, 185.0, 220.0)]
    bar = 60 / 72 * 4
    for k in range(int(TOTAL / bar) + 1):
        s = int(k * bar * SR); e = min(n, int((k + 1) * bar * SR) + SR // 3)
        if s >= n: break
        x = np.arange(e - s) / SR; env = np.minimum(1, x / 0.6) * np.minimum(1, ((e - s) / SR - x) / 0.4)
        for f in chords[k % 4]:
            out[s:e, 0] += np.sin(2 * np.pi * f * x) * env * 0.012; out[s:e, 1] += np.sin(2 * np.pi * (f + .5) * x) * env * 0.012
        for j in range(8):
            f = chords[k % 4][j % 3] * (2 if j in (3, 7) else 1); p = s + int(j * bar / 8 * SR); y = tone(f * 2, 0.6, 0.035, 0.6)
            if p + len(y) < n: out[p:p + len(y)] += y[:, None] * [0.9, 1.0]
    return out * (np.minimum(1, tt / 1.0) * np.minimum(1, (TOTAL - tt) / 1.6))[:, None]

def scratch():
    """chalk on slate: short band-passed noise bursts while each chapter is being written, a soft swish for each wipe"""
    n = int(TOTAL * SR); out = np.zeros(n, np.float32)
    for r in rows:
        t0 = r["t0"] - 0.2; t1 = t0 + min(3.0, (len(r["a"]) / SR) * 0.6); t = t0
        while t < t1:
            L = int((0.08 + rng.random() * 0.18) * SR); s = int(t * SR)
            if s + L >= n: break
            z = rng.standard_normal(L); z = np.diff(np.concatenate([[0], z])); env = np.sin(np.linspace(0, np.pi, L)) ** 2
            out[s:s + L] += z * env * 0.018; t += 0.12 + rng.random() * 0.22
    for r in rows[1:]:
        s = int((r["t0"] - 0.35) * SR); L = int(0.4 * SR); z = np.convolve(rng.standard_normal(L), np.ones(20) / 20, "same")
        out[s:s + L] += z * np.sin(np.linspace(0, np.pi, L)) * 0.12
    return out

def mix():
    m = music(); n = len(m); vo = np.zeros(n, np.float32)
    for r in rows: s = int(r["t0"] * SR); vo[s:s + len(r["a"])] += r["a"][: n - s] * 1.15
    env = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), "same")
    out = m * (1 - 0.5 * np.clip(env * 12, 0, 1))[:, None] + vo[:, None] + scratch()[:, None]
    out /= max(1, np.abs(out).max() / .95); p = f"{HERE}/out/mix.wav"
    with wave.open(p, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
    return p

def post():
    os.makedirs(f"{HERE}/out", exist_ok=True); audio = mix()
    words = [w for r in rows for w in r["words"]]; chs = []
    for i in range(0, len(words), 2):
        g = words[i:i + 2]; chs.append((g[0][0], g[-1][1], " ".join(w for *_, w in g).upper().strip(" ,.:;!?—").replace("«", "").replace("»", "")))
    src = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", f"{STUDIO}/out/mozart.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    out = f"{HERE}/out/mozart.mp4"
    dst = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    f = 0
    while True:
        buf = src.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        t = f / FPS; im = Image.frombytes("RGB", (W, H), buf); cur = None
        for j, (s, e, txt) in enumerate(chs):
            nxt = chs[j + 1][0] if j + 1 < len(chs) else e + 0.4
            if s <= t < max(nxt, s + 0.3) and t < e + 0.6: cur = txt
        if cur: ImageDraw.Draw(im).text((W // 2, 1640), cur, font=FONT, anchor="mm", fill=(255, 226, 40), stroke_width=7, stroke_fill=(10, 10, 10))
        dst.stdin.write(im.tobytes()); f += 1
    dst.stdin.close(); dst.wait(); print(out, round(TOTAL, 2), "s")

if __name__ == "__main__":
    if "--skip-render" not in sys.argv: render()
    post()
