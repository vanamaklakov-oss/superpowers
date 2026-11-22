# «Масштаб»: от одного дерева до карты вывала.
TAIGA = (52, 86, 56)
def radial(d, cx, cy, n, r0, r1, ln, col, w, seed=3):
    g = np.random.default_rng(seed)
    for i in range(n):
        a = g.random() * 2 * math.pi; r = r0 + (r1 - r0) * math.sqrt(g.random()); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line((x, y, x + ln * math.cos(a), y + ln * math.sin(a)), fill=col, width=w)
def sh_tree(p, lt, D):
    im = grad((230, 190, 150), (150, 170, 150)); d = ImageDraw.Draw(im); d.rectangle((0, 1150, W, H), fill=(90, 110, 70))
    for x in range(-40, W, 140): d.polygon((x, 1150, x + 70, 820, x + 140, 1150), fill=(40, 70, 50))
    ang = -0.15 if not p.get("blast") else -0.15 - 1.3 * ease(lt / 0.5)
    tr = Image.new("RGBA", (1400, 140), (0, 0, 0, 0)); td = ImageDraw.Draw(tr); td.rounded_rectangle((0, 20, 1400, 120), 50, fill=(110, 76, 50), outline=INK, width=8)
    for x in range(60, 1400, 90): td.arc((x, 30, x + 60, 110), 200, 340, fill=(80, 54, 34), width=6)
    tr = tr.rotate(math.degrees(-ang) - 90, expand=True, resample=Image.BICUBIC); im.alpha_composite(tr, (int(540 - tr.width / 2 + 300), int(1400 - tr.height)))
    if p.get("blast") and lt < 1.2:
        for i in range(12): y = 300 + i * 90; x = (lt * 2600 + i * 200) % (W + 400) - 200; d.line((x, y, x + 300, y), fill=(255, 240, 220, 200), width=8)
    label(im, "30.06.1908", 540, 260, YEL, F("Inter-Black", 100)); return im
def sh_forest(p, lt, D):
    im = Image.new("RGBA", (W, H), TAIGA + (255,)); d = ImageDraw.Draw(im); z = p.get("zoom", 0); cx, cy = 540, 960
    if z == 0:
        radial(d, -400, 960, 900, 300, 1700, 70, (120, 86, 56), 10)
        d.line((420, 1000, 560, 1000), fill=YEL, width=14); label(im, "наше дерево", 490, 1080, YEL, LBS)
    else:
        radial(d, cx, cy, 3200, 60, 1200, 26, (126, 92, 60), 4); im.alpha_composite(blob(260, 260, (255, 220, 120), 150, 40), (cx - 130, cy - 130))
        if p.get("center"): label(im, "кратера нет", cx, cy - 200, WHITE, LBL, bg=INK)
    return im
def sh_map(p, lt, D):
    im = Image.new("RGBA", (W, H), (40, 74, 50, 255)); d = ImageDraw.Draw(im)
    for i in range(400): x, y = rng.integers(0, W), rng.integers(0, H); d.ellipse((x, y, x + 10, y + 10), fill=(34, 64, 44))
    d.line([(x, 300 + 200 * math.sin(x / 300)) for x in range(-20, W + 40, 40)], fill=(70, 130, 190), width=16)
    sc = 0.45 if p.get("zoom") == 0 else 1.0; cx, cy = 540, 1000
    pts = []
    for k in range(64):
        a = k / 64 * 2 * math.pi; r = 330 * (1 + 0.35 * math.cos(2 * a)) * (1 + 0.1 * math.sin(3 * a)); pts.append((cx + r * math.cos(a) * sc, cy + r * 0.75 * math.sin(a) * sc))
    d.polygon(pts, fill=(130, 96, 64), outline=(240, 200, 120)); radial(d, cx, cy, 900, 10, 300 * sc, 10, (100, 70, 44), 3)
    if p.get("moscow"):
        a = eout(lt / 0.5); m = Image.new("RGBA", (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(m); r = 210
        md.ellipse((cx - r, cy - r * 0.9, cx + r, cy + r * 0.9), fill=(220, 60, 60, int(130 * a)), outline=(255, 255, 255, int(255 * a)), width=8); im.alpha_composite(m)
        label(im, "Москва в МКАД", cx, cy, WHITE, LBS, bg=INK, a=a)
    label(im, "≈2150 км²" if p.get("zoom") else "80 млн деревьев", 540, 300, YEL, F("Inter-Black", 96), bg=INK)
    return im
def sh_sky(p, lt, D):
    im = grad((40, 50, 100), (240, 170, 120)); d = ImageDraw.Draw(im); d.rectangle((0, 1500, W, H), fill=(30, 54, 40))
    for x in range(-40, W, 70): d.polygon((x, 1500, x + 35, 1380, x + 70, 1500), fill=(24, 44, 34))
    if p.get("q"):
        for i, (t_, y) in enumerate((("метеорит?", 600), ("комета?", 800), ("ледяная глыба?", 1000))): label(im, t_, 540, y, WHITE, LBL, bg=INK, a=eout((lt - i * 0.4) / 0.3))
        return im
    u = ease(lt / max(D * 0.7, 0.5)); x, y = -100 + 900 * u, 100 + 700 * u
    tail = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tail); td.line((x - 500, y - 390, x, y), fill=(255, 220, 160, 200), width=40); im.alpha_composite(tail.filter(ImageFilter.GaussianBlur(18)))
    im.alpha_composite(blob(260, 260, (255, 250, 220), 255, 30), (int(x - 130), int(y - 130)))
    if u > 0.95: im.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 230, int(230 * (1 - (lt - D * 0.7) / 0.6)) if lt < D * 0.7 + 0.6 else 0)))
    label(im, "взрыв в воздухе", 540, 1700, WHITE, LBL, bg=INK); return im
def sh_poles(p, lt, D):
    im = grad((200, 190, 170), (150, 150, 140)); d = ImageDraw.Draw(im); d.rectangle((0, 1300, W, H), fill=(90, 90, 70))
    for i in range(9): x = 80 + i * 115; d.rectangle((x, 500 + (i % 3) * 40, x + 26, 1320), fill=(90, 70, 56), outline=INK, width=4)
    for i in range(10): x = i * 120 - 60; d.line((x, 1460, x + 220, 1400 + (i % 2) * 30), fill=(110, 80, 56), width=22)
    label(im, "«телеграфный лес»", 540, 300, YEL, LBL, bg=INK); return im
