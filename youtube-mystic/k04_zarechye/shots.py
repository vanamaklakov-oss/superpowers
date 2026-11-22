# «Изометрия»: деревня собирается сама, потом ночь и свет в одном доме.
TW, TH = 90, 52; OX, OY = 652, 700; SC = 0.62
def iso(i, j, z=0): return OX + (i - j) * TW / 2, OY + (i + j) * TH / 2 - z
HOUSES = [(1, 2), (1, 4), (1, 6), (1, 8), (3, 2), (3, 4), (3, 6), (3, 8), (1, 10), (3, 10), (1, 12), (3, 12), (5, 1), (5, 11)]
TREES = [(6, 3), (7, 5), (6, 7), (7, 9), (8, 11), (6, 12), (0, 0), (4, 0), (7, 1), (8, 7)]
def house(d, i, j, s, lit, night):
    x, y = iso(i + 0.5, j + 0.5); w, h, hh = 62 * s * SC, 36 * s * SC, 60 * s * SC
    wall_l = (196, 140, 96) if not night else (70, 56, 54); wall_r = (166, 112, 76) if not night else (52, 42, 42); roof = (170, 60, 50) if not night else (70, 34, 34)
    d.polygon((x - w, y - hh, x, y - hh + h, x, y + h, x - w, y), fill=wall_l, outline=INK)
    d.polygon((x, y - hh + h, x + w, y - hh, x + w, y, x, y + h), fill=wall_r, outline=INK)
    d.polygon((x - w, y - hh, x, y - hh - h * 1.6, x, y - hh + h), fill=roof, outline=INK); d.polygon((x, y - hh - h * 1.6, x + w, y - hh, x, y - hh + h), fill=tuple(int(c * 0.8) for c in roof), outline=INK)
    wc = (255, 214, 110) if lit else ((120, 170, 210) if not night else (30, 34, 50))
    d.polygon((x + w * 0.3, y - hh * 0.6 + h * 0.4, x + w * 0.7, y - hh * 0.6 + h * 0.15, x + w * 0.7, y - hh * 0.2 + h * 0.15, x + w * 0.3, y - hh * 0.2 + h * 0.4), fill=wc)
def sh_iso(p, lt, D):
    night = p.get("night"); im = grad((150, 200, 240), (230, 240, 250)) if not night else grad((10, 12, 30), (24, 26, 50)); d = ImageDraw.Draw(im)
    for i in range(9):
        for j in range(14):
            pts = [iso(i, j), iso(i + 1, j), iso(i + 1, j + 1), iso(i, j + 1)]; road = i == 2 or (i == 4 and j > 0)
            g = (110, 170, 90) if (i + j) % 2 else (100, 160, 84)
            if night: g = tuple(int(c * 0.35) for c in g)
            col = ((190, 170, 130) if not night else (60, 56, 50)) if i == 2 else g
            d.polygon(pts, fill=col, outline=tuple(int(c * 0.85) for c in col))
    a, b, c = iso(0, 14), iso(9, 14), iso(9, 14, -60); d.polygon((iso(0, 14), iso(9, 14), (b[0], b[1] + 40), (a[0], a[1] + 40)), fill=(90, 70, 50) if not night else (30, 24, 20))
    a, b = iso(9, 0), iso(9, 14); d.polygon((a, b, (b[0], b[1] + 40), (a[0], a[1] + 40)), fill=(110, 86, 60) if not night else (36, 28, 22))
    items = [("h", k, xy) for k, xy in enumerate(HOUSES)] + [("t", k, xy) for k, xy in enumerate(TREES)]
    items.sort(key=lambda it: it[2][0] + it[2][1])
    for kind, k, (i, j) in items:
        s = 1.0
        if p.get("build"): s = eout((lt - (k * 0.16 if kind == "h" else 1.2 + k * 0.08)) / 0.35) * (1 + 0.15 * math.sin(min(1, max(0, lt - k * 0.16)) * 9) * 0.3)
        if s <= 0: continue
        if kind == "h": house(d, i, j, s, k in (p.get("lit") or []), night)
        else:
            x, y = iso(i + 0.5, j + 0.5); tc = (40, 110, 60) if not night else (14, 34, 22)
            s *= SC; d.rectangle((x - 5, y - 30 * s, x + 5, y), fill=(90, 60, 40)); d.polygon((x - 40 * s, y - 30 * s, x, y - 150 * s, x + 40 * s, y - 30 * s), fill=tc, outline=INK)
    if night:
        x, y = iso(5.5, 1.5); im.alpha_composite(blob(600, 500, (255, 200, 100), 110, 70), (int(x - 300), int(y - 300)))
    if p.get("bus"):
        u = (lt * 0.12) % 1; x, y = iso(2.5, 14 * u); d.rounded_rectangle((x - 40, y - 50, x + 40, y), 10, fill=(230, 200, 60), outline=INK, width=4)
    if p.get("eyes") and int(lt * 1.5) % 4 != 3:
        x, y = iso(7.3, 1.2); d.ellipse((x - 16, y - 80, x - 4, y - 70), fill=(255, 240, 160)); d.ellipse((x + 6, y - 80, x + 18, y - 70), fill=(255, 240, 160))
    label(im, "ЗАРЕЧЬЕ", 540, 380, WHITE, F("Inter-Black", 90))
    return im
