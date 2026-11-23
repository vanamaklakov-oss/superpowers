# «40 лет назад»: локации 1986 года. База персонажей/фонов — из h02_chasy (а та — из h01_babushka).
exec(open(os.path.join(os.path.dirname(DIR), "h02_chasy", "shots.py")).read(), globals())
PRESET.update({
    "kir": dict(body=(126, 70, 196), hair="short", hcol=(70, 46, 30)),
    "leha": dict(body=(70, 110, 170), hair="short", hcol=(214, 176, 90)),
    "sedoy": dict(body=(34, 32, 38), hair="short", hcol=(160, 160, 168)),
    "mil": dict(body=(92, 112, 140), hair="short", hcol=(60, 50, 40)),
    "bandit": dict(body=(40, 36, 36), hair="short", hcol=(30, 26, 24), eyes="dot", mouth="line"),
    "bookie": dict(body=(120, 96, 60), hair="short", hcol=(50, 40, 30), glasses=True),
    "ded": dict(body=(120, 110, 100), hair="short", hcol=(236, 236, 236), glasses=False),
    "lmom": dict(body=(180, 96, 96), hair="long", hcol=(110, 70, 40)),
    "babka": dict(body=(196, 120, 150), hair="long", hcol=(80, 50, 30)),
})
_actor0 = actor_sprite
def actor_sprite(a, lt):
    sp = _actor0({**a, "a": a.get("a", "rope" if a.get("baby") else "down")}, lt)
    if a.get("bench"):
        sp = sp.crop((0, 0, sp.width, int(sp.height * 0.72)))
    if a.get("who") == "mil" or a.get("baby") or a.get("phone"):
        sp = sp.copy(); d = ImageDraw.Draw(sp); s_ = a.get("s", 1.0); fl = a.get("flip", False)
        X = lambda x: (sp.width - x * s_) if fl else x * s_
        _el, _rr, _re, _ch = d.ellipse, d.rounded_rectangle, d.rectangle, d.chord
        nb = lambda b: (min(b[0], b[2]), min(b[1], b[3]), max(b[0], b[2]), max(b[1], b[3]))
        class _D:
            ellipse = staticmethod(lambda b, **k: _el(nb(b), **k)); rectangle = staticmethod(lambda b, **k: _re(nb(b), **k))
            rounded_rectangle = staticmethod(lambda b, r, **k: _rr(nb(b), r, **k)); chord = staticmethod(lambda b, a1, a2, **k: _ch(nb(b), a1, a2, **k))
        d = _D()
        if a.get("who") == "mil":
            d.chord((X(78) if not fl else X(262), 20 * s_, X(262) if not fl else X(78), 140 * s_), 180, 360, fill=(70, 90, 120)); d.rectangle((min(X(70), X(270)), 60 * s_, max(X(70), X(270)), 78 * s_), fill=(40, 50, 70)); d.ellipse((X(160), 34 * s_, X(180), 54 * s_), fill=(230, 60, 60))
        if a.get("baby"):
            d.ellipse((min(X(110), X(230)), 250 * s_, max(X(110), X(230)), 340 * s_), fill=(240, 240, 250), outline=INK, width=5); d.ellipse((min(X(190), X(234)), 262 * s_, max(X(190), X(234)), 306 * s_), fill=(250, 220, 200), outline=INK, width=4)
        if a.get("phone"):
            d.rounded_rectangle((min(X(150), X(196)), 260 * s_, max(X(150), X(196)), 340 * s_), 8, fill=(20, 20, 24)); d.rectangle((min(X(156), X(190)), 268 * s_, max(X(156), X(190)), 330 * s_), fill=(120, 190, 255))
    return sp
_draw0 = draw_actors
def draw_actors(im, actors, lt, D):
    for a in actors:
        if a.get("bench"): put(im, actor_sprite(a, lt), a["x"] * W, 860);
    _draw0(im, [a for a in actors if not a.get("bench")], lt, D)

def khrush(d, x0, y0, w, h, col, win, modern=False, lit=0.0, g=None):
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=col)
    for yy in range(y0 + 30, y0 + h - 40, 110):
        for xx in range(x0 + 30, x0 + w - 60, 120):
            on = g is not None and g.random() < lit
            d.rectangle((xx, yy, xx + 70, yy + 70), fill=(255, 210, 120) if on else win)
            if not modern: d.line((xx + 35, yy, xx + 35, yy + 70), fill=col, width=4)
            else: d.rectangle((xx, yy, xx + 70, yy + 70), outline=(240, 240, 240), width=5)
        d.line((x0, yy + 92, x0 + w, yy + 92), fill=tuple(int(c * 0.85) for c in col), width=3)
def bg_dvor(p):
    night = p.get("night"); modern = p.get("modern")
    im = grad((140, 190, 235), (230, 236, 240)) if not night else grad((12, 16, 36), (36, 44, 70)); d = ImageDraw.Draw(im); g = np.random.default_rng(3)
    khrush(d, 0, 150, 900, 700, (200, 186, 160) if not modern else (226, 214, 190), (110, 140, 170) if not night else (30, 36, 56), modern, 0.45 if night else 0, g)
    khrush(d, 1050, 230, 870, 620, (176, 170, 160) if not modern else (210, 200, 196), (110, 140, 170) if not night else (30, 36, 56), modern, 0.4 if night else 0, g)
    d.rectangle((0, 850, W, H), fill=(110, 130, 80) if not night else (34, 44, 34)); d.rectangle((700, 860, 1300, H), fill=(150, 146, 140) if not night else (50, 50, 56))
    if not modern:
        d.line((120, 520, 760, 560), fill=(240, 240, 240), width=3)
        for i, c in enumerate(((230, 80, 80), (80, 140, 220), (240, 240, 240), (240, 200, 80))): x = 180 + i * 140; d.rectangle((x, 528 + i * 6, x + 70, 600 + i * 6), fill=c)
        d.rounded_rectangle((1420, 760, 1640, 900), 50, fill=(240, 200, 40), outline=INK, width=6); d.text((1530, 830), "КВАС", font=F("Inter-Black", 44), fill=(160, 40, 40), anchor="mm")
        for x in (1460, 1600): d.ellipse((x - 26, 880, x + 26, 932), fill=(30, 30, 30))
        d.rectangle((880, 600, 1060, 760), fill=(240, 236, 220), outline=INK, width=5); d.text((970, 640), "КИНО", font=F("Inter-Black", 40), fill=(180, 40, 40), anchor="mm"); d.text((970, 700), "9.VI.86", font=F("Inter-Bold", 34), fill=INK, anchor="mm")
    else:
        for x, c in ((1320, (200, 40, 40)), (1580, (40, 40, 44))): d.rounded_rectangle((x, 800, x + 240, 900), 30, fill=c, outline=INK, width=5)
    d.rectangle((300, 820, 640, 850), fill=(110, 80, 50), outline=INK, width=4); d.rectangle((300, 790, 640, 806), fill=(110, 80, 50))
    for x in (320, 610): d.rectangle((x, 850, x + 14, 900), fill=(60, 60, 60))
    return im
def bg_garages(p):
    im = grad((150, 170, 190), (220, 220, 214)); d = ImageDraw.Draw(im); d.rectangle((0, 880, W, H), fill=(120, 116, 104))
    for i in range(7):
        x = i * 280 - 40; c = [(90, 110, 90), (120, 90, 70), (90, 100, 130)][i % 3]
        d.rectangle((x, 330, x + 270, 880), fill=c, outline=INK, width=5); d.rectangle((x + 20, 420, x + 250, 880), fill=tuple(int(v * 0.85) for v in c), outline=INK, width=4)
        for y in range(440, 880, 40): d.line((x + 20, y, x + 250, y), fill=tuple(int(v * 0.7) for v in c), width=3)
    return im
def bg_market(p):
    im = grad((170, 200, 230), (236, 230, 220)); d = ImageDraw.Draw(im); d.rectangle((0, 860, W, H), fill=(150, 140, 120))
    for i in range(5):
        x = 60 + i * 380; c = [(200, 70, 60), (60, 120, 180), (230, 190, 60)][i % 3]
        d.polygon((x, 420, x + 340, 420, x + 300, 330, x + 40, 330), fill=c); d.rectangle((x + 20, 420, x + 320, 760), fill=(220, 210, 190), outline=INK, width=4)
        d.rectangle((x, 700, x + 340, 760), fill=(140, 100, 60), outline=INK, width=4)
        for k in range(4): d.rectangle((x + 40 + k * 70, 470, x + 90 + k * 70, 600), fill=(60, 90, 150) if i % 2 else (40, 40, 40))
    return im
def bg_kv80(p):
    im = Image.new("RGBA", (W, H), (226, 212, 184, 255)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line((x, 0, x, 900), fill=(214, 198, 168), width=3)
    d.rectangle((0, 900, W, H), fill=(140, 96, 60))
    d.rectangle((90, 140, 820, 620), fill=(150, 40, 40), outline=(100, 30, 30), width=10)
    for i in range(6):
        for j in range(4): cx, cy = 170 + i * 115, 210 + j * 115; d.regular_polygon((cx, cy, 44), 4, rotation=45, fill=(220, 170, 80)); d.regular_polygon((cx, cy, 20), 4, rotation=45, fill=(40, 70, 120))
    d.rectangle((1380, 220, 1840, 900), fill=(120, 76, 44), outline=INK, width=6); d.rectangle((1410, 250, 1810, 560), fill=(170, 200, 210), outline=INK, width=4)
    for i in range(5): d.polygon((1440 + i * 74, 520, 1470 + i * 74, 420, 1500 + i * 74, 520), fill=(230, 240, 250), outline=(120, 140, 160))
    d.rounded_rectangle((940, 560, 1300, 840), 20, fill=(70, 50, 36), outline=INK, width=6); d.rectangle((960, 580, 1220, 800), fill=(40, 46, 44) if not p.get("tv") else (70, 140, 80))
    if p.get("tv") == "score": d.text((1090, 690), "3 : 4", font=F("Inter-Black", 80), fill=WHITE, anchor="mm")
    elif not p.get("tv"): d.polygon((940, 560, 1300, 560, 1260, 640, 980, 640), fill=(240, 240, 240))
    d.rectangle((960, 840, 1280, 900), fill=(100, 70, 44))
    d.rounded_rectangle((160, 700, 820, 900), 40, fill=(160, 110, 70), outline=INK, width=6)
    return im
def bg_katran(p):
    im = grad((40, 34, 30), (16, 14, 12)); d = ImageDraw.Draw(im)
    for y in range(0, 900, 64): d.rectangle((0, y, W, y + 60), fill=(56, 48, 42))
    d.rectangle((0, 900, W, H), fill=(30, 26, 22)); d.ellipse((560, 640, 1360, 860), fill=(40, 110, 60), outline=INK, width=8)
    for i in range(6): d.rectangle((700 + i * 90, 720 + (i % 2) * 20, 760 + i * 90, 760 + (i % 2) * 20), fill=WHITE, outline=INK, width=2)
    d.line((960, 0, 960, 180), fill=INK, width=6); d.polygon((900, 180, 1020, 180, 1000, 230, 920, 230), fill=(60, 60, 60))
    im.alpha_composite(blob(900, 700, (255, 220, 140), 110, 80), (510, 180))
    for i in range(5): im.alpha_composite(blob(500, 160, (200, 200, 200), 40, 40), (200 + i * 300, 300 + (i % 2) * 120))
    return im
def bg_rest(p):
    im = grad((90, 30, 34), (40, 14, 16)); d = ImageDraw.Draw(im)
    for x in range(0, W, 240): d.rectangle((x, 0, x + 120, 880), fill=(120, 36, 40))
    d.rectangle((0, 880, W, H), fill=(60, 30, 24))
    for x in (260, 760, 1300): d.rectangle((x, 700, x + 360, 760), fill=(244, 240, 232), outline=INK, width=4); d.rectangle((x + 30, 760, x + 330, 900), fill=(230, 226, 216))
    d.rounded_rectangle((1700, 600, 1880, 700), 14, fill=(50, 50, 56), outline=INK, width=5); d.ellipse((1720, 620, 1780, 680), fill=(120, 120, 130)); d.ellipse((1800, 620, 1860, 680), fill=(120, 120, 130))
    return im
BGS.update({"dvor": bg_dvor, "garages": bg_garages, "market": bg_market, "kv80": bg_kv80, "katran": bg_katran, "rest": bg_rest})
BGKEYS.update({"night", "modern", "tv"})
_set1 = sh_set
def sh_set(p, lt, D):
    im = _set1({**p, "night": False} if p.get("bg") in ("dvor",) else p, lt, D) if False else _set1(p, lt, D)
    if p.get("volga"):
        c = car_sprite().copy(); arr = np.array(c); m = arr[..., 3] > 0; blue = (arr[..., 2] > 140) & (arr[..., 0] < 100); arr[blue] = [24, 24, 28, 255]; c = Image.fromarray(arr)
        im.alpha_composite(c.resize((900, 480)), (1000, 540))
    return im
def lcd(d, x, y, s, size, col=(30, 40, 30)):
    d.text((x, y), s, font=F("Inter-Black", size), fill=col, anchor="mm")
def sh_watch80(p, lt, D):
    im = grad((60, 50, 44), (20, 16, 14)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((760, 0, 1160, H), 60, fill=(90, 70, 50) if not p.get("new") else (40, 40, 44))
    d.rounded_rectangle((560, 260, 1360, 820), 90, fill=(170, 170, 176) if not p.get("new") else (200, 200, 206), outline=INK, width=10)
    d.rounded_rectangle((640, 360, 1280, 720), 30, fill=(150, 170, 140), outline=INK, width=8)
    d.text((960, 310), "ЭЛЕКТРОНИКА", font=F("Inter-Black", 40), fill=INK, anchor="mm")
    blink = int(lt * 2) % 2 == 0 or not p.get("red")
    lcd(d, 960, 540, p.get("text", "00:00"), 130, (160, 20, 20) if p.get("red") and blink else (30, 40, 30))
    if not p.get("new"):
        for i in range(30): x, y = 580 + (i * 97) % 760, 270 + (i * 53) % 540; d.line((x, y, x + 20, y + 6), fill=(130, 130, 136), width=2)
    return im
def sh_warp(p, lt, D):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im); u = lt * (1 if not p.get("back") else -1)
    for i in range(70):
        a = i * 2.39; r0 = ((i * 37 + lt * 900) % 1100); r1 = r0 + 120 + r0 * 0.4
        d.line((960 + r0 * math.cos(a), 540 + r0 * math.sin(a), 960 + r1 * math.cos(a), 540 + r1 * math.sin(a)), fill=(200, 220, 255) if i % 3 else (255, 200, 120), width=4)
    yr = int(2026 - min(40, lt * 18)) if not p.get("back") else int(1986 + min(40, lt * 18))
    label(im, str(yr), 960, 540, WHITE, F("Inter-Black", 220)); return im
def sh_pockets(p, lt, D):
    im = grad((60, 50, 90), (24, 20, 40)); d = ImageDraw.Draw(im)
    for i, (t, x) in enumerate((("0 ₽", 520), ("нет паспорта", 960), ("нет сети", 1400))):
        a = eout((lt - i * 0.35) / 0.3)
        if a > 0: label(im, t, x, 540, WHITE, F("Inter-Black", 70), bg=(150, 30, 30), a=a)
    return im
def sh_phone26(p, lt, D):
    im = grad((40, 40, 50), (16, 16, 20)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((740, 80, 1180, 1000), 60, fill=(20, 20, 24), outline=(90, 90, 100), width=8); d.rounded_rectangle((770, 110, 1150, 970), 44, fill=(30, 34, 50))
    d.text((960, 300), "НЕТ СЕТИ", font=F("Inter-Black", 60), fill=(240, 80, 80), anchor="mm"); d.text((960, 380), "1986", font=F("Inter-Bold", 44), fill=(170, 170, 180), anchor="mm")
    for k in range(4): d.rectangle((860 + k * 50, 520 - k * 30, 890 + k * 50, 560), outline=(120, 120, 130), width=4)
    return im
def sh_poster(p, lt, D):
    im = grad((200, 186, 160), (170, 156, 130)); d = ImageDraw.Draw(im)
    d.rectangle((560, 120, 1360, 980), fill=(244, 238, 220), outline=INK, width=8)
    d.text((960, 260), "КИНОТЕАТР «РОДИНА»", font=F("Inter-Black", 50), fill=(170, 40, 40), anchor="mm")
    d.text((960, 520), "9 ИЮНЯ", font=F("Inter-Black", 150), fill=INK, anchor="mm"); d.text((960, 700), "1986", font=F("Inter-Black", 170), fill=(170, 40, 40), anchor="mm")
    d.text((960, 880), "сеансы: 10:00 · 14:00 · 19:00", font=F("Inter-Bold", 40), fill=INK, anchor="mm"); return im
def sh_photo80(p, lt, D):
    im = grad((70, 40, 36), (40, 24, 22)); ph = Image.new("RGBA", (1000, 700), (226, 214, 190, 255)); pd = ImageDraw.Draw(ph); pd.rectangle((40, 40, 960, 660), fill=(150, 130, 110))
    for who, x in (("babka", 300), ("sedoy", 620)):
        pr = PRESET[who]; sp = bean(pr["body"], "dot", "smile", "rope" if who == "babka" else "down", s=1.0, hair=pr["hair"], hcol=pr["hcol"]); ph.alpha_composite(sp, (x - 170, 120))
    pd.ellipse((240, 370, 360, 450), fill=(240, 240, 250), outline=INK, width=5)
    cut = p.get("cut")
    if cut is True: pd.ellipse((540, 150, 720, 330), fill=(14, 10, 10))
    arr = np.array(ph.convert("RGB")).astype(np.float32); gry = arr.mean(2, keepdims=True); arr = (arr * 0.3 + gry * 0.7) * np.array([1.08, 0.96, 0.82]); ph = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    if cut == "fade":
        a = 1 - ease(lt / 2.0); ph.putalpha(int(255 * max(0.15, a)))
    put(im, ph.rotate(2, expand=True, resample=Image.BICUBIC), 960, 960); im.alpha_composite(vignette(160)); return im
def sh_booth(p, lt, D):
    night = p.get("night") or True; im = grad((20, 26, 50), (50, 60, 90)); d = ImageDraw.Draw(im); d.rectangle((0, 880, W, H), fill=(40, 44, 50))
    if p.get("close"):
        d.rectangle((560, 120, 1360, 1000), fill=(190, 40, 40), outline=INK, width=10); d.rectangle((620, 200, 1300, 940), fill=(60, 60, 66))
        d.rounded_rectangle((760, 300, 1160, 760), 30, fill=(150, 150, 156), outline=INK, width=8); d.ellipse((860, 420, 1060, 620), fill=(40, 40, 44))
        for k in range(10): a = k * 0.6; d.ellipse((960 + 75 * math.cos(a) - 14, 520 + 75 * math.sin(a) - 14, 960 + 75 * math.cos(a) + 14, 520 + 75 * math.sin(a) + 14), fill=(200, 200, 200))
        d.rounded_rectangle((1180, 300, 1250, 700), 30, fill=(30, 30, 34)); d.text((960, 830), "2 коп", font=F("Inter-Black", 50), fill=YEL, anchor="mm")
    else:
        d.rectangle((780, 260, 1140, 900), fill=(200, 40, 40), outline=INK, width=8); d.rectangle((820, 340, 1100, 860), fill=(170, 200, 220, 120)); d.text((960, 300), "ТЕЛЕФОН", font=F("Inter-Black", 40), fill=WHITE, anchor="mm")
        d.line((300, 900, 300, 300), fill=(30, 30, 34), width=14); im.alpha_composite(blob(500, 700, (255, 220, 150), 90, 60), (50, 260))
    return im
def sh_coins(p, lt, D):
    im = grad((80, 60, 40), (40, 30, 20)); d = ImageDraw.Draw(im)
    for i in range(9):
        x, y = 600 + (i % 3) * 260 + (i // 3) * 40, 340 + (i // 3) * 170; a = eout((lt - i * 0.08) / 0.3)
        if a <= 0: continue
        d.ellipse((x - 90, y - 90, x + 90, y + 90), fill=(200, 150, 70), outline=(120, 80, 30), width=8); d.text((x, y), "2", font=F("Inter-Black", 90), fill=(120, 80, 30), anchor="mm")
    return im
def sh_tv(p, lt, D):
    im = grad((40, 30, 24), (16, 12, 10)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((360, 140, 1560, 940), 50, fill=(90, 60, 40), outline=INK, width=10); d.rounded_rectangle((440, 210, 1380, 870), 40, fill=(60, 130, 70))
    d.line((910, 210, 910, 870), fill=(220, 240, 220), width=6); d.ellipse((810, 440, 1010, 640), outline=(220, 240, 220), width=6)
    for i in range(10): x = 500 + (i * 97 + lt * 80 * (1 if i % 2 else -1)) % 800; y = 260 + (i * 61) % 560; d.ellipse((x, y, x + 24, y + 24), fill=(240, 60, 60) if i % 2 else (240, 240, 240))
    if p.get("screen") == "score": d.rounded_rectangle((520, 240, 1300, 380), 20, fill=(20, 20, 30)); d.text((910, 310), p.get("score", ""), font=F("Inter-Black", 90), fill=WHITE, anchor="mm")
    d.text((910, 830), "МЕХИКО-86", font=F("Inter-Bold", 36), fill=(230, 240, 230), anchor="mm")
    for x in (1440, 1500): d.ellipse((x - 30, 300 + (x - 1440) * 3, x + 30, 360 + (x - 1440) * 3), fill=(40, 30, 24), outline=INK, width=4)
    for i in range(1200): x, y = rng.integers(440, 1380), rng.integers(210, 870); d.point((x, y), fill=(255, 255, 255))
    return im
def sh_barber(p, lt, D):
    im = grad((150, 170, 190), (220, 220, 214)); d = ImageDraw.Draw(im); d.rectangle((0, 880, W, H), fill=(120, 116, 104))
    d.rectangle((300, 200, 1620, 880), fill=(200, 190, 170), outline=INK, width=6); d.rectangle((420, 260, 1500, 360), fill=(60, 90, 140)); d.text((960, 310), "ПАРИКМАХЕРСКАЯ", font=F("Inter-Black", 70), fill=WHITE, anchor="mm")
    d.rectangle((500, 420, 1000, 760), fill=(170, 200, 220), outline=INK, width=6); d.polygon((1200, 880, 1500, 880, 1460, 980, 1240, 980), fill=(30, 26, 22)); d.text((1350, 860), "ВНИЗ →", font=F("Inter-Black", 40), fill=(200, 60, 60), anchor="mm")
    return im
def sh_silhouette(p, lt, D):
    im = grad((14, 14, 20), (4, 4, 8)); d = ImageDraw.Draw(im)
    sp = bean((24, 22, 26), "none", "none", "hips", s=1.6, hair="short", hcol=(150, 150, 156)); sp = sp.copy(); arr = np.array(sp); arr[..., :3] = (arr[..., :3] * 0.25).astype(np.uint8); sp = Image.fromarray(arr)
    put(im, sp, 960, 1080, shadowed=False); im.alpha_composite(blob(900, 400, (255, 200, 120), 50, 80), (510, 0)); label(im, "СЕДОЙ", 960, 140, (220, 220, 220), F("Inter-Black", 90)); return im
def sh_sneakers(p, lt, D):
    im = grad((150, 120, 90), (110, 86, 64)); d = ImageDraw.Draw(im)
    for x in (560, 1000):
        d.rounded_rectangle((x, 520, x + 380, 700), 70, fill=(245, 245, 245), outline=INK, width=8); d.rectangle((x + 20, 660, x + 360, 700), fill=(220, 60, 60)); d.line((x + 120, 560, x + 220, 600), fill=(60, 120, 220), width=12)
    label(im, "из ниоткуда", 960, 240, YEL, LBL, bg=INK); return im
def sh_twowatches(p, lt, D):
    im = grad((240, 236, 226), (210, 204, 190)); d = ImageDraw.Draw(im)
    for i, (x, new) in enumerate(((620, False), (1300, True))):
        if p.get("give") and new: x = 1300 - 600 * ease(lt / 1.2)
        d.rounded_rectangle((x - 230, 380, x + 230, 700), 60, fill=(200, 200, 206) if new else (160, 160, 166), outline=INK, width=8); d.rounded_rectangle((x - 180, 440, x + 180, 640), 20, fill=(150, 170, 140), outline=INK, width=5)
        lcd(d, x, 540, "15:06" if new else "4 д 06", 70)
        if not new:
            for k in range(20): xx, yy = x - 200 + (k * 61) % 400, 400 + (k * 37) % 280; d.line((xx, yy, xx + 16, yy + 5), fill=(120, 120, 126), width=2)
    label(im, "НОВЫЕ" if not p.get("give") else "«эти дойдут»", 1300 if not p.get("give") else 960, 260, INK, LBL, bg=YEL); return im
def sh_split2(p, lt, D):
    l = sh_set({"bg": "rest", "actors": [{"who": "sedoy", "x": 0.6, "flip": True, "m": "line"}]}, lt, D).crop((480, 0, 1440, H))
    r = sh_set({"bg": "flat", "actors": [{"who": "ded", "x": 0.5, "m": "smile"}]}, lt, D).crop((480, 0, 1440, H))
    im = Image.new("RGBA", (W, H)); im.alpha_composite(l, (0, 0)); im.alpha_composite(r, (960, 0)); ImageDraw.Draw(im).rectangle((954, 0, 966, H), fill=INK)
    label(im, "1986", 480, 120, YEL, LBL, bg=INK); label(im, "2026", 1440, 120, YEL, LBL, bg=INK); return im
def sh_raid(p, lt, D):
    im = sh_barber(p, lt, D); d = ImageDraw.Draw(im)
    d.rounded_rectangle((200, 700, 760, 940), 40, fill=(230, 220, 120), outline=INK, width=6); d.rectangle((220, 760, 740, 790), fill=(40, 90, 170)); d.text((480, 860), "МИЛИЦИЯ", font=F("Inter-Black", 44), fill=(40, 90, 170), anchor="mm")
    on = int(lt * 6) % 2; d.rectangle((420, 660, 540, 700), fill=(60, 120, 255) if on else (255, 60, 60)); im.alpha_composite(blob(900, 600, (60, 120, 255) if on else (255, 60, 60), 60, 90), (30, 300))
    put(im, actor_sprite({"who": "mil", "x": 0.6, "flip": True, "a": "point", "e": "angry", "m": "frown"}, lt), 1100, 1000); return im
def sh_bars(p, lt, D):
    im = grad((60, 64, 70), (30, 32, 36)); d = ImageDraw.Draw(im)
    put(im, actor_sprite({"who": "sedoy", "x": 0.5, "e": "closed", "m": "frown"}, lt), 960, 1000)
    for x in range(200, W, 160): d.rectangle((x, 0, x + 26, H), fill=(40, 40, 44))
    label(im, "8 ЛЕТ", 960, 140, WHITE, F("Inter-Black", 110), bg=(150, 30, 30)); return im
def sh_montage(p, lt, D):
    it = p.get("item"); im = grad((150, 170, 190), (220, 220, 214)); d = ImageDraw.Draw(im); d.rectangle((0, 880, W, H), fill=(120, 116, 104))
    if it == "video":
        im = grad((20, 20, 30), (6, 6, 10)); d = ImageDraw.Draw(im); d.rectangle((560, 180, 1360, 660), fill=(60, 130, 200)); d.text((960, 420), "ВИДЕОСАЛОН", font=F("Inter-Black", 80), fill=WHITE, anchor="mm")
        for i in range(8): put(im, bean((40, 40, 50), "dot", "o", s=0.5, hair="short", hcol=(40, 30, 20)), 300 + i * 190, 1000, shadowed=False)
    elif it == "soda":
        for x in (700, 1060):
            d.rectangle((x, 260, x + 300, 880), fill=(200, 60, 50), outline=INK, width=6); d.rectangle((x + 40, 320, x + 260, 460), fill=(220, 230, 240)); d.text((x + 150, 390), "ГАЗ. ВОДА", font=F("Inter-Black", 34), fill=(200, 40, 40), anchor="mm")
            d.text((x + 150, 560), "3 коп", font=F("Inter-Black", 50), fill=WHITE, anchor="mm"); d.rectangle((x + 100, 640, x + 200, 760), fill=(60, 60, 66))
    else:
        d.rectangle((1300, 300, 1800, 880), fill=(220, 210, 190), outline=INK, width=6); d.text((1550, 360), "КОЛБАСА", font=F("Inter-Black", 50), fill=(170, 40, 40), anchor="mm")
        for i in range(9): put(im, bean([(90, 90, 120), (140, 80, 80), (80, 120, 90)][i % 3], "dot", "line", s=0.7, hair="short" if i % 2 else "scarf", hcol=(80, 60, 40) if i % 2 else (180, 60, 60), flip=True), 160 + i * 130, 1000, shadowed=False)
    return im
def sh_windows(p, lt, D):
    im = grad((14, 18, 40), (30, 36, 60)); d = ImageDraw.Draw(im); g = np.random.default_rng(9)
    for bx in (0, 650, 1300):
        d.rectangle((bx + 20, 120, bx + 600, H), fill=(40, 44, 60))
        for yy in range(160, H, 110):
            for xx in range(bx + 50, bx + 560, 110):
                on = g.random() < 0.9; d.rectangle((xx, yy, xx + 70, yy + 70), fill=(120, 170, 230) if on else (24, 28, 40))
    label(im, "15 ИЮНЯ · 20:00", 960, 80, WHITE, LBL, bg=INK); return im
def sh_ticket(p, lt, D):
    im = grad((90, 70, 50), (40, 30, 20)); d = ImageDraw.Draw(im)
    d.rectangle((560, 260, 1360, 820), fill=(240, 230, 200), outline=INK, width=8); d.text((960, 360), "КВИТАНЦИЯ", font=F("Inter-Black", 70), fill=INK, anchor="mm")
    d.text((960, 520), "БЕЛЬГИЯ", font=F("Inter-Black", 100), fill=(170, 40, 40), anchor="mm"); d.text((960, 680), "ставка принята", font=F("Inter-Bold", 44), fill=INK, anchor="mm"); return im
def sh_chapter2(p, lt, D):
    im = Image.new("RGBA", (W, H), (8, 8, 12, 255)); a = eout(lt / 0.5); d = ImageDraw.Draw(im)
    d.text((W // 2, 460), p["a"], font=F("Inter-Black", 150), fill=(240, 240, 240, int(255 * a)), anchor="mm")
    d.text((W // 2, 600), p["b"], font=F("Inter-Bold", 60), fill=(230, 180, 80, int(255 * a)), anchor="mm")
    w = 420 * a; d.line((W // 2 - w, 680, W // 2 + w, 680), fill=(200, 40, 40), width=6); return im

def sh_jeans(p, lt, D):
    im = grad((120, 100, 80), (70, 56, 44)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((420, 520, 1500, 960), 40, fill=(40, 40, 50), outline=INK, width=8)
    for i in range(3):
        x = 560 + i * 300; d.polygon((x, 280 - i * 20, x + 220, 280 - i * 20, x + 240, 760, x + 130, 760, x + 110, 460, x + 90, 760, x - 20, 760), fill=(50, 80, 150), outline=INK)
        d.rectangle((x, 280 - i * 20, x + 220, 320 - i * 20), fill=(40, 66, 130)); d.rectangle((x + 150, 330 - i * 20, x + 200, 360 - i * 20), fill=(170, 120, 60))
    label(im, "≈ 1,5 зарплаты", 960, 160, YEL, LBL, bg=INK); return im

def THUMB():
    im = bg_dvor({"night": True}).copy(); d = ImageDraw.Draw(im); night(im, 90)
    sil = bean((24, 22, 26), "none", "none", "hips", s=1.7, hair="short", hcol=(150, 150, 156)); arr = np.array(sil); arr[..., :3] = (arr[..., :3] * 0.2).astype(np.uint8); sil = Image.fromarray(arr)
    put(im, sil, 1500, 1300, shadowed=False); im.alpha_composite(blob(700, 700, (200, 30, 40), 70, 90), (1150, 350))
    k = actor_sprite({"who": "kir", "x": 0.3, "e": "shock", "m": "scream", "a": "up", "sweat": True, "s": 1.45}, 0); put(im, k, 520, 1240)
    w = sh_watch80({"text": "7 д 00:00", "red": True}, 0, 1).crop((540, 240, 1380, 840)).resize((420, 300)); im.alpha_composite(w, (1460, 40))
    d = ImageDraw.Draw(im); f = F("Inter-Black", 170)
    d.text((W // 2 - 220 + 8, 190), "40 ЛЕТ НАЗАД", font=f, fill=(0, 0, 0), anchor="mm", stroke_width=18, stroke_fill=(0, 0, 0)); d.text((W // 2 - 220, 180), "40 ЛЕТ НАЗАД", font=f, fill=(255, 210, 60), anchor="mm", stroke_width=16, stroke_fill=INK)
    lbl = F("Inter-Black", 72); tx = "7 ДНЕЙ, ЧТОБЫ ВЕРНУТЬСЯ"; tw = d.textlength(tx, font=lbl)
    d.rounded_rectangle((W // 2 - 220 - tw / 2 - 30, 300, W // 2 - 220 + tw / 2 + 30, 400), 20, fill=(200, 40, 40)); d.text((W // 2 - 220, 350), tx, font=lbl, fill=WHITE, anchor="mm")
    im.alpha_composite(vignette(160)); return im
