"""Generate a project's backgrounds with Cloudflare FLUX: python3 ballhead/genbgs.py <project_dir>
Reads <project>/bgs.py: PROMPTS = {name: prompt} (scenery, the shared STYLE is appended) and
RAW = {name: prompt} (full prompt, no "no characters" style: for animals in shot). Skips existing files."""
import os, sys, importlib.util
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gen_cf import gen
d = os.path.abspath(sys.argv[1]); spec = importlib.util.spec_from_file_location("bgs", f"{d}/bgs.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LAND = os.environ.get("LANDSCAPE") == "1"; BG = "bgs_land" if LAND else "bgs"
os.makedirs(f"{d}/{BG}", exist_ok=True)
ANIMAL = ", 3D animated feature film render, cartoon style, warm saturated cinematic light, strong perspective, rich detail, no humans, no text, no letters"
for name, p, style in [(k, v, True) for k, v in m.PROMPTS.items()] + [(k, v + ANIMAL, False) for k, v in getattr(m, "RAW", {}).items()]:
    out = f"{d}/{BG}/{name}.jpg"
    if not os.path.exists(out): print(gen(p, out, style=style, vertical=not LAND, landscape=LAND), flush=True)
