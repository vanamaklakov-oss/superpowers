"""Ball-head Short builder: everything drawn in code. Shots from script.py, characters from ../ballhead/rig.py.
Fast cuts (each sentence split into its shots), camera push-in per shot, idle bob + blinks, lip-sync from the voice
envelope, thought bubbles with a lamp (consciousness on/off) or '?', signs, small gags; one-word captions; no music."""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{HERE}/../ballhead")
from rig import draw, Character
from script import SCENES

W, H, FPS, SR, GAP = 1080, 1920, 30, 48000, 0.08
FONT = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 96)
SIGN = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 120)
GROUND = 1560
rng = np.random.default_rng(11)

CAST = {
    "jerry": Character(hat="none", coat=(150, 110, 70), trim=(230, 210, 160), tie=(70, 90, 130), glasses=True, hair=None, mustache=True),
    "friend": Character(hat="cap", hat_color=(170, 40, 40), coat=(60, 120, 170), trim=(240, 240, 240), tie=(240, 200, 60)),
    "friend2": Character(hat="bowler", hat_color=(60, 50, 40), coat=(110, 140, 80), trim=(240, 220, 140), tie=(150, 40, 40), hair=None),
    "official": Character(hat="none", coat=(40, 45, 60), trim=(220, 220, 230), tie=(160, 30, 40), hair=(60, 50, 40)),
    "clerk": Character(hat="peaked", hat_color=(30, 90, 60), coat=(30, 90, 60), trim=(240, 200, 60), tie=(230, 230, 230)),
    "colonial": Character(hat="bowler", hat_color=(235, 230, 215), coat=(235, 230, 215), trim=(200, 170, 80), tie=(40, 60, 120), hair=None, mustache=True),
    "villager": Character(hat="none", coat=(120, 100, 70), trim=(200, 180, 140), tie=(120, 100, 70), hair=(30, 25, 20)),
    "villager2": Character(hat="none", coat=(70, 110, 90), trim=(200, 200, 170), tie=(70, 110, 90), hair=(30, 25, 20)),
    "traveler": Character(hat="cap", hat_color=(40, 90, 160), coat=(230, 230, 235), trim=(40, 90, 160), tie=(200, 40, 40)),
    "banker": Character(hat="none", coat=(50, 55, 70), trim=(200, 200, 210), tie=(40, 120, 70), glasses=True, hair=(90, 80, 70)),
    "king": Character(hat="tophat", hat_color=(110, 20, 30), coat=(110, 20, 30), trim=(240, 200, 60), tie=(240, 240, 240), hair=(80, 50, 30)),
    "taxman": Character(hat="tricorn", hat_color=(30, 30, 35), coat=(60, 50, 80), trim=(220, 190, 90), tie=(240, 240, 240), hair=(200, 200, 200)),
    "count": Character(hat="tophat", hat_color=(20, 20, 24), coat=(30, 30, 40), trim=(220, 220, 230), tie=(150, 20, 30), hair=None, mustache=True),
    "dealer": Character(hat="bowler", hat_color=(80, 60, 40), coat=(150, 120, 80), trim=(90, 70, 40), tie=(60, 90, 60), hair=None),
    "major": Character(hat="peaked", hat_color=(110, 100, 60), coat=(120, 110, 70), trim=(220, 190, 80), tie=(110, 100, 60), mustache=True),
    "soldier": Character(hat="cap", hat_color=(110, 100, 60), coat=(120, 110, 70), trim=(150, 130, 80), tie=(110, 100, 60)),
    "farmer": Character(hat="bowler", hat_color=(150, 110, 60), coat=(90, 120, 160), trim=(230, 230, 230), tie=(170, 50, 40), hair=None),
    "peter": Character(hat="tricorn", hat_color=(25, 25, 30), coat=(30, 90, 60), trim=(230, 190, 80), tie=(200, 40, 40), hair=(60, 40, 25), mustache=True),
    "boyar": Character(hat="bowler", hat_color=(120, 40, 40), coat=(130, 40, 40), trim=(230, 190, 80), tie=(130, 40, 40), hair=None, beard=(110, 70, 40), mustache=True),
    "boyar2": Character(hat="bowler", hat_color=(60, 60, 110), coat=(70, 70, 130), trim=(230, 200, 120), tie=(70, 70, 130), hair=None, beard=(170, 170, 170), mustache=True),
    "tsar": Character(hat="peaked", hat_color=(240, 240, 240), coat=(30, 60, 120), trim=(240, 200, 60), tie=(240, 240, 240), hair=(120, 90, 60), mustache=True),
    "seward": Character(hat="tophat", hat_color=(20, 20, 24), coat=(40, 40, 50), trim=(220, 220, 230), tie=(30, 30, 30), hair=(200, 200, 200)),
    "miner": Character(hat="cap", hat_color=(120, 80, 40), coat=(150, 60, 50), trim=(230, 200, 140), tie=(150, 60, 50), beard=(120, 80, 50)),
    "ohio": Character(hat="tophat", hat_color=(30, 30, 35), coat=(150, 40, 40), trim=(240, 240, 240), tie=(240, 240, 240), hair=(80, 60, 40)),
    "mich": Character(hat="tophat", hat_color=(30, 30, 35), coat=(40, 70, 150), trim=(240, 220, 120), tie=(240, 240, 240), hair=(160, 120, 70)),
    "driver": Character(hat="none", coat=(220, 180, 60), trim=(60, 60, 60), tie=(40, 90, 160), hair=(230, 210, 150)),
    "driver2": Character(hat="cap", hat_color=(40, 90, 160), coat=(40, 90, 160), trim=(240, 220, 60), tie=(240, 220, 60), hair=(200, 180, 120)),
    "dexter": Character(hat="tophat", hat_color=(40, 25, 20), coat=(120, 60, 120), trim=(240, 200, 60), tie=(240, 240, 240), hair=(200, 200, 200)),
    "scholar": Character(hat="none", coat=(90, 70, 50), trim=(220, 200, 160), tie=(150, 40, 40), glasses=True, hair=(130, 130, 130), beard=(160, 160, 160)),
    "voynich": Character(hat="bowler", hat_color=(40, 40, 45), coat=(60, 60, 70), trim=(210, 210, 220), tie=(120, 30, 40), hair=None, mustache=True),
    "captain": Character(hat="peaked", hat_color=(25, 30, 60), coat=(30, 40, 80), trim=(230, 190, 80), tie=(240, 240, 240), beard=(90, 60, 40)),
    "sailor": Character(hat="cap", hat_color=(240, 240, 240), coat=(40, 70, 140), trim=(240, 240, 240), tie=(200, 40, 40), stripes=True),
    "governor": Character(hat="bowler", hat_color=(30, 30, 30), coat=(110, 30, 40), trim=(240, 220, 150), tie=(240, 240, 240), hair=(120, 90, 60), beard=(120, 90, 60)),
    "prince": Character(hat="none", coat=(40, 60, 140), trim=(240, 200, 60), tie=(240, 240, 240), hair=(220, 180, 100)),
    "prince2": Character(hat="none", coat=(120, 40, 120), trim=(240, 200, 60), tie=(240, 240, 240), hair=(200, 150, 80)),
    "uncle": Character(hat="tophat", hat_color=(30, 30, 35), coat=(60, 20, 30), trim=(240, 200, 60), tie=(30, 30, 35), hair=(50, 40, 30)),
    "diver": Character(hat="none", coat=(60, 120, 150), trim=(230, 230, 230), tie=(60, 120, 150), hair=(30, 25, 20), mustache=True),
    "sailor2": Character(hat="cap", hat_color=(30, 30, 40), coat=(150, 60, 50), trim=(240, 240, 240), tie=(30, 30, 40), beard=(60, 45, 30)),
    "cambyses": Character(hat="tophat", hat_color=(150, 110, 30), coat=(120, 30, 90), trim=(240, 200, 60), tie=(240, 200, 60), hair=(30, 20, 15), beard=(30, 20, 15)),
    "persian": Character(hat="cap", hat_color=(170, 120, 60), coat=(160, 60, 40), trim=(230, 200, 120), tie=(160, 60, 40), beard=(40, 30, 20)),
    "islander": Character(hat="none", coat=(180, 140, 90), trim=(240, 220, 170), tie=(180, 140, 90), hair=(20, 15, 10)),
    "missionary": Character(hat="none", coat=(25, 25, 30), trim=(240, 240, 240), tie=(240, 240, 240), hair=(120, 90, 60), beard=(120, 90, 60)),
    "franklin": Character(hat="peaked", hat_color=(20, 25, 50), coat=(25, 35, 75), trim=(230, 190, 80), tie=(240, 240, 240), hair=(200, 200, 200)),
    "inuk": Character(hat="none", coat=(150, 110, 70), trim=(235, 225, 205), tie=(150, 110, 70), hair=(20, 15, 10)),
    "dancer": Character(hat="none", coat=(200, 80, 70), trim=(240, 220, 170), tie=(200, 80, 70), hair=(150, 90, 40)),
    "dancer2": Character(hat="cap", hat_color=(70, 110, 60), coat=(80, 120, 160), trim=(240, 220, 170), tie=(80, 120, 160)),
    "mayor": Character(hat="bowler", hat_color=(40, 30, 30), coat=(90, 40, 40), trim=(230, 200, 100), tie=(240, 240, 240), hair=None, beard=(110, 90, 70)),
    "fred": Character(hat="tricorn", hat_color=(25, 25, 30), coat=(30, 50, 110), trim=(240, 200, 60), tie=(240, 240, 240), hair=(230, 230, 230)),
    "detective": Character(hat="bowler", hat_color=(70, 65, 60), coat=(150, 130, 100), trim=(90, 80, 60), tie=(120, 40, 40), hair=None),
    "keeper": Character(hat="peaked", hat_color=(25, 30, 50), coat=(30, 40, 70), trim=(230, 200, 90), tie=(30, 40, 70), beard=(110, 80, 50)),
    "keeper2": Character(hat="cap", hat_color=(60, 60, 70), coat=(70, 80, 90), trim=(220, 220, 220), tie=(70, 80, 90), mustache=True),
    "keeper3": Character(hat="none", coat=(90, 60, 50), trim=(220, 200, 160), tie=(90, 60, 50), hair=(200, 120, 60), beard=(200, 120, 60)),
    "digger": Character(hat="bowler", hat_color=(210, 190, 150), coat=(200, 180, 140), trim=(120, 100, 70), tie=(60, 90, 60), hair=None, glasses=True),
    "greenboy": Character(hat="none", coat=(90, 140, 70), trim=(200, 230, 170), tie=(90, 140, 70), hair=(60, 80, 40), skin=(150, 200, 120)),
    "greengirl": Character(hat="none", coat=(60, 120, 90), trim=(200, 230, 170), tie=(60, 120, 90), hair=(140, 100, 50), skin=(150, 200, 120)),
    "agnes": Character(hat="none", coat=(60, 120, 90), trim=(200, 230, 170), tie=(60, 120, 90), hair=(140, 100, 50)),
    "peasant": Character(hat="cap", hat_color=(120, 100, 60), coat=(130, 100, 70), trim=(200, 180, 140), tie=(130, 100, 70), beard=(110, 80, 50)),
    "rich": Character(hat="tophat", hat_color=(30, 30, 35), coat=(40, 70, 50), trim=(230, 200, 90), tie=(240, 240, 240), hair=(140, 110, 80)),
    "doctor": Character(hat="none", coat=(25, 25, 30), trim=(240, 240, 240), tie=(25, 25, 30), glasses=True, hair=(170, 170, 170)),
    "dealer2": Character(hat="bowler", hat_color=(30, 30, 30), coat=(90, 90, 100), trim=(200, 200, 200), tie=(150, 40, 40), hair=None, mustache=True),
    "soldier2": Character(hat="cap", hat_color=(110, 100, 60), coat=(120, 110, 70), trim=(150, 130, 80), tie=(110, 100, 60), hair=(150, 90, 40)),
}

# ---------------- audio ----------------
def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 600, 0), min(on[-1] + 1800, len(a)); return a[s:e], s / SR

rows, t = [], 0.15
for n, text, shots in SCENES:
    a, lead = trim(pcm(f"{HERE}/vo/{n:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{n:02d}.mp3.json"))
    words = [(t + w["s"] - lead, t + w["s"] - lead + w["d"], w["w"]) for w in meta["words"]]
    rows.append(dict(t0=t, a=a, words=words, shots=shots)); t += len(a) / SR + GAP
TOTAL = t + 0.6
for i, r in enumerate(rows): r["t1"] = rows[i + 1]["t0"] if i + 1 < len(rows) else TOTAL
# split each sentence into its shots, cutting on word boundaries
SHOTS = []
for r in rows:
    k = len(r["shots"]); starts = [r["t0"]]
    for j in range(1, k):
        target = r["t0"] + (r["t1"] - r["t0"]) * j / k
        starts.append(min((w[0] for w in r["words"]), key=lambda s: abs(s - target)))
    for j, sh in enumerate(r["shots"]):
        SHOTS.append(dict(sh, a=starts[j], b=starts[j + 1] if j + 1 < k else r["t1"]))
VOICE = np.zeros(int(TOTAL * SR), np.float32)
for r in rows: s = int(r["t0"] * SR); VOICE[s:s + len(r["a"])] += r["a"][: len(VOICE) - s]
ENV = np.convolve(np.abs(VOICE), np.ones(SR // 25) / (SR // 25), "same"); ENV /= ENV.max()

def boom(L_s=1.8, f0=85, f1=32, gain=0.9):
    """Cinematic impact: falling sub-bass + noise transient + a dark 'braam' layer."""
    L = int(L_s * SR); tt = np.arange(L) / SR
    sub = np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-tt / 0.25)) / SR) * np.exp(-tt / 0.55)
    hit = np.convolve(rng.standard_normal(L), np.ones(6) / 6, "same") * np.exp(-tt / 0.045)
    braam = sum(np.sign(np.sin(2 * np.pi * 55 * h * tt)) / h for h in (1, 1.5, 2)) * np.exp(-tt / 0.7) * np.minimum(1, tt / 0.02)
    braam = np.convolve(braam, np.ones(40) / 40, "same")
    return (sub * 0.9 + hit * 0.5 + braam * 0.22) * gain

def mix():
    n = len(VOICE); out = VOICE * 1.25
    hooks = [sh for sh in SHOTS if sh.get("hook")]
    if hooks:                                                # opening impact under the hook line, and a smaller one into the story
        b = boom(); out[: min(n, len(b))] += b[: n]
        e = int(hooks[-1]["b"] * SR) - int(0.05 * SR); b2 = boom(1.0, 70, 40, 0.45)
        if 0 < e < n - len(b2): out[e:e + len(b2)] += b2
    for sh in SHOTS[1:]:                                    # tiny whoosh on each cut
        s = int((sh["a"] - 0.12) * SR); L = int(0.18 * SR)
        if 0 < s < n - L: out[s:s + L] += np.convolve(rng.standard_normal(L), np.ones(10) / 10, "same") * np.hanning(L) * 0.05
    out = np.tanh(out * 1.05) * 0.97; p = f"{HERE}/out/mix.wav"        # soft limiter: the boom hits hard without ducking the voice
    with wave.open(p, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
    return p

# ---------------- backgrounds (drawn once) ----------------
def grad(top, bot, split=None, gtop=None, gbot=None):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im); split = split or H
    for y in range(H):
        if y < split: k = y / split; c = tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3))
        else: k = (y - split) / (H - split); c = tuple(int(gtop[i] + (gbot[i] - gtop[i]) * k) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return im, d
def bg_street():
    im, d = grad((110, 170, 235), (250, 210, 160), GROUND - 40, (170, 160, 150), (120, 110, 105))
    r = np.random.default_rng(3); x = -40
    while x < W + 40:
        w = r.integers(150, 260); h = r.integers(420, 900); col = tuple(int(v) for v in r.integers(150, 230, 3))
        d.rectangle([x, GROUND - 40 - h, x + w, GROUND - 40], fill=col, outline=(70, 60, 60), width=4)
        for yy in range(GROUND - 40 - h + 50, GROUND - 120, 110):
            for xx in range(x + 25, x + w - 50, 70): d.rectangle([xx, yy, xx + 40, yy + 60], fill=(250, 235, 170) if r.random() < 0.4 else (90, 110, 140))
        x += w + 10
    d.rectangle([0, GROUND - 40, W, GROUND - 20], fill=(200, 195, 185)); return im
def bg_dark():
    im, d = grad((20, 18, 40), (50, 30, 70)); r = np.random.default_rng(5)
    for _ in range(160): x, y = r.integers(0, W), r.integers(0, H); d.ellipse([x, y, x + 3, y + 3], fill=(200, 190, 255))
    glow = Image.new("RGB", (W, H)); ImageDraw.Draw(glow).ellipse([140, 500, 940, 1500], fill=(110, 80, 170))
    return Image.blend(im, Image.blend(im, glow.filter(ImageFilter.GaussianBlur(160)), 1), 0.35)
def bg_lab():
    im, d = grad((215, 225, 230), (190, 205, 215), GROUND - 60, (120, 125, 135), (90, 95, 105))
    d.rectangle([140, 260, 940, 760], fill=(40, 70, 60), outline=(120, 90, 60), width=18)
    for k, s in enumerate(["E = mc²", "?  ≠  ?", "мозг = ?"]): d.text((200, 320 + k * 140), s, font=ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 90), fill=(230, 235, 225))
    return im
def bg_library():
    im, d = grad((120, 80, 55), (90, 60, 40), GROUND - 50, (100, 70, 50), (70, 50, 35)); r = np.random.default_rng(8)
    for sy in range(180, GROUND - 200, 230):
        d.rectangle([0, sy + 190, W, sy + 210], fill=(70, 45, 30)); x = 10
        while x < W:
            w = int(r.integers(26, 52)); h = int(r.integers(130, 185)); c = tuple(int(v) for v in r.integers(60, 200, 3))
            d.rectangle([x, sy + 190 - h, x + w, sy + 190], fill=c, outline=(40, 25, 20), width=3); x += w + 3
    return Image.blend(im, Image.new("RGB", (W, H), (60, 40, 25)), 0.25)
def bg_cinema():
    im, d = grad((30, 10, 15), (80, 20, 30)); d.rectangle([90, 200, 990, 760], fill=(230, 230, 235), outline=(20, 20, 20), width=12)
    for k in range(7): d.rectangle([60 + k * 140, 1500, 160 + k * 140, 1600], fill=(120, 20, 30))
    return im
import glob
BGS = {os.path.basename(p)[:-4]: Image.open(p).convert("RGB").resize((W, H)) for p in glob.glob(f"{HERE}/bgs/*.jpg")}
BGS.setdefault("dark", bg_dark())

# ---------------- overlays ----------------
def bubble(im, hx, hy, kind, t):
    d = ImageDraw.Draw(im); bx, by, R = hx + 150, hy - 320, 120
    for k, rr in enumerate((18, 30)): d.ellipse([hx + 40 + k * 45 - rr, hy - 120 - k * 80 - rr, hx + 40 + k * 45 + rr, hy - 120 - k * 80 + rr], fill=(255, 255, 255), outline=(30, 30, 30), width=5)
    d.ellipse([bx - R * 1.2, by - R, bx + R * 1.2, by + R], fill=(255, 255, 255), outline=(30, 30, 30), width=6)
    if kind == "?":
        d.text((bx, by), "?", font=SIGN, anchor="mm", fill=(40, 40, 40)); return
    on = kind == "on"
    if on:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([bx - 110, by - 110, bx + 110, by + 110], fill=(255, 220, 90, int(150 + 60 * math.sin(t * 8))))
        im.paste(g.filter(ImageFilter.GaussianBlur(30)), (0, 0), g.filter(ImageFilter.GaussianBlur(30)))
        d = ImageDraw.Draw(im)
    d.ellipse([bx - 55, by - 70, bx + 55, by + 40], fill=(255, 225, 90) if on else (90, 90, 100), outline=(30, 30, 30), width=6)
    d.rectangle([bx - 28, by + 38, bx + 28, by + 75], fill=(150, 150, 160), outline=(30, 30, 30), width=5)
    if on:
        for k in range(8): a = k * math.pi / 4; d.line([(bx + math.cos(a) * 80, by - 15 + math.sin(a) * 80), (bx + math.cos(a) * 105, by - 15 + math.sin(a) * 105)], fill=(240, 170, 30), width=8)

def hook_title(im, text, t):
    """Huge two-line hook title that punches in, with the background dimmed."""
    dim = Image.new("RGB", (W, H), (10, 5, 5)); im.paste(Image.blend(im, dim, 0.45))
    k = 1.0 + 0.6 * max(0.0, 1 - t / 0.14); d = ImageDraw.Draw(im)
    lines = text.split("\n"); size = int(150 * k)
    f = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", size)
    widest = max(f.getlength(l) for l in lines)
    if widest > W - 80: f = f.font_variant(size=int(size * (W - 80) / widest))
    y = 430 - (len(lines) - 1) * f.size * 0.55
    for i, l in enumerate(lines):
        d.text((W // 2, y + i * f.size * 1.1), l, font=f, anchor="mm", fill=(255, 60, 50) if i == len(lines) - 1 else (255, 255, 255), stroke_width=10, stroke_fill=(0, 0, 0))

def sign(im, text, t):
    d = ImageDraw.Draw(im); pop = min(1, t / 0.15); f = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", int(120 * (0.6 + 0.4 * pop)))
    box = d.multiline_textbbox((W // 2, 330), text, font=f, anchor="mm", align="center")
    d.rounded_rectangle([box[0] - 40, box[1] - 30, box[2] + 40, box[3] + 30], radius=24, fill=(250, 235, 190), outline=(60, 40, 20), width=8)
    d.multiline_text((W // 2, 330), text, font=f, anchor="mm", fill=(60, 30, 20), align="center")

def gag(im, kind, hand, t, sh=None):
    sh = sh or {}
    d = ImageDraw.Draw(im)
    if kind == "flame":
        x, y = hand; f = 1 + 0.15 * math.sin(t * 30)
        d.polygon([(x - 40 * f, y + 60), (x, y - 90 * f), (x + 40 * f, y + 60)], fill=(250, 130, 30)); d.polygon([(x - 20, y + 60), (x, y - 40 * f), (x + 20, y + 60)], fill=(255, 220, 80))
    if kind == "ouch":
        f = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", int(170 + 20 * math.sin(t * 20)))
        d.text((W // 2 + 200, 520), "АЙ!", font=f, anchor="mm", fill=(230, 40, 40), stroke_width=8, stroke_fill=(255, 255, 255))
    if kind == "money":
        r = np.random.default_rng(4)
        for k in range(26):
            x = (r.random() * W + math.sin(t * 2 + k) * 40); y = ((r.random() * H) + t * (300 + 200 * r.random())) % (H + 200) - 100
            a = (t * 90 + k * 37) % 360; bill = Image.new("RGBA", (150, 70), (90, 160, 90, 255)); bd = ImageDraw.Draw(bill)
            bd.rectangle([4, 4, 145, 65], outline=(40, 90, 40), width=5); bd.ellipse([55, 15, 95, 55], outline=(40, 90, 40), width=4); bd.text((75, 35), "$", font=ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 34), anchor="mm", fill=(30, 70, 30))
            bill = bill.rotate(a, expand=True); im.paste(bill, (int(x), int(y)), bill)
    if kind == "stamp":
        p = max(0, min(1, t / 0.18)); f = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", int(170 * min(1, 7 / len(sh.get("stamp_text", "ЗАКОННО"))) * (1.6 - 0.6 * p)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([170, 640, 910, 900], radius=30, outline=(40, 170, 60, 230), width=16); ld.text((540, 770), sh.get("stamp_text", "ЗАКОННО"), font=f, anchor="mm", fill=(40, 170, 60, 230))
        lay = lay.rotate(-8, center=(540, 770)); im.paste(lay, (0, 0), lay)
    if kind == "calc":
        f = ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 110); lines = sh.get("calc_lines", ["БИЛЕТЫ: −", "ВЫИГРЫШИ: +", "= ПРИБЫЛЬ"])
        for k, ln in enumerate(lines):
            if t > k * 0.35: ImageDraw.Draw(im).text((540, 250 + k * 150), ln, font=f, anchor="mm", fill=(255, 235, 120) if k == 2 else (255, 255, 255), stroke_width=6, stroke_fill=(20, 20, 20))
    if kind == "nozombie":
        cx, cy = 540, 560
        d.ellipse([cx - 70, cy - 190, cx + 70, cy - 50], fill=(120, 170, 100), outline=(30, 30, 30), width=6)
        d.rectangle([cx - 80, cy - 50, cx + 80, cy + 180], fill=(90, 110, 80), outline=(30, 30, 30), width=6)
        d.line([(cx - 80, cy + 10), (cx - 220, cy - 10)], fill=(120, 170, 100), width=26); d.line([(cx + 80, cy + 10), (cx + 220, cy - 10)], fill=(120, 170, 100), width=26)
        d.line([(cx - 260, cy - 260), (cx + 260, cy + 240)], fill=(220, 30, 30), width=36); d.line([(cx + 260, cy - 260), (cx - 260, cy + 240)], fill=(220, 30, 30), width=36)
    if kind == "book":
        x, y = hand; d.rectangle([x - 90, y - 140, x + 90, y + 20], fill=(150, 30, 40), outline=(30, 30, 30), width=6)
        d.text((x, y - 60), sh.get("book_text", "СОЗНАЮЩИЙ\nУМ"), font=ImageFont.truetype(f"{HERE}/../fonts/Oswald-Bold.ttf", 34), anchor="mm", fill=(250, 230, 160), align="center")

# ---------------- frames ----------------
def frame(t):
    t = float(t); sh = next((s for s in SHOTS if s["a"] <= t < s["b"]), None) or max((s for s in SHOTS if s["a"] <= t), key=lambda s: s["a"], default=SHOTS[0]); lt = float(t - sh["a"]); dur = sh["b"] - sh["a"]
    im = BGS[sh["bg"]].copy()
    talk_lvl = float(ENV[min(len(ENV) - 1, int(t * SR))])
    heads = []
    for i, (who, x, pose) in enumerate(sh["cast"]):
        p = {k: v for k, v in pose.items() if k != "talk"}
        if pose.get("talk"): p["mouth_open"] = min(1, talk_lvl * 2.2)
        seed = hash((who, i)) % 97
        p.setdefault("blink", 1.0 if ((t * FPS + seed * 7) % 95) < 3 else 0.0)
        p["bob"] = p.get("bob", 0) + math.sin(t * 4 + seed) * 5
        if "rage" in p: p["rage"] = min(p["rage"], lt / 0.35 * p["rage"])
        p["t"] = t
        hgt = 920; ci = draw(CAST[who], height=hgt, **p)
        px, py = int(x - ci.width / 2), GROUND - ci.height + 20
        im.paste(ci, (px, py), ci); heads.append((x, py + hgt * 0.24, (px + ci.width * 0.5 + (0.5 if p.get("arm_r", 0) > 0 else -0.5) * ci.width * 0.6, py + hgt * 0.62)))
    if sh.get("bubble"): i, kind = sh["bubble"]; bubble(im, heads[i][0], heads[i][1], kind, t)
    if sh.get("fx") in ("flame", "book"): gag(im, sh["fx"], heads[0][2] if heads else (540, 900), lt, sh)
    # camera: push-in from zoom*0.94 to zoom over the shot, centred on (fx, fy)
    z0, fx, fy = sh["cam"]; z = max(1.0, z0 * (0.94 + 0.06 * min(1, lt / max(0.4, dur))))
    if sh.get("hook") and lt < 0.45: z *= 1.04; fx += math.sin(lt * 90) * 22 * (1 - lt / 0.45); fy += math.cos(lt * 77) * 22 * (1 - lt / 0.45)   # impact shake
    cw, ch = W / z, H / z; x0 = min(max(0, fx - cw / 2), W - cw); y0 = min(max(0, fy - ch / 2), H - ch)
    im = im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)
    if sh.get("fx") in ("ouch", "nozombie", "money", "stamp", "calc"): gag(im, sh["fx"], None, lt, sh)     # screen space: never cropped by the camera
    if sh.get("sign"): sign(im, sh["sign"], lt)
    if sh.get("hook"): hook_title(im, sh["hook"], lt)
    if lt < 0.07: im = im.filter(ImageFilter.GaussianBlur(float(10 * (1 - lt / 0.07))))   # snap on the cut
    # one-word caption
    words = [w for r in rows for w in r["words"]]
    cur = next((w for j, w in enumerate(words) if w[0] <= t < (words[j + 1][0] if j + 1 < len(words) else w[1] + 0.3)), None)
    if cur and t < cur[1] + 0.35 and not sh.get("hook"):
        txt = cur[2].strip(" ,.:;!?«»—").upper()
        if txt: ImageDraw.Draw(im).text((W // 2, int(H * 0.64)), txt, font=FONT if FONT.getlength(txt) < W - 80 else FONT.font_variant(size=int(FONT.size * (W - 80) / FONT.getlength(txt))), anchor="mm", fill=(255, 255, 255), stroke_width=7, stroke_fill=(20, 20, 20))
    return im

def main():
    os.makedirs(f"{HERE}/out", exist_ok=True); audio = mix(); out = f"{HERE}/out/{os.path.basename(HERE)}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", out], stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)):
        im = frame(f / FPS); fade = min(1, (TOTAL - f / FPS) / 0.4)
        if fade < 1: im = Image.blend(Image.new("RGB", (W, H)), im, max(0, fade))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait(); print(out, round(TOTAL, 1), "s,", len(SHOTS), "shots")

if __name__ == "__main__":
    if "--stills" in sys.argv:
        ims = [frame(s["a"] + min(0.6, (s["b"] - s["a"]) * 0.6)).resize((216, 384)) for s in SHOTS]
        sheet = Image.new("RGB", (216 * 8, 384 * math.ceil(len(ims) / 8)), "white")
        for k, im in enumerate(ims): sheet.paste(im, ((k % 8) * 216, (k // 8) * 384))
        os.makedirs(f"{HERE}/out", exist_ok=True); sheet.save(f"{HERE}/out/stills.png"); print(len(ims), "shots", round(TOTAL, 1), "s")
    else: main()
