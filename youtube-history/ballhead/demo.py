"""4-second motion test: engineer (smug, blinking, bob) and boss (rage fills, steam) over a simple backdrop."""
import math, subprocess
from PIL import Image, ImageDraw
from rig import draw, ENGINEER, BOSS
W, H, FPS, N = 1080, 1920, 30, 120
bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
for y in range(H):
    k = y / H; c = (int(120 + 120 * k), int(170 + 40 * k), int(235 - 120 * k)) if y < H * 0.62 else (int(190 - 40 * k), int(120 - 30 * k), int(80 - 20 * k))
    d.line([(0, y), (W, y)], fill=c)
ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "out/demo.mp4"], stdin=subprocess.PIPE)
import os; os.makedirs("out", exist_ok=True)
for f in range(N):
    t = f / FPS; z = 1 + 0.06 * t / 4                       # slow push-in
    im = bg.copy()
    blink = 1.0 if (f % 70) in (40, 41, 42) else 0.0
    e = draw(ENGINEER, height=900, expr="smug", blink=blink, bob=math.sin(t * 5) * 6, t=t, arm_r=20 + 10 * math.sin(t * 3))
    rage = min(1, max(0, (t - 1.2) / 0.35))
    b = draw(BOSS, height=950, expr="angry" if t > 1.0 else "neutral", rage=rage, steam=t > 1.6, t=t, bob=math.sin(t * 9) * 4 * (t > 1.6),
             arm_l=40 + 30 * math.sin(t * 8) * (t > 1.6), lean=-4 * (t > 1.0))
    im.paste(e, (90, H - e.height - 170), e); im.paste(b, (W - b.width - 60, H - b.height - 160), b)
    cw, ch = W / z, H / z; im = im.transform((W, H), Image.EXTENT, ((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2), Image.BICUBIC)
    ff.stdin.write(im.tobytes())
ff.stdin.close(); ff.wait(); print("ok")
