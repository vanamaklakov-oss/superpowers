"""Our own ball-head character rig, drawn in code (PIL, 3x supersampled).
A character = hat + costume colours. Every pose parameter is animatable per frame:
  expr: neutral | angry | smug | shock | worried | happy | talk
  blink (0..1), rage (0..1, head fills purple from the chin), steam (bool), sweat (bool),
  arm_l / arm_r (angle in degrees from hanging down), bob (px), lean (deg), mouth_open (0..1)
Usage: from rig import Character, draw; img = draw(Character(...), height=900, expr="angry", t=0.4)"""
import math
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFilter

INK = (24, 22, 26)
SS = 3   # supersampling

@dataclass
class Character:
    hat: str = "cap"                 # cap | bowler | tophat | peaked | tricorn | none
    hat_color: tuple = (60, 70, 90)
    coat: tuple = (40, 150, 130)     # main costume colour
    trim: tuple = (240, 225, 120)    # buttons / lapels
    shirt: tuple = (235, 235, 240)
    tie: tuple = (190, 40, 50)
    hair: tuple = (90, 60, 40)       # a tuft under the hat; None = bald
    stripes: bool = False            # striped cap / waistcoat
    mustache: bool = False
    glasses: bool = False

def _ellipse(d, cx, cy, rx, ry, **kw): d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], **kw)
def _line(d, pts, w, fill=INK): d.line(pts, fill=fill, width=w, joint="curve"); [_ellipse(d, x, y, w / 2, w / 2, fill=fill) for x, y in (pts[0], pts[-1])]

def draw(ch: Character, height=900, expr="neutral", blink=0.0, rage=0.0, steam=False, sweat=False,
         arm_l=6, arm_r=6, bob=0.0, lean=0.0, mouth_open=0.0, t=0.0, look=0.0):
    """Returns an RGBA image (width ~0.62*height). Feet at the bottom centre."""
    H = height * SS; W = int(H * 0.62); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    u = H / 100.0                      # one unit = 1 % of the height
    cx = W / 2; by = bob * SS
    lw = max(3, int(1.15 * u))         # ink line width
    # ---- legs (stick) ----
    hip_y = 66 * u + by; foot_y = 99 * u
    for s in (-1, 1):
        kx = cx + s * 4 * u + s * math.sin(t * 6) * 0.4 * u
        _line(d, [(cx + s * 3 * u, hip_y), (kx, (hip_y + foot_y) / 2), (cx + s * 4.5 * u, foot_y - 1.2 * u)], lw)
        _ellipse(d, cx + s * 6 * u, foot_y - 1.2 * u, 3.2 * u, 1.4 * u, fill=INK)                 # shoe
    # ---- body (costume) ----
    top = 40 * u + by; bot = 68 * u + by; bw = 15 * u
    body = [(cx - bw * 0.78, top), (cx + bw * 0.78, top), (cx + bw, bot), (cx - bw, bot)]
    d.polygon(body, fill=ch.coat, outline=INK, width=lw)
    d.polygon([(cx - 4 * u, top), (cx + 4 * u, top), (cx, top + 9 * u)], fill=ch.shirt, outline=INK, width=max(2, lw // 2))  # collar V
    d.polygon([(cx - 1.4 * u, top + 2 * u), (cx + 1.4 * u, top + 2 * u), (cx + 1.8 * u, top + 9 * u), (cx, top + 11 * u), (cx - 1.8 * u, top + 9 * u)], fill=ch.tie)
    if ch.stripes:
        for k in range(-3, 4):
            x = cx + k * 3.6 * u; d.line([(x, top + 10 * u), (x * 1.0 + k * 0.6 * u, bot - 1 * u)], fill=tuple(int(c * 0.8) for c in ch.coat), width=max(2, lw // 2))
    for k in range(3): _ellipse(d, cx + 5.5 * u, top + (12 + k * 5) * u, 1.0 * u, 1.0 * u, fill=ch.trim, outline=INK, width=max(1, lw // 3))
    # ---- arms (stick, from shoulders); angle 0 = hanging down, positive = raised outward ----
    for s_, ang in ((-1, arm_l), (1, arm_r)):
        sx, sy = cx + s_ * bw * 0.80, top + 2.5 * u
        a1 = math.radians(max(-30, ang)); a2 = math.radians(max(-30, ang) * 1.25 + 12)
        ex, ey = sx + s_ * math.sin(a1 + 0.18) * 11 * u, sy + math.cos(a1 + 0.18) * 11 * u
        hx, hy = ex + s_ * math.sin(a2) * 10 * u, ey + math.cos(a2) * 10 * u
        _line(d, [(sx, sy), (ex, ey), (hx, hy)], lw)
        _ellipse(d, hx, hy, 2.1 * u, 2.1 * u, fill=(250, 250, 250), outline=INK, width=lw)        # mitten hand
    # ---- head ----
    hr = 15.5 * u; hcx = cx + look * 1.5 * u; hcy = 24 * u + by
    _ellipse(d, hcx, hcy, hr, hr, fill=(252, 252, 252), outline=INK, width=lw)
    if rage > 0:                                  # purple fills up from the chin
        mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask); _ellipse(md, hcx, hcy, hr - lw / 2, hr - lw / 2, fill=255)
        lvl = hcy + hr - 2 * hr * min(1, rage); md.rectangle([0, 0, W, lvl], fill=0)
        im.paste(Image.new("RGBA", (W, H), (120, 60, 160, 255)), (0, 0), mask); d = ImageDraw.Draw(im)
        _ellipse(d, hcx, hcy, hr, hr, outline=INK, width=lw)
    if ch.hair and ch.hat in ("cap", "none", "peaked"):          # a short fringe under the hat brim
        fy = hcy - hr * 0.55 if ch.hat != "none" else hcy - hr * 0.75
        d.polygon([(hcx - hr * 0.85, fy), (hcx - hr * 0.2, fy - 1 * u), (hcx - hr * 0.35, fy + 3.2 * u), (hcx - hr * 0.6, fy + 1.6 * u), (hcx - hr * 0.8, fy + 3.6 * u)], fill=ch.hair)
    # eyes
    ey = hcy + 0.5 * u; ex = 5.2 * u; er = 1.5 * u
    shut = blink > 0.5
    for s in (-1, 1):
        x = hcx + s * ex + look * 1.2 * u
        if shut: d.line([(x - er, ey), (x + er, ey)], fill=INK, width=lw)
        elif expr == "shock": _ellipse(d, x, ey, er * 2.1, er * 2.1, fill=(255, 255, 255), outline=INK, width=lw); _ellipse(d, x, ey, er * 0.55, er * 0.55, fill=INK)
        elif expr == "happy": d.arc([x - er * 1.4, ey - er, x + er * 1.4, ey + er * 1.6], 200, 340, fill=INK, width=lw)
        else: _ellipse(d, x, ey, er, er * 1.15, fill=INK)
        if ch.glasses: _ellipse(d, x, ey, er * 2.4, er * 2.4, outline=INK, width=max(2, lw // 2))
    # brows: the main acting
    bro = {"neutral": (0, 0), "angry": (-1, 1), "smug": (1, -0.3), "shock": (0, -1.6), "worried": (1, -0.8), "happy": (0, -1), "talk": (0.2, -0.4)}[expr]
    for s in (-1, 1):
        x = hcx + s * ex; y = ey - 4.2 * u + bro[1] * 1.4 * u
        tilt = bro[0] * 1.6 * u * s * -1 if expr != "angry" else 1.8 * u
        inner, outer = (x - s * 2.4 * u, y + (tilt if expr == "angry" else -tilt / 2)), (x + s * 2.4 * u, y - (tilt / 2 if expr == "angry" else -tilt / 2))
        d.line([inner, outer], fill=INK, width=lw)
    # mouth
    my = hcy + 7.5 * u; mo = max(mouth_open, 0.0)
    if expr == "angry":
        d.rounded_rectangle([hcx - 4 * u, my - 1.6 * u, hcx + 4 * u, my + 1.6 * u], radius=u, fill=(255, 255, 255), outline=INK, width=max(2, lw // 2))
        for k in range(1, 4): x = hcx - 4 * u + k * 2 * u; d.line([(x, my - 1.6 * u), (x, my + 1.6 * u)], fill=INK, width=max(1, lw // 3))
    elif expr in ("happy", "smug"):
        d.arc([hcx - 4 * u, my - 3 * u, hcx + (4 if expr == "happy" else 3) * u, my + 1.5 * u], 20, 160 if expr == "happy" else 120, fill=INK, width=lw)
    elif expr == "shock" or mo > 0.15:
        _ellipse(d, hcx, my, 1.6 * u + mo * 1.2 * u, 1.2 * u + mo * 2.4 * u, fill=(120, 30, 40), outline=INK, width=max(2, lw // 2))
    elif expr == "worried": d.arc([hcx - 3 * u, my - 0.5 * u, hcx + 3 * u, my + 3 * u], 200, 340, fill=INK, width=lw)
    else: d.line([(hcx - 2.4 * u, my), (hcx + 2.4 * u, my)], fill=INK, width=lw)
    if ch.mustache: d.chord([hcx - 4 * u, my - 3.2 * u, hcx + 4 * u, my + 0.4 * u], 180, 360, fill=INK)
    # ---- hat ----
    hy = hcy - hr * 0.62; hc = ch.hat_color
    if ch.hat == "cap":
        d.chord([hcx - hr * 0.98, hy - 9 * u, hcx + hr * 0.98, hy + 6 * u], 180, 360, fill=hc, outline=INK, width=lw)
        d.rounded_rectangle([hcx - hr * 1.05, hy - 1.2 * u, hcx + hr * 1.15, hy + 1.6 * u], radius=u, fill=hc, outline=INK, width=lw)
        if ch.stripes:
            for k in range(-4, 5): d.line([(hcx + k * 2.6 * u, hy - 7.5 * u + abs(k) * 0.5 * u), (hcx + k * 3.1 * u, hy - 1.4 * u)], fill=(235, 235, 240), width=max(2, lw // 2))
    elif ch.hat == "bowler":
        d.chord([hcx - hr * 0.8, hy - 11 * u, hcx + hr * 0.8, hy + 6 * u], 180, 360, fill=hc, outline=INK, width=lw)
        d.ellipse([hcx - hr * 1.12, hy - 1.6 * u, hcx + hr * 1.12, hy + 2.4 * u], fill=hc, outline=INK, width=lw)
    elif ch.hat == "tophat":
        d.rectangle([hcx - hr * 0.62, hy - 17 * u, hcx + hr * 0.62, hy], fill=hc, outline=INK, width=lw)
        d.rectangle([hcx - hr * 0.62, hy - 4.5 * u, hcx + hr * 0.62, hy - 2 * u], fill=ch.tie)
        d.ellipse([hcx - hr * 1.05, hy - 1.6 * u, hcx + hr * 1.05, hy + 2.2 * u], fill=hc, outline=INK, width=lw)
    elif ch.hat == "peaked":
        d.rounded_rectangle([hcx - hr * 0.95, hy - 8 * u, hcx + hr * 0.95, hy + 1 * u], radius=2 * u, fill=hc, outline=INK, width=lw)
        d.rectangle([hcx - hr * 0.95, hy - 1.8 * u, hcx + hr * 0.95, hy + 0.2 * u], fill=ch.trim)
        d.chord([hcx - hr * 0.6, hy - 1 * u, hcx + hr * 0.9, hy + 4.5 * u], 0, 180, fill=INK)
    elif ch.hat == "tricorn":
        d.polygon([(hcx - hr * 1.2, hy + 1 * u), (hcx, hy - 10 * u), (hcx + hr * 1.2, hy + 1 * u), (hcx, hy + 3 * u)], fill=hc, outline=INK)
        d.line([(hcx - hr * 1.1, hy + 1 * u), (hcx, hy + 2.6 * u), (hcx + hr * 1.1, hy + 1 * u)], fill=ch.trim, width=lw)
    # ---- extras ----
    if sweat:
        sx, sy = hcx + hr * 0.95, hcy - hr * 0.3 + (t * 30 % 1) * 2 * u
        d.polygon([(sx, sy - 3 * u), (sx - 1.8 * u, sy + 0.6 * u), (sx + 1.8 * u, sy + 0.6 * u)], fill=(120, 190, 240))
        _ellipse(d, sx, sy + 0.8 * u, 1.9 * u, 1.9 * u, fill=(120, 190, 240))
    if steam:
        for s in (-1, 1):
            ph = (t * 1.6 + (0.5 if s > 0 else 0)) % 1
            px, py = hcx + s * hr * 0.9, hcy - hr * 0.9 - ph * 8 * u; r = (2.5 + ph * 3) * u
            for k in range(3): _ellipse(d, px + s * k * r * 0.6, py - k * r * 0.3, r * (1 - k * 0.15), r * (1 - k * 0.15), fill=(255, 255, 255), outline=(150, 150, 160), width=max(2, lw // 2))
    if lean: im = im.rotate(-lean, resample=Image.BICUBIC, center=(cx, H * 0.98))
    return im.resize((W // SS, H // SS), Image.LANCZOS)

ENGINEER = Character(hat="cap", hat_color=(70, 80, 110), stripes=True, coat=(40, 150, 130), tie=(190, 40, 50))
BOSS = Character(hat="bowler", hat_color=(40, 40, 46), coat=(200, 160, 40), trim=(120, 80, 20), tie=(120, 60, 30), hair=None, mustache=False)
RICH = Character(hat="tophat", hat_color=(30, 30, 36), coat=(60, 40, 70), trim=(220, 190, 80), tie=(160, 30, 40), hair=None, mustache=True)
CLERK = Character(hat="none", coat=(90, 110, 160), trim=(230, 230, 230), tie=(40, 40, 60), glasses=True)
OFFICER = Character(hat="peaked", hat_color=(40, 50, 110), coat=(40, 50, 110), trim=(230, 190, 70), tie=(200, 200, 210))
