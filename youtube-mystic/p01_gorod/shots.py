# Плоский вектор без контуров, 4 слоя параллакса, день → ночь, ходьба «на двойках».
def mix(a, b, t): return tuple(int(x + (y - x) * t) for x, y in zip(a, b))
DAY = dict(sky0=(236, 200, 160), sky1=(250, 226, 190), far=(201, 160, 130), mid=(217, 195, 163), mid2=(224, 122, 95), roof=(92, 64, 51), road=(150, 120, 100), walk=(190, 160, 130), fg=(110, 80, 60), win=(140, 170, 190))
NIGHT = dict(sky0=(18, 22, 40), sky1=(43, 58, 74), far=(30, 38, 56), mid=(43, 58, 74), mid2=(60, 50, 64), roof=(20, 24, 36), road=(30, 34, 44), walk=(44, 50, 62), fg=(14, 16, 24), win=(30, 36, 52))
LIGHT = (244, 162, 97)
def pal(t): return {k: mix(DAY[k], NIGHT[k], t) for k in DAY}
def layer_far(c):
    im = Image.new("RGBA", (2400, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(im); g = np.random.default_rng(5)
    x = 0
    while x < 2400: w = int(g.integers(120, 260)); h = int(g.integers(300, 760)); d.rectangle((x, 900 - h, x + w, 900), fill=c); x += w + int(g.integers(0, 30))
    return im
HOUSES = []
_g = np.random.default_rng(11); _x = 0
while _x < 4000: _w = int(_g.integers(300, 460)); HOUSES.append((_x, _w, int(_g.integers(520, 820)), int(_g.integers(0, 2)))); _x += _w + int(_g.integers(40, 120))
def sh_walk(p, lt, D):
    T = p["t0"] + lt; td = p.get("tod0", 0) + (p.get("tod", 0) - p.get("tod0", 0)) * ease(lt / 1.6); P = pal(td)
    im = grad(P["sky0"], P["sky1"]); d = ImageDraw.Draw(im)
    if td > 0.6:
        for i in range(60): x, y = (i * 211) % W, (i * 97) % 900; d.ellipse((x, y, x + 4, y + 4), fill=(255, 255, 255, int(200 * (td - 0.6) / 0.4)))
    else: d.ellipse((760, 260, 940, 440), fill=mix((255, 236, 190), (255, 210, 160), td))
    walking = not p.get("stop"); speed = 260 if walking else 0
    camx = (p["t0"] * 260 + (lt * speed if walking else 0))
    fl = layer_far(P["far"]); ox = -int(camx * 0.2) % 1200; im.alpha_composite(fl, (-ox, 620)); im.alpha_composite(fl, (2400 - ox, 620))
    # средний план: дома
    gy = 1440; d = ImageDraw.Draw(im)
    for i, (hx, hw, hh, kind) in enumerate(HOUSES):
        x = hx - camx * 0.55 % 4000
        if x > W + 50 or x + hw < -50: continue
        wall = P["mid"] if kind else P["mid2"]; d.rectangle((x, gy - hh, x + hw, gy), fill=wall); d.polygon((x - 20, gy - hh, x + hw / 2, gy - hh - 140, x + hw + 20, gy - hh), fill=P["roof"])
        d.rectangle((x + hw - 40, gy - hh, x + hw, gy), fill=mix(wall, (0, 0, 0), 0.12))
        for r in range(int((hh - 120) / 150)):
            for cidx in range(int((hw - 60) / 110)):
                wx, wy = x + 40 + cidx * 110, gy - hh + 60 + r * 150; lit = False
                if p.get("wave"): lit = lt > 0.6 + ((wx + camx * 0.55) % 900) / 900 * 1.2
                elif p.get("tod0", 0) >= 1: lit = True
                d.rectangle((wx, wy, wx + 60, wy + 80), fill=LIGHT if lit else P["win"])
                if lit: im.alpha_composite(blob(160, 180, LIGHT, 70, 25), (int(wx - 50), int(wy - 50))); d = ImageDraw.Draw(im)
    # неон
    nx = 2600 - camx * 0.55 % 4000
    if -300 < nx < W:
        on = td > 0.4 and int(T * 7) % 9 != 0; d.rounded_rectangle((nx, gy - 470, nx + 280, gy - 380), 16, fill=(30, 30, 40))
        d.text((nx + 140, gy - 425), "ОТКРЫТО", font=F("Inter-Black", 46), fill=(255, 80, 160) if on else (90, 60, 80), anchor="mm")
        if on: im.alpha_composite(blob(420, 220, (255, 80, 160), 70, 40), (int(nx - 70), gy - 535)); d = ImageDraw.Draw(im)
    # тротуар и дорога
    d.rectangle((0, gy, W, gy + 140), fill=P["walk"]); d.rectangle((0, gy + 140, W, H), fill=P["road"])
    for k in range(-1, 8): x = k * 300 - (camx * 1.0) % 300; d.rectangle((x, gy + 330, x + 150, gy + 345), fill=mix((240, 230, 210), (90, 90, 100), td))
    # фонари и люди
    for k in range(-1, 6):
        lx = k * 520 - (camx * 1.0) % 520 + 200
        d.rectangle((lx, gy - 560, lx + 16, gy + 60), fill=mix((70, 60, 56), (20, 22, 30), td)); d.rectangle((lx - 40, gy - 580, lx + 40, gy - 556), fill=mix((70, 60, 56), (20, 22, 30), td))
        if td > 0.45:
            a = min(1, (td - 0.45) / 0.4); cone = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cone)
            cd.polygon(((lx - 30, gy - 556), (lx + 46, gy - 556), (lx + 230, gy + 120), (lx - 214, gy + 120)), fill=LIGHT + (int(70 * a),)); im.alpha_composite(cone.filter(ImageFilter.GaussianBlur(14)))
            d = ImageDraw.Draw(im); d.ellipse((lx - 24, gy - 566, lx + 40, gy - 540), fill=mix((200, 200, 200), (255, 230, 170), a))
        if p.get("people") and k in (1, 2, 3) and lx > 500:
            a = eout((lt - 0.3 - k * 0.25) / 0.5)
            if a > 0:
                fig = Image.new("RGBA", (200, 640), (0, 0, 0, 0)); fd = ImageDraw.Draw(fig)
                fd.ellipse((60, 0, 140, 100), fill=(8, 8, 12)); fd.rounded_rectangle((40, 90, 160, 460), 50, fill=(8, 8, 12)); fd.rectangle((60, 440, 90, 640), fill=(8, 8, 12)); fd.rectangle((110, 440, 140, 640), fill=(8, 8, 12))
                fd.ellipse((70, 42, 84, 52), fill=(255, 240, 200)); fd.ellipse((96, 42, 110, 52), fill=(255, 240, 200))
                fig.putalpha(fig.getchannel("A").point(lambda v: int(v * a))); im.alpha_composite(fig, (int(lx + 40), gy + 100 - 640)); d = ImageDraw.Draw(im)
    # герой
    ph = (int(T * 12) / 12 * 2.0) % 1 if walking else None
    im.alpha_composite(hero_side(ph, td), (240, gy + 150 - 945))
    # листья
    if td < 0.8:
        for i in range(14):
            x = (i * 167 - T * (90 + i * 7)) % (W + 100) - 50; y = (i * 241 + T * (120 + i * 9)) % H; a = T * 3 + i
            lf = Image.new("RGBA", (40, 24), (0, 0, 0, 0)); ImageDraw.Draw(lf).ellipse((0, 0, 40, 24), fill=(214, 110, 50) if i % 2 else (230, 160, 60)); lf = lf.rotate(math.degrees(a) % 360, expand=True)
            im.alpha_composite(lf, (int(x), int(y)))
    # передний план
    for k in range(-1, 5): x = k * 360 - (camx * 1.5) % 360; d.ellipse((x - 60, H - 170, x + 260, H + 90), fill=P["fg"])
    if p.get("plaque"):
        a = eout(lt / 0.35); s = p["plaque"]; f = F("Inter-Black", 86); tw = d.textlength(s, font=f)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); y = 260 - 40 * (1 - a)
        ld.rounded_rectangle((540 - tw / 2 - 40, y - 70, 540 + tw / 2 + 40, y + 70), 24, fill=(20, 22, 30, int(220 * a))); ld.text((540, y), s, font=f, fill=(255, 210, 120, int(255 * a)), anchor="mm"); im.alpha_composite(lay)
    return im
def hero_side(ph, td):
    key = ("hero", None if ph is None else round(ph, 3), round(td, 1))
    def mk():
        k = 2; im = Image.new("RGBA", (300 * k, 700 * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        skin = mix((236, 192, 150), (150, 120, 110), td * 0.6); hood = mix((60, 120, 140), (36, 70, 84), td * 0.6); pants = mix((50, 56, 80), (30, 34, 50), td * 0.6); hair = (60, 40, 30)
        sw = math.sin(2 * math.pi * ph) if ph is not None else 0
        def limb(cx, cy, ang, ln, w, col):
            ex, ey = cx + ln * math.sin(ang), cy + ln * math.cos(ang); d.line((cx * k, cy * k, ex * k, ey * k), fill=col, width=int(w * k)); d.ellipse(((ex - w / 2) * k, (ey - w / 2) * k, (ex + w / 2) * k, (ey + w / 2) * k), fill=col); return ex, ey
        hip = (150, 400)
        for sgn, shade in ((-1, 0.82), (1, 1.0)):
            a = 0.62 * sw * sgn; kx, ky = limb(hip[0], hip[1], a, 140, 42, mix(pants, (0, 0, 0), 1 - shade)); fx, fy = limb(kx, ky, a - 0.25 * max(0, -sw * sgn), 140, 38, mix(pants, (0, 0, 0), 1 - shade))
            d.rounded_rectangle(((fx - 16) * k, (fy - 8) * k, (fx + 40) * k, (fy + 16) * k), 10 * k, fill=(240, 240, 240) if shade == 1 else (200, 200, 200))
        limb(150, 210, -0.75 * sw, 120, 34, mix(hood, (0, 0, 0), 0.2)); 
        d.rounded_rectangle((95 * k, 180 * k, 205 * k, 420 * k), 48 * k, fill=hood); d.rectangle((95 * k, 380 * k, 205 * k, 420 * k), fill=mix(hood, (0, 0, 0), 0.15))
        ax, ay = limb(150, 210, 0.75 * sw, 120, 34, hood); d.ellipse(((ax - 15) * k, (ay - 10) * k, (ax + 15) * k, (ay + 20) * k), fill=skin)
        d.rectangle((140 * k, 150 * k, 166 * k, 190 * k), fill=skin)
        d.ellipse((100 * k, 40 * k, 210 * k, 165 * k), fill=skin); d.chord((96 * k, 30 * k, 214 * k, 130 * k), 180, 360, fill=hair); d.polygon((96 * k, 80 * k, 130 * k, 80 * k, 110 * k, 130 * k), fill=hair)
        d.ellipse((178 * k, 92 * k, 190 * k, 104 * k), fill=(30, 30, 30)); d.polygon((206 * k, 100 * k, 218 * k, 120 * k, 204 * k, 122 * k), fill=mix(skin, (0, 0, 0), 0.1))
        bob = 0 if ph is None else abs(math.cos(2 * math.pi * ph)) * 8
        out = im.resize((405, 945), Image.LANCZOS); o2 = Image.new("RGBA", (405, 945), (0, 0, 0, 0)); o2.alpha_composite(out, (0, int(-bob * 1.35 + 10))); return o2
    return cached(key, mk)
