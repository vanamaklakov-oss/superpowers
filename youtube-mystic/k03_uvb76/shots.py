# «Глобус»: точечный шар с дугами к городам.
CITIES = [("Хельсинки", 60.2, 24.9), ("Берлин", 52.5, 13.4), ("Лондон", 51.5, -0.1), ("Нью-Йорк", 40.7, -74.0)]
SRC = (57.0, 30.0)
def v3(lat, lon):
    la, lo = math.radians(lat), math.radians(lon); return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
def proj(v, rot, R=430, cx=540, cy=860):
    lo0, la0 = rot; c, s = math.cos(-lo0), math.sin(-lo0); x, y, z = v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2]
    c2, s2 = math.cos(-la0), math.sin(-la0); x, z = x * c2 - z * s2, x * s2 + z * c2
    return cx + R * y, cy - R * z, x
def sh_globe(p, lt, D):
    im = grad((6, 10, 26), (2, 4, 12)); d = ImageDraw.Draw(im); rot = (math.radians(-5 + lt * 2), math.radians(35))
    im.alpha_composite(blob(1100, 1100, (40, 90, 200), 60, 80), (-10, 310))
    for la in range(-80, 90, 6):
        for lo in range(-180, 180, 6):
            X, Y, Z = proj(v3(la, lo), rot)
            if Z > 0: r = 2 + 3 * Z; d.ellipse((X - r, Y - r, X + r, Y + r), fill=(80, 140, 230) if not p.get("dim") else (50, 70, 110))
    sx, sy, _ = proj(v3(*SRC), rot); n = p.get("arcs", 0)
    for i, (nm, la, lo) in enumerate(CITIES[:n]):
        u = eout((lt - i * 1.0) / 0.9)
        if u <= 0: continue
        a, b = v3(*SRC), v3(la, lo); om = math.acos(np.clip(a @ b, -1, 1)); pts = []
        for k in range(int(40 * u) + 1):
            t = k / 40; v = (math.sin((1 - t) * om) * a + math.sin(t * om) * b) / math.sin(om); v = v * (1 + 0.25 * math.sin(math.pi * t) * om)
            X, Y, Z = proj(v, rot); pts.append((X, Y))
        if len(pts) > 1: d.line(pts, fill=(255, 200, 80), width=6)
        if u >= 1: X, Y, _ = proj(b, rot); d.ellipse((X - 12, Y - 12, X + 12, Y + 12), fill=WHITE); d.text((X + 18 if i % 2 else X - 18, Y + (i - 1.5) * 20), nm, font=F("Inter-Black", 40), fill=WHITE, anchor="lm" if i % 2 else "rm", stroke_width=6, stroke_fill=INK)
    r = 18 + 8 * math.sin(lt * 6); d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=REDC); im.alpha_composite(blob(260, 260, (255, 60, 60), 140, 40), (int(sx - 130), int(sy - 130)))
    label(im, "УВБ-76 · ?", sx, sy - 70, WHITE, LBS, bg=(150, 30, 30))
    return im
def sh_radio(p, lt, D):
    im = grad((40, 30, 26), (16, 12, 10)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 560, 990, 1360), 50, fill=(120, 80, 50), outline=INK, width=10); d.rounded_rectangle((150, 620, 930, 900), 20, fill=(10, 20, 14), outline=INK, width=6)
    pts = []
    for x in range(160, 920, 4):
        t = lt + x / 900
        if p.get("voice"): amp = 90 * abs(math.sin(t * 7)) * (0.5 + 0.5 * math.sin(x * 0.3 + lt * 30))
        else: amp = 100 * (1 if (t * 1.2) % 1 < 0.35 else 0.05) * math.sin(x * 0.9)
        pts.append((x, 760 + amp))
    d.line(pts, fill=(90, 255, 140) if not p.get("voice") else (255, 90, 90), width=4)
    d.rounded_rectangle((150, 960, 930, 1060), 16, fill=(230, 210, 160), outline=INK, width=6)
    for i in range(30): d.line((170 + i * 25, 970, 170 + i * 25, 990 if i % 5 else 1005), fill=INK, width=3)
    d.line((600, 960, 600, 1060), fill=REDC, width=8); d.text((540, 1180), "4625 кГц", font=F("Inter-Black", 110), fill=YEL, anchor="mm")
    for x in (260, 820): d.ellipse((x - 60, 1220, x + 60, 1340), fill=(60, 40, 30), outline=INK, width=6)
    if p.get("voice"): label(im, "ГОЛОС", 540, 420, WHITE, LBL, bg=(170, 30, 30))
    else: label(im, "ЖЖЖЖЖ…", 540, 420, YEL, LBL)
    return im
def sh_code(p, lt, D):
    im = Image.new("RGBA", (W, H), (8, 10, 14, 255)); d = ImageDraw.Draw(im)
    lines = ["Я УВБ-76…", "ЛАДОГА · 84 51 27", "ВЕТЕР · 09 33 61", "КОНЕЦ"]
    for i, s in enumerate(lines):
        n = int(max(0, lt * 30 - i * 14)); d.text((120, 600 + i * 150), s[:n], font=F("Inter-Black", 76), fill=(200, 255, 210))
    label(im, "так это звучит (пример)", 540, 360, (180, 180, 190), LBS); return im
