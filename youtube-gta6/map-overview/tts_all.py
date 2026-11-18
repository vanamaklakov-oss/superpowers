import sys, os
sys.path.insert(0, '/home/user/bd'); import build
lines = [l.strip() for l in open('lines.txt', encoding='utf-8') if l.strip()]
for i, t in enumerate(lines):
    p = f'v{i:02d}.mp3'
    if os.path.exists(p + '.json') and os.path.exists(p + '.txt') and open(p + '.txt').read() == t: continue
    build.tts(t, p, '+16%', '+2Hz'); open(p + '.txt', 'w').write(t); print(i, 'ok', flush=True)
