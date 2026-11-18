"""GTA 6 map overview: official Rockstar screenshots panned in 9:16, region title cards, word captions, music."""
import json, re, subprocess, sys
sys.path.insert(0, '/home/user/bd'); import build
SP = '/tmp/claude-0/-home-user/0ec894cc-99b2-57e2-86d6-3ac041a64a76/scratchpad'
IMG = f'{SP}/rsmap/clean'; CLIP = f'{SP}/wait'
FPS, LEAD, PAUSE = 30, 0.3, 0.3
lines = [l.strip() for l in open('lines.txt', encoding='utf-8') if l.strip()]
W = [build.split_words(json.load(open(f'v{i:02d}.mp3.json'))) for i in range(len(lines))]
# shots per line: images (official screenshots) or a trailer clip
SHOTS = [["clip:w1.mov", "Vice_City_01"], ["Vice_City_03", "Vice_City_08", "Vice_City_09"], ["Leonida_Keys_01", "Leonida_Keys_05", "Leonida_Keys_04"],
         ["Grassrivers_04", "Grassrivers_02", "Grassrivers_03"], ["Port_Gellhorn_01", "Port_Gellhorn_02"], ["Ambrosia_01", "Ambrosia_04", "Ambrosia_03"],
         ["Mount_Kalaga_National_Park_04", "Mount_Kalaga_National_Park_05", "Mount_Kalaga_National_Park_06"], ["Mount_Kalaga_National_Park_02", "Vice_City_02"]]
REGIONS = [None, ("ВАЙС-СИТИ", "#ff4fd8"), ("ЛЕОНИДА-КИС", "#00e5ff"), ("ГРАССРИВЕРС", "#a6e34b"), ("ПОРТ-ГЕЛЛХОРН", "#ff9f43"), ("АМБРОЗИЯ", "#ffd84d"), ("МАУНТ-КАЛАГА", "#6ee7b7")]
starts, t = [], 0.0
for i, w in enumerate(W): starts.append(t); t += (LEAD if i == 0 else 0.15) + w[-1]['s'] + w[-1]['d'] + PAUSE
TOT = t + 1.0; vs = [s + (LEAD if i == 0 else 0.15) for i, s in enumerate(starts)]
ends = starts[1:] + [TOT]

def shot(src, d, k, out):
    n = max(1, round(d * FPS)); dirn = k % 2
    x = f"(iw-1080)*{'t/' + str(d) if dirn == 0 else '(1-t/' + str(d) + ')'}"
    vf = f"scale=-2:2050:flags=lanczos,crop=1080:1920:x='{x}':y='(ih-1920)/2',setsar=1,fps={FPS},format=yuv420p"
    if src.startswith('clip:'):
        inp = ['-stream_loop', '-1', '-i', f'{CLIP}/{src[5:]}']
    else:
        inp = ['-loop', '1', '-framerate', str(FPS), '-i', f'{IMG}/{src}.jpg']
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *inp, '-t', f'{d:.3f}', '-vf', vf, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', out], check=True)

parts, k = [], 0
for i, shots in enumerate(SHOTS):
    a, b = round(starts[i] * FPS), round(ends[i] * FPS); total = b - a
    cuts = [a + round(total * j / len(shots)) for j in range(len(shots) + 1)]
    for j, s in enumerate(shots):
        out = f'shot{k:02d}.mp4'; shot(s, (cuts[j + 1] - cuts[j]) / FPS, k, out); parts.append(out); k += 1
open('shots.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'shots.txt', '-c', 'copy', 'joined.mp4'], check=True)

# ---- titles and captions
tt = lambda x: '%d:%02d:%05.2f' % (x // 3600, (x % 3600) // 60, x % 60)
bgr = lambda h: '&H00%s%s%s&' % (h[5:7], h[3:5], h[1:3])
pop = '{\\fscx40\\fscy40\\t(0,160,\\fscx112\\fscy112)\\t(160,260,\\fscx100\\fscy100)}'
ev = []
def D(a, b, style, text, layer=1): ev.append(f'Dialogue: {layer},{tt(a)},{tt(b)},{style},,0,0,0,,{text}')
D(0.1, ends[0], 'Big', pop + 'КАРТА {\\c&H004DD8FF&}GTA 6'); D(0.5, ends[0], 'Pill', '{\\fad(200,0)}ШТАТ ЛЕОНИДА · 6 РЕГИОНОВ')
for i in range(1, 7):
    name, col = REGIONS[i]
    D(starts[i] + 0.05, ends[i], 'Pill', f'{{\\fad(150,0)}}РЕГИОН {i}/6')
    D(starts[i] + 0.05, ends[i], 'Big', pop + f'{{\\3c&H000000&\\4c{bgr(col)}}}' + name)
    dots = ''.join((f'{{\\c{bgr(col)}}}●' if j == i else '{\\c&HFFFFFF&\\alpha&H80&}●{\\alpha&H00&}') + ' ' for j in range(1, 7))
    D(starts[i] + 0.2, ends[i], 'Dots', dots)
D(starts[7] + 0.1, TOT, 'Big', pop + 'КАКОЙ РЕГИОН'); D(starts[7] + 0.4, TOT, 'Big2', pop + '{\\c&H004DD8FF&}ЖДЁШЬ?')
keys = {build.norm(x) for r in REGIONS[1:] for x in r[0].replace('-', ' ').split()} | {'gta', '6', 'шесть', 'леонида', 'майами', 'флорида', 'эверглейдс', 'аллигаторы', 'байкеры', 'релиза', 'рокстар'}
for i, w in enumerate(W):
    toks = lines[i].split(); j = 0; seq = []
    for x in w:
        while j < len(toks) and build.norm(toks[j]) != build.norm(x['w']): j += 1
        seq.append((toks[j] if j < len(toks) else x['w'], x['s'], x['s'] + x['d'])); j += 1
    chunks, cur = [], []
    for s in seq:
        if s[0] in ('—', '-'): continue
        cur.append(s)
        if len(cur) == 3 or s[0][-1] in '.,:?!—»': chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for c_i, c in enumerate(chunks):
        a = vs[i] + c[0][1]; b = vs[i] + (chunks[c_i + 1][0][1] if c_i + 1 < len(chunks) else c[-1][2] + 0.3)
        txt = ' '.join(('{\\c&H0000E1FF&}' + s.upper() + '{\\c&HFFFFFF&}') if any(build.norm(p) in keys for p in s.split('-')) else s.upper() for s, _, _ in c)
        D(a, b, 'Cap', '{\\fscx116\\fscy116\\t(0,110,\\fscx100\\fscy100)}' + txt, 0)
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Big,Inter Display Black,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00D84FFF,0,0,0,0,100,100,2,0,1,11,9,8,50,50,330,1
Style: Big2,Inter Display Black,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,11,9,8,50,50,480,1
Style: Pill,Inter Display Black,46,&H00FFFFFF,&H00FFFFFF,&H00141414,&H00141414,0,0,0,0,100,100,3,0,3,14,0,8,50,50,230,1
Style: Dots,Inter Display Black,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,4,0,8,50,50,500,1
Style: Cap,Inter Display Black,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,9,5,2,60,60,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('titles.ass', 'w').write(hdr + '\n'.join(ev) + '\n')

# ---- music and mix
build.bed('bed.wav', TOT, starts[1:], seed=77)
ins = ['-i', 'bed.wav']; fc = []
for i in range(len(lines)):
    ins += ['-i', f'v{i:02d}.mp3']; ms = int(vs[i] * 1000); fc.append(f'[{i + 1}]aresample=48000,adelay={ms}|{ms}[a{i}]')
n = len(lines)
fc = ';'.join(fc) + ';' + ''.join(f'[a{i}]' for i in range(n)) + f'amix=inputs={n}:normalize=0,aformat=channel_layouts=stereo,highpass=f=80,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3,aecho=0.85:0.4:28:0.08,apad,atrim=0:{TOT},volume=1.3,asplit[vo][sc];[0]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.01:ratio=8:attack=15:release=400[d];[d][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5'
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *ins, '-filter_complex', fc, '-ar', '48000', 'mix.wav'], check=True)
vf = "drawbox=x=0:y=0:w=1080:h=700:color=black@0.28:t=fill,drawbox=x=0:y=1450:w=1080:h=470:color=black@0.25:t=fill,eq=saturation=1.12:contrast=1.04,subtitles=titles.ass"
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', 'joined.mp4', '-i', 'mix.wav', '-vf', vf, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', '/home/user/gta6_map_ru.mp4'], check=True)
print('done', round(TOT, 1), 's')
