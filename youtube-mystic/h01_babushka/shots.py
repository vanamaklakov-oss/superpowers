# Планы для «Бабушки» (горизонталь 1920×1080). Подгружается toon.py через exec — доступны его хелперы.
BOYC, MOMC, DADC, GRC, PETC = (236, 132, 48), (150, 92, 186), (70, 128, 92), (128, 70, 64), (200, 64, 64)
PRESET = {
    "boy": dict(body=BOYC, hair="short", hcol=(92, 60, 36)),
    "mom": dict(body=MOMC, hair="long", hcol=(60, 36, 28)),
    "dad": dict(body=DADC, hair="short", hcol=(40, 30, 26), glasses=True),
    "granny": dict(body=GRC, hair="scarf", hcol=(206, 58, 58), glasses=True),
    "other": dict(body=GRC, hair="scarf", hcol=(150, 40, 40), eyes="void", mouth="grin"),
    "petka": dict(body=PETC, hair="short", hcol=(214, 170, 80)),
    "mom_x": dict(body=MOMC, hair="long", hcol=(60, 36, 28), eyes="none", mouth="none"),
    "dad_x": dict(body=DADC, hair="short", hcol=(40, 30, 26), eyes="none", mouth="none"),
}
LOG, LOGD = (138, 96, 60), (104, 70, 44)

def actor_sprite(a, lt):
    pr = dict(PRESET[a["who"]]); kw = {}
    for k, kk in (("e", "eyes"), ("m", "mouth"), ("a", "arms"), ("body", "body")):
        if k in a: pr[kk] = a[k]
    pr.setdefault("eyes", "dot"); pr.setdefault("mouth", "smile" if a["who"] in ("granny", "petka") else "line")
    legs = "stand"; arms = pr.pop("arms", a.get("a", "down"))
    if a.get("walk"): ph = int(lt * 6) % 2; legs = "run1" if ph else "run2"; arms = legs
    sp = bean(pr.pop("body"), pr.pop("eyes"), pr.pop("mouth"), arms, legs, sweat=a.get("sweat", False), flip=a.get("flip", False), s=a.get("s", 1.0), **pr)
    if a.get("tears"):
        sp = sp.copy(); d = ImageDraw.Draw(sp); sc = a.get("s", 1.0)
        for sx in (-1, 1):
            y0 = 140 * sc + (lt * 120 % 60) * sc; d.ellipse((170 * sc + sx * 32 * sc - 7, y0, 170 * sc + sx * 32 * sc + 7, y0 + 18), fill=(120, 190, 255))
    return sp

def draw_actors(im, actors, lt, D):
    for a in actors:
        if a.get("bed"): continue
        x = a["x"]
        if a.get("walk"): x0, x1 = a["walk"]; x = x0 + (x1 - x0) * ease(lt / max(D, 0.5))
        bob = math.sin(lt * 3 + x * 9) * 4
        put(im, actor_sprite(a, lt), x * W, a.get("y", 1000) + bob)

# ---------- фоны ----------
def logwall(im, y0=0, y1=None, col=LOG):
    d = ImageDraw.Draw(im); y1 = y1 or H
    for y in range(y0, y1, 64):
        d.rounded_rectangle((-20, y, W + 20, y + 60), 28, fill=col, outline=tuple(int(c * 0.6) for c in col), width=4)
        d.line((0, y + 18, W, y + 18), fill=tuple(min(255, int(c * 1.12)) for c in col), width=3)
def bg_flat(p):
    im = grad((214, 196, 168), (176, 156, 130)); d = ImageDraw.Draw(im)
    d.rectangle((0, 900, W, H), fill=(126, 88, 58)); [d.line((x, 900, x - 140, H), fill=(104, 72, 46), width=4) for x in range(0, W + 200, 160)]
    d.rounded_rectangle((1240, 150, 1660, 620), 16, fill=(150, 196, 230), outline=(240, 236, 226), width=22); d.line((1450, 150, 1450, 620), fill=(240, 236, 226), width=14)
    d.rectangle((1210, 600, 1690, 640), fill=(236, 230, 220))
    d.rounded_rectangle((120, 600, 1000, 900), 50, fill=(60, 120, 130), outline=INK, width=8); d.rounded_rectangle((160, 520, 960, 700), 50, fill=(70, 138, 148), outline=INK, width=8)
    d.rectangle((420, 180, 700, 380), fill=(230, 220, 200), outline=(90, 70, 50), width=14)
    return im
def bg_house(p):
    dawn = p.get("dawn"); im = grad((250, 170, 120), (140, 170, 210)) if dawn else grad((60, 40, 80), (220, 130, 90))
    d = ImageDraw.Draw(im)
    for i in range(14):  # лес
        x = i * 150 - 40; h = 260 + (i * 37) % 120; d.polygon((x, 760, x + 90, 760 - h, x + 180, 760), fill=(34, 54, 46) if not dawn else (60, 90, 70))
    d.rectangle((0, 760, W, H), fill=(70, 100, 56) if not dawn else (96, 140, 76))
    ruin = p.get("ruin")
    # изба
    d.rectangle((820, 360, 1540, 900), fill=LOG); [d.line((820, y, 1540, y), fill=LOGD, width=6) for y in range(380, 900, 46)]
    d.polygon((780, 380, 1180, 120, 1580, 380), fill=(84, 60, 50) if not ruin else (70, 60, 56), outline=INK); d.polygon((1080, 290, 1180, 200, 1280, 290), fill=(236, 220, 190))
    lit = not dawn and not ruin
    for wx in (900, 1300):
        d.rectangle((wx, 470, wx + 160, 640), fill=(255, 214, 110) if lit else (60, 70, 90), outline=(236, 224, 200), width=14)
        d.line((wx + 80, 470, wx + 80, 640), fill=(236, 224, 200), width=8)
        if ruin: d.polygon((wx + 20, 490, wx + 70, 560, wx + 30, 620), fill=(20, 24, 30))
    d.rectangle((1110, 520, 1240, 900), fill=(84, 54, 36), outline=INK, width=6); d.rectangle((1070, 880, 1280, 930), fill=(110, 80, 56), outline=INK, width=5)
    for x in range(0, 760, 46): d.rectangle((x, 740, x + 30, 900), fill=(116, 86, 60), outline=INK, width=3)
    d.rectangle((0, 790, 760, 806), fill=(100, 72, 50))
    if lit: im.alpha_composite(blob(600, 400, (255, 210, 120), 70, 60), (680, 360)); im.alpha_composite(blob(600, 400, (255, 210, 120), 70, 60), (1080, 360))
    if ruin:
        for i in range(30): x, y = 830 + (i * 97) % 700, 380 + (i * 53) % 500; d.line((x, y, x + 30, y + 40), fill=(70, 50, 34), width=3)
    return im
def bg_village(p):
    im = grad((70, 50, 90), (230, 140, 100)); d = ImageDraw.Draw(im)
    d.rectangle((0, 780, W, H), fill=(80, 96, 58)); d.polygon((700, H, 1220, H, 1000, 780, 940, 780), fill=(130, 110, 84))
    for i in range(10): x = 1500 + i * 60; h = 300 + (i * 41) % 140; d.polygon((x, 790, x + 60, 790 - h, x + 120, 790), fill=(30, 46, 40))
    for i, (x, sc) in enumerate(((60, 1.0), (430, 0.85), (1250, 0.7), (1560, 0.6))):
        w, h = 300 * sc, 230 * sc; y = 790 - h; dark = i < 3
        d.rectangle((x, y, x + w, 790), fill=(96, 72, 54) if dark else LOG); d.polygon((x - 20 * sc, y, x + w / 2, y - 140 * sc, x + w + 20 * sc, y), fill=(60, 46, 40))
        wx, wy = x + w * 0.3, y + h * 0.25; ww = w * 0.4
        d.rectangle((wx, wy, wx + ww, wy + ww * 0.8), fill=(30, 30, 36) if dark else (255, 214, 110))
        if dark: d.line((wx, wy, wx + ww, wy + ww * 0.8), fill=(150, 120, 90), width=8); d.line((wx + ww, wy, wx, wy + ww * 0.8), fill=(150, 120, 90), width=8)
        else: im.alpha_composite(blob(400, 300, (255, 210, 120), 90, 50), (int(wx - 150), int(wy - 120)))
    for x in range(0, W, 120): d.polygon((x, 900, x + 40, 840, x + 80, 900), fill=(100, 130, 70))
    return im
def bg_kitchen(p):
    ruin = p.get("ruin"); im = Image.new("RGBA", (W, H), LOG + (255,)); logwall(im, 0, 900, LOG if not ruin else (110, 96, 80)); d = ImageDraw.Draw(im)
    d.rectangle((0, 900, W, H), fill=(110, 76, 48))
    d.rounded_rectangle((60, 260, 520, 960), 30, fill=(236, 232, 222) if not ruin else (170, 166, 160), outline=INK, width=8); d.rounded_rectangle((170, 560, 410, 760), 60, fill=(30, 20, 16))
    if not ruin: im.alpha_composite(blob(300, 220, (255, 130, 40), 160, 30), (140, 560))
    d.rectangle((640, 640, 1420, 690), fill=(200, 60, 60) if not ruin else (120, 90, 80), outline=INK, width=6)
    for x in (680, 1360): d.rectangle((x, 690, x + 30, 940), fill=(100, 66, 40), outline=INK, width=5)
    if not ruin:
        d.rounded_rectangle((940, 480, 1100, 640), 40, fill=(214, 170, 60), outline=INK, width=6); d.polygon((990, 480, 1050, 480, 1020, 430), fill=(214, 170, 60), outline=INK)
        for x in (760, 1180, 1300): d.ellipse((x - 50, 620, x + 50, 650), fill=WHITE, outline=INK, width=4)
    if p.get("pies") or not ruin:
        for i in range(5): d.ellipse((960 + i * 26 - 30, 600 - (i % 2) * 14, 960 + i * 26 + 30, 640 - (i % 2) * 14), fill=(220, 150, 70), outline=INK, width=4)
    # часы
    d.ellipse((1100, 110, 1280, 290), fill=(240, 230, 210), outline=INK, width=8); cx, cy = 1190, 200
    if p.get("tick"): ang = -math.pi / 2 + (p.get("_lt", 0) * 2 * math.pi / 2)
    else: ang = -math.pi / 2 + 2 * math.pi * 55 / 60
    d.line((cx, cy, cx + 70 * math.cos(ang), cy + 70 * math.sin(ang)), fill=INK, width=8); d.line((cx, cy, cx + 45 * math.cos(-math.pi / 2 + 2 * math.pi * 2.9 / 12), cy + 45 * math.sin(-math.pi / 2 + 2 * math.pi * 2.9 / 12)), fill=INK, width=12)
    d.rectangle((1180, 290, 1200, 420), fill=(150, 120, 60)); d.ellipse((1160, 400, 1220, 460), fill=(200, 160, 60), outline=INK, width=4)
    # зеркало под тканью
    d.rectangle((1580, 160, 1800, 520), fill=(80, 70, 70), outline=INK, width=8); d.polygon((1560, 150, 1820, 150, 1840, 560, 1700, 520, 1540, 570), fill=(220, 214, 200), outline=INK)
    if ruin:
        for (x, y) in ((0, 0), (W, 0)):
            for r in range(40, 260, 50): d.arc((x - r, y - r, x + r, y + r), 0, 360, fill=(220, 220, 220), width=2)
            for a in range(0, 360, 30): d.line((x, y, x + 260 * math.cos(math.radians(a)), y + 260 * math.sin(math.radians(a))), fill=(220, 220, 220), width=2)
        im.alpha_composite(Image.new("RGBA", (W, H), (90, 90, 80, 70)))
    return im
def bg_bedroom(p):
    im = Image.new("RGBA", (W, H)); logwall(im, 0, 900); d = ImageDraw.Draw(im); d.rectangle((0, 900, W, H), fill=(100, 70, 46))
    d.rounded_rectangle((640, 160, 960, 480), 10, fill=(24, 34, 70), outline=(220, 210, 190), width=16); d.ellipse((800, 200, 880, 280), fill=(240, 240, 220)); d.line((800, 160, 800, 480), fill=(220, 210, 190), width=10)
    d.rectangle((120, 260, 420, 920), fill=(96, 62, 40), outline=INK, width=8); d.ellipse((370, 580, 400, 610), fill=(200, 170, 80))
    if p.get("door") == "light": d.rectangle((126, 912, 414, 924), fill=(255, 220, 140))
    d.rectangle((960, 640, 1740, 820), fill=(160, 110, 70), outline=INK, width=8); d.rectangle((940, 520, 990, 900), fill=(140, 96, 60), outline=INK, width=6)
    return im
def bg_door(p):
    im = Image.new("RGBA", (W, H)); logwall(im, 0, 940); d = ImageDraw.Draw(im); d.rectangle((0, 940, W, H), fill=(100, 70, 46))
    d.rectangle((640, 40, 1280, 950), fill=(104, 68, 44), outline=INK, width=12)
    for y in (120, 520): d.rectangle((700, y, 1220, y + 340), outline=(80, 52, 34), width=10)
    d.ellipse((1180, 520, 1230, 570), fill=(210, 170, 70), outline=INK, width=5)
    if p.get("door") in ("light", "feet"):
        d.rectangle((640, 950, 1280, 970), fill=(255, 220, 140)); im.alpha_composite(blob(900, 200, (255, 210, 120), 90, 40), (510, 880))
        if p["door"] == "feet": d.rectangle((860, 950, 930, 970), fill=(20, 14, 12)); d.rectangle((990, 950, 1060, 970), fill=(20, 14, 12))
    return im
def bg_fence(p):
    im = grad((140, 196, 240), (220, 236, 246)); d = ImageDraw.Draw(im); d.ellipse((1600, 60, 1780, 240), fill=(255, 230, 120))
    d.rectangle((0, 760, W, H), fill=(96, 150, 70)); d.rectangle((1100, 300, 1800, 800), fill=(150, 170, 200), outline=INK, width=8); d.polygon((1060, 300, 1450, 100, 1840, 300), fill=(170, 70, 60), outline=INK)
    d.rectangle((1300, 420, 1480, 600), fill=(220, 240, 250), outline=WHITE, width=12)
    for x in range(0, W, 70): d.rectangle((x, 640, x + 46, 920), fill=(200, 170, 110), outline=INK, width=4)
    d.rectangle((0, 700, W, 726), fill=(176, 146, 96)); d.rectangle((0, 840, W, 866), fill=(176, 146, 96))
    return im
BGS = {"flat": bg_flat, "house": bg_house, "village": bg_village, "kitchen": bg_kitchen, "bedroom": bg_bedroom, "door": bg_door, "fence": bg_fence}

def night(im, a=150, col=(10, 14, 40)): im.alpha_composite(Image.new("RGBA", (W, H), col + (a,)))
def bed_actor(im, a):
    d = ImageDraw.Draw(im); x = a["x"] * W
    if a.get("bed") == "hide":
        d.rounded_rectangle((x - 320, 560, x + 360, 700), 60, fill=(90, 120, 190), outline=INK, width=8); return
    sp = actor_sprite(a, 0).crop((0, 0, int(340 * a.get("s", 1)), int(260 * a.get("s", 1)))); im.alpha_composite(sp, (int(x - 440), 470))
    d.rounded_rectangle((x - 200, 600, x + 360, 700), 50, fill=(90, 120, 190), outline=INK, width=8)
    d.rounded_rectangle((x - 360, 590, x - 180, 660), 30, fill=WHITE, outline=INK, width=6)

def sh_set(p, lt, D):
    key = ("bg", p["bg"], bool(p.get("ruin")), bool(p.get("dawn")), p.get("door"), bool(p.get("pies")))
    im = (BGS[p["bg"]]({**p, "_lt": lt}) if p.get("tick") else cached(key, lambda: BGS[p["bg"]](p))).copy()
    d = ImageDraw.Draw(im)
    if p.get("car") is not None:
        cx = p["car"] * W if p["car"] != "leave" else (0.15 - 0.5 * ease(lt / max(D, 0.5))) * W
        im.alpha_composite(car_sprite(), (int(cx - 300), 700))
    for a in p.get("actors", []):
        if a.get("bed"): bed_actor(im, a)
    draw_actors(im, p.get("actors", []), lt, D)
    if p.get("pies"):
        for i in range(3):
            pts = [(1000 + i * 30 + math.sin(y / 30 + lt * 3 + i) * 14, y) for y in range(560, 420, -10)]; d.line(pts, fill=(255, 255, 255, 160), width=6)
    if p.get("hand"):
        d.ellipse((700, 190, 760, 260), fill=(200, 210, 220)); [d.line((690 + i * 20, 200, 680 + i * 22, 150), fill=(200, 210, 220), width=12) for i in range(4)]
    if p.get("night"): night(im, 200 if p.get("dark") else 150)
    if p.get("night") and p.get("bg") == "door" and p.get("door") in ("light", "feet"): im.alpha_composite(blob(900, 200, (255, 210, 120), 120, 40), (510, 880))
    if p.get("ruin") and p["bg"] == "kitchen":
        for i in range(40): x = (i * 193 + lt * 30) % W; y = (i * 97 + lt * 20) % H; d.ellipse((x, y, x + 4, y + 4), fill=(240, 230, 200, 120))
    if p.get("text"): label(im, p["text"], W // 2, 120, YEL, LBL, bg=INK)
    im.alpha_composite(vignette(150)); return im

def car_sprite():
    def mk():
        def dr(d, k):
            K = k; L = lambda *a: [v * K for v in a]
            d.rounded_rectangle(L(20, 140, 600, 270), int(40 * K), fill=(60, 110, 170), outline=INK, width=int(8 * K)); d.polygon(L(130, 140, 200, 50, 430, 50, 500, 140), fill=(60, 110, 170), outline=INK)
            d.polygon(L(160, 135, 215, 70, 305, 70, 305, 135), fill=(0, 0, 0, 0)); d.polygon(L(325, 135, 325, 70, 420, 70, 470, 135), fill=(0, 0, 0, 0))
            for x in (150, 470): d.ellipse(L(x - 55, 215, x + 55, 325), fill=(30, 30, 34), outline=INK, width=int(6 * K)); d.ellipse(L(x - 22, 248, x + 22, 292), fill=(180, 180, 190))
            d.ellipse(L(570, 170, 600, 200), fill=(255, 240, 160))
        return ss(620, 330, dr)
    return cached(("car",), mk)
def sh_car(p, lt, D):
    im = grad((240, 170, 110), (250, 220, 170)); d = ImageDraw.Draw(im); off = lt * 120
    for i in range(8): x = (i * 300 - off * 0.3) % (W + 300) - 150; d.ellipse((x, 520, x + 500, 820), fill=(150, 160, 120))
    d.rectangle((0, 700, W, H), fill=(110, 140, 80)); d.rectangle((0, 840, W, 980), fill=(80, 80, 86))
    for i in range(12): x = (i * 200 - off * 4) % (W + 200) - 100; d.rectangle((x, 905, x + 100, 915), fill=(240, 230, 200))
    for i in range(7):
        x = (i * 340 - off * 1.6) % (W + 340) - 170; d.rectangle((x + 40, 560, x + 60, 760), fill=(90, 60, 40)); d.ellipse((x - 20, 420, x + 120, 620), fill=(60, 110, 60), outline=INK, width=5)
    big = car_sprite().resize((1240, 660), Image.LANCZOS); bob = math.sin(lt * 18) * 3; ox, oy = 340, int(330 + bob)
    for (who, cx, sc) in (("boy", 0.4, 0.36), ("dad", 0.58, 0.42), ("mom", 0.7, 0.42)):
        sp = bean(PRESET[who]["body"], "dot", "line", s=sc, hair=PRESET[who]["hair"], hcol=PRESET[who]["hcol"], glasses=PRESET[who].get("glasses", False), look=1)
        im.alpha_composite(sp, (int(ox + cx * 1240 - sp.width / 2), int(oy + 125)))
    im.alpha_composite(big, (ox, oy))
    if p.get("static"):
        for i in range(60): y = rng.integers(0, H); d.line((0, y, W, y), fill=(255, 255, 255, 50), width=2)
        label(im, "ШШШ…", 1500, 200, WHITE, LBL)
    return im
def sh_note(p, lt, D):
    im = grad((60, 44, 34), (30, 22, 18)); n = p.get("show", 0)
    rules = ["1. После заката из дома не выходи", "2. Позовут по имени — не отвечай", "3. Дверь никому не открывай"]
    def mk(n=n, hl=p.get("hl")):
        def dr(d, k):
            d.rounded_rectangle((0, 0, 1300 * k, 860 * k), 24 * k, fill=(240, 232, 210), outline=INK, width=8 * k)
            for y in range(150, 860, 90): d.line((40 * k, y * k, 1260 * k, y * k), fill=(170, 190, 220), width=3 * k)
            d.text((650 * k, 90 * k), "ПРАВИЛА", font=F("Inter-Black", 70 * k), fill=(160, 40, 40), anchor="mm")
            for i in range(n):
                d.text((70 * k, (230 + i * 190) * k), rules[i], font=F("Inter-ExtraBold", 60 * k), fill=(40, 40, 90) if hl != i + 1 else (200, 30, 30))
            if n >= 2: d.text((110 * k, 510 * k), "даже если это бабушка", font=F("Inter-Bold", 44 * k), fill=(120, 60, 60))
            if n >= 3: d.text((110 * k, 700 * k), "даже нам", font=F("Inter-Bold", 44 * k), fill=(120, 60, 60))
        return ss(1300, 860, dr).rotate(-2, expand=True, resample=Image.BICUBIC)
    put(im, cached(("note", n, p.get("hl")), mk), W // 2, 1040); im.alpha_composite(vignette(140)); return im
def photo_img(cut):
    def mk():
        def dr(d, k):
            d.rectangle((0, 0, 1100 * k, 760 * k), fill=(232, 222, 196), outline=(120, 100, 80), width=6 * k)
            d.rectangle((50 * k, 50 * k, 1050 * k, 710 * k), fill=(170, 150, 120))
        im = ss(1100, 760, dr)
        for who, x in (("mom", 300), ("dad", 520), ("granny", 750)):
            sp = bean(PRESET[who]["body"], "dot", "smile", s=1.05, hair=PRESET[who]["hair"], hcol=PRESET[who]["hcol"], glasses=PRESET[who].get("glasses", False))
            im.alpha_composite(sp, (int(x - sp.width / 2), 120))
        d = ImageDraw.Draw(im); d.ellipse((330, 360, 420, 430), fill=(240, 240, 250), outline=INK, width=5); d.ellipse((350, 340, 400, 390), fill=WHITE, outline=INK, width=4)
        arr = np.array(im.convert("RGB")).astype(np.float32); g = arr.mean(2, keepdims=True); arr = arr * 0.35 + g * 0.65; arr *= np.array([1.08, 0.98, 0.84])
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
        if cut:
            d.ellipse((655, 155, 845, 345), fill=(14, 10, 10) if cut is True else (40, 34, 40))
            if cut == "ghost": d.ellipse((690, 215, 720, 255), fill=(200, 200, 210)); d.ellipse((780, 215, 810, 255), fill=(200, 200, 210))
        return im
    return cached(("photo", cut), mk)
def sh_photo(p, lt, D):
    im = grad((70, 40, 36), (40, 24, 22)); d = ImageDraw.Draw(im); d.rectangle((260, 60, 1660, 1040), fill=(96, 30, 30), outline=INK, width=10)
    put(im, photo_img(p.get("cut", True)).rotate(2, expand=True, resample=Image.BICUBIC), W // 2, 960); im.alpha_composite(vignette(160)); return im
def sh_phone(p, lt, D):
    im = grad((30, 30, 44), (12, 12, 20)) if p.get("night") else grad((200, 180, 150), (150, 130, 110)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((690, 40, 1230, 1080), 70, fill=(20, 20, 24), outline=INK, width=10); d.rounded_rectangle((720, 80, 1200, 1060), 50, fill=(28, 34, 52))
    d.ellipse((860, 220, 1060, 420), fill=(150, 92, 186)); d.text((960, 320), "М", font=F("Inter-Black", 110), fill=WHITE, anchor="mm")
    d.text((960, 500), p.get("name", "Мама"), font=F("Inter-Black", 70), fill=WHITE, anchor="mm")
    if p.get("lost"): d.text((960, 590), "Связь потеряна", font=F("Inter-Bold", 44), fill=(240, 90, 90), anchor="mm")
    elif p.get("call"): d.text((960, 590), f"00:{int(lt) + 3:02d}", font=F("Inter-Bold", 48), fill=(170, 180, 200), anchor="mm"); d.ellipse((900, 840, 1020, 960), fill=(220, 60, 60))
    else:
        r = 60 + 10 * math.sin(lt * 10); d.text((960, 590), "вызов…", font=F("Inter-Bold", 44), fill=(170, 180, 200), anchor="mm")
        d.ellipse((960 - r, 900 - r, 960 + r, 900 + r), fill=(60, 190, 90))
    if p.get("night"): im.alpha_composite(blob(800, 1000, (120, 140, 220), 60, 80), (560, 40))
    return im
def sh_title(p, lt, D):
    im = Image.new("RGBA", (W, H), (8, 8, 12, 255)); a = eout(lt / 0.4); d = ImageDraw.Draw(im)
    d.text((W // 2, H // 2 - 60), p["text"], font=F("Inter-Black", 150), fill=(230, 50, 50, int(255 * a)), anchor="mm")
    return im
def sh_black(p, lt, D): return Image.new("RGBA", (W, H), (0, 0, 0, 255))
def sh_split(p, lt, D):
    l = sh_set({"bg": "kitchen", "night": True, "actors": [{"who": "other", "x": 0.3}]}, lt, D).crop((0, 0, W // 2, H))
    r = sh_set({"bg": "door", "night": True, "door": "feet"}, lt, D).crop((W // 4, 0, W // 4 + W // 2, H))
    im = Image.new("RGBA", (W, H)); im.alpha_composite(l, (0, 0)); im.alpha_composite(r, (W // 2, 0)); ImageDraw.Draw(im).rectangle((W // 2 - 6, 0, W // 2 + 6, H), fill=INK)
    label(im, "КУХНЯ", W // 4, 120, YEL, LBS, bg=INK); label(im, "ЗА ДВЕРЬЮ", 3 * W // 4, 120, YEL, LBS, bg=INK); return im
def sh_flash(p, lt, D):
    im = grad((40, 30, 50), (14, 10, 20)); d = ImageDraw.Draw(im)
    grow = ease(lt / 1.2); h = 560 + 120 * grow; x = 1400
    d.polygon((x - 120, 1000, x - 60, 1000 - h, x + 60, 1000 - h, x + 120, 1000), fill=(6, 4, 8)); d.ellipse((x - 110, 1000 - h - 160, x + 110, 1000 - h + 40), fill=(6, 4, 8))
    for sx in (-1, 1): d.line((x + sx * 70, 1000 - h + 60, x + sx * (420 + 80 * grow), 700 - 200 * grow), fill=(6, 4, 8), width=26)
    for sx in (-1, 1): d.ellipse((x + sx * 40 - 12, 1000 - h - 80, x + sx * 40 + 12, 1000 - h - 56), fill=(240, 240, 255))
    if p.get("voices"):
        for i, s in enumerate(("сынок…", "внучек…", "иди сюда…")): label(im, s, 1400 + (i - 1) * 300, 220 + i * 70, (200, 200, 230), LBS)
    g = bean(GRC, "angry" if p.get("shield") else "dot", "line", "up" if p.get("shield") else "down", s=1.0, hair="scarf", hcol=(206, 58, 58), glasses=True)
    put(im, g, 600 if not p.get("shield") else 900, 1000)
    d.ellipse((480 if not p.get("shield") else 520, 760, 620 if not p.get("shield") else 660, 860), fill=(240, 240, 250), outline=INK, width=5)
    arr = np.array(im.convert("RGB")).astype(np.float32); arr = arr * np.array([1.05, 0.92, 0.8]); im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    im.alpha_composite(vignette(200)); return im
def sh_winout(p, lt, D):
    out = Image.new("RGBA", (W, H), (14, 18, 40, 255)); d = ImageDraw.Draw(out)
    d.rectangle((0, 700, W, H), fill=(30, 46, 34)); [d.rectangle((x, 640, x + 30, 800), fill=(60, 46, 36)) for x in range(0, W, 46)]
    out.alpha_composite(car_sprite(), (300, 560)); d.polygon((900, 640, 1600, 560, 1600, 760), fill=(255, 240, 160, 60))
    for who, x in (("mom_x", 1060), ("dad_x", 1300)):
        sp = bean(PRESET[who]["body"], "none", "none", "up" if p.get("wave") and int(lt * 3) % 2 else "down", s=0.75, hair=PRESET[who]["hair"], hcol=PRESET[who]["hcol"])
        out.alpha_composite(sp, (int(x - sp.width / 2), int(840 - sp.height)))
    night(out, 90)
    im = Image.new("RGBA", (W, H)); logwall(im); im.alpha_composite(out.crop((360, 140, 1560, 940)), (360, 140))
    d = ImageDraw.Draw(im); d.rectangle((360, 140, 1560, 940), outline=(220, 210, 190), width=30); d.line((960, 140, 960, 940), fill=(220, 210, 190), width=20); d.line((360, 540, 1560, 540), fill=(220, 210, 190), width=20)
    night(im, 90); return im
def sh_sill(p, lt, D):
    im = grad((250, 210, 160), (200, 170, 140)); d = ImageDraw.Draw(im)
    d.rectangle((360, 80, 1560, 760), fill=(170, 210, 240), outline=WHITE, width=30); d.line((960, 80, 960, 760), fill=WHITE, width=20)
    d.rectangle((260, 760, 1660, 840), fill=(240, 236, 226), outline=INK, width=6); d.ellipse((760, 700, 1160, 780), fill=WHITE, outline=INK, width=5)
    for i in range(6): d.ellipse((800 + i * 50 - 50, 690 - (i % 2) * 20, 800 + i * 50 + 50, 750 - (i % 2) * 20), fill=(220, 150, 70), outline=INK, width=4)
    for i in range(4):
        pts = [(840 + i * 70 + math.sin(y / 30 + lt * 3 + i) * 16, y) for y in range(660, 420, -10)]; d.line(pts, fill=(255, 255, 255, 180), width=7)
    im.alpha_composite(blob(900, 700, (255, 230, 170), 90, 80), (500, 100)); return im
