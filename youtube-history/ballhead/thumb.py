"""YouTube thumbnails (1280x720) for ball-head videos: big hook text, a character, a bright accent.
Usage: python3 ballhead/thumb.py  (edit THUMBS below or import make())."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rig import draw, Character
FONT = f"{HERE}/../fonts/Oswald-Bold.ttf"
TW, TH = 1280, 720

def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 60 * s, y - 210 * s, x + 60 * s, y + 10 * s], radius=20 * s, fill=(25, 25, 30), outline=(10, 10, 10), width=6)
    d.rounded_rectangle([x - 50 * s, y - 196 * s, x + 50 * s, y - 4 * s], radius=12 * s, fill=(90, 170, 255))
    for k in range(4): d.rounded_rectangle([x - 40 * s, y + (-182 + k * 44) * s, x + 40 * s, y + (-154 + k * 44) * s], radius=6 * s, fill=(235, 245, 255))

def badge(d, x, y, r, n):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 40, 45), outline=(255, 255, 255), width=max(3, r // 8))
    d.text((x, y), str(n), font=ImageFont.truetype(FONT, int(r * 1.1)), anchor="mm", fill=(255, 255, 255))

def make(bg, lines, out, char, expr="shock", side="right", accent=(255, 60, 50), badges=True, money=False):
    im = Image.open(bg).convert("RGB").resize((TW, TH))
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(3))).enhance(0.55)
    v = Image.new("L", (TW, TH), 0); ImageDraw.Draw(v).ellipse([-200, -150, TW + 200, TH + 150], fill=255)
    im = Image.composite(im, Image.new("RGB", (TW, TH), (5, 5, 10)), v.filter(ImageFilter.GaussianBlur(120)))
    cx = 880 if side == "right" else 330
    glow = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([cx - 330, 60, cx + 330, 700], fill=accent + (120,))
    im.paste(glow.filter(ImageFilter.GaussianBlur(90)), (0, 0), glow.filter(ImageFilter.GaussianBlur(90)))
    ch = draw(char, height=980, expr=expr, arm_r=60 if side == "right" else 0, arm_l=0 if side == "right" else 60, sweat=True)
    px, py = int(cx - ch.width / 2), 150
    im.paste(ch, (px, py), ch); d = ImageDraw.Draw(im)
    hand = (px + ch.width * 0.5 + (0.3 if side == "right" else -0.3) * ch.width, py + 980 * 0.62)
    phone(d, hand[0], hand[1] + 30, 1.1)
    if badges:
        for (dx, dy, r, n) in [(-70, -240, 46, 99), (40, -310, 38, 47), (95, -190, 32, 12)]: badge(d, hand[0] + dx, hand[1] + dy, r, n)
    if money:
        for k in range(10):
            x = (cx - 300 + k * 67) % TW; y = 40 + (k * 97) % 260; b = Image.new("RGBA", (130, 60), (90, 160, 90, 255)); bd = ImageDraw.Draw(b)
            bd.rectangle([3, 3, 126, 56], outline=(40, 90, 40), width=4); bd.text((65, 30), "$", font=ImageFont.truetype(FONT, 34), anchor="mm", fill=(30, 70, 30))
            b = b.rotate((k * 37) % 360, expand=True); im.paste(b, (int(x), int(y)), b)
    d = ImageDraw.Draw(im)
    tx = 60 if side == "right" else TW - 60; anchor = "lm" if side == "right" else "rm"
    maxw = 700 if side == "right" else 620; y = TH / 2 - (len(lines) - 1) * 80
    for i, (text, col) in enumerate(lines):
        size = 170
        f = ImageFont.truetype(FONT, size)
        while f.getlength(text) > maxw: size -= 6; f = ImageFont.truetype(FONT, size)
        d.text((tx + 8, y + 8), text, font=f, anchor=anchor, fill=(0, 0, 0))
        d.text((tx, y), text, font=f, anchor=anchor, fill=col, stroke_width=10, stroke_fill=(0, 0, 0))
        y += size * 1.0
    im.save(out, quality=92); return out

if __name__ == "__main__":
    U = Character(hat="none", coat=(60, 130, 200), trim=(240, 240, 240), tie=(60, 130, 200), hair=(70, 50, 35))
    A = f"{HERE}/../attention"
    W_, R_, Y_ = (255, 255, 255), (255, 60, 50), (255, 215, 60)
    print(make(f"{A}/bgs_land/servers.jpg", [("ТЫ НЕ", W_), ("КЛИЕНТ.", W_), ("ТЫ ТОВАР", R_)], f"{A}/thumbs/thumb1.jpg", U, "shock"))
    print(make(f"{A}/bgs_land/boardroom.jpg", [("КТО", W_), ("ПРОДАЁТ", W_), ("ТВОЁ ВРЕМЯ?", Y_)], f"{A}/thumbs/thumb2.jpg", U, "worried", side="left", accent=(255, 190, 40), badges=True, money=False))
    print(make(f"{A}/bgs_land/night.jpg", [("6 ЧАСОВ", R_), ("В ДЕНЬ.", W_), ("КТО ЭТО ЗАБРАЛ?", W_)], f"{A}/thumbs/thumb3.jpg", U, "shock", accent=(80, 140, 255)))
