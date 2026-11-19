"""Find the best moments in a recorded stream and cut vertical clips with captions.
python3 highlights.py live_xxx.mp4 [N_CLIPS]
Score per second = loudness jump over the rolling median + excited words in the transcript + on-screen motion.
Clips are 15-40 s, start just before the peak and end on a sentence boundary."""
import json, re, subprocess, sys, os
import numpy as np

src = sys.argv[1]; NCLIP = int(sys.argv[2]) if len(sys.argv) > 2 else 6
base = os.path.splitext(os.path.basename(src))[0]; out_dir = f'/home/user/stream/clips_{base}'; os.makedirs(out_dir, exist_ok=True)
probe = lambda k: subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', f'stream={k}', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip()
W, H = map(int, probe('width,height').split(','))
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
print(f'{src}: {W}x{H}, {dur/60:.1f} min')

# 1. loudness per second
a = np.frombuffer(subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
n = len(a) // 16000; rms = np.array([np.sqrt((a[i*16000:(i+1)*16000]**2).mean()) + 1e-6 for i in range(n)]); db = 20*np.log10(rms)
med = np.array([np.median(db[max(0, i-60):i+1]) for i in range(n)]); loud = np.clip(db - med - 3, 0, 15) / 15

# 2. motion per second (2 fps, small grey frames)
g = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', src, '-vf', 'fps=2,scale=96:-2,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
gw = 96; gh = round(H * 96 / W / 2) * 2; fr = np.frombuffer(g, dtype=np.uint8)[: (len(g)//(gw*gh))*gw*gh].reshape(-1, gh, gw).astype(np.float32)
mo = np.abs(np.diff(fr, axis=0)).mean((1, 2)); mot = np.zeros(n)
for i in range(min(n, len(mo)//2)): mot[i] = mo[2*i:2*i+2].mean()
mot = np.clip((mot - np.median(mot)) / (np.percentile(mot, 95) - np.median(mot) + 1e-6), 0, 1)

# 3. transcript with word times (cached)
tj = f'{out_dir}/transcript.json'
if not os.path.exists(tj):
    from faster_whisper import WhisperModel
    m = WhisperModel('small', device='cpu', compute_type='int8')
    segs, info = m.transcribe(a, word_timestamps=True, vad_filter=True); print('language:', info.language)
    words = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in s.words]
    json.dump(words, open(tj, 'w'), ensure_ascii=False)
words = json.load(open(tj))
for w in words: w['w'] = re.sub(r"[^0-9A-Za-zА-Яа-яЁё.,!?'\-]", '', w['w'])
words = [w for w in words if w['w']]
HYPE = r'(смотри|гляди|ого|вау|жесть|капец|кошмар|ахах|хаха|ахаха|нифига|ничего себе|офиген|охрен|красав|топ|имба|что\?|чего\?|да ладно|не может|погнали|бежим|стреляй|полиц|догон|авари|взрыв|улет|угар|лол|кринж|ору|рофл|wow|whoa|oh my god|omg|bro|what|no way|insane|crazy|sick|lets go|let.s go|holy|dude|yo|look|wait|run|police|cops|crash|boom|damn|bruh|lol|haha)'
txt = np.zeros(n); talk = np.zeros(n)
for w in words:
    i = int(w['s'])
    if i < n:
        talk[i] = 1
        if re.search(HYPE, w['w'].lower()): txt[max(0, i-1):i+2] += 0.5
        if w['w'].endswith('!') or w['w'].endswith('?!'): txt[i] += 0.3
CTA = r'^(like|likes|liking|comment|comments|subscribe|follow|share|hype|tap|лайк|подпиш|коммент)'
for w in words:  # streamer asking chat for likes is not a highlight
    i = int(w['s'])
    if i < n and re.search(CTA, w['w'].lower()): txt[max(0, i-10):i+10] -= 1.5
txt = np.clip(txt, -1, 1)
score = 0.45*loud + 0.35*txt + 0.2*mot
sm = np.convolve(score, np.ones(8)/8, 'same')

# 4. pick peaks, at least 60 s apart
picks = []
for i in np.argsort(-sm):
    if sm[i] <= 0.05: break
    if all(abs(i - p) > 60 for p in picks): picks.append(int(i))
    if len(picks) == NCLIP: break
ends = [w['e'] for w in words if re.search(r'[.!?]$', w['w'])]
def clip_bounds(p):
    a0 = max(0, p - 8); b0 = min(dur, a0 + 22)
    later = [e for e in ends if a0 + 15 <= e <= a0 + 40]
    return a0, (later[0] + 0.4 if later else min(dur, a0 + 30))

tt = lambda x: '%d:%02d:%05.2f' % (x // 3600, (x % 3600) // 60, x % 60)
report = []
for k, p in enumerate(sorted(picks)):
    a0, b0 = clip_bounds(p)
    ws = [w for w in words if a0 <= w['s'] < b0]
    hooks = sorted(ws, key=lambda w: -(bool(re.search(HYPE, w['w'].lower())) + loud[min(n-1, int(w['s']))]))
    hook_line = ' '.join(x['w'] for x in ws if hooks and abs(x['s'] - hooks[0]['s']) < 1.6)[:40].upper() or 'СМОТРИ ДО КОНЦА'
    ev, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or re.search(r'[.,!?]$', w['w']):
            ev.append(cur); cur = []
    if cur: ev.append(cur)
    lines = [f"Dialogue: 0,{tt(c[0]['s']-a0)},{tt((ev[j+1][0]['s'] if j+1 < len(ev) else c[-1]['e']+0.3)-a0)},Cap,,0,0,0,,{{\\fscx116\\fscy116\\t(0,110,\\fscx100\\fscy100)}}" + ' '.join(('{\\c&H0000E1FF&}'+x['w'].upper()+'{\\c&HFFFFFF&}') if re.search(HYPE, x['w'].lower()) else x['w'].upper() for x in c) for j, c in enumerate(ev)]
    lines.append(f"Dialogue: 1,{tt(0)},{tt(min(3.5, b0-a0))},Hook,,0,0,0,,{{\\fscx40\\fscy40\\t(0,180,\\fscx108\\fscy108)\\t(180,280,\\fscx100\\fscy100)}}{hook_line}")
    ass = f'{out_dir}/c{k+1}.ass'
    open(ass, 'w').write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,8,4,2,60,60,330,1
Style: Hook,Inter Display Black,92,&H0000E1FF,&H0000E1FF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,10,5,8,60,60,230,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + '\n'.join(lines) + '\n')
    vertical = H > W
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" if vertical else
          "split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2")
    out = f'{out_dir}/clip{k+1}_{int(a0//60):02d}m{int(a0%60):02d}s.mp4'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{a0:.2f}', '-t', f'{b0-a0:.2f}', '-i', src, '-filter_complex', f"[0:v]{vf},subtitles={ass},format=yuv420p[v];[0:a]loudnorm=I=-14:TP=-1.5[au]",
                    '-map', '[v]', '-map', '[au]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-maxrate', '6M', '-bufsize', '12M', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    report.append(dict(clip=out, start=round(a0, 1), end=round(b0, 1), score=round(float(sm[p]), 2), hook=hook_line, text=' '.join(w['w'] for w in ws)[:200]))
    print(f'clip {k+1}: {tt(a0)}-{tt(b0)} score {sm[p]:.2f} | {hook_line}')
json.dump(report, open(f'{out_dir}/report.json', 'w'), ensure_ascii=False, indent=1)
