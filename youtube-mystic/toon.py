#!/usr/bin/env python3
# Движок «мультяшный explainer» (стиль 2.5D: объёмные фоны + человечки-«фонарики»), см. research/ricksclips.md.
# Использование: python3 toon.py <папка> tts|check|stills|build
# story.py: SCENES = [(n, "текст", [shot, ...])], shot = {"at": слово|индекс|None, "k": вид плана, "cam": in|out|l|r|up|down, "sfx": ..., ...}
# План начинается на слове "at" (первый план сцены — с начала сцены). Цель: 2–3 плана на фразу, 7–10 склеек на 10 секунд.
import importlib.util, json, math, os, re, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 48000
FD = "/usr/share/fonts/opentype/inter"
def F(name, size): return ImageFont.truetype(f"{FD}/{name}.otf", size)
CAP = F("Inter-Black", 100); LBL = F("Inter-Black", 64); LBS = F("Inter-ExtraBold", 44)
INK = (20, 18, 26); WHITE = (250, 250, 248); YEL = (255, 214, 0); REDC = (238, 64, 64)
rng = np.random.default_rng(7)

DIR = os.path.abspath(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else "build"; NAME = os.path.basename(DIR)
spec = importlib.util.spec_from_file_location("story", f"{DIR}/story.py"); ST = importlib.util.module_from_spec(spec); spec.loader.exec_module(ST)
SCENES, YELLOW, RED = ST.SCENES, {w.lower() for w in ST.YELLOW}, {w.lower() for w in ST.RED}
VOICE, RATE, PITCH = getattr(ST, "VOICE", ("ru-RU-DmitryNeural", 10, 4))
STY = getattr(ST, "STYLE", {}); W, H = STY.get("size", (W, H)); CAP = F("Inter-Black", STY.get("capsize", 100))

# ---------------- voice ----------------
def tts():
    import asyncio, ssl, time, edge_tts, edge_tts.communicate as c
    c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt"); VO = f"{DIR}/vo"; os.makedirs(VO, exist_ok=True)
    def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    def say(text, out, VOICE=VOICE, RATE=RATE, PITCH=PITCH):
        for dr in (0, 1, -1, 2, 0, -2, 3):
            async def go():
                com = edge_tts.Communicate(text, voice=VOICE, rate=f"{RATE + dr:+d}%", pitch=f"{PITCH:+d}Hz", boundary="WordBoundary"); ws = []
                with open(out, "wb") as f:
                    async for ch in com.stream():
                        if ch["type"] == "audio": f.write(ch["data"])
                        elif ch["type"] == "WordBoundary": ws.append({"w": ch["text"], "s": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
                return ws
            try:
                ws = asyncio.run(asyncio.wait_for(go(), 45))
                if ws and os.path.getsize(out) > 2000: return ws
            except Exception: time.sleep(6)
        raise RuntimeError(f"tts failed: {text}")
    for n, text, _, *ex in SCENES:
        if not text: continue
        if os.environ.get("SHARD") and n % 2 != int(os.environ["SHARD"]): continue
        out = f"{VO}/{n:02d}.mp3"; vs = list((ex[0] if ex else {}).get("voice", (VOICE, RATE, PITCH)))
        if os.path.exists(out + ".json"):
            j = json.load(open(out + ".json"))
            if j.get("text") == text and j.get("voice") == vs: continue
        parts = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]; files, words, t = [], [], 0.0
        for i, s in enumerate(parts):
            pf = f"{VO}/{n:02d}.p{i}.mp3"; ws = say(s, pf, *vs); files.append(pf); words += [{**w, "s": w["s"] + t} for w in ws]; t += dur(pf)
        lst = f"{VO}/{n:02d}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
        for f in files + [lst]: os.remove(f)
        json.dump({"text": text, "voice": vs, "dur": dur(out), "words": words}, open(out + ".json", "w"), ensure_ascii=False)
        print(n, "ok", round(dur(out), 2), flush=True)

FX = {"ghost": "aecho=0.8:0.75:70|160:0.45|0.3,lowpass=f=3000,volume=1.1", "whisper": "highpass=f=300,aecho=0.6:0.5:40:0.3,volume=1.2", "phone": "highpass=f=400,lowpass=f=3200,volume=1.3"}
def pcm(p, fx=None, tempo=1.0):
    af = ",".join(([FX[fx]] if fx else []) + ([f"atempo={tempo}"] if tempo != 1.0 else []))
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p] + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def check():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", compute_type="int8")
    for n, text, _, *ex in SCENES:
        if not text: continue
        a = pcm(f"{DIR}/vo/{n:02d}.mp3")[::3]
        s, _ = m.transcribe(a, language="ru"); got = " ".join(x.text.strip() for x in s)
        norm = lambda z: re.sub(r"[^а-яё ]", "", z.lower().replace("ё", "е")).split()
        miss = [w for w in norm(text) if w not in norm(got)]
        print(f"{n:2d} {'OK ' if not miss else 'ПРОВЕРИТЬ'} | {got}" + (f"   ← нет: {miss}" if miss else ""))

if MODE == "tts": tts(); sys.exit()
if MODE == "check": check(); sys.exit()

# ---------------- timeline ----------------
def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 720, 0), min(on[-1] + 1800, len(a)); return a[s:e], s / SR
rows, t = [], 0.25
for n, text, shots, *ex in SCENES:
    ex = ex[0] if ex else {}
    if not text:
        rows.append({"n": n, "t0": t, "a": np.zeros(int(ex.get("silent", 2.5) * SR), np.float32), "words": [], "shots": shots, "who": None}); t += ex.get("silent", 2.5); continue
    TP = STY.get("tempo", 1.0); a, lead = trim(pcm(f"{DIR}/vo/{n:02d}.mp3", ex.get("fx"), TP)); meta = json.load(open(f"{DIR}/vo/{n:02d}.mp3.json"))
    words = [(t + w["s"] / TP - lead, t + (w["s"] + w["d"]) / TP - lead, w["w"]) for w in meta["words"]]
    rows.append({"n": n, "t0": t, "a": a, "words": words, "shots": shots, "who": ex.get("who")}); t += len(a) / SR + 0.08 + ex.get("hold", STY.get("gap", 0))
TOTAL = t + 1.4
def wt(r, i):
    if i is None: return r["t0"]
    if isinstance(i, str):
        w, _, k = i.partition("#"); k = int(k or 1); cl = lambda z: re.sub(r"[^\wё]", "", z.lower())
        hits = [x for x in r["words"] if cl(x[2]).startswith(cl(w))]
        if len(hits) < k: raise ValueError(f"сцена {r['n']}: нет слова {i!r}")
        return hits[k - 1][0] - 0.06
    return r["words"][min(i, len(r["words"]) - 1)][0] - 0.06
SHOTS = []
for r in rows:
    for s in r["shots"]: SHOTS.append({**s, "t0": max(r["t0"], wt(r, s.get("at"))), "row": r})
SHOTS.sort(key=lambda s: s["t0"]); SHOTS[0]["t0"] = 0.0
for i, s in enumerate(SHOTS): s["t1"] = SHOTS[i + 1]["t0"] if i + 1 < len(SHOTS) else TOTAL; s["i"] = i

# ---------------- drawing helpers ----------------
def ss(w, h, fn, k=2):
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), k); return im.resize((w, h), Image.LANCZOS)
def grad(c0, c1, w=W, h=H, horiz=False):
    a = np.linspace(0, 1, w if horiz else h); a = a[None, :, None] if horiz else a[:, None, None]
    arr = (np.array(c0) * (1 - a) + np.array(c1) * a).astype(np.uint8)
    arr = np.repeat(arr, h, 0) if horiz else np.repeat(arr, w, 1); return Image.fromarray(arr, "RGB").convert("RGBA")
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def eout(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def blob(w, h, col, a, blur):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((blur * 2, blur * 2, w - blur * 2, h - blur * 2), fill=col + (a,))
    return im.filter(ImageFilter.GaussianBlur(blur))
def shadow(im, off=(0, 18), blur=18, a=110):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); out = Image.new("RGBA", (im.width + abs(off[0]) + blur * 2, im.height + abs(off[1]) + blur * 2), (0, 0, 0, 0))
    out.alpha_composite(sh, (blur + off[0], blur + off[1])); out.alpha_composite(im, (blur, blur)); return out, blur
def put(base, spr, cx, by, shadowed=True):  # по центру-низу
    if shadowed: spr, b = shadow(spr); cx, by = cx, by + b
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(by - spr.height)))
def label(base, s, cx, cy, col=WHITE, font=LBL, bg=None, a=1.0):
    d = ImageDraw.Draw(base)
    if bg:
        w = d.textlength(s, font=font); pad = 26
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((cx - w / 2 - pad, cy - 50, cx + w / 2 + pad, cy + 50), 26, fill=bg + (int(235 * a),))
        base.alpha_composite(lay)
    d.text((cx, cy), s, font=font, fill=col + (int(255 * a),), anchor="mm", stroke_width=0 if bg else 8, stroke_fill=INK)
C = {}
def cached(key, fn):
    if key not in C: C[key] = fn()
    return C[key]

# ---------- персонаж «фонарик» ----------
def bean(body=(70, 110, 190), eyes="dot", mouth="smile", arms="down", legs="stand", cap=False, sweat=False, flip=False, s=1.0, look=0, hair=None, glasses=False, hcol=(60, 40, 30)):
    key = ("bean", body, eyes, mouth, arms, legs, cap, sweat, flip, s, look, hair, glasses, hcol)
    if key in C: return C[key]
    w, h = int(340 * s), int(560 * s)
    def dr(d, k):
        K = k * s; L = lambda *p: [v * K for v in p]; lw = int(9 * K)
        hx, hy, hr = 170, 125, 88
        # ноги
        lg = {"stand": [((140, 380), (128, 505)), ((200, 380), (212, 505))], "run1": [((140, 380), (90, 480)), ((200, 380), (250, 470))],
              "run2": [((140, 380), (180, 500)), ((200, 380), (150, 495))], "sit": [((140, 380), (100, 420)), ((200, 380), (240, 420))]}[legs]
        for (a, b) in lg:
            d.line(L(*a, *b), fill=INK, width=lw); d.ellipse(L(b[0] - 26, b[1] - 12, b[0] + 26, b[1] + 14), fill=INK)
        # руки
        am = {"down": [((108, 250), (78, 360)), ((232, 250), (262, 360))], "up": [((108, 250), (40, 150)), ((232, 250), (300, 150))],
              "point": [((108, 250), (78, 360)), ((232, 250), (330, 210))], "run1": [((108, 250), (50, 300)), ((232, 250), (300, 200))],
              "run2": [((108, 250), (60, 190)), ((232, 250), (290, 320))], "bino": [((108, 250), (130, 150)), ((232, 250), (210, 150))],
              "hips": [((108, 250), (60, 310)), ((232, 250), (280, 310))], "rope": [((108, 250), (150, 340)), ((232, 250), (200, 340))]}[arms]
        for (a, b) in am:
            d.line(L(*a, *b), fill=INK, width=lw); d.ellipse(L(b[0] - 15, b[1] - 15, b[0] + 15, b[1] + 15), fill=WHITE, outline=INK, width=int(6 * K))
        # тело
        d.rounded_rectangle(L(100, 205, 240, 395), radius=int(62 * K), fill=body, outline=INK, width=lw)
        lt = tuple(min(255, c + 38) for c in body); d.rounded_rectangle(L(118, 222, 150, 330), radius=int(16 * K), fill=lt)
        # голова
        if hair == "long": d.rounded_rectangle(L(hx - hr - 14, hy - hr - 8, hx + hr + 14, hy + 120), radius=int(70 * K), fill=hcol, outline=INK, width=lw)
        if hair == "scarf": d.polygon(L(hx - hr - 20, hy - 10, hx + hr + 20, hy - 10, hx + 40, hy + 120, hx - 40, hy + 120), fill=hcol, outline=INK, width=lw)
        d.ellipse(L(hx - hr, hy - hr, hx + hr, hy + hr), fill=WHITE, outline=INK, width=lw)
        if hair == "long": d.chord(L(hx - hr, hy - hr - 6, hx + hr, hy + 10), 180, 360, fill=hcol, outline=INK, width=lw)
        if hair == "short": d.chord(L(hx - hr, hy - hr - 10, hx + hr, hy - 10), 180, 360, fill=hcol, outline=INK, width=lw)
        if hair == "scarf":
            d.chord(L(hx - hr - 12, hy - hr - 14, hx + hr + 12, hy + 40), 180, 360, fill=hcol, outline=INK, width=lw)
            for i in range(5): d.ellipse(L(hx - 70 + i * 34, hy - 60 - (i % 2) * 18, hx - 58 + i * 34, hy - 48 - (i % 2) * 18), fill=WHITE)
        d.ellipse(L(hx - hr + 22, hy - hr + 18, hx - hr + 62, hy - hr + 48), fill=(255, 255, 255))
        ex = 32; ey = hy - 8; lx = look * 10
        if eyes == "dot":
            for sx in (-1, 1): d.ellipse(L(hx + sx * ex - 11 + lx, ey - 15, hx + sx * ex + 11 + lx, ey + 15), fill=INK)
        elif eyes in ("wide", "shock"):
            r0 = 26 if eyes == "wide" else 32; rp = 9 if eyes == "wide" else 6
            for sx in (-1, 1):
                d.ellipse(L(hx + sx * ex - r0, ey - r0, hx + sx * ex + r0, ey + r0), fill=WHITE, outline=INK, width=int(6 * K))
                d.ellipse(L(hx + sx * ex - rp + lx, ey - rp, hx + sx * ex + rp + lx, ey + rp), fill=INK)
            if eyes == "shock":
                for sx in (-1, 1): d.line(L(hx + sx * ex - 24, ey - 50 - sx * 0, hx + sx * ex + 20 * sx * 0 + 24, ey - 56), fill=INK, width=int(7 * K))
        elif eyes == "angry":
            for sx in (-1, 1):
                d.ellipse(L(hx + sx * ex - 11, ey - 10, hx + sx * ex + 11, ey + 18), fill=INK)
                d.line(L(hx + sx * ex - 26, ey - 36 + (sx * 10), hx + sx * ex + 26, ey - 36 - (sx * 10)), fill=INK, width=int(8 * K))
        elif eyes == "void":
            for sx in (-1, 1): d.ellipse(L(hx + sx * ex - 24, ey - 26, hx + sx * ex + 24, ey + 26), fill=(6, 4, 8))
        elif eyes == "closed":
            for sx in (-1, 1): d.arc(L(hx + sx * ex - 18, ey - 10, hx + sx * ex + 18, ey + 18), 200, 340, fill=INK, width=int(7 * K))
        my = hy + 40
        if mouth == "smile": d.arc(L(hx - 30, my - 26, hx + 30, my + 18), 20, 160, fill=INK, width=int(7 * K))
        elif mouth == "line": d.line(L(hx - 22, my, hx + 22, my), fill=INK, width=int(7 * K))
        elif mouth == "frown": d.arc(L(hx - 26, my, hx + 26, my + 34), 200, 340, fill=INK, width=int(7 * K))
        elif mouth == "grin":
            d.chord(L(hx - 52, my - 34, hx + 52, my + 34), 0, 180, fill=(10, 6, 8), outline=INK, width=int(5 * K))
            for i in range(7): d.line(L(hx - 42 + i * 14, my, hx - 42 + i * 14, my + 14), fill=WHITE, width=int(4 * K))
        elif mouth == "o": d.ellipse(L(hx - 14, my - 12, hx + 14, my + 20), fill=INK)
        elif mouth == "scream": d.ellipse(L(hx - 26, my - 14, hx + 26, my + 40), fill=INK); d.ellipse(L(hx - 14, my + 14, hx + 14, my + 36), fill=(220, 80, 90))
        if glasses:
            for sx in (-1, 1): d.ellipse(L(hx + sx * ex - 26, ey - 24, hx + sx * ex + 26, ey + 24), outline=INK, width=int(6 * K))
            d.line(L(hx - 8, ey, hx + 8, ey), fill=INK, width=int(5 * K))
        if cap:
            d.chord(L(hx - 86, hy - 100, hx + 86, hy + 30), 180, 360, fill=(32, 44, 78), outline=INK, width=lw)
            d.rounded_rectangle(L(hx - 98, hy - 40, hx + 98, hy - 24), radius=int(8 * K), fill=(24, 30, 52), outline=INK, width=int(5 * K))
            d.ellipse(L(hx - 14, hy - 78, hx + 14, hy - 54), fill=YEL, outline=INK, width=int(4 * K))
        if sweat:
            d.polygon(L(hx + 80, hy - 50, hx + 66, hy - 18, hx + 94, hy - 18), fill=(120, 190, 255)); d.ellipse(L(hx + 66, hy - 34, hx + 94, hy - 6), fill=(120, 190, 255))
        if arms == "bino":
            d.rounded_rectangle(L(118, 100, 222, 150), radius=int(14 * K), fill=(40, 40, 50), outline=INK, width=int(5 * K))
    im = ss(w, h, dr, 2)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    C[key] = im; return im
KEEPER = (44, 70, 130); SHIRT = (236, 236, 226); OILSKIN = (246, 196, 40)

# ---------- окружение ----------
def storm_sky(dark=0.0):
    def mk():
        im = grad((14, 22, 44), (52, 72, 104))
        for i in range(9):
            b = blob(int(rng.integers(500, 900)), int(rng.integers(180, 320)), (30 + i * 3, 40 + i * 3, 64 + i * 3), 200, 40)
            im.alpha_composite(b, (int(rng.integers(-300, 700)), int(rng.integers(-60, 700))))
        return im
    return cached(("sky",), mk)
def sea_layer(y0, t, amp=1.0, col=(18, 44, 78)):
    im = Image.new("RGBA", (W, H - y0 + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for band in range(6):
        yy = 40 + band * 90; c = tuple(int(v * (1 + band * 0.08)) for v in col)
        pts = [(x, yy + math.sin(x / 90 + t * (1.6 + band * 0.3) + band) * 16 * amp) for x in range(-20, W + 40, 30)]
        d.polygon(pts + [(W + 40, im.height), (-20, im.height)], fill=c)
        for x in range(-20, W, 140): d.line([(x + (t * 60) % 140, yy + math.sin((x) / 90 + t * 1.6 + band) * 16 * amp - 2), (x + 50 + (t * 60) % 140, yy - 4)], fill=(150, 190, 220), width=3)
    return im
RAIN = []
for i in range(3):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(240):
        x, y = rng.integers(-200, W), rng.integers(0, H); d.line([(x, y), (x + 22, y + 70)], fill=(190, 210, 235, 90), width=3)
    RAIN.append(im)
def rain(im, t, a=1.0):
    r = RAIN[int(t * 12) % 3]
    if a < 1: r = r.copy(); r.putalpha(r.getchannel("A").point(lambda v: int(v * a)))
    im.alpha_composite(r)
def cliffs(w=W, h=900, col=(46, 52, 60), top=(64, 104, 60), seed=1):
    def mk():
        g = np.random.default_rng(seed)
        def dr(d, k):
            pts = [(0, 140)]
            for x in range(0, w + 60, 60): pts.append((x, 120 + g.integers(-30, 40) + (0 if 200 < x < 800 else 60)))
            pts += [(w, h), (0, h)]; P = [(x * k, y * k) for x, y in pts]
            d.polygon(P, fill=col); d.line(P[:-2], fill=top, width=int(40 * k))
            for _ in range(26):
                x, y = g.integers(0, w), g.integers(260, h); d.line([(x * k, y * k), ((x + g.integers(-60, 60)) * k, (y + 80) * k)], fill=(36, 40, 48), width=int(5 * k))
        return ss(w, h, dr)
    return cached(("cliff", w, h, col, seed), mk)
def tower(lit=True, s=1.0):
    def mk():
        w, h = int(300 * s), int(700 * s)
        def dr(d, k):
            K = k * s; L = lambda *p: [v * K for v in p]
            d.polygon(L(60, 680, 240, 680, 210, 230, 90, 230), fill=(236, 234, 226), outline=INK, width=int(8 * K))
            d.polygon(L(150, 680, 240, 680, 210, 230, 150, 230), fill=(204, 204, 198))
            d.rectangle(L(70, 200, 230, 236), fill=(60, 60, 70), outline=INK, width=int(7 * K))
            d.rectangle(L(95, 110, 205, 200), fill=(255, 226, 120) if lit else (54, 64, 80), outline=INK, width=int(7 * K))
            for x in (125, 150, 175): d.line(L(x, 110, x, 200), fill=INK, width=int(4 * K))
            d.polygon(L(85, 112, 215, 112, 150, 50), fill=(70, 70, 80), outline=INK, width=int(7 * K))
            d.rounded_rectangle(L(120, 520, 180, 680), radius=int(26 * K), fill=(70, 60, 54), outline=INK, width=int(6 * K))
        return ss(w, h, dr)
    return cached(("tower", lit, s), mk)
def beam(cx, cy, ang, length=1400, a=90):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for side in (0, math.pi):
        a0 = ang + side; p1 = (cx + math.cos(a0 - 0.12) * length, cy + math.sin(a0 - 0.12) * length * 0.35); p2 = (cx + math.cos(a0 + 0.12) * length, cy + math.sin(a0 + 0.12) * length * 0.35)
        d.polygon([(cx, cy), p1, p2], fill=(255, 236, 150, a))
    return im.filter(ImageFilter.GaussianBlur(14))
def vignette(a=170):
    def mk():
        y, x = np.ogrid[:H, :W]; r = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.6)) ** 2)
        al = (np.clip(r - 0.55, 0, 1) / 0.45) ** 1.6 * a; return Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), al.astype(np.uint8)]), "RGBA")
    return cached(("vig", a), mk)
def wall(col=(74, 62, 54)):
    def mk():
        im = grad(col, tuple(int(c * 0.6) for c in col)); d = ImageDraw.Draw(im)
        for x in range(0, W, 150): d.line([(x, 0), (x, H)], fill=tuple(int(c * 0.75) for c in col), width=6)
        return im
    return cached(("wall", col), mk)
def floor(im, y, col=(58, 44, 36)):
    ImageDraw.Draw(im).rectangle((0, y, W, H), fill=col); im.alpha_composite(grad((0, 0, 0, 0), (0, 0, 0, 120), W, H - y), (0, y))
def big_wave(w, h, t, col=(30, 80, 120)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0, h)] + [(x, h * 0.25 + math.sin(x / w * 3.1) * -h * 0.22 + math.sin(x / 50 + t * 5) * 14) for x in range(0, w + 1, 20)] + [(w, h)]
    d.polygon(pts, fill=col); d.line(pts[1:-1], fill=(220, 240, 250), width=18)
    for _ in range(40):
        x = rng.integers(0, w); y = h * 0.2 + math.sin(x / w * 3.1) * -h * 0.22 - rng.integers(0, 120); r = rng.integers(6, 20)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 245, 250, 220))
    return im

# ---------------- планы ----------------
def sh_lighthouse(p, lt, D):
    im = storm_sky().copy(); lit = p.get("lit", True)
    if p.get("lightning") and abs(lt - p["lightning"]) < 0.12: im.alpha_composite(Image.new("RGBA", (W, H), (220, 230, 255, 150)))
    if lit: im.alpha_composite(beam(540, 640, lt * 1.3 + 0.4))
    im.alpha_composite(sea_layer(0, lt), (0, 1180)); im.alpha_composite(cliffs(), (0, 1020))
    put(im, tower(lit), 540, 1170)
    if lit: im.alpha_composite(blob(420, 420, (255, 230, 140), 120, 60), (330, 430))
    if p.get("ship"): sp = ship_sprite(0.45); im.alpha_composite(sp, (int(80 + lt * 30), 1150))
    if p.get("text"): label(im, p["text"], 540, 300, YEL, bg=INK)
    rain(im, lt); return im
def ship_sprite(s=1.0):
    def mk():
        w, h = int(700 * s), int(420 * s)
        def dr(d, k):
            K = k * s; L = lambda *p: [v * K for v in p]
            d.polygon(L(20, 260, 680, 260, 600, 400, 90, 400), fill=(40, 36, 44), outline=INK, width=int(8 * K)); d.rectangle(L(60, 262, 640, 290), fill=(170, 40, 40))
            d.rectangle(L(200, 170, 480, 262), fill=(232, 226, 214), outline=INK, width=int(7 * K))
            for x in (230, 300, 370, 440): d.rectangle(L(x, 195, x + 26, 225), fill=(255, 220, 120))
            d.rectangle(L(380, 60, 440, 170), fill=(60, 56, 60), outline=INK, width=int(7 * K)); d.rectangle(L(380, 60, 440, 84), fill=(170, 40, 40))
            for i, r in enumerate((30, 42, 56)): d.ellipse(L(420 + i * 50 - r, 40 - i * 30 - r, 420 + i * 50 + r, 40 - i * 30 + r), fill=(120, 120, 130))
        return ss(w, h, dr)
    return cached(("ship", s), mk)
def sh_ship(p, lt, D):
    im = storm_sky().copy(); im.alpha_composite(tower(False, 0.35), (820, 980)); im.alpha_composite(cliffs(500, 300, seed=3), (650, 1180))
    im.alpha_composite(sea_layer(0, lt, 1.3), (0, 1240)); bob = math.sin(lt * 2.2) * 14
    im.alpha_composite(ship_sprite(1.2), (-40, int(1020 + bob)))
    put(im, bean(KEEPER, "wide", "o", "bino", cap=True, s=0.8), 330, int(1295 + bob))
    if lt > 0.5: label(im, "?!", 470, int(860 + bob), YEL, LBL)
    rain(im, lt); return im
def sh_map(p, lt, D):
    im = grad((26, 70, 118), (16, 44, 80)); d = ImageDraw.Draw(im)
    def land():
        def dr(d, k):
            P = [(1080, 300), (760, 380), (700, 520), (780, 640), (690, 760), (760, 900), (700, 1060), (820, 1200), (760, 1400), (880, 1560), (1080, 1600)]
            d.polygon([(x * k, y * k) for x, y in P], fill=(92, 140, 84), outline=(40, 60, 40), width=int(10 * k))
            for (x, y, r) in ((560, 640, 70), (520, 760, 46), (600, 520, 38)): d.ellipse(((x - r) * k, (y - r) * k, (x + r) * k, (y + r * 1.6) * k), fill=(92, 140, 84), outline=(40, 60, 40), width=int(8 * k))
        return ss(W, H, dr)
    im.alpha_composite(cached(("land",), land)); label(im, "ШОТЛАНДИЯ", 900, 980, WHITE, LBS)
    for i in range(0, 12):
        if lt * 14 > i: d.ellipse((470 - i * 22 - 7, 690 - i * 8 - 7, 470 - i * 22 + 7, 690 - i * 8 + 7), fill=(255, 255, 255, 200))
    pa = eout((lt - 0.7) / 0.3);
    if pa > 0:
        y = 600 - 40 * (1 - pa); d.ellipse((205, y + 25, 245, y + 65), fill=REDC, outline=INK, width=6); d.polygon([(212, y + 55), (238, y + 55), (225, y + 90)], fill=REDC)
        label(im, p.get("pin", "ОСТРОВА ФЛАННАН"), 300, y - 30, YEL, LBS, bg=INK)
    label(im, p.get("title", "ДЕКАБРЬ 1900"), 540, 260, WHITE, LBL, bg=(200, 50, 50)); return im
def sh_calendar(p, lt, D):
    im = wall((60, 72, 96)).copy(); a, b = p.get("from", 15), p.get("to", 26)
    n = a + int((b - a) * ease((lt - 0.2) / max(0.4, D - 0.6)))
    def card(num):
        def dr(d, k):
            d.rounded_rectangle((0, 0, 640 * k, 700 * k), radius=40 * k, fill=WHITE, outline=INK, width=10 * k); d.rounded_rectangle((0, 0, 640 * k, 200 * k), radius=40 * k, fill=(210, 54, 54), outline=INK, width=10 * k)
            d.rectangle((5 * k, 150 * k, 635 * k, 200 * k), fill=(210, 54, 54)); d.text((320 * k, 100 * k), "ДЕКАБРЬ", font=F("Inter-Black", 80 * k), fill=WHITE, anchor="mm")
            d.text((320 * k, 450 * k), str(num), font=F("Inter-Black", 330 * k), fill=INK, anchor="mm")
            for x in (140, 500): d.ellipse(((x - 22) * k, -22 * k, (x + 22) * k, 22 * k), fill=(40, 40, 46))
        return ss(640, 700, dr)
    put(im, cached(("cal", n), lambda: card(n)), 540, 1280)
    if p.get("label"): label(im, p["label"], 540, 420, YEL, LBL, bg=INK)
    return im
def sh_climb(p, lt, D):
    im = storm_sky().copy(); im.alpha_composite(sea_layer(0, lt), (0, 1350))
    def steps():
        def dr(d, k):
            d.polygon([(0, 500 * k), (W * k, 120 * k), (W * k, 1100 * k), (0, 1100 * k)], fill=(50, 56, 64))
            for i in range(14): x = i * 80; y = 500 - i * 27; d.rectangle((x * k, y * k, (x + 80) * k, (y + 18) * k), fill=(120, 120, 124), outline=INK, width=4 * k)
            d.line([(0, 380 * k), (W * k, 0)], fill=(140, 120, 90), width=10 * k)
        return ss(W, 1100, dr)
    im.alpha_composite(cached(("steps",), steps), (0, 560)); x = 160 + lt / max(D, 0.1) * 380; y = 1060 - (x) * 0.34
    put(im, bean(KEEPER, "dot", "line", "run1" if int(lt * 5) % 2 else "run2", "run1" if int(lt * 5) % 2 else "run2", cap=True, s=1.0), x, y)
    im.alpha_composite(tower(False, 0.55), (760, 260)); rain(im, lt); return im
def sh_door(p, lt, D):
    im = storm_sky().copy(); d = ImageDraw.Draw(im)
    def house():
        def dr(d, k):
            d.rectangle((90 * k, 300 * k, 990 * k, 1500 * k), fill=(214, 210, 200), outline=INK, width=10 * k); d.rectangle((540 * k, 300 * k, 990 * k, 1500 * k), fill=(188, 184, 176))
            d.rounded_rectangle((380 * k, 700 * k, 700 * k, 1500 * k), radius=30 * k, fill=(92, 62, 46), outline=INK, width=10 * k)
            d.ellipse((640 * k, 1080 * k, 670 * k, 1110 * k), fill=YEL); d.rectangle((0, 1500 * k, W * k, H * k), fill=(70, 96, 62))
            for x in range(0, W, 70): d.rectangle(((x + 10) * k, 1440 * k, (x + 30) * k, 1720 * k), fill=(60, 60, 66), outline=INK, width=4 * k)
            d.line([(0, 1500 * k), (W * k, 1500 * k)], fill=(60, 60, 66), width=16 * k); d.line([(0, 1600 * k), (W * k, 1600 * k)], fill=(60, 60, 66), width=16 * k)
        return ss(W, H, dr)
    im.alpha_composite(cached(("house",), house))
    if p.get("closed", True) and lt > 0.3: label(im, p.get("text", "ЗАКРЫТО"), 540, 560, YEL, LBL, bg=INK)
    put(im, bean(KEEPER, "wide", "line", "down", cap=True, s=1.0, look=1), 230, 1480); rain(im, lt); return im
def room_base(lamp=False):
    def mk():
        im = wall().copy(); floor(im, 1300)
        def dr(d, k):
            d.rounded_rectangle((300 * k, 280 * k, 780 * k, 760 * k), radius=20 * k, fill=(30, 44, 70), outline=INK, width=12 * k); d.line([(540 * k, 280 * k), (540 * k, 760 * k)], fill=INK, width=10 * k); d.line([(300 * k, 520 * k), (780 * k, 520 * k)], fill=INK, width=10 * k)
            d.rectangle((180 * k, 1160 * k, 900 * k, 1210 * k), fill=(120, 80, 52), outline=INK, width=8 * k)
            for x in (220, 840): d.rectangle((x * k, 1210 * k, (x + 30) * k, 1480 * k), fill=(100, 66, 44), outline=INK, width=6 * k)
            for x, fl in ((80, 1), (930, -1)): d.rectangle((x * k, 1000 * k, (x + 70) * k, 1450 * k), fill=(110, 74, 50), outline=INK, width=6 * k)
        im.alpha_composite(ss(W, H, dr)); return im
    return cached(("room",), mk)
def sh_room(p, lt, D):
    im = room_base().copy(); d = ImageDraw.Draw(im)
    if p.get("lamp"):
        d.rounded_rectangle((470, 1000, 610, 1160), 30, fill=(250, 220, 120), outline=INK, width=8); im.alpha_composite(blob(600, 600, (255, 220, 120), 90, 70), (240, 780))
        for i in range(4):
            ph = (lt * 2 + i * 0.25) % 1; sx, sy = 420 + i * 70, 980 - ph * 160; r = 18 * (1 - abs(ph - 0.5) * 2)
            d.polygon([(sx, sy - r * 2), (sx + r * 0.5, sy), (sx, sy + r * 2), (sx - r * 0.5, sy)], fill=(255, 255, 255)); d.polygon([(sx - r * 2, sy), (sx, sy + r * 0.5), (sx + r * 2, sy), (sx, sy - r * 0.5)], fill=(255, 255, 255))
    if p.get("who"): put(im, bean(KEEPER, "shock", "o", "up" if lt > 0.4 else "down", cap=True, sweat=lt > 0.4, s=1.1), 300 if p.get("lamp") else 540, 1500)
    if p.get("text") and lt > 0.25: label(im, p["text"], 540, 180, YEL, LBL, bg=INK)
    im.alpha_composite(vignette(150)); return im
def coat(col):
    def dr(d, k):
        d.polygon([(110 * k, 0), (190 * k, 0), (300 * k, 120 * k), (280 * k, 560 * k), (20 * k, 560 * k), (0, 120 * k)], fill=col, outline=INK, width=9 * k)
        d.line([(150 * k, 40 * k), (150 * k, 560 * k)], fill=INK, width=6 * k)
        for y in (180, 300, 420): d.ellipse((168 * k, y * k, 190 * k, (y + 22) * k), fill=INK)
        d.polygon([(110 * k, 0), (150 * k, 70 * k), (190 * k, 0)], fill=tuple(int(c * 0.7) for c in col), outline=INK, width=6 * k)
    return ss(300, 560, dr)
def sh_hooks(p, lt, D):
    im = wall((88, 70, 56)).copy(); d = ImageDraw.Draw(im); d.rectangle((0, 560, W, 620), fill=(110, 80, 56), outline=INK, width=8)
    coats = p.get("coats", [1, 1, 1]); gone = p.get("gone")
    for i, x in enumerate((220, 540, 860)):
        d.rounded_rectangle((x - 18, 560, x + 18, 650), 12, fill=(150, 150, 160), outline=INK, width=6)
        a = 1.0
        if gone and i in gone: a = 1 - ease((lt - 0.3) / 0.5)
        if coats[i] and a > 0:
            c = cached(("coat",), lambda: coat(OILSKIN)).copy()
            if a < 1: c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
            put(im, c, x, 1220)
        elif not coats[i]: label(im, "?", x, 900, (200, 200, 210), F("Inter-Black", 160))
    if p.get("spot") is not None:
        x = (220, 540, 860)[p["spot"]]; ov = Image.new("RGBA", (W, H), (0, 0, 0, 170)); ImageDraw.Draw(ov).ellipse((x - 260, 480, x + 260, 1340), fill=(0, 0, 0, 0))
        im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(40)))
    if p.get("text") and lt > 0.2: label(im, p["text"], 540, 1500, YEL, LBL, bg=INK)
    im.alpha_composite(vignette(140)); return im
def sh_trio(p, lt, D):
    im = grad((40, 50, 80), (16, 20, 34)); f = p.get("fade", False)
    for i, x in enumerate((230, 540, 850)):
        b = bean(KEEPER, "dot", "smile" if not f else "line", "down", cap=True, s=0.95).copy()
        a = 1 - ease((lt - 0.3 - i * 0.25) / 0.4) if f else eout((lt - i * 0.12) / 0.25)
        if a <= 0: label(im, "?", x, 1150, (150, 160, 190), F("Inter-Black", 200)); continue
        b.putalpha(b.getchannel("A").point(lambda v: int(v * a))); put(im, b, x, 1400 if f else 1400 + (1 - a) * 200)
    if p.get("text"): label(im, p["text"], 540, 420, YEL, LBL, bg=INK)
    return im
def sh_runner(p, lt, D):
    im = storm_sky().copy(); d = ImageDraw.Draw(im); d.rectangle((0, 1300, W, H), fill=(58, 86, 54))
    for i in range(6):
        y = 400 + i * 160; x = (W - (lt * 1400 + i * 300) % (W + 400)); d.line([(x, y), (x + 260, y)], fill=(200, 215, 235, 120), width=5)
    ph = int(lt * 8) % 2; x = 260 + min(lt, 2) * 200
    put(im, bean(SHIRT, "shock", "scream", "run1" if ph else "run2", "run1" if ph else "run2", sweat=True, s=1.25), x, 1480 + (12 if ph else 0))
    if p.get("text") and lt > 0.2: label(im, p["text"], 540, 380, YEL, LBL, bg=INK)
    rain(im, lt); return im
def landing_base():
    def mk():
        im = storm_sky().copy()
        def dr(d, k):
            d.polygon([(560 * k, 0), (W * k, 0), (W * k, H * k), (380 * k, H * k), (420 * k, 1500 * k), (500 * k, 1300 * k), (470 * k, 1100 * k), (600 * k, 900 * k), (560 * k, 650 * k)], fill=(50, 56, 64))
            d.line([(560 * k, 650 * k), (600 * k, 900 * k)], fill=(66, 100, 60), width=30 * k)
            d.rectangle((600 * k, 880 * k, W * k, 905 * k), fill=(120, 120, 124), outline=INK, width=5 * k)
            d.line([(760 * k, 880 * k), (760 * k, 640 * k), (560 * k, 600 * k)], fill=(70, 70, 76), width=22 * k); d.line([(560 * k, 600 * k), (560 * k, 760 * k)], fill=INK, width=6 * k)
            d.line([(300 * k, 900 * k), (300 * k, 1740 * k)], fill=WHITE, width=8 * k)
            for y in range(900, 1741, 120): d.line([(280 * k, y * k), (320 * k, y * k)], fill=WHITE, width=6 * k)
        im.alpha_composite(ss(W, H, dr)); label(im, "33 М", 180, 1300, YEL, LBL); return im
    return cached(("landing",), mk)
def sh_landing(p, lt, D):
    im = landing_base().copy(); wv = p.get("wave"); box_y = 820
    if wv is not None:
        g = ease((lt - wv) / 0.8); im.alpha_composite(sea_layer(0, lt, 2.0), (0, 1700))
        if g > 0:
            h = int(200 + 1100 * g); im.alpha_composite(big_wave(900, h, lt), (-120, 1800 - h + 60))
            box_y = 820 - 500 * ease((lt - wv - 0.5) / 0.6)
    else: im.alpha_composite(sea_layer(0, lt, 1.5), (0, 1700))
    bx = 680 - (0 if wv is None else 200 * ease((lt - wv - 0.5) / 0.6)); d = ImageDraw.Draw(im)
    if p.get("box", True): d.rectangle((bx, box_y, bx + 130, box_y + 70), fill=(150, 104, 60), outline=INK, width=7); d.text((bx + 65, box_y + 35), "ТРОСЫ", font=F("Inter-Black", 24), fill=WHITE, anchor="mm")
    if p.get("men"):
        for i, x in enumerate((760, 900)): put(im, bean(KEEPER, "shock" if wv is not None and lt > wv else "dot", "scream" if wv is not None and lt > wv else "line", "up" if wv is not None and lt > wv else "rope", cap=True, s=0.7), x, 886)
    if p.get("text") and lt > 0.2: label(im, p["text"], 540, 300, YEL, LBL, bg=INK)
    rain(im, lt); return im
def sh_railing(p, lt, D):
    im = storm_sky().copy(); d = ImageDraw.Draw(im); d.rectangle((0, 1250, W, H), fill=(58, 70, 64))
    bend = ease((lt - 0.2) / 0.5)
    for i, x in enumerate(range(80, 1040, 160)):
        bb = bend * (1 - abs(i - 3) / 3.5) * 220; d.line([(x, 1260), (x + bb * 0.6, 1000 + bb * 0.4)], fill=(80, 82, 92), width=26)
    pts = [(x, 1000 + (bend * (1 - abs((x - 560) / 480)) * 180 if abs(x - 560) < 480 else 0)) for x in range(40, 1081, 40)]; d.line(pts, fill=(96, 98, 108), width=30)
    for i in range(8): d.polygon([(100 + i * 120, 1400), (150 + i * 120, 1360 + (i % 3) * 20), (200 + i * 120, 1420)], fill=(76, 110, 60))
    if p.get("text") and lt > 0.2: label(im, p["text"], 540, 400, YEL, LBL, bg=INK)
    rain(im, lt); return im
def sh_window(p, lt, D):
    im = wall().copy(); d = ImageDraw.Draw(im)
    out = storm_sky().crop((200, 300, 880, 1100)).copy(); out.alpha_composite(sea_layer(0, lt, 2).crop((0, 0, 680, 400)), (0, 520))
    g = ease((lt - 0.3) / 0.8);
    if g > 0: h = int(700 * g); out.alpha_composite(big_wave(680, h, lt).resize((680, h)), (0, 800 - h))
    im.alpha_composite(out, (200, 300)); d.rectangle((200, 300, 880, 1100), outline=INK, width=24); d.line([(540, 300), (540, 1100)], fill=INK, width=18); d.line([(200, 700), (880, 700)], fill=INK, width=18)
    rain(out, lt); put(im, bean(SHIRT, "shock", "scream" if g > 0.4 else "o", "up" if g > 0.4 else "down", sweat=g > 0.4, s=1.0, flip=True), 540, 1560)
    im.alpha_composite(vignette(130)); return im
def sh_geo(p, lt, D):
    im = grad((28, 40, 64), (14, 20, 34)); d = ImageDraw.Draw(im)
    def rock():
        def dr(d, k):
            d.polygon([(0, 500 * k), (420 * k, 470 * k), (460 * k, 1500 * k), (0, 1500 * k)], fill=(60, 64, 72), outline=INK, width=10 * k)
            d.polygon([(560 * k, 470 * k), (W * k, 440 * k), (W * k, 1500 * k), (520 * k, 1500 * k)], fill=(60, 64, 72), outline=INK, width=10 * k)
            d.line([(0, 500 * k), (420 * k, 470 * k)], fill=(70, 110, 60), width=26 * k); d.line([(560 * k, 470 * k), (W * k, 440 * k)], fill=(70, 110, 60), width=26 * k)
        return ss(W, 1500, dr)
    im.alpha_composite(cached(("rock",), rock), (0, 300))
    lvl = 1650 - 1250 * ease((lt - 0.5) / 0.7); d.rectangle((462, lvl, 520, 1800), fill=(40, 120, 180))
    d.rectangle((0, 1600, W, H), fill=(30, 80, 130)); im.alpha_composite(sea_layer(0, lt, 1.6), (0, 1560))
    if lt > 1.1:
        for i in range(30):
            ph = ((lt - 1.1) * 1.5 + i / 30) % 1; x = 490 + math.sin(i * 7.3) * 220 * ph; y = 760 - ph * 520 + ph * ph * 300; r = 8 + (i % 4) * 5
            d.ellipse((x - r, y - r, x + r, y + r), fill=(230, 245, 255))
    for i in range(3):
        ax = 60 + ((lt * 300 + i * 120) % 360); d.polygon([(ax, 1700), (ax + 60, 1680), (ax + 60, 1720)], fill=YEL)
    label(im, p.get("text", "РАСЩЕЛИНА"), 540, 220, YEL, LBL, bg=INK); return im
def sh_search(p, lt, D):
    im = grad((40, 60, 90), (90, 110, 130)); im.alpha_composite(sea_layer(0, lt, 0.6, (34, 70, 104)), (0, 1000))
    for i, x0 in enumerate((100, 600)): im.alpha_composite(ship_sprite(0.35), (int(x0 + lt * 40 * (1 if i else -1)), int(930 + math.sin(lt * 2 + i) * 10)))
    if lt > 0.3: label(im, p.get("text", "НИКОГО"), 540, 640, WHITE, LBL, bg=(190, 50, 50))
    return im
def sh_legend(p, lt, D):
    im = grad((60, 44, 34), (30, 22, 18))
    def paper():
        def dr(d, k):
            d.rounded_rectangle((0, 0, 820 * k, 1000 * k), radius=30 * k, fill=(236, 220, 186), outline=INK, width=10 * k)
            for i, s in enumerate(p.get("lines", [])):
                d.text((60 * k, (120 + i * 140) * k), s, font=F("Inter-ExtraBold", 58 * k), fill=(70, 50, 40))
                d.line([(60 * k, (160 + i * 140) * k), (760 * k, (160 + i * 140) * k)], fill=(170, 150, 120), width=4 * k)
        return ss(820, 1000, dr)
    pp = cached(("paper", tuple(p.get("lines", []))), paper).rotate(-3, expand=True, resample=Image.BICUBIC); put(im, pp, 540, 1480)
    sa = (lt - p.get("stamp", 0.8))
    if sa > 0:
        s = 1 + 1.5 * (1 - eout(sa / 0.15)); st = Image.new("RGBA", (760, 220), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((10, 10, 750, 210), 20, outline=REDC, width=16); sd.text((380, 110), p.get("word", "ВЫДУМКА"), font=F("Inter-Black", 130), fill=REDC, anchor="mm")
        st = st.rotate(12, expand=True, resample=Image.BICUBIC); st = st.resize((int(st.width * s), int(st.height * s)))
        im.alpha_composite(st, (int(540 - st.width / 2), int(1000 - st.height / 2)))
    return im
if os.path.exists(f"{DIR}/shots.py"): exec(open(f"{DIR}/shots.py").read(), globals())
KINDS = {k[3:]: v for k, v in globals().items() if k.startswith("sh_")}

# ---------------- камера и кадр ----------------
def camera(im, s, cam, lt, D):
    u = ease(lt / max(D, 0.3)); z, dx, dy = 1.0, 0.0, 0.0; a = s.get("amt", 0.14)
    if cam == "in": z = 1.0 + a * u
    elif cam == "out": z = 1.0 + a * (1 - u)
    elif cam in ("l", "r"): z = 1.12; dx = (u - 0.5) * W * 0.09 * (1 if cam == "r" else -1)
    elif cam in ("up", "down"): z = 1.12; dy = (u - 0.5) * H * 0.07 * (1 if cam == "down" else -1)
    z += 0.07 * (1 - eout(lt / 0.18)) if s["i"] > 0 else 0
    fx, fy = s.get("focus", (0.5, 0.5)); cx = W * (0.5 + (fx - 0.5) * (1 - 1 / z)) + dx; cy = H * (0.5 + (fy - 0.5) * (1 - 1 / z)) + dy
    if s.get("shake") is not None and lt > s["shake"]: k = max(0, 1 - (lt - s["shake"]) / 0.8) * 18; cx += math.sin(lt * 70) * k; cy += math.cos(lt * 53) * k
    return im.transform((W, H), Image.AFFINE, (1 / z, 0, cx - W / (2 * z), 0, 1 / z, cy - H / (2 * z)), Image.BILINEAR)

def groups(words):
    out, cur = [], []
    for k, w in enumerate(words):
        if cur and w[0] - cur[-1][1] > 0.22: out.append(cur); cur = []
        cur.append(w)
        if len(cur) == 2 or sum(len(x[2]) for x in cur) > 11 or re.search(r"[.,!?:;»—]$", w[2]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CAPC = {}
def caption(g):
    if id(g) in CAPC: return CAPC[id(g)]
    toks = [re.sub(r"[^\wёЁ\-]", "", w[2]) for w in g]; im = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lines = [toks] if d.textlength(" ".join(toks).upper(), font=CAP) < W - 80 else [[x] for x in toks]
    for li, ln in enumerate(lines):
        tw = sum(d.textlength(x.upper(), font=CAP) for x in ln) + 28 * (len(ln) - 1); x = (W - tw) / 2; y = 40 + li * 118
        for wd in ln:
            lw = wd.lower(); col = REDC if lw in RED else YEL if lw in YELLOW else WHITE
            d.text((x, y), wd.upper(), font=CAP, fill=col, stroke_width=13, stroke_fill=INK); x += d.textlength(wd.upper(), font=CAP) + 28
    CAPC[id(g)] = im; return im
SUBF = F("Inter-Bold", 50); NAMEF = F("Inter-Black", 34)
WHO = getattr(ST, "WHO", {})
def punct(r):
    toks = [x for x in SC_TEXT.get(r["n"], "").split() if re.search(r"[\wё]", x, re.I)]; cl = lambda z: re.sub(r"[^\wё]", "", z.lower()); out, j = [], 0
    for w in r["words"]:
        k = j
        while k < len(toks) and not cl(toks[k]).startswith(cl(w[2])[:3]): k += 1
        if k < len(toks): out.append((w[0], w[1], toks[k])); j = k + 1
        else: out.append(w)
    return out
SC_TEXT = {sc[0]: sc[1] for sc in SCENES}
def phrase_caps():
    caps = []
    for r in rows:
        ch, cur = [], []
        for w in punct(r):
            cur.append(w)
            if re.search(r"[.!?…]$", w[2]) or len(" ".join(x[2] for x in cur)) > 60: ch.append(cur); cur = []
        if cur: ch.append(cur)
        for i, g in enumerate(ch): caps.append((g[0][0], ch[i + 1][0][0] if i + 1 < len(ch) else g[-1][1] + 0.6, g, r.get("who")))
    return caps
def phrase_img(g, who):
    key = ("ph", id(g))
    if key in CAPC: return CAPC[key]
    txt = " ".join(w[2] for w in g); d = ImageDraw.Draw(Image.new("RGB", (1, 1))); lines, cur = [], ""
    for wd in txt.split():
        if cur and d.textlength(cur + " " + wd, font=SUBF) > W - 520: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur); lh = 66; bw = max(d.textlength(l, font=SUBF) for l in lines) + 70; bh = lh * len(lines) + 34
    im = Image.new("RGBA", (W, bh + 60), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); x0 = (W - bw) / 2
    dd.rounded_rectangle((x0, 50, x0 + bw, 50 + bh), 18, fill=(0, 0, 0, 170))
    for i, l in enumerate(lines): dd.text((W / 2, 50 + 17 + lh * i + lh / 2), l, font=SUBF, fill=(255, 255, 255), anchor="mm")
    if who and who in WHO:
        nm, col = WHO[who]; tw = dd.textlength(nm, font=NAMEF); dd.rounded_rectangle((x0, 4, x0 + tw + 36, 52), 12, fill=col + (255,)); dd.text((x0 + 18, 28), nm, font=NAMEF, fill=(255, 255, 255), anchor="lm")
    CAPC[key] = im; return im
def captions():
    if STY.get("subs") == "phrase": return phrase_caps()
    caps = []
    for r in rows:
        gs = groups(r["words"])
        for gi, g in enumerate(gs): caps.append((g[0][0], gs[gi + 1][0][0] if gi + 1 < len(gs) else g[-1][1] + 0.25, g))
    return caps
CAPY = STY.get("capy", 1540)
def frame(t, caps):
    s = next(x for x in SHOTS if x["t0"] <= t < x["t1"]) if t < TOTAL - 1e-6 else SHOTS[-1]
    lt, D = t - s["t0"], s["t1"] - s["t0"]
    im = camera(KINDS[s["k"]](s, lt, D), s, s.get("cam", "in"), lt, D)
    for c in caps:
        c0, c1, g = c[0], c[1], c[2]
        if len(c) > 3 and c0 <= t < c1:
            pi = phrase_img(g, c[3]); a = min(1.0, (t - c0) / 0.12)
            if a < 1: pi = pi.copy(); pi.putalpha(pi.getchannel("A").point(lambda v: int(v * a)))
            im.alpha_composite(pi, (0, H - pi.height - 40)); break
        if c0 <= t < c1:
            cap = caption(g); pop = eout((t - c0) / 0.1)
            if pop < 1: sc = 0.8 + 0.2 * pop; cw, ch = int(W * sc), int(300 * sc); cap = cap.resize((cw, ch), Image.BILINEAR); im.alpha_composite(cap, ((W - cw) // 2, CAPY + (300 - ch) // 2))
            else: im.alpha_composite(cap, (0, CAPY))
            break
    if t > TOTAL - 0.6: im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (t - TOTAL + 0.6) / 0.6))))
    return im

# ---------------- звук ----------------
def build_audio(path):
    N = int(TOTAL * SR); voice = np.zeros(N, np.float32); fx = np.zeros(N, np.float32); x = np.arange(N) / SR
    for r in rows: i = int(r["t0"] * SR); voice[i:i + len(r["a"])] += r["a"][:N - i]
    voice *= 0.95 / (np.abs(voice).max() + 1e-6)
    def add(sig, at, v=1.0):
        i = int(at * SR); j = min(N, i + len(sig))
        if 0 <= i < N: fx[i:j] += sig[:j - i] * v
    def noise(d, sm=8): n = rng.standard_normal(int(d * SR)).astype(np.float32); return np.convolve(n, np.ones(sm) / sm, "same") if sm > 1 else n
    def whoosh(at): n = noise(0.3, 6); tt = np.arange(len(n)) / SR; add(n * np.sin(np.pi * tt / 0.3) ** 2, at - 0.12, 0.18)
    def wave_s(at): n = noise(2.2, 40); tt = np.arange(len(n)) / SR; add(n * np.clip(tt / 0.6, 0, 1) * np.exp(-np.clip(tt - 0.6, 0, None) * 2.2) * 3, at, 0.9)
    def thud(at, v=0.7): tt = np.arange(int(0.6 * SR)) / SR; add((np.sin(2 * np.pi * (50 + 60 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 7)).astype(np.float32), at, v)
    def ding(at): tt = np.arange(int(0.8 * SR)) / SR; add((np.sin(2 * np.pi * 1568 * tt) + 0.6 * np.sin(2 * np.pi * 2349 * tt)).astype(np.float32) * np.exp(-tt * 5), at, 0.12)
    def horn(at): tt = np.arange(int(1.4 * SR)) / SR; add(((np.sign(np.sin(2 * np.pi * 98 * tt)) * 0.3 + np.sin(2 * np.pi * 196 * tt)) * np.clip(tt / 0.1, 0, 1) * np.clip((1.4 - tt) / 0.3, 0, 1)).astype(np.float32), at, 0.18)
    def flip(at, k=8):
        for i in range(k): add(noise(0.05, 3) * np.hanning(int(0.05 * SR)).astype(np.float32), at + i * 0.09, 0.3)
    def pop(at): tt = np.arange(int(0.12 * SR)) / SR; add((np.sin(2 * np.pi * (300 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30)).astype(np.float32), at, 0.35)
    def thunder(at): n = noise(2.5, 80); tt = np.arange(len(n)) / SR; add(n * np.exp(-tt * 1.5) * 6, at, 0.7)
    def steps(t0, t1):
        a = t0
        while a < t1: add(noise(0.06, 20) * np.hanning(int(0.06 * SR)).astype(np.float32) * 3, a, 0.4); a += 0.28
    def knock(at):
        for o in (0, 0.28, 0.56):
            tt = np.arange(int(0.25 * SR)) / SR; sg = np.sin(2 * np.pi * 95 * tt * (1 - tt)) * np.exp(-tt * 22)
            add((sg + noise(0.25, 24) * np.exp(-tt * 60) * 1.5).astype(np.float32), at + o, 0.8)
    def creak(at): tt = np.arange(int(1.2 * SR)) / SR; f = 180 + 60 * np.sin(tt * 5); add((np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * tt / 1.2) * (0.5 + 0.5 * np.sin(tt * 90))).astype(np.float32), at, 0.06)
    def ring(at):
        tt = np.arange(int(2.0 * SR)) / SR; add(((np.sin(2 * np.pi * 880 * tt) + np.sin(2 * np.pi * 1100 * tt)) * (tt % 1.0 < 0.7) * (np.sin(2 * np.pi * 20 * tt) > 0)).astype(np.float32), at, 0.06)
    def engine(at): n = noise(3.0, 60); tt = np.arange(len(n)) / SR; add((n * 4 + np.sin(2 * np.pi * 45 * tt) * 0.5).astype(np.float32) * np.clip(tt / 0.5, 0, 1) * np.clip((3 - tt) / 1, 0, 1), at, 0.25)
    def sting(at):
        tt = np.arange(int(2.5 * SR)) / SR; add(((np.sin(2 * np.pi * 40 * tt) * 1.2 + noise(2.5, 4) * 0.3 + np.sin(2 * np.pi * 311 * tt) * 0.3 + np.sin(2 * np.pi * 330 * tt) * 0.3) * np.exp(-tt * 1.4)).astype(np.float32), at, 0.45)
    def tick(t0, t1):
        a = t0
        while a < t1: add(noise(0.02, 2) * 2, a, 0.15); a += 0.5
    def heart(t0, t1):
        tt = np.arange(int(0.18 * SR)) / SR; th = (np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 25)).astype(np.float32); a = t0
        while a < t1: add(th, a, 0.6); add(th, a + 0.22, 0.45); a += 0.75
    def birds(at):
        for k in range(5):
            tt = np.arange(int(0.12 * SR)) / SR; add((np.sin(2 * np.pi * (2600 + 900 * np.sin(tt * 60)) * tt) * np.hanning(len(tt))).astype(np.float32), at + k * 0.35 + rng.random() * 0.1, 0.05)
    SFX = {"knock": knock, "creak": creak, "ring": ring, "engine": engine, "sting": sting, "birds": birds, "wave": wave_s, "thud": thud, "ding": ding, "horn": horn, "flip": flip, "pop": pop, "thunder": thunder}
    for s in SHOTS:
        if s["i"] > 0: whoosh(s["t0"])
        for name in (s.get("sfx") or "").split():
            nm, _, off = name.partition("@"); at = s["t0"] + float(off or 0)
            if nm == "steps": steps(s["t0"], s["t1"])
            elif nm == "tick": tick(s["t0"], s["t1"])
            elif nm == "heart": heart(s["t0"], s["t1"])
            else: SFX[nm](at)
    wind = noise(TOTAL + 0.1, 90)[:N] * 9 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.09 * x)); rainn = noise(TOTAL + 0.1, 2)[:N] * 0.05
    pulse = np.zeros(N, np.float32); tt = np.arange(int(0.25 * SR)) / SR; note = np.exp(-tt * 9)
    seq = [55, 55, 65.4, 55, 49, 55, 73.4, 65.4]; b, i = 0.0, 0
    while b < TOTAL:
        f = seq[i % 8]; s = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2 * tt)) * note
        j = int(b * SR); k = min(N, j + len(s)); pulse[j:k] += s[:k - j].astype(np.float32); b += 0.25; i += 1
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, "same"); duck = 1 - 0.5 * np.clip(env / 0.08, 0, 1)
    if STY.get("mood") == "horror":
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * x); pulse = (np.sin(2 * np.pi * 55 * x) + np.sin(2 * np.pi * 55.35 * x) + 0.5 * np.sin(2 * np.pi * 82.6 * x) + 0.25 * np.sin(2 * np.pi * 116.6 * x + np.sin(x * 0.7))) * lfo * 0.7; rainn = rainn * 0
    bed = (wind * 0.03 + rainn + pulse * 0.07) * duck * np.clip(x / 0.5, 0, 1) * np.clip((TOTAL - x) / 1.0, 0, 1)
    mix = np.tanh((voice + bed + fx) * 1.05) * 0.95
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

if MODE == "thumb":
    im = THUMB().convert("RGB"); im.save(f"{DIR}/thumb_full.png"); im.resize((1280, 720) if W > H else (720, 1280), Image.LANCZOS).save(f"{DIR}/thumb.jpg", quality=92)
    print("thumb", f"{DIR}/thumb.jpg"); sys.exit()
if MODE == "stills":
    os.makedirs(f"{DIR}/stills", exist_ok=True); caps = captions(); ims = []
    for s in SHOTS: ims.append(frame(s["t0"] + (s["t1"] - s["t0"]) * 0.7, caps).convert("RGB").resize((tw := 270 if H > W else 384, th := 480 if H > W else 216)))
    cols = 8 if H > W else 6; sheet = Image.new("RGB", (tw * cols, th * math.ceil(len(ims) / cols)))
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(f"{DIR}/stills/sheet.jpg"); print("stills", f"{DIR}/stills/sheet.jpg", round(TOTAL, 1), "s,", len(SHOTS), "планов,", round(len(SHOTS) / TOTAL * 10, 1), "склеек/10с")
elif MODE == "build":
    out = f"{DIR}/{NAME}.mp4"; build_audio(f"{DIR}/mix.wav"); caps = captions()
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", f"{DIR}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "3500k", "-bufsize", "7000k", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fi in range(int(TOTAL * FPS)): ff.stdin.write(frame(fi / FPS, caps).convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print("done", out, round(TOTAL, 1), "s")
