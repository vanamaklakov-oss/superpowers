# «Рентген» для пирамиды: разрез, мюоны, пустота, коридор.
CY = (90, 220, 255)
AP, BL, BR = (540, 330), (40, 1330), (1040, 1330)
def pyr_base():
    def mk():
        im = grad((6, 14, 30), (2, 6, 14)); d = ImageDraw.Draw(im)
        d.polygon((AP, BL, BR), fill=(26, 50, 74), outline=CY)
        for y in range(360, 1330, 40):
            t = (y - 330) / 1000; d.line((540 - 500 * t, y, 540 + 500 * t, y), fill=(36, 66, 92), width=2)
        d.rectangle((0, 1330, W, H), fill=(12, 24, 36))
        d.polygon(((470, 1100), (610, 1100), (610, 1050), (470, 1050)), outline=CY)            # камера царицы
        d.line((420, 1180, 520, 980), fill=CY, width=14)                                        # Большая галерея (наклон)
        d.rectangle((520, 920, 640, 980), outline=CY, width=4)                                  # камера царя
        d.line((300, 1160, 520, 1240), fill=CY, width=4); d.line((300, 1160, 330, 1060), fill=CY, width=4)  # нисходящий/восходящий
        for t_, (x, y) in (("камера царя", (660, 950)), ("Большая галерея", (300, 1010)), ("камера царицы", (630, 1080))): d.text((x, y), t_, font=F("Inter-Bold", 30), fill=(140, 200, 230), anchor="lm")
        return im
    return cached(("pyr",), mk)
def sh_pyr(p, lt, D):
    im = pyr_base().copy(); d = ImageDraw.Draw(im)
    if p.get("muons"):
        for i in range(26):
            x0 = (i * 83) % W; ph = (lt * 1.4 + i * 0.13) % 1; y = -40 + ph * 1600; x = x0 + ph * 120
            d.line((x, y, x + 12, y + 90), fill=(255, 240, 160), width=4)
        for x in (200, 540, 880): d.rounded_rectangle((x - 60, 1380, x + 60, 1440), 10, fill=(60, 70, 90), outline=WHITE, width=4)
    if p.get("scan"):
        y = 330 + ((lt * 400) % 1000); im.alpha_composite(blob(1300, 140, CY, 60, 30), (-110, int(y - 70)))
    v = p.get("void", 0) * eout(lt / 0.8) if not p.get("void_static") else p.get("void", 0)
    if v > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.polygon(((420, 880), (600, 760), (640, 790), (460, 910)), fill=(255, 220, 100, int(220 * v))); im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
        im.alpha_composite(blob(520, 400, (255, 200, 80), int(110 * v), 50), (270, 640)); d = ImageDraw.Draw(im)
        d.text((660, 760), "≥ 30 м", font=F("Inter-Black", 54), fill=YEL, anchor="lm")
        if p.get("q"): label(im, "?", 530, 830, WHITE, F("Inter-Black", 160))
    if p.get("corridor"):
        a = eout(lt / 0.6); d.line((250, 1080, 250 + 110 * a, 1080), fill=(120, 255, 160), width=18); d.text((300, 1020), "коридор ≈9 м", font=F("Inter-Black", 40), fill=(120, 255, 160), anchor="mm")
    label(im, "ПИРАМИДА ХЕОПСА", 540, 200, WHITE, LBL); return im
def sh_detector(p, lt, D):
    im = grad((14, 18, 30), (4, 6, 12)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((180, 760, 900, 1200), 30, fill=(60, 70, 90), outline=WHITE, width=8)
    for i in range(8): d.rectangle((220 + i * 82, 820, 280 + i * 82, 1140), fill=(30, 40, 56), outline=CY, width=3)
    for i in range(6):
        ph = (lt * 1.2 + i * 0.17) % 1; x = 260 + i * 110; d.line((x - 60 + 120 * ph, -40 + 1300 * ph, x - 50 + 120 * ph, 50 + 1300 * ph), fill=(255, 240, 160), width=6)
        if 0.6 < ph < 0.7: im.alpha_composite(blob(200, 200, CY, 160, 30), (x - 40, 880))
    label(im, "мюоны из космоса", 540, 520, YEL, LBL); return im
def sh_endoscope(p, lt, D):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im); cx, cy, R = 540, 900, 460
    view = grad((120, 96, 60), (40, 30, 20), 2 * R, 2 * R); vd = ImageDraw.Draw(view); z = 1 + lt * 0.08
    for k in range(6):
        s = (k + 1) / 6 / z; vd.rectangle((R - R * s, R - R * s * 0.8, R + R * s, R + R * s * 0.8), outline=(70, 54, 36), width=10)
    vd.polygon((0, 0, R, R * 0.2, 2 * R, 0), fill=(150, 120, 80)); vd.polygon((0, 0, R, R * 0.35, 0, 2 * R), fill=(96, 74, 48))
    m = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * R, 2 * R), fill=255); im.paste(view, (cx - R, cy - R), m)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(60, 60, 60), width=16); d.text((120, 300), "REC ● 2023", font=F("Inter-Black", 44), fill=(255, 80, 80))
    label(im, "эндоскоп", 540, 1460, WHITE, LBS, bg=INK); return im
