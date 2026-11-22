# «Рентген»: разрез Земли со скважиной.
CY = (90, 220, 255)
def kmy(km): return 360 + km * 86
def sh_xray(p, lt, D):
    im = grad((6, 14, 30), (2, 6, 14)); d = ImageDraw.Draw(im)
    layers = [(0, 2.5, (40, 70, 90), "осадочные"), (2.5, 7, (30, 56, 80), "гранит"), (7, 14, (24, 44, 70), "гнейс, базальт")]
    for a, b, c, nm in layers:
        d.rectangle((0, kmy(a), W, kmy(b)), fill=c); d.text((60, kmy(a) + 30), nm, font=F("Inter-Bold", 34), fill=(120, 190, 230))
    for y in range(int(kmy(0)), H, 18): d.line((0, y, W, y), fill=(0, 0, 0, 40), width=1)
    for km in range(0, 15, 2):
        y = kmy(km); d.line((W - 160, y, W - 120, y), fill=CY, width=4); d.text((W - 110, y), f"{km} км", font=F("Inter-Bold", 30), fill=CY, anchor="lm")
    d.rectangle((0, 0, W, kmy(0)), fill=(10, 20, 36))
    for i in range(5): d.line((500 + i * 20, kmy(0), 540, 160), fill=CY, width=3)
    dep = p.get("depth", 1) * (0.85 + 0.15 * eout(lt / 1.0)); y1 = kmy(dep)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.line((540, kmy(0), 540, y1), fill=CY + (255,), width=10)
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(im); d.line((540, kmy(0), 540, y1), fill=(220, 250, 255), width=4)
    d.ellipse((520, y1 - 20, 560, y1 + 20), fill=(255, 255, 255)); im.alpha_composite(blob(200, 200, CY, 140, 30), (440, int(y1 - 100)))
    if p.get("depth", 0) >= 6: d.text((600, kmy(6)), "← планктон", font=F("Inter-Black", 40), fill=YEL, anchor="lm")
    if p.get("heat"):
        im.alpha_composite(blob(900, 500, (255, 60, 20), int(120 + 40 * math.sin(lt * 6)), 70), (90, int(y1 - 250))); d = ImageDraw.Draw(im)
        d.rounded_rectangle((140, 1000, 220, 1500), 40, fill=(30, 30, 40), outline=WHITE, width=6); d.rounded_rectangle((160, 1460 - 440 * eout(lt / 1.2), 200, 1480), 20, fill=(240, 60, 40))
        d.text((250, 1060), "180 °C", font=F("Inter-Black", 90), fill=(255, 90, 60), anchor="lm"); d.text((250, 1160), "ждали 100", font=F("Inter-Bold", 44), fill=(200, 200, 210), anchor="lm")
    if p.get("mantle"):
        d.polygon((520, 1700, 560, 1700, 540, 1780), fill=YEL); d.text((540, 1630), "до мантии ещё ≈20 км", font=F("Inter-Black", 46), fill=YEL, anchor="mm")
    y = (lt * 500) % H; im.alpha_composite(blob(W + 400, 120, CY, 50, 30), (-200, int(y - 60)))
    label(im, f"{int(dep * 1000):,} м".replace(",", " "), 540, 240, WHITE, F("Inter-Black", 110))
    return im
def sh_lid(p, lt, D):
    im = grad((150, 160, 170), (100, 106, 112)); d = ImageDraw.Draw(im)
    for i in range(200): x, y = rng.integers(0, W), rng.integers(0, H); d.ellipse((x, y, x + 6, y + 6), fill=(120, 124, 130))
    d.ellipse((240, 660, 840, 1260), fill=(90, 70, 60), outline=INK, width=10); d.ellipse((300, 720, 780, 1200), fill=(110, 84, 66), outline=(70, 50, 40), width=8)
    for k in range(12): a = k * math.pi / 6; x, y = 540 + 270 * math.cos(a), 960 + 270 * math.sin(a); d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(70, 60, 56), outline=INK, width=4)
    for i in range(40): x, y = 300 + rng.integers(0, 480), 720 + rng.integers(0, 480); d.ellipse((x, y, x + 14, y + 10), fill=(150, 80, 40))
    for i in range(60): x = (i * 97 + lt * 60) % W; y = (i * 151 + lt * 180) % H; d.ellipse((x, y, x + 8, y + 8), fill=(255, 255, 255, 200))
    im.alpha_composite(vignette(160)); return im
def sh_surface(p, lt, D):
    im = grad((40, 60, 110), (180, 190, 210)); d = ImageDraw.Draw(im); d.rectangle((0, 1250, W, H), fill=(220, 226, 232))
    for x in (380, 700):
        d.polygon((x, 1250, x + 120, 1250, x + 60, 520), outline=(40, 44, 54), width=10)
        for y in range(600, 1250, 70): d.line((x + 60 - (y - 520) / 12, y, x + 60 + (y - 520) / 12, y), fill=(40, 44, 54), width=6)
    d.rectangle((120, 1050, 380, 1250), fill=(120, 70, 50), outline=INK, width=6); d.rectangle((780, 1100, 1000, 1250), fill=(160, 160, 170), outline=INK, width=6)
    for i in range(80): x = (i * 131 + lt * 50) % W; y = (i * 71 + lt * 140) % H; d.ellipse((x, y, x + 7, y + 7), fill=(255, 255, 255, 220))
    label(im, "1970", 540, 300, YEL, F("Inter-Black", 120)); return im
def sh_fossil(p, lt, D):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im); d.ellipse((90, 510, 990, 1410), fill=(20, 40, 50))
    for i in range(14):
        x, y, r = 300 + (i * 173) % 480, 700 + (i * 97) % 500, 26 + (i % 3) * 12; a = lt * 0.4 + i
        d.ellipse((x - r, y - r, x + r, y + r), outline=(140, 240, 220), width=4)
        for k in range(10): b = a + k * 0.628; d.line((x + r * math.cos(b), y + r * math.sin(b), x + (r + 14) * math.cos(b), y + (r + 14) * math.sin(b)), fill=(140, 240, 220), width=3)
    d.ellipse((90, 510, 990, 1410), outline=(200, 200, 200), width=24); label(im, "≈6 км вниз", 540, 360, YEL, LBL); return im
def sh_width(p, lt, D):
    im = grad((40, 44, 54), (20, 22, 28)); d = ImageDraw.Draw(im); r = 230 * eout(lt / 0.6)
    d.ellipse((540 - r, 900 - r, 540 + r, 900 + r), fill=(0, 0, 0), outline=(140, 140, 150), width=14)
    d.rectangle((300, 1220, 780, 1300), fill=(240, 210, 90), outline=INK, width=6)
    for i in range(24): d.line((300 + i * 20, 1220, 300 + i * 20, 1250 if i % 5 else 1270), fill=INK, width=3)
    label(im, "23 см", 540, 1420, YEL, F("Inter-Black", 120)); label(im, "и 12 км вниз", 540, 520, WHITE, LBL); return im
def sh_hoax(p, lt, D):
    im = grad((60, 50, 40), (30, 24, 20)); d = ImageDraw.Draw(im)
    pg = Image.new("RGBA", (860, 1100), (236, 228, 208, 255)); pd = ImageDraw.Draw(pg)
    pd.text((430, 90), "ГАЗЕТА · 1989", font=F("Inter-Bold", 44), fill=(80, 70, 60), anchor="mm"); pd.line((40, 140, 820, 140), fill=INK, width=4)
    pd.text((430, 260), "БУРОВИКИ", font=F("Inter-Black", 96), fill=INK, anchor="mm"); pd.text((430, 380), "УСЛЫШАЛИ", font=F("Inter-Black", 96), fill=INK, anchor="mm"); pd.text((430, 500), "КРИКИ АДА", font=F("Inter-Black", 96), fill=(160, 30, 30), anchor="mm")
    for y in range(600, 1050, 40): pd.line((60, y, 800, y), fill=(160, 150, 130), width=8)
    pg = pg.rotate(-3, expand=True, resample=Image.BICUBIC); im.alpha_composite(pg, (100, 360))
    if p.get("stamp"):
        s = 1 + 1.4 * (1 - eout(lt / 0.15)); st = Image.new("RGBA", (700, 240), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((10, 10, 690, 230), 24, outline=REDC, width=18); sd.text((350, 120), "УТКА", font=F("Inter-Black", 170), fill=REDC, anchor="mm")
        st = st.rotate(14, expand=True, resample=Image.BICUBIC); st = st.resize((int(st.width * s), int(st.height * s))); im.alpha_composite(st, (int(540 - st.width / 2), int(900 - st.height / 2)))
    return im
