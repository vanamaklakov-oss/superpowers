"""Движок вертикальных страшилок «экран телефона + плоские мультяшные персонажи». Всё рисуется кодом (PIL).
История = папка со story.py (SCENES, YELLOW, RED, META). Каждая сцена: (n, текст озвучки, вид, параметры).
Числа "at"/"on"/"knocks" — индекс слова фразы, на котором элемент появляется (-1 = сразу).

  python3 engine.py <папка> tts        озвучка vo/NN.mp3 + тайминги слов
  python3 engine.py <папка> check      распознать озвучку faster-whisper small и сравнить с текстом
  python3 engine.py <папка> stills     кадры stills/sheet.jpg
  python3 engine.py <папка> build      <папка>/<имя>.mp4

Виды сцен и параметры:
  lock   {date, clock, app, name, av, text, at}                 экран блокировки + уведомление
  wake   {..как lock.., on}                                      тёмный экран загорается на слове on
  chat   {title, sub, av, clock, msgs:[{day?, av, name, col, text, tm, red?, me?, voice?, play?, at}], typing:{text, at}}
  pinned {title, sub, author, author_sub, av, rules:[{text, red?, at}]}
  call   {name, av, accept?}                                     входящий звонок, на accept — идёт разговор
  doors  {left, right, ghost}                                    подъезд/коридор: две двери и «несуществующая» между ними
  door_open {num}                                                распахнутая дверь в темноту
  room   {who: boy|girl, clock, note?, scared?, sleep?}         герой в комнате ночью
  knock  {knocks:[..], notif?:{av, name, text, at}}              входная дверь изнутри, «ТУК»
  window {knocks:[..], at}                                       окно ночью, силуэт за стеклом
  choice {a, asub, b, bsub, part}                                финальный выбор (без субтитров)
Аватары: t:<текст>:<red|blue|green|gray|purple> или лица kolya, tamara, mom, grandma, girl, boy, teacher, petya, unknown."""
import importlib.util, json, math, os, re, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR, GAP = 1080, 1920, 30, 48000, 0.25
FD = "/usr/share/fonts/opentype/inter"
def F(name, size): return ImageFont.truetype(f"{FD}/{name}.otf", size)
f_reg, f_semi, f_bold = (lambda s: F("Inter-Regular", s)), (lambda s: F("Inter-SemiBold", s)), (lambda s: F("Inter-Bold", s))
f_black = lambda s: F("InterDisplay-Black", s)
CAP = f_black(88)
SCR = (23, 29, 43); BUB = (37, 45, 63); MYB = (52, 92, 170); TXT = (236, 239, 246); SUB = (138, 148, 170)
BLUE = (96, 146, 236); REDC = (236, 78, 78); YEL = (255, 225, 0); OUTL = (24, 22, 30)
NAMECOL = {"red": (220, 84, 84), "blue": (110, 170, 240), "green": (120, 200, 140), "purple": (180, 140, 240), "orange": (240, 160, 80)}
rng = np.random.default_rng(13)

# ---------------- story ----------------
DIR = os.path.abspath(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else "build"
spec = importlib.util.spec_from_file_location("story", f"{DIR}/story.py"); ST = importlib.util.module_from_spec(spec); spec.loader.exec_module(ST)
SCENES, YELLOW, RED = ST.SCENES, {w.lower() for w in ST.YELLOW}, {w.lower() for w in ST.RED}
VOICE, RATE, PITCH = getattr(ST, "VOICE", ("ru-RU-DmitryNeural", 6, 14))
NAME = os.path.basename(DIR)

def tts():
    import asyncio, ssl, time, edge_tts, edge_tts.communicate as c
    c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt"); VO = f"{DIR}/vo"; os.makedirs(VO, exist_ok=True)
    def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    def say(text, out):
        for dr, dp in [(0, 0), (1, 0), (-1, 1), (2, -1), (0, 2), (-2, 0), (3, 1)]:
            async def go():
                com = edge_tts.Communicate(text, voice=VOICE, rate=f"{RATE + dr:+d}%", pitch=f"{PITCH + dp:+d}Hz", boundary="WordBoundary"); ws = []
                with open(out, "wb") as f:
                    async for ch in com.stream():
                        if ch["type"] == "audio": f.write(ch["data"])
                        elif ch["type"] == "WordBoundary": ws.append({"w": ch["text"], "s": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
                return ws
            try:
                ws = asyncio.run(go())
                if ws and os.path.getsize(out) > 2000: return ws
            except Exception: time.sleep(1.5)
        raise RuntimeError(f"tts failed: {text}")
    for n, text, *_ in SCENES:
        out = f"{VO}/{n:02d}.mp3"
        if os.path.exists(out + ".json") and json.load(open(out + ".json")).get("text") == text: continue
        parts = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]; files, words, t = [], [], 0.0
        for i, s in enumerate(parts):
            pf = f"{VO}/{n:02d}.p{i}.mp3"; ws = say(s, pf); files.append(pf); words += [{**w, "s": w["s"] + t} for w in ws]; t += dur(pf)
        lst = f"{VO}/{n:02d}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
        for f in files + [lst]: os.remove(f)
        json.dump({"text": text, "dur": dur(out), "words": words}, open(out + ".json", "w"), ensure_ascii=False)
        print(n, "ok", round(dur(out), 2), [w["w"] for w in words], flush=True)

def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def check():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", compute_type="int8")
    for n, text, *_ in SCENES:
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
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR
rows, t = [], 0.35
for n, text, kind, par in SCENES:
    a, lead = trim(pcm(f"{DIR}/vo/{n:02d}.mp3")); meta = json.load(open(f"{DIR}/vo/{n:02d}.mp3.json"))
    words = [(t + w["s"] - lead, t + w["s"] - lead + w["d"], w["w"]) for w in meta["words"]]
    extra = par.get("hold", 0.5 if kind in ("knock", "wake", "window", "call") else 0.0)
    rows.append({"n": n, "kind": kind, "par": par, "t0": t, "a": a, "words": words}); t += len(a) / SR + GAP + extra
TOTAL = t + 2.2
for i, r in enumerate(rows): r["t1"] = rows[i + 1]["t0"] if i + 1 < len(rows) else TOTAL
def wt(r, i):
    if isinstance(i, str):  # "слово" или "слово#2" — начало N-го вхождения слова
        w, _, k = i.partition("#"); k = int(k or 1); cl = lambda z: re.sub(r"[^\wё]", "", z.lower())
        hits = [x for x in r["words"] if cl(x[2]).startswith(cl(w))]
        if len(hits) < k: raise ValueError(f"сцена {r['n']}: нет слова {i!r}")
        return hits[k - 1][0]
    return -1e9 if i is None or i < 0 else r["words"][min(i, len(r["words"]) - 1)][0]
def has(i): return isinstance(i, str) or (i is not None and i >= 0)
def appear(t, t0, dur=0.25): return max(0.0, min(1.0, (t - t0) / dur))

# ---------------- drawing ----------------
def ss(w, h, fn, k=3):
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), k); return im.resize((w, h), Image.LANCZOS)
def ttext(d, xy, s, font, fill, anchor="la"): d.text(xy, s, font=font, fill=fill, anchor=anchor)
def fade(im, a):
    if a < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im
def grad(c0, c1, w=W, h=H):
    a = np.linspace(0, 1, h)[:, None, None]; arr = (np.array(c0) * (1 - a) + np.array(c1) * a).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, 1), "RGB").convert("RGBA")
def wrap(d, s, font, maxw):
    out, cur = [], ""
    for w in s.split():
        if cur and d.textlength(cur + " " + w, font=font) > maxw: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]

def face(d, k, cx, cy, r, skin=(233, 196, 160), hair=None, style="", eyes="open", px=0, brow=0.4, mouth="line", lw=5, glasses=False):
    S = lambda v: int(v * k); o = OUTL; L = S(lw)
    if style == "long": d.rounded_rectangle([S(cx - r * 1.1), S(cy - r * 0.9), S(cx + r * 1.1), S(cy + r * 1.3)], S(r * 0.6), fill=hair, outline=o, width=L)
    if style == "bun": d.ellipse([S(cx - r * 0.45), S(cy - r * 1.55), S(cx + r * 0.45), S(cy - r * 0.7)], fill=hair, outline=o, width=L)
    for sx in (-1, 1):
        d.ellipse([S(cx + sx * r * 0.95 - r * 0.13), S(cy - r * 0.2), S(cx + sx * r * 0.95 + r * 0.13), S(cy + r * 0.25)], fill=skin, outline=o, width=L)
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=skin, outline=o, width=L)
    if hair is not None and style != "bald":
        d.chord([S(cx - r * 1.02), S(cy - r * 1.06), S(cx + r * 1.02), S(cy + r * 0.5)], 180, 360, fill=hair, outline=o, width=L)
        if style in ("boy", "long"):
            for j in range(5):
                x0 = cx - r * 0.9 + j * r * 0.38
                d.polygon([(S(x0), S(cy - r * 0.32)), (S(x0 + r * 0.42), S(cy - r * 0.32)), (S(x0 + r * 0.3), S(cy - r * 0.05))], fill=hair)
    ex, ey, er = r * 0.38, cy - r * 0.02, r * (0.27 if eyes != "scared" else 0.31)
    for sx in (-1, 1):
        x = cx + sx * ex
        if eyes == "closed": d.arc([S(x - er), S(ey - er * 0.6), S(x + er), S(ey + er * 0.6)], 10, 170, fill=o, width=L)
        else:
            d.ellipse([S(x - er), S(ey - er), S(x + er), S(ey + er)], fill=(250, 250, 250), outline=o, width=L)
            pr = er * (0.45 if eyes == "open" else 0.26)
            d.ellipse([S(x + px * er * 0.4 - pr), S(ey - pr), S(x + px * er * 0.4 + pr), S(ey + pr)], fill=o)
        by = ey - er - r * (0.1 + 0.08 * brow); tilt = r * 0.03 * (brow - 0.5)
        d.line([S(x - er * 0.9), S(by + sx * tilt), S(x + er * 0.9), S(by - sx * tilt)], fill=o, width=L)
        if glasses: d.ellipse([S(x - er * 1.25), S(ey - er * 1.25), S(x + er * 1.25), S(ey + er * 1.25)], outline=o, width=L)
    if style == "bald": d.line([S(cx - r * 0.35), S(cy + r * 0.42), S(cx + r * 0.35), S(cy + r * 0.42)], fill=(80, 70, 70), width=S(r * 0.12))
    if mouth == "line": d.arc([S(cx - r * 0.18), S(cy + r * 0.38), S(cx + r * 0.18), S(cy + r * 0.62)], 20, 160, fill=o, width=L)
    elif mouth == "o": d.ellipse([S(cx - r * 0.09), S(cy + r * 0.45), S(cx + r * 0.09), S(cy + r * 0.66)], fill=(70, 30, 35), outline=o, width=L)

FACES = {  # bg, style, hair, glasses, skin
    "kolya": ((92, 122, 170), "bald", None, False), "tamara": ((150, 108, 172), "bun", (190, 190, 200), True),
    "mom": ((205, 112, 118), "long", (110, 66, 44), False), "grandma": ((120, 150, 120), "bun", (215, 215, 220), True),
    "girl": ((200, 140, 200), "long", (60, 40, 32), False), "boy": ((214, 128, 58), "boy", (86, 58, 40), False),
    "teacher": ((90, 100, 120), "boy", (50, 50, 56), True), "petya": ((90, 170, 130), "boy", (200, 110, 50), False)}
TXTAV = {"red": ((36, 34, 40), (205, 60, 60)), "blue": ((70, 108, 196), (255, 255, 255)), "green": ((60, 140, 90), (255, 255, 255)),
         "gray": ((60, 64, 74), (200, 200, 210)), "purple": ((110, 80, 170), (255, 255, 255))}
AVC = {}
def avatar(kind, D):
    if (kind, D) in AVC: return AVC[(kind, D)]
    def fn(d, k):
        S = lambda v: int(v * k); r = D / 2
        if kind.startswith("t:") or kind == "unknown":
            _, txt, col = kind.split(":") if kind != "unknown" else ("t", "?", "gray"); bg, fg = TXTAV[col]
            d.ellipse([0, 0, S(D) - 1, S(D) - 1], fill=bg); d.text((S(r), S(r)), txt, font=f_black(S(D * (0.42 if len(txt) < 3 else 0.3))), fill=fg, anchor="mm")
        else:
            bg, st, hair, gl = FACES[kind]; d.ellipse([0, 0, S(D) - 1, S(D) - 1], fill=bg)
            face(d, k, r, r * 1.08, r * 0.56, hair=hair, style=st, lw=max(1.2, D / 40), glasses=gl)
    im = ss(D, D, fn, 4); m = Image.new("L", (D * 4, D * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (D, D), 0), m.resize((D, D), Image.LANCZOS))); AVC[(kind, D)] = im; return im

def hero(who="boy", eyes="open", px=0, scared=False):
    w, h = 820, 1300
    def fn(d, k):
        S = lambda v: int(v * k); o = OUTL; L = S(6)
        hood = (214, 128, 58) if who == "boy" else (120, 96, 200)
        d.rounded_rectangle([S(90), S(700), S(730), S(h + 200)], S(200), fill=hood, outline=o, width=L)
        d.line([S(410), S(760), S(410), S(h)], fill=o, width=L)
        d.line([S(360), S(720), S(345), S(860)], fill=(240, 236, 226), width=S(8)); d.line([S(460), S(720), S(475), S(860)], fill=(240, 236, 226), width=S(8))
        d.rectangle([S(350), S(600), S(470), S(720)], fill=(226, 180, 140)); d.line([S(350), S(600), S(350), S(712)], fill=o, width=L); d.line([S(470), S(600), S(470), S(712)], fill=o, width=L)
        face(d, k, 410, 400, 250, skin=(226, 182, 142), hair=(86, 58, 40) if who == "boy" else (60, 40, 32), style="boy" if who == "boy" else "long",
             eyes=("scared" if scared and eyes != "closed" else eyes), px=px, brow=(1.6 if scared else 0.4), mouth=("o" if scared else "line"), lw=6)
    return ss(w, h, fn, 2)

def zoom(im, s, cx=0.5, cy=0.5):
    s = max(1.0, s); w, h = W / s, H / s; x0, y0 = (W - w) * cx, (H - h) * cy
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))

CACHE = {}
def cached(key, fn):
    if key not in CACHE: CACHE[key] = fn()
    return CACHE[key]

# ---------------- phone UI ----------------
PX0, PY0, PX1, PY1 = 34, 40, W - 34, H - 40
def phone_base(clock="03:13"):
    def mk():
        im = grad((26, 32, 64), (14, 16, 30)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([PX0, PY0, PX1, PY1], 96, fill=(8, 9, 14)); d.rounded_rectangle([PX0 + 14, PY0 + 14, PX1 - 14, PY1 - 14], 84, fill=SCR)
        d.rounded_rectangle([W // 2 - 70, PY0 + 34, W // 2 + 70, PY0 + 74], 20, fill=(4, 4, 6)); ttext(d, (120, PY0 + 40), clock, f_semi(36), TXT)
        for j in range(4): d.rectangle([W - 250 + j * 14, PY0 + 60 - j * 7, W - 241 + j * 14, PY0 + 70], fill=TXT)
        d.rounded_rectangle([W - 180, PY0 + 46, W - 120, PY0 + 72], 7, outline=TXT, width=3); d.rectangle([W - 175, PY0 + 51, W - 140, PY0 + 67], fill=TXT)
        return im
    return cached(("phone", clock), mk).copy()

def header(im, title, sub, av, subcol=SUB):
    d = ImageDraw.Draw(im); d.rectangle([PX0 + 14, 150, PX1 - 14, 300], fill=(28, 35, 52)); ttext(d, (95, 225), "‹", f_reg(80), BLUE, "lm")
    if av: im.alpha_composite(avatar(av, 104), (150, 173))
    x = 278 if av else 150; ttext(d, (x, 205), title, f_bold(44), TXT, "lm"); ttext(d, (x, 255), sub, f_reg(32), subcol, "lm")

def pill(d, y, s):
    f = f_semi(28); w = d.textlength(s, font=f) + 44
    d.rounded_rectangle([W / 2 - w / 2, y, W / 2 + w / 2, y + 46], 23, fill=(40, 50, 72)); ttext(d, (W / 2, y + 23), s, f, (200, 208, 224), "mm"); return y + 70

def msg(im, y, m, a=1.0, prog=None):
    c = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(c); ft, fn = f_reg(42), f_semi(32); me = m.get("me")
    name = "" if me else m.get("name", ""); top = 22 + (44 if name else 0)
    if m.get("voice"):
        lines = []; bw = 600; bh = top + 110
    else:
        lines = wrap(d, m["text"], ft, 640); bw = max(max(d.textlength(l, font=ft) for l in lines), d.textlength(name, font=fn)) + 150; bh = top + 56 * len(lines) + 40
    x0 = (W - 80 - bw) if me else 190
    d.rounded_rectangle([x0, 0, x0 + bw, bh], 34, fill=MYB if me else BUB)
    if name: ttext(d, (x0 + 34, 22), name, fn, NAMECOL.get(m.get("col"), (110, 170, 240)))
    for i, l in enumerate(lines): ttext(d, (x0 + 34, top + i * 56), l, ft, TXT)
    if m.get("voice"):
        cy = top + 40; d.ellipse([x0 + 30, cy - 38, x0 + 106, cy + 38], fill=BLUE); d.polygon([(x0 + 58, cy - 18), (x0 + 58, cy + 18), (x0 + 86, cy)], fill=(255, 255, 255))
        bars = np.abs(np.sin(np.arange(34) * 1.7) * np.cos(np.arange(34) * 0.45)) * 34 + 6
        for i, bh2 in enumerate(bars):
            xx = x0 + 130 + i * 12; on = prog is not None and i / len(bars) <= prog
            d.rounded_rectangle([xx, cy - bh2 / 2, xx + 6, cy + bh2 / 2], 3, fill=(255, 255, 255) if on else (120, 132, 160))
        ttext(d, (x0 + 130, cy + 44), m["voice"], f_semi(26), SUB)
    ttext(d, (x0 + bw - 28, bh - 28), m.get("tm", ""), f_semi(26), REDC if m.get("red") else SUB, "rm")
    if not me: c.alpha_composite(avatar(m.get("av", "unknown"), 92), (82, bh - 100))
    im.alpha_composite(fade(c, a), (0, int(y + (1 - a) * 30))); return y + bh + 30

def notif_card(n, a, w=W):
    c = Image.new("RGBA", (w, 240), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([70, 0, w - 70, 210], 40, fill=(46, 54, 80, 240)); c.alpha_composite(avatar(n["av"], 110), (105, 50))
    if n.get("app"): ttext(d, (245, 34), n["app"], f_semi(30), (176, 186, 208))
    ttext(d, (w - 110, 34), n.get("when", "сейчас"), f_reg(28), (176, 186, 208), "ra")
    ttext(d, (245, 80 if n.get("app") else 50, ), n["name"], f_bold(40), TXT); ttext(d, (245, 132 if n.get("app") else 108), n["text"], f_reg(40), TXT)
    return fade(c, a)

# ---------------- scenes ----------------
def sc_lock(r, t, bright=1.0):
    p = r["par"]
    def base():
        im = phone_base(p.get("clock", "03:13")); d = ImageDraw.Draw(im)
        im.alpha_composite(grad((30, 38, 78), (16, 18, 36), PX1 - PX0 - 28, PY1 - PY0 - 200), (PX0 + 14, PY0 + 110))
        ttext(d, (W / 2, 330), p.get("date", "среда, 18 ноября"), f_semi(46), (210, 216, 236), "mm")
        ttext(d, (W / 2, 470), p.get("clock", "03:13"), f_black(230), (240, 242, 250), "mm")
        if p.get("alarm"): ttext(d, (W / 2, 620), "⏰ " + p["alarm"] if False else p["alarm"], f_semi(44), (255, 190, 90), "mm")
        return im
    im = cached(("lock", r["n"]), base).copy()
    a = appear(t, wt(r, p.get("at", -1)), 0.3)
    if a > 0 and p.get("text"): im.alpha_composite(notif_card(p, a), (0, int(700 - (1 - a) * 60)))
    if bright < 1: im.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, int(255 * (1 - bright)))))
    return im

def sc_wake(r, t):
    ton = wt(r, r["par"]["on"])
    if t < ton:
        im = phone_base(); ImageDraw.Draw(im).rounded_rectangle([PX0 + 14, PY0 + 14, PX1 - 14, PY1 - 14], 84, fill=(4, 5, 8)); return im
    return sc_lock(dict(r, par=dict(r["par"], at=-1)), t, 0.15 + 0.85 * appear(t, ton, 0.35))

def sc_chat(r, t):
    p = r["par"]; ty = p.get("typing"); typing = ty and wt(r, ty["at"]) - 1.6 < t < wt(r, ty["at"])
    im = phone_base(p.get("clock", "03:13")); header(im, p["title"], ty["text"] if typing else p.get("sub", ""), p.get("av"), REDC if typing else SUB)
    d = ImageDraw.Draw(im); y = 340
    for m in p["msgs"]:
        a = appear(t, wt(r, m.get("at", -1)))
        if a <= 0: break
        if m.get("day"): y = pill(d, y, m["day"])
        prog = None
        if m.get("play") is not None: prog = min(1.0, max(0.0, (t - wt(r, m["play"])) / m.get("plen", 3.0))) if t >= wt(r, m["play"]) else 0.0
        y = msg(im, y, m, a, prog)
    return im

def sc_pinned(r, t):
    p = r["par"]
    def base():
        im = phone_base(p.get("clock", "16:41")); d = ImageDraw.Draw(im); d.rectangle([PX0 + 14, 150, PX1 - 14, 300], fill=(28, 35, 52))
        ttext(d, (95, 225), "‹", f_reg(80), BLUE, "lm"); ttext(d, (150, 200), "Закреплённые", f_bold(46), TXT, "lm"); ttext(d, (150, 252), p["title"], f_reg(32), SUB, "lm")
        d.rounded_rectangle([70, 340, W - 70, 1200], 36, fill=BUB); im.alpha_composite(avatar(p["av"], 96), (100, 370))
        ttext(d, (220, 395), p["author"], f_bold(40), (120, 200, 140)); ttext(d, (220, 445), p.get("author_sub", ""), f_reg(30), SUB); return im
    im = cached(("pin", r["n"]), base).copy(); y = 540
    for i, ru in enumerate(p["rules"]):
        c = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.ellipse([110, 6, 166, 62], fill=(60, 74, 104)); ttext(d, (138, 34), str(i + 1), f_bold(34), TXT, "mm")
        ls = wrap(d, ru["text"], f_semi(42), 760)
        for j, l in enumerate(ls): ttext(d, (195, 8 + j * 56), l, f_semi(42), TXT)
        hh = 8 + 56 * len(ls)
        if ru.get("red"): ttext(d, (195, hh), ru["red"], f_bold(40), REDC); hh += 56
        a = appear(t, wt(r, ru.get("at", -1)), 0.3)
        if a > 0: im.alpha_composite(fade(c, a), (int((1 - a) * 40), y))
        y += hh + 40
    return im

def sc_call(r, t):
    p = r["par"]; lt = t - r["t0"]; acc = wt(r, p["accept"]) if "accept" in p else 1e9
    im = phone_base(p.get("clock", "03:20")); im.alpha_composite(grad((40, 50, 90), (18, 20, 36), PX1 - PX0 - 28, PY1 - PY0 - 200), (PX0 + 14, PY0 + 110))
    d = ImageDraw.Draw(im); on = t >= acc
    if not on:
        pr = (lt * 1.2) % 1; ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse([W / 2 - 150 - pr * 90, 470 - 150 - pr * 90, W / 2 + 150 + pr * 90, 470 + 150 + pr * 90], outline=(255, 255, 255, int(120 * (1 - pr))), width=6)
        im.alpha_composite(ring)
    im.alpha_composite(avatar(p["av"], 280), (W // 2 - 140, 330))
    ttext(d, (W / 2, 700), p["name"], f_bold(70), TXT, "mm")
    sub = f"{int(t - acc) // 60:02d}:{int(t - acc) % 60:02d}" if on else p.get("sub", "входящий вызов")
    ttext(d, (W / 2, 780), sub, f_semi(42), SUB, "mm")
    if on: d.ellipse([W / 2 - 75, 1640, W / 2 + 75, 1790], fill=(230, 70, 70)); ttext(d, (W / 2, 1715), "✕" if False else "—", f_black(70), (255, 255, 255), "mm")
    else:
        for cx, col in ((300, (230, 70, 70)), (780, (60, 190, 100))): d.ellipse([cx - 75, 1640, cx + 75, 1790], fill=col)
        ttext(d, (300, 1715), "—", f_black(70), (255, 255, 255), "mm"); ttext(d, (780, 1712), "✓" if False else "+", f_black(80), (255, 255, 255), "mm")
    return im

def doors_base(p):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 760], fill=(118, 122, 112)); d.rectangle([0, 760, W, 1560], fill=(46, 84, 70)); d.rectangle([0, 752, W, 768], fill=(34, 60, 50))
        for y in range(1560, H, 60):
            for x in range(-((y // 60) % 2) * 60, W, 120): d.rectangle([x, y, x + 58, y + 58], fill=(74, 62, 56) if (x // 60) % 2 else (62, 52, 48))
        for x0, num in ((70, p.get("left", "12")), (720, p.get("right", "14"))):
            d.rectangle([x0 - 16, 560, x0 + 306, 1580], fill=(36, 30, 28)); d.rectangle([x0, 576, x0 + 290, 1580], fill=(104, 64, 42), outline=OUTL, width=6)
            d.rectangle([x0 + 30, 620, x0 + 260, 1000], outline=(80, 48, 30), width=6); d.rectangle([x0 + 30, 1080, x0 + 260, 1500], outline=(80, 48, 30), width=6)
            d.rounded_rectangle([x0 + 236, 1050, x0 + 276, 1072], 8, fill=(200, 190, 150), outline=OUTL, width=3)
            fw = max(90, d.textlength(num, font=f_black(46)) + 40)
            d.rounded_rectangle([x0 + 145 - fw / 2, 440, x0 + 145 + fw / 2, 520], 40, fill=(225, 222, 210), outline=OUTL, width=5); ttext(d, (x0 + 145, 480), num, f_black(46), (40, 40, 40), "mm")
        d.line([W / 2, 0, W / 2, 110], fill=(20, 20, 20), width=5); return im
    return mk

def sc_doors(r, t):
    p = r["par"]; lt = t - r["t0"]; im = cached(("doors", r["n"]), doors_base(p)).copy()
    ghost = 0.5 + 0.5 * math.sin(lt * 1.7 - 1.5); g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    al = int(80 * ghost * appear(lt, 1.5, 1.5)); gt = p.get("ghost", "13")
    d.rectangle([400, 576, 680, 1580], outline=(200, 200, 210, al), width=5)
    fw = max(90, d.textlength(gt, font=f_black(46)) + 40)
    d.rounded_rectangle([540 - fw / 2, 440, 540 + fw / 2, 520], 40, outline=(220, 70, 70, al), width=5); ttext(d, (540, 480), gt, f_black(46), (220, 70, 70, al), "mm")
    im.alpha_composite(g); fl = 1.0 if (int(lt * 9) * 7919) % 13 else 0.35
    glow = cached("lampglow", lambda: (lambda gg: (ImageDraw.Draw(gg).ellipse([W / 2 - 520, -380, W / 2 + 520, 640], fill=(255, 230, 160, 70)), gg.filter(ImageFilter.GaussianBlur(90)))[1])(Image.new("RGBA", (W, H), (0, 0, 0, 0))))
    if fl > 0.5: im.alpha_composite(glow)
    d = ImageDraw.Draw(im); d.ellipse([W / 2 - 34, 100, W / 2 + 34, 168], fill=(255, 238, 190) if fl > 0.5 else (120, 110, 90))
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    return zoom(im, 1.0 + 0.07 * (lt / (r["t1"] - r["t0"])), 0.5, 0.45)

def sc_door_open(r, t):
    p = r["par"]; lt = t - r["t0"]
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 760], fill=(110, 114, 104)); d.rectangle([0, 760, W, 1600], fill=(42, 78, 64)); d.rectangle([0, 1600, W, H], fill=(64, 54, 50))
        d.rectangle([250, 500, 760, 1610], fill=(30, 26, 24)); d.rectangle([270, 520, 740, 1610], fill=(3, 3, 5))
        d.polygon([(740, 520), (930, 440), (930, 1700), (740, 1610)], fill=(104, 64, 42)); d.line([(740, 520), (930, 440), (930, 1700), (740, 1610), (740, 520)], fill=OUTL, width=6)
        d.ellipse([810, 600, 890, 660], fill=(225, 222, 210), outline=OUTL, width=4); ttext(d, (850, 630), p.get("num", "10"), f_black(30), (40, 40, 40), "mm")
        d.polygon([(270, 1610), (740, 1610), (900, H), (120, H)], fill=(0, 0, 0)); im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60))); return im
    return zoom(cached(("dopen", r["n"]), mk).copy(), 1.0 + 0.16 * lt / (r["t1"] - r["t0"]), 0.45, 0.5)

def sc_room(r, t):
    p = r["par"]; lt = t - r["t0"]; scared = p.get("scared", False); who = p.get("who", "boy")
    def mk():
        im = grad((38, 36, 78), (22, 20, 46)) if not scared else grad((58, 26, 40), (24, 14, 24)); d = ImageDraw.Draw(im)
        d.rectangle([600, 210, 960, 700], fill=(16, 20, 48), outline=OUTL, width=10); d.line([780, 210, 780, 700], fill=OUTL, width=10); d.line([600, 455, 960, 455], fill=OUTL, width=10)
        d.ellipse([820, 260, 910, 350], fill=(232, 226, 196)); d.ellipse([845, 248, 930, 338], fill=(16, 20, 48))
        d.rounded_rectangle([110, 260, 380, 380], 18, fill=(14, 14, 18), outline=OUTL, width=6); ttext(d, (245, 322), p.get("clock", "03:12"), f_black(78), (255, 70, 60), "mm")
        if p.get("note"):
            d.polygon([(130, 520), (420, 500), (440, 760), (150, 780)], fill=(250, 220, 90)); d.line([(270, 500), (275, 530)], fill=(200, 60, 60), width=10)
            n = Image.new("RGBA", (300, 220), (0, 0, 0, 0)); nd = ImageDraw.Draw(n)
            for i, l in enumerate(p["note"]): ttext(nd, (150, 50 + i * 60), l, f_bold(36) if i == 0 else f_semi(32), (60, 40, 30), "mm")
            im.alpha_composite(n.rotate(4, Image.BICUBIC), (135, 540))
        return im
    im = cached(("room", r["n"]), mk).copy()
    sleep = p.get("sleep") and ("wake" not in p or t < wt(r, p["wake"]))
    blink = sleep or (lt % 2.9) < 0.13; px = 0 if scared else (-1 if (lt % 4) < 2 else 0.6)
    b = cached(("hero", who, blink, px, scared), lambda: hero(who, "closed" if blink else "open", px, scared))
    sh = int(4 * math.sin(lt * 40)) if scared else 0
    im.alpha_composite(b, ((W - b.width) // 2 + sh, H - b.height))
    if scared: im.alpha_composite(Image.new("RGBA", (W, H), (60, 0, 0, int(30 + 25 * math.sin(lt * 6)))))
    return zoom(im, 1.0 + 0.05 * lt / (r["t1"] - r["t0"]), 0.5, 0.6)

def knocks_at(r, t):
    sh, pops = 0.0, []
    for j, ki in enumerate(r["par"].get("knocks", [])):
        dt = t - wt(r, ki)
        if 0 <= dt < 0.35: sh += 10 * math.exp(-dt * 12) * math.sin(dt * 90)
        if 0 <= dt < 0.9: pops.append((j, dt))
    return sh, pops
def draw_pops(im, pops):
    for j, dt in pops:
        a = 1 - max(0, dt - 0.5) / 0.4; sc = min(1, 0.6 + dt * 4); c = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
        ttext(ImageDraw.Draw(c), (W / 2 + [-170, 160, -60, 120, -140][j % 5], 150), "ТУК", f_black(int(150 * sc)), (255, 255, 255, int(255 * a)), "mm")
        im.alpha_composite(c, (0, 380 + (j % 3) * 230))

def door_leaf():
    def fn(d, k):
        S = lambda v: int(v * k); d.rectangle([0, 0, S(540), S(1360)], fill=(118, 54, 44), outline=OUTL, width=S(7))
        for yy in range(1, 9):
            for xx in range(1, 5):
                cx, cy = xx * 108, yy * 150
                d.line([S(cx - 54), S(cy), S(cx), S(cy - 75), S(cx + 54), S(cy), S(cx), S(cy + 75), S(cx - 54), S(cy)], fill=(92, 40, 34), width=S(4))
                d.ellipse([S(cx - 9), S(cy - 9), S(cx + 9), S(cy + 9)], fill=(200, 170, 110))
        d.ellipse([S(250), S(430), S(290), S(470)], fill=(170, 170, 176), outline=OUTL, width=S(5)); d.ellipse([S(262), S(442), S(278), S(458)], fill=(250, 240, 200))
        d.rounded_rectangle([S(440), S(700), S(520), S(730)], S(10), fill=(200, 190, 150), outline=OUTL, width=S(4)); d.rectangle([S(458), S(770), S(500), S(830)], fill=(170, 160, 130), outline=OUTL, width=S(3))
    return ss(540, 1360, fn, 2)
def sc_knock(r, t):
    p = r["par"]; lt = t - r["t0"]
    def mk():
        im = grad((52, 44, 64), (26, 22, 32)); d = ImageDraw.Draw(im); d.rectangle([0, 1690, W, H], fill=(58, 44, 36))
        for x in range(-200, W + 200, 140): d.line([x, 1690, x + 80, H], fill=(48, 36, 30), width=4)
        d.rectangle([250, 330, 830, 1700], fill=(30, 24, 26)); d.rectangle([270, 1690, 810, 1704], fill=(255, 220, 150))
        d.rectangle([450, 1690, 520, 1704], fill=(10, 8, 8)); d.rectangle([570, 1690, 640, 1704], fill=(10, 8, 8))
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).rectangle([260, 1660, 820, 1730], fill=(255, 200, 120, 90)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(30)))
        return im
    im = cached("kbase", mk).copy(); sh, pops = knocks_at(r, t)
    im.alpha_composite(cached("leaf", door_leaf), (270 + int(sh), 335)); draw_pops(im, pops)
    if p.get("notif"):
        a = appear(t, wt(r, p["notif"]["at"]), 0.3)
        if a > 0: im.alpha_composite(notif_card(p["notif"], a), (0, int(70 - (1 - a) * 80)))
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 40)))
    return zoom(im, 1.0 + 0.06 * lt / (r["t1"] - r["t0"]), 0.5, 0.35)

def sc_window(r, t):
    p = r["par"]; lt = t - r["t0"]
    def mk():
        im = grad((30, 28, 56), (14, 12, 26)); d = ImageDraw.Draw(im)
        d.rectangle([170, 300, 910, 1500], fill=(12, 16, 40));
        for i in range(40):
            x, y = rng.integers(180, 900), rng.integers(310, 1100); d.ellipse([x, y, x + 4, y + 4], fill=(200, 200, 230))
        for i in range(9):  # far city lights low
            x = 190 + i * 80; d.rectangle([x, 1260 - (i * 37) % 120, x + 60, 1500], fill=(20, 22, 44))
        return im
    im = cached(("win", r["n"]), mk).copy(); sh, pops = knocks_at(r, t)
    a = appear(t, wt(r, p.get("at", -1)), 1.2)
    if a > 0:
        s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(s); cx = 540 + int(sh)
        d.ellipse([cx - 120, 620, cx + 120, 880], fill=(4, 4, 8, 255)); d.rounded_rectangle([cx - 260, 860, cx + 260, 1600], 160, fill=(4, 4, 8, 255))
        d.ellipse([cx - 62, 730, cx - 38, 748], fill=(230, 230, 210, 255)); d.ellipse([cx + 38, 730, cx + 62, 748], fill=(230, 230, 210, 255))
        s.putalpha(s.getchannel("A").point(lambda v: int(v * a)))
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle([170, 300, 910, 1500], fill=255); im.paste(s, (0, 0), Image.composite(s.getchannel("A"), Image.new("L", (W, H), 0), m))
    d = ImageDraw.Draw(im)
    d.rectangle([170, 300, 910, 1500], outline=(230, 228, 220), width=26); d.line([540, 300, 540, 1500], fill=(230, 228, 220), width=22); d.line([170, 800, 910, 800], fill=(230, 228, 220), width=22)
    d.rectangle([110, 1500, 970, 1560], fill=(230, 228, 220), outline=OUTL, width=6)
    for x0, x1 in ((0, 200), (880, W)): d.rectangle([x0, 220, x1, 1640], fill=(90, 40, 60)); d.line([x0 + 60, 220, x0 + 60, 1640], fill=(70, 30, 46), width=10)
    d.rectangle([0, 200, W, 240], fill=(60, 60, 70)); draw_pops(im, pops)
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 40)))
    return zoom(im, 1.0 + 0.08 * lt / (r["t1"] - r["t0"]), 0.5, 0.45)

def sc_choice(r, t):
    p = r["par"]; im = grad((30, 16, 30), (8, 8, 14)); d = ImageDraw.Draw(im); w = r["words"]; nw = len(w)
    tb = wt(r, p["b_at"]) if "b_at" in p else w[max(1, nw // 2)][0]; a1, a2, a3 = appear(t, w[0][0]), appear(t, tb), appear(t, w[-1][0], 0.2)
    def card(y, txt, sub, col, a):
        c = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(c); fz = 84
        while cd.textlength(txt, font=f_black(fz)) > 820: fz -= 4
        cd.rounded_rectangle([80, 0, W - 80, 300], 44, fill=col + (235,), outline=(255, 255, 255, 200), width=5)
        ttext(cd, (W / 2, 115), txt, f_black(fz), (255, 255, 255), "mm"); ttext(cd, (W / 2, 210), sub, f_semi(40), (255, 255, 255, 220), "mm")
        im.alpha_composite(fade(c, a), (0, int(y + (1 - a) * 40)))
    card(330, p["a"], p.get("asub", ""), (150, 40, 44), a1)
    if a2 > 0: ttext(d, (W / 2, 735), "или", f_bold(60), (220, 220, 230, int(255 * a2)), "mm")
    card(830, p["b"], p.get("bsub", ""), (36, 64, 128), a2)
    if a3 > 0:
        ttext(d, (W / 2, 1360), "РЕШАЙ", f_black(int(170 * (1 + 0.25 * (1 - a3)))), YEL + (int(255 * a3),), "mm")
        ttext(d, (W / 2, 1520), "ответ — в комментариях", f_semi(50), (230, 230, 240, int(255 * a3)), "mm")
        ttext(d, (W / 2, 1610), p.get("part", "Часть 1"), f_semi(44), SUB + (int(255 * a3),), "mm")
    return im

RENDER = {"lock": sc_lock, "wake": sc_wake, "chat": sc_chat, "pinned": sc_pinned, "call": sc_call, "doors": sc_doors, "door_open": sc_door_open,
          "room": sc_room, "knock": sc_knock, "window": sc_window, "choice": sc_choice}

# ---------------- captions ----------------
def groups(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or sum(len(x[2]) for x in cur) > 17 or re.search(r"[.,!?:;»]$", w[2]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CAPC = {}
def caption(g, nshow):
    key = (id(g), nshow)
    if key in CAPC: return CAPC[key]
    toks = [re.sub(r"[^\wёЁ\-]", "", w[2]) for w in g]; d = ImageDraw.Draw(Image.new("RGB", (1, 1))); lines, cur = [], []
    for x in toks:
        if cur and d.textlength(" ".join(cur + [x]).upper(), font=CAP) > 980: lines.append(cur); cur = []
        cur.append(x)
    lines.append(cur); im = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); i = 0
    for li, ln in enumerate(lines):
        tw = sum(dd.textlength(x.upper(), font=CAP) for x in ln) + 26 * (len(ln) - 1); x = (W - tw) / 2; y = 30 + li * 104
        for wd in ln:
            lw = wd.lower(); col = REDC if lw in RED else YEL if lw in YELLOW else (255, 255, 255)
            if i < nshow: dd.text((x, y), wd.upper(), font=CAP, fill=col, stroke_width=11, stroke_fill=(0, 0, 0))
            x += dd.textlength(wd.upper(), font=CAP) + 26; i += 1
    CAPC[key] = im; return im

# ---------------- audio ----------------
def build_audio(path):
    N = int(TOTAL * SR); voice = np.zeros(N, np.float32); fx = np.zeros(N, np.float32); x = np.arange(N) / SR
    for r in rows: i = int(r["t0"] * SR); voice[i:i + len(r["a"])] += r["a"][:N - i]
    voice *= 0.92 / (np.abs(voice).max() + 1e-6)
    def add(sig, at, v=1.0):
        i = int(at * SR); j = min(N, i + len(sig))
        if 0 <= i < N: fx[i:j] += sig[:j - i] * v
    def ping(at):
        tt = np.arange(int(0.35 * SR)) / SR; add((np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 14) + 0.6 * np.sin(2 * np.pi * 1980 * tt) * np.exp(-tt * 18) * (tt > 0.07)).astype(np.float32), at, 0.16)
    def knock(at):
        tt = np.arange(int(0.25 * SR)) / SR; s = np.sin(2 * np.pi * 95 * tt * (1 - tt)) * np.exp(-tt * 22)
        add((s + np.convolve(rng.standard_normal(len(tt)), np.ones(24) / 24, "same") * np.exp(-tt * 60) * 1.5).astype(np.float32), at, 0.8)
    def glass(at):
        tt = np.arange(int(0.2 * SR)) / SR; add((np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 40) + 0.5 * np.sin(2 * np.pi * 1250 * tt) * np.exp(-tt * 50)).astype(np.float32), at, 0.6)
    def boom(at, v=0.55):
        tt = np.arange(int(2.5 * SR)) / SR; add((np.sin(2 * np.pi * (42 + 30 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 1.6)).astype(np.float32), at, v)
    def ring(t0, t1):
        tt = np.arange(int(1.0 * SR)) / SR; s = ((np.sin(2 * np.pi * 880 * tt) + np.sin(2 * np.pi * 1100 * tt)) * (tt < 0.8) * (np.sin(2 * np.pi * 20 * tt) > 0)).astype(np.float32)
        a = t0
        while a < t1 - 0.3: add(s[:int(min(1.0, t1 - a) * SR)], a, 0.07); a += 2.0
    hs = None
    for r in rows:
        p, k = r["par"], r["kind"]
        if k == "lock" and p.get("text"): ping(wt(r, p["at"]) if has(p.get("at", -1)) else r["t0"])
        if k == "chat":
            for m in p["msgs"]:
                if has(m.get("at", -1)): ping(wt(r, m["at"]))
        if k == "pinned":
            for ru in p["rules"]:
                if has(ru.get("at", -1)): ping(wt(r, ru["at"]))
        if k == "wake": boom(wt(r, p["on"]), 0.4); ping(wt(r, p["on"]) + 0.1)
        if k == "call": ring(r["t0"], wt(r, p["accept"]) if "accept" in p else r["t1"])
        if k in ("knock", "window"):
            for ki in p.get("knocks", []): (knock if k == "knock" else glass)(wt(r, ki))
            if p.get("notif"): ping(wt(r, p["notif"]["at"]))
        if k == "window" and p.get("at") is not None: boom(wt(r, p["at"]), 0.35)
        if k == "door_open": boom(r["t0"], 0.35)
        if k == "choice": boom(r["words"][-1][0], 0.7)
        if k == "room" and p.get("scared") and hs is None: hs = r["t0"]
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * x)
    dr = (np.sin(2 * np.pi * 55 * x) + np.sin(2 * np.pi * 55.35 * x) + 0.5 * np.sin(2 * np.pi * 82.6 * x) + 0.25 * np.sin(2 * np.pi * 116.6 * x + np.sin(x * 0.7))) * lfo
    wind = rng.standard_normal(N).astype(np.float32)
    for _ in range(3): wind = np.convolve(wind, np.ones(64) / 64, "same")
    wind *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * x + 1)) * 6
    hb = np.zeros(N, np.float32); he = next((r["t0"] for r in rows if r["kind"] == "choice"), TOTAL)
    tt = np.arange(int(0.18 * SR)) / SR; thump = (np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 25)).astype(np.float32); bt = hs if hs is not None else he
    while bt < he:
        for off, v in ((0, 1.0), (0.22, 0.7)):
            i = int((bt + off) * SR); j = min(N, i + len(thump)); hb[i:j] += thump[:j - i] * v
        bt += 0.78
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, "same"); duck = 1 - 0.45 * np.clip(env / 0.08, 0, 1)
    bed = (dr * 0.05 + wind * 0.03) * (0.7 + 0.6 * x / TOTAL) * duck + hb * 0.45
    mix = np.tanh((voice + bed * np.clip((TOTAL - x) / 1.5, 0, 1) * np.clip(x / 0.6, 0, 1) + fx) * 1.05) * 0.95
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

def frame(t, caps):
    r = next((x for x in rows if x["t0"] <= t < x["t1"]), rows[0] if t < rows[0]["t0"] else rows[-1])
    im = RENDER[r["kind"]](r, max(t, r["t0"]))
    if im.mode != "RGBA": im = im.convert("RGBA")
    for c0, c1, g in caps:
        if c0 <= t < c1:
            cap = caption(g, sum(1 for w in g if w[0] <= t + 0.03)); pop = appear(t, c0, 0.12)
            if pop < 1: cap = cap.resize((W, int(260 * (0.9 + 0.1 * pop))), Image.BILINEAR)
            im.alpha_composite(cap, (0, 1300)); break
    if t < rows[0]["t0"] + 0.15: im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / (rows[0]["t0"] + 0.15))))))
    return im

def captions():
    caps = []
    for r in rows:
        if r["kind"] == "choice": continue
        gs = groups(r["words"])
        for gi, g in enumerate(gs): caps.append((g[0][0], gs[gi + 1][0][0] if gi + 1 < len(gs) else min(g[-1][1] + 0.5, r["t1"]), g))
    return caps

if MODE == "stills":
    os.makedirs(f"{DIR}/stills", exist_ok=True); caps = captions(); ims = []
    for r in rows:
        tt = r["t1"] - 0.25
        if r["par"].get("knocks"): tt = wt(r, r["par"]["knocks"][0]) + 0.1
        ims.append(frame(tt, caps).convert("RGB").resize((270, 480)))
    cols = 8; sheet = Image.new("RGB", (270 * cols, 480 * math.ceil(len(ims) / cols)))
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
    sheet.save(f"{DIR}/stills/sheet.jpg"); print("stills", f"{DIR}/stills/sheet.jpg", round(TOTAL, 1), "s")
elif MODE == "build":
    out = f"{DIR}/{NAME}.mp4"; build_audio(f"{DIR}/mix.wav"); caps = captions()
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", f"{DIR}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fi in range(int(TOTAL * FPS)): ff.stdin.write(frame(fi / FPS, caps).convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print("done", out, round(TOTAL, 1), "s")
