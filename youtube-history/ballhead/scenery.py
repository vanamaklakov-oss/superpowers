"""Code-drawn 9:16 backgrounds for when the FLUX quota is spent: python3 ballhead/scenery.py <name> <out.jpg>
Names: forest, mine, snow, harbor, field, road."""
import sys, math, random
from PIL import Image, ImageDraw, ImageFilter
W, H, HOR = 1080, 1920, 1050

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def sky(im, top, bot, sun=True):
    d = ImageDraw.Draw(im)
    for y in range(HOR): d.line([(0, y), (W, y)], fill=lerp(top, bot, (y / HOR) ** 1.4))
    if sun:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([600, 480, 1000, 880], fill=(255, 235, 170, 190))
        g = g.filter(ImageFilter.GaussianBlur(90)); im.paste(g, (0, 0), g); ImageDraw.Draw(im).ellipse([740, 620, 860, 740], fill=(255, 245, 210))
def ground(im, top, bot, y0=HOR):
    d = ImageDraw.Draw(im)
    for y in range(y0, H): d.line([(0, y), (W, y)], fill=lerp(top, bot, (y - y0) / (H - y0)))
def finish(im, out):
    v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
    im = Image.composite(im, Image.blend(im, Image.new("RGB", (W, H), (25, 20, 15)), 0.5), v.filter(ImageFilter.GaussianBlur(200)))
    im.save(out, quality=93)
def pine(d, x, y, s, c=(40, 90, 55), snow=False):
    d.rectangle([x - 8 * s, y - 40 * s, x + 8 * s, y], fill=(90, 60, 40))
    for k in range(3):
        w, top = (90 - k * 22) * s, y - (40 + k * 70) * s
        d.polygon([(x - w, top), (x, top - 130 * s), (x + w, top)], fill=lerp(c, (20, 50, 30), k * 0.15))
        if snow: d.polygon([(x - w * 0.35, top - 85 * s), (x, top - 130 * s), (x + w * 0.35, top - 85 * s)], fill=(245, 248, 255))

def forest():
    im = Image.new("RGB", (W, H)); sky(im, (110, 170, 220), (240, 220, 180)); ground(im, (70, 110, 60), (50, 85, 45)); d = ImageDraw.Draw(im)
    d.rectangle([0, HOR - 40, W, HOR + 30], fill=(80, 140, 190))   # lake strip
    r = random.Random(4)
    for _ in range(90):
        y = r.uniform(HOR - 10, H + 100); s = 0.25 + (y - HOR) / (H - HOR) * 1.6; x = r.uniform(-50, W + 50)
        if 260 < x < 820 and y > 1350: continue    # keep a clearing for the cast
        pine(d, x, y, s, c=lerp((40, 100, 60), (30, 80, 45), r.random()))
    return im
def mine():
    im = Image.new("RGB", (W, H), (35, 28, 24)); d = ImageDraw.Draw(im)
    for r in range(30, 0, -1):   # tunnel receding into darkness
        t = r / 30; w, h = 520 * t + 40, 760 * t + 60; cy = 900 + 260 * t
        d.rounded_rectangle([W / 2 - w, cy - h, W / 2 + w, cy + h * 0.6], radius=int(w * 0.5), fill=lerp((10, 8, 8), (95, 70, 50), t))
    for k, t in enumerate([1.0, 0.75, 0.55, 0.4]):
        w, h, cy = 520 * t + 40, 760 * t + 60, 900 + 260 * t; bw = int(34 * t)
        d.rectangle([W / 2 - w + 20, cy - h + 60, W / 2 - w + 20 + bw, cy + h * 0.55], fill=(120, 85, 45)); d.rectangle([W / 2 + w - 20 - bw, cy - h + 60, W / 2 + w - 20, cy + h * 0.55], fill=(120, 85, 45))
        d.rectangle([W / 2 - w + 20, cy - h + 60, W / 2 + w - 20, cy - h + 60 + bw], fill=(130, 95, 50))
    d.line([(W / 2 - 60, 1100), (150, H)], fill=(140, 140, 150), width=14); d.line([(W / 2 + 60, 1100), (930, H)], fill=(140, 140, 150), width=14)
    r = random.Random(3)
    for _ in range(60):
        x, y = r.uniform(60, 1020), r.uniform(300, 1500); s = r.uniform(8, 22)
        if abs(x - W / 2) < 330 and y > 600: continue
        d.ellipse([x - s, y - s * 0.7, x + s, y + s * 0.7], fill=r.choice([(200, 110, 50), (230, 140, 70), (170, 90, 40)]))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([300, 200, 780, 600], fill=(255, 200, 110, 140))
    g = g.filter(ImageFilter.GaussianBlur(80)); im.paste(g, (0, 0), g); ImageDraw.Draw(im).ellipse([510, 330, 570, 400], fill=(255, 230, 150))
    return im
def snow():
    im = Image.new("RGB", (W, H)); sky(im, (120, 160, 210), (225, 230, 240), sun=False); d = ImageDraw.Draw(im)
    for x0, h, c in [(-200, 520, (190, 205, 225)), (300, 640, (175, 190, 215)), (650, 480, (200, 212, 230))]:
        d.polygon([(x0, HOR), (x0 + 330, HOR - h), (x0 + 660, HOR)], fill=c); d.polygon([(x0 + 250, HOR - h + 110), (x0 + 330, HOR - h), (x0 + 410, HOR - h + 110)], fill=(250, 252, 255))
    ground(im, (235, 240, 248), (215, 225, 240)); d = ImageDraw.Draw(im); r = random.Random(6)
    for _ in range(40):
        y = r.uniform(HOR, H + 80); s = 0.25 + (y - HOR) / (H - HOR) * 1.5; x = r.uniform(-50, W + 50)
        if 250 < x < 830 and y > 1300: continue
        pine(d, x, y, s, c=(40, 80, 60), snow=True)
    for _ in range(500): x, y, s = r.uniform(0, W), r.uniform(0, H), r.uniform(2, 6); d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255))
    return im
def harbor():
    im = Image.new("RGB", (W, H)); sky(im, (100, 160, 215), (250, 215, 170)); d = ImageDraw.Draw(im)
    for y in range(HOR, 1380): d.line([(0, y), (W, y)], fill=lerp((60, 120, 170), (40, 90, 140), (y - HOR) / 330))
    r = random.Random(2)
    for _ in range(140): x, y = r.uniform(0, W), r.uniform(HOR + 10, 1370); d.line([(x, y), (x + r.uniform(15, 50), y)], fill=(150, 195, 225), width=3)
    sx, sy = 560, 1180   # tall ship
    d.polygon([(sx - 300, sy - 90), (sx + 330, sy - 90), (sx + 260, sy + 20), (sx - 250, sy + 20)], fill=(110, 70, 40), outline=(60, 35, 20))
    d.rectangle([sx - 300, sy - 130, sx + 330, sy - 90], fill=(150, 100, 55))
    for mx, mh in [(sx - 150, 560), (sx + 60, 640), (sx + 240, 470)]:
        d.line([(mx, sy - 90), (mx, sy - 90 - mh)], fill=(80, 50, 30), width=12)
        for k in range(3):
            top = sy - 90 - mh + 40 + k * mh * 0.3; w = 120 - k * 5
            d.polygon([(mx - w, top), (mx + w, top), (mx + w * 0.9, top + mh * 0.25), (mx - w * 0.9, top + mh * 0.25)], fill=(245, 238, 220), outline=(190, 180, 160))
    for k, c in enumerate([(160, 115, 70), (140, 100, 60)]): d.rectangle([0, 1380 + k * 10, W, H], fill=c)
    for y in range(1400, H, 70): d.line([(0, y), (W, y)], fill=(110, 75, 45), width=5)
    for cx, cy in [(80, 1500), (180, 1470), (930, 1490)]: d.rectangle([cx - 60, cy - 110, cx + 60, cy], fill=(130, 90, 50), outline=(70, 45, 25), width=6); d.line([(cx - 60, cy - 55), (cx + 60, cy - 55)], fill=(70, 45, 25), width=5)
    return im

if __name__ == "__main__":
    finish({"forest": forest, "mine": mine, "snow": snow, "harbor": harbor}[sys.argv[1]](), sys.argv[2])
