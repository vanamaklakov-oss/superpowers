"""Build a 'Machiavelli quote' Short. Default: cut-out figure over backgrounds that switch on each word
(set MODE=classic for the older two-picture push-in).
Like the reference: slow push-in on a dark picture,
one big word at a time in the centre, deep slow voice, dark synthesized drone + low piano.
Usage: python3 build.py q1 [q2 ...] | all"""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
from script import VIDEOS

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{HERE}/../machiavelli/images"
MODE = os.environ.get("MODE", "cutout")
BGDIR = f"{HERE}/images/bg"
W, H, FPS, SR = 1080, 1920, 30, 48000
FB = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 92)
FT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 40)
PAUSE = 0.55

def pcm(p):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def trim(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
    s, e = max(on[0] - 960, 0), min(on[-1] + 2400, len(a)); return a[s:e], s / SR

def music(n, rng):
    t = np.arange(n) / SR; out = np.zeros((n, 2), np.float32)
    for f, g in [(55, .05), (82.4, .03), (110, .018)]:          # A minor drone with slow swell
        sw = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9 + f)
        out[:, 0] += np.sin(2 * np.pi * f * t) * g * sw; out[:, 1] += np.sin(2 * np.pi * (f + .3) * t) * g * sw
    notes = [220, 261.6, 196, 174.6, 220, 329.6, 293.7, 261.6]  # sparse low piano
    for k, tt in enumerate(np.arange(0.5, n / SR - 1, 2.4)):
        s = int(tt * SR); L = min(int(2.6 * SR), n - s); x = np.arange(L) / SR; f = notes[k % len(notes)] / 2
        y = (np.sin(2 * np.pi * f * x) + .4 * np.sin(4 * np.pi * f * x) + .15 * np.sin(6 * np.pi * f * x)) * np.exp(-x * 1.6) * .07
        out[s:s + L] += y[:, None] * [0.8, 1.0]
    noise = np.convolve(rng.standard_normal(n), np.ones(400) / 400, "same") * .02   # wind
    out += noise[:, None]
    fade = np.minimum(1, t / 1.5) * np.minimum(1, (n / SR - t) / 2); return out * fade[:, None]

def frame_base(img, p, k):
    z = 1.03 + 0.12 * p; cw, ch = W / z, H / z; x0 = (W - cw) * (0.5 + 0.05 * (1 if k % 2 else -1) * p); y0 = (H - ch) * 0.45
    return img.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)

def prep(name):
    p = f"{IMG}/{name}.jpg"
    im = ImageOps.fit(Image.open(p).convert("RGB"), (W, H), Image.LANCZOS)
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.8)).enhance(0.62)   # darker, moodier
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.45 * (((xx - W / 2) / (W / 1.2)) ** 2 + ((yy - H / 2) / (H / 1.2)) ** 2)
    return Image.fromarray((np.asarray(im) * v[..., None]).clip(0, 255).astype(np.uint8))

def load_bgs():
    import glob
    fs = sorted(glob.glob(f"{BGDIR}/*.jpg") + glob.glob(f"{BGDIR}/*.png"))
    out = []
    for p in fs:
        im = ImageOps.fit(Image.open(p).convert("RGB"), (W, H), Image.LANCZOS)
        im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.9)).enhance(0.78)
        out.append(im)
    return out

FIG = None
def figure():
    global FIG
    if FIG is None:
        f = Image.open(f"{HERE}/images/figure.png").convert("RGBA"); bb = f.getbbox(); f = f.crop(bb)
        h = int(H * 0.74); w = int(f.width * h / f.height); f = f.resize((w, h), Image.LANCZOS)
        sh = Image.new("RGBA", f.size, (0, 0, 0, 0)); sh.putalpha(f.getchannel("A").filter(ImageFilter.GaussianBlur(25)).point(lambda v: v * 0.7))
        FIG = (f, sh)
    return FIG

def build(vid):
    title, images, sents = VIDEOS[vid]; rng = np.random.default_rng(int(vid[1:]))
    words, voice, t = [], [], 0.6
    for i in range(len(sents)):
        a, lead = trim(pcm(f"{HERE}/vo/{vid}/{i:02d}.mp3")); meta = json.load(open(f"{HERE}/vo/{vid}/{i:02d}.mp3.json"))
        voice.append((t, a)); words += [(t + w["s"] - lead, w["w"]) for w in meta["words"]]; t += len(a) / SR + PAUSE
    total = t + 1.2; n = int(total * SR)
    vo = np.zeros(n, np.float32)
    for t0, a in voice: s = int(t0 * SR); vo[s:s + len(a)] += a[: n - s] * 1.2
    m = music(n, rng); env = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), "same")
    mix = m * (1 - 0.4 * np.clip(env * 12, 0, 1))[:, None] + vo[:, None]; mix /= max(1, np.abs(mix).max() / .95)
    os.makedirs(f"{HERE}/out", exist_ok=True); wav = f"{HERE}/out/{vid}.wav"
    with wave.open(wav, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())
    imgs = [prep(x) for x in images] if MODE != "cutout" else []; cut = words[len(words) // 2][0]
    bgs = load_bgs() if MODE == "cutout" else []; bg_off = int(vid[1:]) * 7
    out = f"{HERE}/out/machiavelli_{vid}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    for f in range(int(total * FPS)):
        tt = f / FPS; k = 0 if tt < cut else 1
        if MODE == "cutout":
            wi = max([j for j, (ws, _) in enumerate(words) if ws <= tt] or [0])
            bi = (wi + bg_off) % len(bgs); bstart = words[wi][0] if tt >= words[0][0] else 0
            p = min(1, (tt - bstart) / 0.6); im = frame_base(bgs[bi], p * 0.4, bi)
            fg, sh = figure(); x = (W - fg.width) // 2; y = H - fg.height
            im.paste((0, 0, 0), (x - 10, y + 10), sh); im.paste(fg, (x, y), fg)
            d = ImageDraw.Draw(im); cur = None
            for j, (ws, w) in enumerate(words):
                nxt = words[j + 1][0] if j + 1 < len(words) else ws + 0.8
                if ws <= tt < min(nxt, ws + 0.9): cur = w
            txt = (cur or "").upper().strip(" ,.:;!?«»—")
            if txt:
                d.text((W // 2, int(H * 0.62)), txt, font=FB, anchor="mm", fill=(255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0))
            d.text((W // 2, 150), "НИККОЛО МАКИАВЕЛЛИ", font=FT, anchor="mm", fill=(235, 235, 235), stroke_width=3, stroke_fill=(0, 0, 0))
            d.text((W // 2, 205), title, font=FT, anchor="mm", fill=(220, 40, 40), stroke_width=3, stroke_fill=(0, 0, 0))
            fade = min(1, tt / 0.4, (total - tt) / 0.8)
            if fade < 1: im = Image.blend(Image.new("RGB", (W, H)), im, max(0, fade))
            ff.stdin.write(im.tobytes()); continue
        seg0, seg1 = (0, cut) if k == 0 else (cut, total)
        im = frame_base(imgs[k], (tt - seg0) / (seg1 - seg0), k)
        if abs(tt - cut) < 0.35:   # soft dissolve between the two pictures
            a0 = frame_base(imgs[0], min(1, tt / cut), 0); a1 = frame_base(imgs[1], max(0, (tt - cut) / (total - cut)), 1)
            im = Image.blend(a0, a1, (tt - (cut - 0.35)) / 0.7)
        d = ImageDraw.Draw(im)
        d.text((W // 2, 150), "НИККОЛО МАКИАВЕЛЛИ", font=FT, anchor="mm", fill=(225, 225, 225), stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((W // 2, 205), title, font=FT, anchor="mm", fill=(205, 40, 40), stroke_width=2, stroke_fill=(0, 0, 0))
        cur = None
        for j, (ws, w) in enumerate(words):
            nxt = words[j + 1][0] if j + 1 < len(words) else ws + 0.8
            if ws <= tt < min(nxt, ws + 0.9): cur = w
        if cur:
            txt = cur.upper().strip(" ,.:;!?«»—");
            if txt:
                lay = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
                ld.text((W // 2, 150), txt, font=FB, anchor="mm", fill=(0, 0, 0, 200)); lay = lay.filter(ImageFilter.GaussianBlur(10))
                im.paste(lay, (0, int(H * 0.52) - 150), lay)
                d.text((W // 2, int(H * 0.52)), txt, font=FB, anchor="mm", fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        fade = min(1, tt / 0.5, (total - tt) / 0.8)
        if fade < 1: im = Image.blend(Image.new("RGB", (W, H)), im, max(0, fade))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait(); print(out, round(total, 1), "s", flush=True)

for v in (VIDEOS if sys.argv[1:] == ["all"] else sys.argv[1:]): build(v)
