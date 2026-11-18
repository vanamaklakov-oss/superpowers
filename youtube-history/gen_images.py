"""Generate scene pictures for a history Short with the Gemini image API.
Reads <project>/PROMPTS.md (style line, [HERO] line, scene prompts), writes <project>/images/NN.png.
Scene 00 (hero portrait) is made first and passed as a reference to every scene that shows the hero.
The API key is injected by the environment's network proxy (header x-goog-api-key); none is stored here.
Usage: python3 gen_images.py <project> [scene numbers...] [--force]"""
import base64, json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = ["gemini-3.1-flash-image", "gemini-2.5-flash-image"]
URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"

def parse(md):
    style = re.search(r"\*\*Общий стиль\*\*.*?\n`([^`]+)`", md, re.S).group(1)
    hero = re.search(r"`\[(?:HERO|LEO)\] = ([^`]+)`", md).group(1)
    scenes = {}
    for m in re.finditer(r"^\*\*(\d\d)(?: —[^*\n]*\*\*|\*\* — «[^»\n]*»)\s*(.*?)\s*\+ стиль", md, re.S | re.M):
        scenes[int(m.group(1))] = m.group(2).strip()
    return style, hero, scenes

def call(parts):
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    last = None
    for model in MODELS:
        for attempt in range(3):
            req = urllib.request.Request(URL.format(model), json.dumps(body).encode(), {"Content-Type": "application/json", "x-goog-api-key": "injected-by-proxy"})
            try:
                d = json.load(urllib.request.urlopen(req, timeout=180))
                for c in d.get("candidates", []):
                    for p in c.get("content", {}).get("parts", []):
                        if "inlineData" in p: return base64.b64decode(p["inlineData"]["data"]), model
                last = f"{model}: no image ({json.dumps(d)[:300]})"
            except urllib.error.HTTPError as e:
                last = f"{model}: HTTP {e.code} {e.read()[:300]!r}"
                if e.code in (400, 403, 404): break
            time.sleep(4 * (attempt + 1))
    raise RuntimeError(last)

def main():
    proj = sys.argv[1]; force = "--force" in sys.argv
    want = [int(a) for a in sys.argv[2:] if a.isdigit()]
    D = f"{HERE}/{proj}"; os.makedirs(f"{D}/images", exist_ok=True)
    style, hero, scenes = parse(open(f"{D}/PROMPTS.md").read())
    order = sorted(scenes) if not want else sorted(set(want) | {0})
    for n in order:
        out = f"{D}/images/{n:02d}.png"
        if os.path.exists(out) and not force and n not in want: continue
        text = scenes[n].replace("[HERO]", hero).replace("[LEO]", hero) + ", " + style
        parts = [{"text": text}]
        if n != 0 and ("[HERO]" in scenes[n] or "[LEO]" in scenes[n]) and os.path.exists(f"{D}/images/00.png"):
            ref = base64.b64encode(open(f"{D}/images/00.png", "rb").read()).decode()
            parts = [{"inlineData": {"mimeType": "image/png", "data": ref}},
                     {"text": "Use the person in this reference portrait as the same character (same face, hair and clothing). " + text}]
        img, model = call(parts); open(out, "wb").write(img); print(proj, n, "ok", model, flush=True)

main()
