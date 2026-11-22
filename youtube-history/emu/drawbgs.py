"""Code-drawn backgrounds for the Emu War short (fallback when the FLUX quota is spent): python3 drawbgs.py"""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter
W, H, HOR = 1080, 1920, 1050
HERE = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f"{HERE}/bgs", exist_ok=True)

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def base(ground_top, ground_bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(HOR): d.line([(0, y), (W, y)], fill=lerp((95, 160, 225), (250, 215, 160), (y / HOR) ** 1.4))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([600, 500, 1000, 900], fill=(255, 235, 170, 200))
    im.paste(g.filter(ImageFilter.GaussianBlur(90)), (0, 0), g.filter(ImageFilter.GaussianBlur(90))); d = ImageDraw.Draw(im)
    d.ellipse([740, 640, 860, 760], fill=(255, 245, 200))
    r = random.Random(2); pts = [(0, HOR)] + [(x, HOR - 40 - r.randint(0, 60) - 30 * math.sin(x / 170)) for x in range(0, W + 60, 60)] + [(W, HOR)]
    d.polygon(pts, fill=(170, 95, 70))
    for y in range(HOR, H): d.line([(0, y), (W, y)], fill=lerp(ground_top, ground_bot, (y - HOR) / (H - HOR)))
    return im, d

def wheat(d, seed=1, top=HOR):
    r = random.Random(seed)
    for _ in range(2600):
        y = r.uniform(top, H); s = 0.2 + (y - HOR) / (H - HOR) * 1.6; x = r.uniform(-20, W + 20)
        c = lerp((200, 150, 60), (250, 210, 100), r.random())
        d.line([(x, y), (x + r.uniform(-6, 6) * s, y - 40 * s)], fill=c, width=max(1, int(3 * s)))
        d.ellipse([x - 4 * s, y - 52 * s, x + 4 * s, y - 34 * s], fill=lerp(c, (255, 230, 140), 0.4))

def emu(d, x, y, s, flip=1, run=0.0):
    body = (70, 60, 55); dark = (45, 38, 35)
    leg = [(x - 10 * s, y - 60 * s), (x - 10 * s - 30 * s * math.sin(run), y)], [(x + 12 * s, y - 60 * s), (x + 12 * s + 30 * s * math.sin(run), y)]
    for a, b in leg: d.line([a, b], fill=(120, 95, 70), width=max(2, int(7 * s)))
    d.ellipse([x - 60 * s, y - 140 * s, x + 60 * s, y - 50 * s], fill=body, outline=dark, width=max(1, int(4 * s)))
    nx, ny = x + flip * 40 * s, y - 120 * s; hx, hy = x + flip * 62 * s, y - 230 * s
    d.line([(nx, ny), (hx, hy)], fill=(90, 110, 140), width=max(3, int(18 * s)))
    d.ellipse([hx - 18 * s, hy - 16 * s, hx + 18 * s, hy + 16 * s], fill=(90, 110, 140), outline=dark, width=max(1, int(3 * s)))
    d.polygon([(hx + flip * 14 * s, hy - 5 * s), (hx + flip * 40 * s, hy + 2 * s), (hx + flip * 14 * s, hy + 8 * s)], fill=(60, 50, 40))
    d.ellipse([hx + flip * 4 * s - 6 * s, hy - 9 * s, hx + flip * 4 * s + 6 * s, hy + 3 * s], fill=(255, 255, 255)); d.ellipse([hx + flip * 6 * s - 3 * s, hy - 6 * s, hx + flip * 6 * s + 3 * s, hy], fill=(0, 0, 0))

def house(d):
    d.rectangle([90, 820, 470, 1090], fill=(225, 205, 170), outline=(90, 70, 50), width=6)
    d.polygon([(60, 830), (280, 690), (500, 830)], fill=(160, 165, 170), outline=(90, 90, 95))
    for k in range(9): d.line([(80 + k * 48, 830 - (k < 5) * 0), (280, 690)], fill=(140, 145, 150), width=2)
    d.rectangle([150, 900, 230, 980], fill=(110, 160, 200), outline=(90, 70, 50), width=6); d.rectangle([320, 940, 400, 1090], fill=(120, 80, 50))
    d.line([(800, 1080), (840, 640)], fill=(90, 90, 95), width=10); d.line([(880, 1080), (840, 640)], fill=(90, 90, 95), width=10)
    for k in range(8): a = k * math.pi / 4 + 0.3; d.line([(840, 640), (840 + 120 * math.cos(a), 640 + 120 * math.sin(a))], fill=(200, 200, 205), width=12)
    d.ellipse([825, 625, 855, 655], fill=(80, 80, 85))

def truck(d, x, y, s=1.0):
    k = (40, 60, 40); d.rectangle([x, y - 200 * s, x + 330 * s, y - 70 * s], fill=(95, 105, 70), outline=(40, 45, 30), width=6)
    d.rectangle([x + 330 * s, y - 280 * s, x + 500 * s, y - 70 * s], fill=(110, 120, 80), outline=(40, 45, 30), width=6)
    d.rectangle([x + 360 * s, y - 250 * s, x + 470 * s, y - 170 * s], fill=(170, 210, 230), outline=(40, 45, 30), width=5)
    d.rectangle([x + 500 * s, y - 170 * s, x + 600 * s, y - 70 * s], fill=(95, 105, 70), outline=(40, 45, 30), width=6)
    for wx in (x + 100 * s, x + 470 * s): d.ellipse([wx - 70 * s, y - 140 * s, wx + 70 * s, y], fill=(30, 30, 30)); d.ellipse([wx - 30 * s, y - 100 * s, wx + 30 * s, y - 40 * s], fill=(140, 140, 140))
    d.line([(x + 120 * s, y - 200 * s), (x + 60 * s, y - 300 * s)], fill=(30, 30, 30), width=int(16 * s))

def dust(im, boxes):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for b in boxes: gd.ellipse(b, fill=(220, 180, 130, 170))
    g = g.filter(ImageFilter.GaussianBlur(40)); im.paste(g, (0, 0), g)

def finish(im, name):
    v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
    im = Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (40, 25, 15)), 0.5), v.filter(ImageFilter.GaussianBlur(200)))
    im.save(f"{HERE}/bgs/{name}.jpg", quality=93)

im, d = base((215, 165, 70), (240, 190, 90)); wheat(d, 1); finish(im, "wheat")
im, d = base((215, 165, 70), (240, 190, 90)); house(d); wheat(d, 2, top=1100); finish(im, "farm")
im, d = base((190, 110, 70), (215, 135, 85))
d.polygon([(560, 1150), (790, 820), (1040, 1150)], fill=(140, 140, 90), outline=(80, 80, 50)); d.polygon([(760, 1150), (790, 900), (820, 1150)], fill=(60, 60, 40))
for cx, cy in [(120, 1180), (230, 1210), (170, 1110)]: d.rectangle([cx, cy - 90, cx + 130, cy], fill=(150, 110, 60), outline=(80, 55, 30), width=6); d.line([(cx, cy - 45), (cx + 130, cy - 45)], fill=(80, 55, 30), width=4)
truck(d, 280, 1100, 0.55); finish(im, "camp")
im, d = base((190, 110, 70), (215, 135, 85))
d.polygon([(470, HOR), (610, HOR), (1080, H), (0, H)], fill=(170, 95, 60))
truck(d, 150, 1250, 1.2); dust(im, [(-100, 1050, 300, 1350), (-200, 1150, 250, 1450), (650, 1100, 1000, 1300)]); finish(im, "truck")
im, d = base((215, 165, 70), (240, 190, 90)); wheat(d, 3)
r = random.Random(5); flock = sorted([(r.uniform(-50, W + 50), r.uniform(HOR + 20, H - 40)) for _ in range(46)], key=lambda p: p[1])
for x, y in flock: s = 0.15 + (y - HOR) / (H - HOR) * 1.4; emu(d, x, y, s, flip=r.choice([-1, 1]), run=r.uniform(-0.6, 0.6))
dust(im, [(0, 980, 1080, 1150)]); finish(im, "emus")
print("ok")
