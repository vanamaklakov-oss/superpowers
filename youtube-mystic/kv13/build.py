"""«Квартира 13» — вертикальная страшилка в стиле «экран телефона + плоские мультяшные персонажи».
Всё рисуется кодом (PIL): экраны чата/блокировки, подъезд, дверь, герой. Озвучка vo/NN.mp3 (+.json с таймингами слов),
субтитры по 2–3 слова с подсветкой, свой эмбиент, стук, уведомления.  python3 build.py [out.mp4]"""
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script import SCENES, YELLOW, RED

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/kv13_part1.mp4"
W, H, FPS, SR, GAP = 1080, 1920, 30, 48000, 0.25
FD = "/usr/share/fonts/opentype/inter"
def F(name, size): return ImageFont.truetype(f"{FD}/{name}.otf", size)
f_reg, f_semi, f_bold = (lambda s: F("Inter-Regular", s)), (lambda s: F("Inter-SemiBold", s)), (lambda s: F("Inter-Bold", s))
f_black = lambda s: F("InterDisplay-Black", s)
CAP = f_black(88)

BG = (20, 24, 44); SCR = (23, 29, 43); BUB = (37, 45, 63); TXT = (236, 239, 246); SUB = (138, 148, 170)
BLUE = (96, 146, 236); REDC = (236, 78, 78); YEL = (255, 225, 0); OUTL = (24, 22, 30)
rng = np.random.default_rng(13)

# ---------------- timeline ----------------
def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR

rows, t = [], 0.35
for n, text, kind, par in SCENES:
    a, lead = trim(pcm(f"{HERE}/vo/{n:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{n:02d}.mp3.json"))
    words = [(t + w["s"] - lead, t + w["s"] - lead + w["d"], w["w"]) for w in meta["words"]]
    extra = 0.5 if kind in ("knock", "wake") else 0.0
    rows.append({"n": n, "kind": kind, "par": par, "t0": t, "a": a, "words": words}); t += len(a) / SR + GAP + extra
TOTAL = t + 2.2
for i, r in enumerate(rows): r["t1"] = rows[i + 1]["t0"] if i + 1 < len(rows) else TOTAL
def wt(r, i):  # time a word index starts (-1 → from scene start)
    return -1e9 if i is None or i < 0 else r["words"][min(i, len(r["words"]) - 1)][0]

# ---------------- drawing helpers ----------------
def ss(w, h, fn, k=3):
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), k)
    return im.resize((w, h), Image.LANCZOS)

def face(d, k, cx, cy, r, skin=(233, 196, 160), hair=None, style="", eyes="open", px=0, brow=0, mouth="line", lw=5):
    S = lambda v: int(v * k); o = OUTL; L = S(lw)
    if style == "long":
        d.rounded_rectangle([S(cx - r * 1.08), S(cy - r * 0.9), S(cx + r * 1.08), S(cy + r * 1.25)], S(r * 0.6), fill=hair, outline=o, width=L)
    if style == "bun":
        d.ellipse([S(cx - r * 0.45), S(cy - r * 1.55), S(cx + r * 0.45), S(cy - r * 0.7)], fill=hair, outline=o, width=L)
    d.ellipse([S(cx - r * 1.08), S(cy - r * 0.2), S(cx - r * 0.82), S(cy + r * 0.25)], fill=skin, outline=o, width=L)
    d.ellipse([S(cx + r * 0.82), S(cy - r * 0.2), S(cx + r * 1.08), S(cy + r * 0.25)], fill=skin, outline=o, width=L)
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=skin, outline=o, width=L)
    if hair is not None and style != "bald":
        d.chord([S(cx - r * 1.02), S(cy - r * 1.06), S(cx + r * 1.02), S(cy + r * 0.5)], 180, 360, fill=hair, outline=o, width=L)
        if style in ("boy", ""):
            for j in range(5):
                x0 = cx - r * 0.9 + j * r * 0.38
                d.polygon([(S(x0), S(cy - r * 0.32)), (S(x0 + r * 0.42), S(cy - r * 0.32)), (S(x0 + r * 0.3), S(cy - r * 0.05))], fill=hair)
    if style == "bun" or style == "bald":
        pass
    ex, ey, er = r * 0.38, cy - r * 0.02, r * (0.27 if eyes != "scared" else 0.31)
    for sx in (-1, 1):
        x = cx + sx * ex
        if eyes == "closed":
            d.line([S(x - er), S(ey), S(x + er), S(ey)], fill=o, width=L)
        else:
            d.ellipse([S(x - er), S(ey - er), S(x + er), S(ey + er)], fill=(250, 250, 250), outline=o, width=L)
            pr = er * (0.45 if eyes == "open" else 0.26)
            d.ellipse([S(x + px * er * 0.4 - pr), S(ey - pr), S(x + px * er * 0.4 + pr), S(ey + pr)], fill=o)
        by = ey - er - r * (0.1 + 0.08 * brow)
        d.line([S(x - er * 0.9), S(by + sx * r * 0.03 * (brow - 0.5) * -1), S(x + er * 0.9), S(by - sx * r * 0.03 * (brow - 0.5) * -1)], fill=o, width=L)
    if style == "bald":
        d.line([S(cx - r * 0.35), S(cy + r * 0.42), S(cx + r * 0.35), S(cy + r * 0.42)], fill=(80, 70, 70), width=S(r * 0.12))
    if style == "bun":
        for sx in (-1, 1):
            x = cx + sx * ex; d.ellipse([S(x - er * 1.25), S(ey - er * 1.25), S(x + er * 1.25), S(ey + er * 1.25)], outline=o, width=L)
    if mouth == "line":
        d.arc([S(cx - r * 0.18), S(cy + r * 0.38), S(cx + r * 0.18), S(cy + r * 0.62)], 20, 160, fill=o, width=L)
    elif mouth == "o":
        d.ellipse([S(cx - r * 0.09), S(cy + r * 0.45), S(cx + r * 0.09), S(cy + r * 0.66)], fill=(70, 30, 35), outline=o, width=L)

def avatar(kind, D):
    def fn(d, k):
        S = lambda v: int(v * k); r = D / 2
        if kind == "13":
            d.ellipse([0, 0, S(D) - 1, S(D) - 1], fill=(36, 34, 40))
            f = f_black(S(D * 0.42)); d.text((S(r), S(r)), "13", font=f, fill=(205, 60, 60), anchor="mm")
        elif kind == "group":
            d.ellipse([0, 0, S(D) - 1, S(D) - 1], fill=(70, 108, 196))
            d.text((S(r), S(r)), "7", font=f_bold(S(D * 0.48)), fill=(255, 255, 255), anchor="mm")
        else:
            bgc = {"kolya": (92, 122, 170), "tamara": (150, 108, 172), "mom": (205, 112, 118)}[kind]
            d.ellipse([0, 0, S(D) - 1, S(D) - 1], fill=bgc)
            st = {"kolya": "bald", "tamara": "bun", "mom": "long"}[kind]
            hair = {"kolya": None, "tamara": (190, 190, 200), "mom": (110, 66, 44)}[kind]
            face(d, k, r, r * 1.08, r * 0.56, hair=hair, style=st, lw=max(1.2, D / 40))
    im = ss(D, D, fn, 4); m = Image.new("L", (D * 4, D * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (D, D), 0), m.resize((D, D), Image.LANCZOS))); return im

def boy(eyes="open", px=0, scared=False):
    w, h = 820, 1300
    def fn(d, k):
        S = lambda v: int(v * k); o = OUTL; L = S(6)
        hood = (214, 128, 58)
        d.rounded_rectangle([S(90), S(700), S(730), S(h + 200)], S(200), fill=hood, outline=o, width=L)
        d.line([S(410), S(760), S(410), S(h)], fill=o, width=L)
        d.line([S(360), S(720), S(345), S(860)], fill=(240, 236, 226), width=S(8)); d.line([S(460), S(720), S(475), S(860)], fill=(240, 236, 226), width=S(8))
        d.rectangle([S(350), S(600), S(470), S(720)], fill=(226, 180, 140)); d.line([S(350), S(600), S(350), S(712)], fill=o, width=L); d.line([S(470), S(600), S(470), S(712)], fill=o, width=L)
        face(d, k, 410, 400, 250, skin=(226, 182, 142), hair=(86, 58, 40), style="boy",
             eyes=("scared" if scared and eyes != "closed" else eyes), px=px, brow=(1.6 if scared else 0.4), mouth=("o" if scared else "line"), lw=6)
    return ss(w, h, fn, 2)

def grad(c0, c1, w=W, h=H):
    a = np.linspace(0, 1, h)[:, None, None]; arr = (np.array(c0) * (1 - a) + np.array(c1) * a).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, 1), "RGB").convert("RGBA")

def ttext(d, xy, s, font, fill, anchor="la"): d.text(xy, s, font=font, fill=fill, anchor=anchor)

# ---------------- phone frame ----------------
PX0, PY0, PX1, PY1 = 34, 40, W - 34, H - 40
def phone_base(clock="03:13", bright=1.0):
    im = grad((26, 32, 64), (14, 16, 30)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX0, PY0, PX1, PY1], 96, fill=(8, 9, 14)); d.rounded_rectangle([PX0 + 14, PY0 + 14, PX1 - 14, PY1 - 14], 84, fill=SCR)
    d.rounded_rectangle([W // 2 - 70, PY0 + 34, W // 2 + 70, PY0 + 74], 20, fill=(4, 4, 6))
    ttext(d, (120, PY0 + 40), clock, f_semi(36), TXT)
    for j in range(4): d.rectangle([W - 250 + j * 14, PY0 + 70 - 10 - j * 7, W - 241 + j * 14, PY0 + 70], fill=TXT)
    d.rounded_rectangle([W - 180, PY0 + 46, W - 120, PY0 + 72], 7, outline=TXT, width=3); d.rectangle([W - 175, PY0 + 51, W - 140, PY0 + 67], fill=TXT)
    return im

def header(im, title, sub, av, subcol=SUB):
    d = ImageDraw.Draw(im); d.rectangle([PX0 + 14, 150, PX1 - 14, 300], fill=(28, 35, 52))
    ttext(d, (95, 225), "‹", f_reg(80), BLUE, "lm")
    im.alpha_composite(avatar(av, 104), (150, 173)); ttext(d, (278, 205), title, f_bold(44), TXT, "lm"); ttext(d, (278, 255), sub, f_reg(32), subcol, "lm")

def pill(d, y, s):
    f = f_semi(28); w = d.textlength(s, font=f) + 44
    d.rounded_rectangle([W / 2 - w / 2, y, W / 2 + w / 2, y + 46], 23, fill=(40, 50, 72)); ttext(d, (W / 2, y + 23), s, f, (200, 208, 224), "mm")
    return y + 70

def msg(im, y, av, name, namecol, text, tm, tmcol=SUB, alpha=1.0, slide=0):
    d0 = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(d0)
    ft, fn = f_reg(42), f_semi(32); tw = d.textlength(text, font=ft)
    bw = max(tw, d.textlength(name, font=fn)) + 190; x0 = 190
    d.rounded_rectangle([x0, y, x0 + bw, y + 140], 34, fill=BUB)
    ttext(d, (x0 + 34, y + 22), name, fn, namecol); ttext(d, (x0 + 34, y + 66), text, ft, TXT)
    ttext(d, (x0 + bw - 28, y + 112), tm, f_semi(26), tmcol, "rm")
    d0.alpha_composite(avatar(av, 92), (82, y + 46))
    if slide: d0 = d0.transform(d0.size, Image.AFFINE, (1, 0, 0, 0, 1, -slide))
    if alpha < 1: d0.putalpha(d0.getchannel("A").point(lambda v: int(v * alpha)))
    im.alpha_composite(d0); return y + 170

def appear(t, t0, dur=0.25): return max(0.0, min(1.0, (t - t0) / dur))

# ---------------- caption ----------------
def groups(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or sum(len(x[2]) for x in cur) > 17 or re.search(r"[.,!?:;]$", w[2]) or (len(cur) == 2 and len(w[2]) > 7): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CAPCACHE = {}
def caption(g, nshow):
    key = (id(g), nshow)
    if key in CAPCACHE: return CAPCACHE[key]
    toks = [re.sub(r"[^\wёЁ\-]", "", w[2]) for w in g]; d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines, cur = [], []
    for x in toks:
        if cur and d.textlength(" ".join(cur + [x]).upper(), font=CAP) > 980: lines.append(cur); cur = []
        cur.append(x)
    lines.append(cur)
    im = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); i = 0
    for li, ln in enumerate(lines):
        tw = sum(dd.textlength(x.upper(), font=CAP) for x in ln) + 26 * (len(ln) - 1); x = (W - tw) / 2; y = 30 + li * 104
        for wd in ln:
            lw = wd.lower(); col = REDC if lw in RED else YEL if lw in YELLOW else (255, 255, 255)
            if i < nshow: dd.text((x, y), wd.upper(), font=CAP, fill=col, stroke_width=11, stroke_fill=(0, 0, 0))
            x += dd.textlength(wd.upper(), font=CAP) + 26; i += 1
    CAPCACHE[key] = im; return im

# ---------------- scenes ----------------
CACHE = {}
def cached(key, fn):
    if key not in CACHE: CACHE[key] = fn()
    return CACHE[key]

def lock_screen(notif_a=1.0, slide=0.0, bright=1.0):
    def base():
        im = phone_base(); d = ImageDraw.Draw(im)
        d.rectangle([PX0 + 14, 140, PX1 - 14, PY1 - 100], fill=SCR)
        im2 = grad((30, 38, 78), (16, 18, 36), PX1 - PX0 - 28, PY1 - PY0 - 200); im.alpha_composite(im2, (PX0 + 14, PY0 + 110))
        ttext(d, (W / 2, 330), "среда, 18 ноября", f_semi(46), (210, 216, 236), "mm")
        ttext(d, (W / 2, 470), "03:13", f_black(230), (240, 242, 250), "mm"); return im
    im = cached("lock", base).copy()
    if notif_a > 0:
        c = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle([90, 0, W - 90, 210], 40, fill=(48, 56, 82, 235)); c.alpha_composite(avatar("13", 110), (125, 50))
        ttext(d, (265, 34), "Дом 7 · подъезд 2", f_semi(30), (176, 186, 208)); ttext(d, (W - 130, 34), "сейчас", f_reg(28), (176, 186, 208), "ra")
        ttext(d, (265, 80), "кв. 13", f_bold(40), TXT); ttext(d, (265, 132), "Соседи, кто не спит?", f_reg(40), TXT)
        c.putalpha(c.getchannel("A").point(lambda v: int(v * notif_a))); im.alpha_composite(c, (0, int(640 - slide)))
    if bright < 1:
        dark = Image.new("RGBA", im.size, (0, 0, 0, int(255 * (1 - bright)))); im.alpha_composite(dark)
    return im

def scene_lock(r, t):
    tn = wt(r, r["par"]["notif"]); a = appear(t, tn, 0.3)
    return lock_screen(a, (1 - a) * 60)

def scene_wake(r, t):
    ton = wt(r, r["par"]["on"]); b = appear(t, ton, 0.35)
    if t < ton:
        im = phone_base(); ImageDraw.Draw(im).rounded_rectangle([PX0 + 14, PY0 + 14, PX1 - 14, PY1 - 14], 84, fill=(4, 5, 8)); return im
    return lock_screen(1.0, 0, 0.15 + 0.85 * b)

CHAT_DAYS = [("16 ноября", "03:13"), ("17 ноября", "03:13"), ("18 ноября", "03:13")]
def scene_chat(r, t):
    im = cached("chatbase", lambda: (lambda b: (header(b, "Дом 7 · подъезд 2", "48 участников", "group"), b)[1])(phone_base("16:40"))).copy()
    d = ImageDraw.Draw(im); y = 340; p = r["par"]
    for i, ti in enumerate(p["msgs"]):
        a = appear(t, wt(r, ti))
        if a <= 0: break
        y = pill(d, y, CHAT_DAYS[i][0]); y = msg(im, y, "13", "кв. 13", (210, 80, 80), "Соседи, кто не спит?", "03:13", REDC, a, (1 - a) * 30)
    if "reply" in p:
        a = appear(t, wt(r, p["reply"]))
        if a > 0: msg(im, y, "kolya", "Николай, кв. 10", (110, 170, 240), "Я не сплю", "03:14", SUB, a, (1 - a) * 30)
    return im

def scene_chat2(r, t):
    tm = wt(r, r["par"]["m2"]); typing = tm - 1.6 < t < tm
    im = phone_base("03:13"); header(im, "Дом 7 · подъезд 2", "кв. 13 печатает…" if typing else "48 участников", "group", REDC if typing else SUB)
    d = ImageDraw.Draw(im); y = pill(d, 340, "Сегодня"); y = msg(im, y, "13", "кв. 13", (210, 80, 80), "Соседи, кто не спит?", "03:13", REDC)
    a = appear(t, tm)
    if a > 0: msg(im, y, "13", "кв. 13", (210, 80, 80), "Максим, ты же не спишь.", "03:14", REDC, a, (1 - a) * 30)
    return im

RULES = [("Тринадцатой не отвечай", None), ("Ночью постучат — в глазок не смотри", None), ("Никому не открывай", "Даже своим")]
def scene_pinned(r, t):
    def base():
        im = phone_base("16:41"); d = ImageDraw.Draw(im); d.rectangle([PX0 + 14, 150, PX1 - 14, 300], fill=(28, 35, 52))
        ttext(d, (95, 225), "‹", f_reg(80), BLUE, "lm"); ttext(d, (150, 200), "Закреплённые", f_bold(46), TXT, "lm"); ttext(d, (150, 252), "Дом 7 · подъезд 2", f_reg(32), SUB, "lm")
        d.rounded_rectangle([70, 340, W - 70, 1120], 36, fill=BUB); im.alpha_composite(avatar("tamara", 96), (100, 370))
        ttext(d, (220, 395), "Тамара Петровна", f_bold(40), (120, 200, 140)); ttext(d, (220, 445), "старшая по дому", f_reg(30), SUB)
        return im
    im = cached("pinbase", base).copy(); y = 540
    for i, ti in enumerate(r["par"]["rules"]):
        a = appear(t, wt(r, ti), 0.3)
        if a > 0:
            c = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
            d.ellipse([110, 6, 166, 62], fill=(60, 74, 104)); ttext(d, (138, 34), str(i + 1), f_bold(34), TXT, "mm")
            words = RULES[i][0]; fz = f_semi(42)
            if d.textlength(words, font=fz) > 760:
                p1, p2 = words.split(" — "); ttext(d, (195, 8), p1 + " —", fz, TXT); ttext(d, (195, 64), p2, fz, TXT); hh = 120
            else: ttext(d, (195, 8), words, fz, TXT); hh = 70
            if RULES[i][1]: ttext(d, (195, hh), RULES[i][1], f_bold(40), REDC); hh += 60
            c.putalpha(c.getchannel("A").point(lambda v: int(v * a))); im.alpha_composite(c, (int((1 - a) * 40), y))
        y += [110, 170, 170][i]
    return im

def zoom(im, s, cx=0.5, cy=0.5):
    s = max(1.0, s); w, h = W / s, H / s; x0, y0 = (W - w) * cx, (H - h) * cy
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))

def stairs_base():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 760], fill=(118, 122, 112)); d.rectangle([0, 760, W, 1560], fill=(46, 84, 70)); d.rectangle([0, 752, W, 768], fill=(34, 60, 50))
    for y in range(1560, H, 60):
        for x in range(-((y // 60) % 2) * 60, W, 120): d.rectangle([x, y, x + 58, y + 58], fill=(74, 62, 56) if (x // 60) % 2 else (62, 52, 48))
    for x0, num in ((70, "12"), (720, "14")):
        d.rectangle([x0 - 16, 560, x0 + 306, 1580], fill=(36, 30, 28)); d.rectangle([x0, 576, x0 + 290, 1580], fill=(104, 64, 42), outline=OUTL, width=6)
        d.rectangle([x0 + 30, 620, x0 + 260, 1000], outline=(80, 48, 30), width=6); d.rectangle([x0 + 30, 1080, x0 + 260, 1500], outline=(80, 48, 30), width=6)
        d.rounded_rectangle([x0 + 236, 1050, x0 + 276, 1072], 8, fill=(200, 190, 150), outline=OUTL, width=3)
        d.ellipse([x0 + 100, 440, x0 + 190, 520], fill=(225, 222, 210), outline=OUTL, width=5); ttext(d, (x0 + 145, 480), num, f_black(46), (40, 40, 40), "mm")
    d.line([W / 2, 0, W / 2, 110], fill=(20, 20, 20), width=5)
    return im

def scene_stairs(r, t):
    lt = t - r["t0"]; im = cached("stairs", stairs_base).copy()
    ghost = 0.5 + 0.5 * math.sin(lt * 1.7 - 1.5); g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    al = int(70 * ghost * appear(lt, 2.0, 1.5))
    d.rectangle([400, 576, 680, 1580], outline=(200, 200, 210, al), width=5)
    d.ellipse([495, 440, 585, 520], outline=(220, 70, 70, al), width=5); ttext(d, (540, 480), "13", f_black(46), (220, 70, 70, al), "mm")
    im.alpha_composite(g)
    fl = 1.0 if (int(lt * 9) * 7919) % 13 else 0.35
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([W / 2 - 520, -380, W / 2 + 520, 640], fill=(255, 230, 160, int(70 * fl))); glow = glow.filter(ImageFilter.GaussianBlur(90))
    im.alpha_composite(glow); d = ImageDraw.Draw(im); d.ellipse([W / 2 - 34, 100, W / 2 + 34, 168], fill=(255, 238, 190) if fl > 0.5 else (120, 110, 90))
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    return zoom(im, 1.0 + 0.07 * (lt / (r["t1"] - r["t0"])), 0.5, 0.45)

def door_open_base():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 760], fill=(110, 114, 104)); d.rectangle([0, 760, W, 1600], fill=(42, 78, 64)); d.rectangle([0, 1600, W, H], fill=(64, 54, 50))
    d.rectangle([250, 500, 760, 1610], fill=(30, 26, 24)); d.rectangle([270, 520, 740, 1610], fill=(3, 3, 5))
    d.polygon([(740, 520), (930, 440), (930, 1700), (740, 1610)], fill=(104, 64, 42), outline=OUTL)
    d.line([(740, 520), (930, 440), (930, 1700), (740, 1610), (740, 520)], fill=OUTL, width=6)
    d.ellipse([820, 600, 880, 660], fill=(225, 222, 210), outline=OUTL, width=4); ttext(d, (850, 630), "10", f_black(30), (40, 40, 40), "mm")
    d.polygon([(270, 1610), (740, 1610), (900, H), (120, H)], fill=(0, 0, 0, 90))
    return im

def scene_door_open(r, t):
    lt = t - r["t0"]; im = cached("dopen", door_open_base).copy(); p = lt / (r["t1"] - r["t0"])
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60)))
    return zoom(im, 1.0 + 0.16 * p, 0.45, 0.5)

def room_base(scared):
    def mk():
        im = grad((38, 36, 78), (22, 20, 46)) if not scared else grad((58, 26, 40), (24, 14, 24)); d = ImageDraw.Draw(im)
        d.rectangle([600, 210, 960, 700], fill=(16, 20, 48), outline=OUTL, width=10); d.line([780, 210, 780, 700], fill=OUTL, width=10); d.line([600, 455, 960, 455], fill=OUTL, width=10)
        d.ellipse([820, 260, 910, 350], fill=(232, 226, 196)); d.ellipse([845, 248, 930, 338], fill=(16, 20, 48))
        d.rounded_rectangle([110, 260, 380, 380], 18, fill=(14, 14, 18), outline=OUTL, width=6)
        ttext(d, (245, 322), "03:12" if not scared else "03:15", f_black(78), (255, 70, 60), "mm")
        if scared:
            d.polygon([(130, 520), (420, 500), (440, 760), (150, 780)], fill=(250, 220, 90)); d.line([(270, 500), (275, 530)], fill=(200, 60, 60), width=10)
            n = Image.new("RGBA", (300, 200), (0, 0, 0, 0)); nd = ImageDraw.Draw(n)
            ttext(nd, (150, 60), "Смена до 8:00", f_bold(38), (60, 40, 30), "mm"); ttext(nd, (150, 125), "мама", f_semi(34), (60, 40, 30), "mm")
            n = n.rotate(4, Image.BICUBIC, expand=False); im.alpha_composite(n, (135, 540))
        return im
    return mk

def scene_boy(r, t, scared=False):
    lt = t - r["t0"]; im = cached(f"room{scared}", room_base(scared)).copy()
    blink = (lt % 2.9) < 0.13; px = 0 if scared else (-1 if (lt % 4) < 2 else 0.6)
    b = cached(("boy", blink, px, scared), lambda: boy("closed" if blink else "open", px, scared))
    sh = int(4 * math.sin(lt * 40)) if scared else 0
    im.alpha_composite(b, ((W - b.width) // 2 + sh, H - b.height))
    if scared: im.alpha_composite(Image.new("RGBA", (W, H), (60, 0, 0, int(30 + 25 * math.sin(lt * 6)))))
    return zoom(im, 1.0 + 0.05 * lt / (r["t1"] - r["t0"]), 0.5, 0.6)

def knock_base():
    im = grad((52, 44, 64), (26, 22, 32)); d = ImageDraw.Draw(im)
    d.rectangle([0, 1690, W, H], fill=(58, 44, 36))
    for x in range(-200, W + 200, 140): d.line([x, 1690, x + 80, H], fill=(48, 36, 30), width=4)
    d.rectangle([250, 330, 830, 1700], fill=(30, 24, 26))
    return im
def door_leaf():
    def fn(d, k):
        S = lambda v: int(v * k); d.rectangle([0, 0, S(540), S(1360)], fill=(118, 54, 44), outline=OUTL, width=S(7))
        for yy in range(1, 9):
            for xx in range(1, 5):
                cx, cy = xx * 108, yy * 150
                d.line([S(cx - 54), S(cy), S(cx), S(cy - 75), S(cx + 54), S(cy), S(cx), S(cy + 75), S(cx - 54), S(cy)], fill=(92, 40, 34), width=S(4))
                d.ellipse([S(cx - 9), S(cy - 9), S(cx + 9), S(cy + 9)], fill=(200, 170, 110))
        d.ellipse([S(250), S(430), S(290), S(470)], fill=(170, 170, 176), outline=OUTL, width=S(5)); d.ellipse([S(262), S(442), S(278), S(458)], fill=(250, 240, 200))
        d.rounded_rectangle([S(440), S(700), S(520), S(730)], S(10), fill=(200, 190, 150), outline=OUTL, width=S(4))
        d.rectangle([S(458), S(770), S(500), S(830)], fill=(170, 160, 130), outline=OUTL, width=S(3))
    return ss(540, 1360, fn, 2)

TUK = {}
def scene_knock(r, t):
    lt = t - r["t0"]; im = cached("kbase", knock_base).copy(); p = r["par"]
    sh = 0.0; pops = []
    for ki in p["knocks"]:
        for j, tk in enumerate([wt(r, ki)]):
            dt = t - tk
            if 0 <= dt < 0.35: sh += 10 * math.exp(-dt * 12) * math.sin(dt * 90)
            if 0 <= dt < 0.9: pops.append((ki, dt))
    d = ImageDraw.Draw(im)
    d.rectangle([270, 1690, 810, 1704], fill=(255, 220, 150)); d.rectangle([450, 1690, 520, 1704], fill=(10, 8, 8)); d.rectangle([570, 1690, 640, 1704], fill=(10, 8, 8))
    gl = cached("kglow", lambda: (lambda g: (ImageDraw.Draw(g).rectangle([260, 1660, 820, 1730], fill=(255, 200, 120, 90)), g.filter(ImageFilter.GaussianBlur(30)))[1])(Image.new("RGBA", (W, H), (0, 0, 0, 0))))
    im.alpha_composite(gl)
    im.alpha_composite(cached("leaf", door_leaf), (270 + int(sh), 335))
    for ki, dt in pops:
        a = 1 - max(0, dt - 0.5) / 0.4; sc = min(1, 0.6 + dt * 4)
        f = f_black(int(150 * sc)); c = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
        ttext(ImageDraw.Draw(c), (W / 2 + [-170, 160, -60, 120, -140][ki % 5], 150), "ТУК", f, (255, 255, 255, int(255 * a)), "mm")
        im.alpha_composite(c, (0, 380 + (ki % 3) * 230))
    if "notif" in p:
        a = appear(t, wt(r, p["notif"]), 0.3)
        if a > 0:
            c = Image.new("RGBA", (W, 240), (0, 0, 0, 0)); d2 = ImageDraw.Draw(c)
            d2.rounded_rectangle([60, 10, W - 60, 220], 40, fill=(40, 46, 66, 245)); c.alpha_composite(avatar("mom", 110), (95, 60))
            ttext(d2, (235, 50), "Мама", f_bold(42), TXT); ttext(d2, (235, 110), "Почему ты не открываешь?", f_reg(40), TXT)
            ttext(d2, (W - 100, 50), "03:15", f_reg(30), SUB, "ra"); c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
            im.alpha_composite(c, (0, int(70 - (1 - a) * 80)))
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 40)))
    return zoom(im, 1.0 + 0.06 * lt / (r["t1"] - r["t0"]), 0.5, 0.35)

def scene_mom(r, t):
    tm = wt(r, r["par"]["m1"]); typing = t < tm
    im = phone_base("03:14"); header(im, "Мама", "печатает…" if typing else "в сети", "mom", BLUE if typing else SUB)
    d = ImageDraw.Draw(im); y = pill(d, 340, "Сегодня"); a = appear(t, tm)
    if a > 0:
        c = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); dd = ImageDraw.Draw(c)
        dd.rounded_rectangle([82, 0, 900, 200], 36, fill=BUB); ttext(dd, (120, 30), "Сынок, открой,", f_reg(46), TXT); ttext(dd, (120, 92), "я ключи забыла", f_reg(46), TXT)
        ttext(dd, (870, 168), "03:14", f_semi(26), SUB, "rm"); c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
        im.alpha_composite(c, (0, int(y + (1 - a) * 30)))
    return im

def scene_choice(r, t):
    im = grad((30, 16, 30), (8, 8, 14)); d = ImageDraw.Draw(im); w = r["words"]
    a1, a2, a3 = appear(t, w[0][0]), appear(t, w[3][0]), appear(t, w[-1][0], 0.2)
    def card(y, txt, sub, col, a):
        c = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle([80, 0, W - 80, 300], 44, fill=col + (235,), outline=(255, 255, 255, 200), width=5)
        ttext(cd, (W / 2, 115), txt, f_black(84), (255, 255, 255), "mm"); ttext(cd, (W / 2, 210), sub, f_semi(40), (255, 255, 255, 220), "mm")
        c.putalpha(c.getchannel("A").point(lambda v: int(v * a))); im.alpha_composite(c, (0, int(y + (1 - a) * 40)))
    card(330, "ОТКРЫТЬ", "это мама?", (150, 40, 44), a1)
    if a2 > 0: ttext(d, (W / 2, 735), "или", f_bold(60), (220, 220, 230, int(255 * a2)), "mm")
    card(830, "НЕ ОТКРЫВАТЬ", "верить правилам", (36, 64, 128), a2)
    if a3 > 0:
        s = 1 + 0.25 * (1 - a3); f = f_black(int(170 * s))
        ttext(d, (W / 2, 1360), "РЕШАЙ", f, YEL + (int(255 * a3),), "mm"); ttext(d, (W / 2, 1520), "ответ — в комментариях", f_semi(50), (230, 230, 240, int(255 * a3)), "mm")
        ttext(d, (W / 2, 1610), "Часть 1", f_semi(44), SUB + (int(255 * a3),), "mm")
    return im

RENDER = {"lock": scene_lock, "wake": scene_wake, "chat": scene_chat, "chat2": scene_chat2, "pinned": scene_pinned, "stairs": scene_stairs,
          "door_open": scene_door_open, "boy": scene_boy, "boy_scared": lambda r, t: scene_boy(r, t, True), "knock": scene_knock,
          "mom": scene_mom, "choice": scene_choice}

# ---------------- audio ----------------
def build_audio():
    N = int(TOTAL * SR); voice = np.zeros(N, np.float32); fx = np.zeros(N, np.float32); x = np.arange(N) / SR
    for r in rows:
        i = int(r["t0"] * SR); voice[i:i + len(r["a"])] += r["a"][:N - i]
    voice *= 0.92 / (np.abs(voice).max() + 1e-6)
    def add(sig, at, v=1.0):
        i = int(at * SR); j = min(N, i + len(sig))
        if 0 <= i < N: fx[i:j] += sig[:j - i] * v
    def ping(at):
        tt = np.arange(int(0.35 * SR)) / SR; s = np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 14) + 0.6 * np.sin(2 * np.pi * 1980 * tt) * np.exp(-tt * 18) * (tt > 0.07)
        add(s.astype(np.float32), at, 0.16)
    def knock(at):
        tt = np.arange(int(0.25 * SR)) / SR; s = np.sin(2 * np.pi * 95 * tt * (1 - tt)) * np.exp(-tt * 22)
        nz = np.convolve(rng.standard_normal(len(tt)), np.ones(24) / 24, "same") * np.exp(-tt * 60) * 1.5
        add((s + nz).astype(np.float32), at, 0.8)
    def boom(at, v=0.55):
        tt = np.arange(int(2.5 * SR)) / SR; s = np.sin(2 * np.pi * (42 + 30 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 1.6)
        add(s.astype(np.float32), at, v)
    for r in rows:
        p, k = r["par"], r["kind"]
        if k == "lock": ping(wt(r, p["notif"]))
        if k == "chat":
            for ti in p["msgs"]:
                if ti >= 0: ping(wt(r, ti))
            if "reply" in p: ping(wt(r, p["reply"]))
        if k == "chat2": ping(wt(r, p["m2"]))
        if k == "pinned":
            for ti in p["rules"]:
                if ti >= 0: ping(wt(r, ti))
        if k == "mom": ping(wt(r, p["m1"]))
        if k == "wake": boom(wt(r, p["on"]), 0.4); ping(wt(r, p["on"]) + 0.1)
        if k == "knock":
            for ki in p["knocks"]: knock(wt(r, ki))
            if "notif" in p: ping(wt(r, p["notif"]))
        if k == "door_open": boom(r["t0"], 0.35)
        if k == "choice": boom(r["words"][-1][0], 0.7)
    # drone: detuned low sines + slow-breathing wind, darker toward the end
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * x)
    dr = (np.sin(2 * np.pi * 55 * x) + np.sin(2 * np.pi * 55.35 * x) + 0.5 * np.sin(2 * np.pi * 82.6 * x) + 0.25 * np.sin(2 * np.pi * 116.6 * x + np.sin(x * 0.7))) * lfo
    wind = rng.standard_normal(N).astype(np.float32);
    for _ in range(3): wind = np.convolve(wind, np.ones(64) / 64, "same")
    wind *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * x + 1)) * 6
    ramp = 0.7 + 0.6 * (x / TOTAL)
    # heartbeat from the scared scene onward
    hb = np.zeros(N, np.float32); hs = next(r["t0"] for r in rows if r["kind"] == "boy_scared"); he = next(r["t0"] for r in rows if r["kind"] == "choice")
    tt = np.arange(int(0.18 * SR)) / SR; thump = (np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 25)).astype(np.float32); bt = hs
    while bt < he:
        for off, v in ((0, 1.0), (0.22, 0.7)):
            i = int((bt + off) * SR); j = min(N, i + len(thump)); hb[i:j] += thump[:j - i] * v
        bt += 0.78
    env = np.convolve(np.abs(voice), np.ones(2400) / 2400, "same"); duck = 1 - 0.45 * np.clip(env / 0.08, 0, 1)
    bed = (dr * 0.05 + wind * 0.03) * ramp * duck + hb * 0.45
    fade = np.clip((TOTAL - x) / 1.5, 0, 1) * np.clip(x / 0.6, 0, 1)
    mix = np.tanh((voice + bed * fade + fx) * 1.05) * 0.95
    import wave
    with wave.open(f"{HERE}/mix.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------------- video ----------------
def main():
    build_audio()
    caps = []
    for r in rows:
        if r["kind"] == "choice": continue
        gs = groups(r["words"])
        for gi, g in enumerate(gs):
            end = gs[gi + 1][0][0] if gi + 1 < len(gs) else min(g[-1][1] + 0.5, r["t1"])
            caps.append((g[0][0], end, g))
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", f"{HERE}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    nf = int(TOTAL * FPS)
    for fi in range(nf):
        t = fi / FPS; r = next(x for x in rows if x["t0"] <= t < x["t1"]) if t >= rows[0]["t0"] else rows[0]
        im = RENDER[r["kind"]](r, max(t, r["t0"]))
        if im.mode != "RGBA": im = im.convert("RGBA")
        for c0, c1, g in caps:
            if c0 <= t < c1:
                ns = sum(1 for w in g if w[0] <= t + 0.03)
                cap = caption(g, ns); pop = appear(t, c0, 0.12)
                if pop < 1: cap = cap.resize((W, int(260 * (0.9 + 0.1 * pop))), Image.BILINEAR)
                im.alpha_composite(cap, (0, 1300)); break
        if t < rows[0]["t0"] + 0.15: im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - (t / (rows[0]["t0"] + 0.15)))))))
        ff.stdin.write(im.convert("RGB").tobytes())
        if fi % 300 == 0: print(f"{fi}/{nf}", flush=True)
    ff.stdin.close(); ff.wait(); print("done", OUT, round(TOTAL, 1), "s")

if __name__ == "__main__":
    if "--stills" in sys.argv:
        os.makedirs(f"{HERE}/stills", exist_ok=True)
        for r in rows:
            tt = (r["t1"] - 0.2) if r["kind"] != "knock" else wt(r, r["par"]["knocks"][0]) + 0.1
            RENDER[r["kind"]](r, tt).convert("RGB").resize((360, 640)).save(f"{HERE}/stills/{r['n']:02d}.jpg")
    else: main()
