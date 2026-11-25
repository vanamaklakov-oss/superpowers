"""Generate pictures with Cloudflare Workers AI (FLUX.1 schnell, free daily quota).
The API token is injected by the environment's network proxy (Authorization: Bearer ...); none is stored here.
Usage: python3 gen_cf.py <out.jpg> "<prompt>" [--vertical]   (--vertical: centre-crop to 9:16, 1080x1920)
Also importable: gen(prompt, out, vertical=True)."""
import base64, io, json, sys, time, urllib.error, urllib.request
from PIL import Image, ImageFilter

ACCOUNT = "9e9c365e89bbbaf23301c89d3e97f7fa"      # Cloudflare account id (not a secret)
URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell"
STYLE = ", 3D animated feature film render, warm saturated cinematic light, strong perspective, rich detail, no people, no characters, no text, no letters"

def gen(prompt, out, vertical=True, steps=8, seed=None, style=True, landscape=False):
    body = {"prompt": prompt + (STYLE if style else ""), "steps": steps}
    last = None
    for attempt in range(4):
        req = urllib.request.Request(URL, json.dumps(body).encode(), {"Content-Type": "application/json", "Authorization": "Bearer injected-by-proxy"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=120))
            if d.get("success"):
                im = Image.open(io.BytesIO(base64.b64decode(d["result"]["image"]))).convert("RGB")
                if vertical:   # 1024x1024 -> centre 576x1024 -> 1080x1920
                    w, h = im.size; cw = int(h * 9 / 16); im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h)).resize((1080, 1920), Image.LANCZOS)
                    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
                elif landscape:   # 1024x1024 -> centre 1024x576 -> 1920x1080
                    w, h = im.size; chh = int(w * 9 / 16); im = im.crop((0, (h - chh) // 2, w, (h - chh) // 2 + chh)).resize((1920, 1080), Image.LANCZOS)
                    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
                im.save(out, quality=93); return out
            last = d.get("errors")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code} {e.read()[:200]!r}"
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"cloudflare: {last}")

if __name__ == "__main__":
    print(gen(sys.argv[2], sys.argv[1], vertical="--vertical" in sys.argv))
