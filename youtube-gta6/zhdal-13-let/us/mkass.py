import json
starts={1:0.35,2:5.0,3:9.0,4:15.4}
KEY={'gta','5','six','years','where','son','together','real','finally','made'}
def t(x):
    return '%d:%02d:%05.2f'%(x//3600,(x%3600)//60,x%60)
C='m 0 -150 b 83 -150 150 -83 150 0 b 150 83 83 150 0 150 b -83 150 -150 83 -150 0 b -150 -83 -83 -150 0 -150'
hdr='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Inter Display Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,7,0,8,50,50,170,1
Style: Year,Inter Display Black,170,&H0000E1FF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,6,0,1,9,0,8,50,50,300,1
Style: Cap,Inter Display Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,9,4,2,60,60,560,1
Style: Big,Inter Display Black,150,&H00FFFFFF,&H00FFFFFF,&H000000C8,&H80000000,0,0,0,0,100,100,0,0,1,12,0,5,40,40,0,1
Style: Cta,Inter Display Black,70,&H0000E1FF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,7,0,2,60,60,420,1
Style: Draw,Inter Display Black,10,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Txt,Inter Display Black,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
ev=[]
D=lambda *a: ev.append('Dialogue: '+','.join(map(str,a)))
pop='{\\fscx125\\fscy125\\t(0,120,\\fscx100\\fscy100)}'
D(2,t(0),t(3.2),'Hook','',0,0,0,'','{\\fad(0,200)}HE WAITED FOR {\\c&H0000E1FF&}GTA 6{\\c&HFFFFFF&}...')
for a,b,y in [(0,4.5,2013),(4.5,8.5,2018),(8.5,13,2022),(15,19,2026)]:
    D(1,t(a),t(b),'Year','',0,0,0,'',pop+str(y))
import re
# captions
CH={1:[(2,'FINALLY BEAT'),(2,'*GTA 5!*'),(4,'*SIX* IS COMING OUT'),(3,'IN A COUPLE'),(2,'OF *YEARS!*')],
    2:[(1,'SOOO...'),(3,'*WHERE* IS IT?')],
    3:[(1,'*SON,*'),(2,'SOMEDAY WE\'LL'),(3,'PLAY IT *TOGETHER...*')],
    4:[(3,'IS THIS *REAL?*'),(2,'I FINALLY'),(2,'*MADE IT...*')]}
def hl(x): return re.sub(r'\*(.+?)\*', lambda m:'{\c&H0000E1FF&}'+m.group(1)+'{\c&HFFFFFF&}', x)
for n,st in starts.items():
    w=json.load(open(f'l{n}.mp3.json')); i=0; spans=[]
    for k,txt in CH[n]:
        spans.append((w[i]['s'], w[i+k-1]['s']+w[i+k-1]['d'], txt)); i+=k
    assert i==len(w),(n,i,len(w))
    for j,(a,e,txt) in enumerate(spans):
        b = spans[j+1][0] if j+1<len(spans) else e+0.3
        D(0,t(st+a),t(st+b),'Cap','',0,0,0,'',pop+hl(txt))
# calendar card 13-15
D(0,t(13),t(15),'Draw','',0,0,0,'','{\\pos(240,560)\\1c&HF4F4F4&\\p1}m 0 0 l 600 0 l 600 760 l 0 760{\\p0}')
D(1,t(13),t(15),'Draw','',0,0,0,'','{\\pos(240,560)\\1c&H2828D2&\\p1}m 0 0 l 600 0 l 600 170 l 0 170{\\p0}')
D(2,t(13),t(15),'Txt','',0,0,0,'','{\\pos(540,645)\\fs72}NOVEMBER 2026')
D(2,t(13),t(15),'Txt','',0,0,0,'','{\\pos(540,1030)\\fs330\\c&H202020&}19')
D(3,t(13.35),t(15),'Draw','',0,0,0,'','{\\an7\\pos(540,1030)\\1a&HFF&\\3c&H0000E6&\\bord16\\fscx0\\fscy0\\t(0,350,\\fscx125\\fscy125)\\p1}'+C+'{\\p0}')
# loading 19-21.5
D(0,t(19),t(21.5),'Txt','',0,0,0,'','{\\pos(540,820)\\fs66}Downloading update...')
D(0,t(19),t(21.5),'Draw','',0,0,0,'','{\\pos(170,920)\\1a&HFF&\\3c&HFFFFFF&\\bord5\\p1}m 0 0 l 740 0 l 740 56 l 0 56{\\p0}')
D(1,t(19),t(21.5),'Draw','',0,0,0,'','{\\pos(170,920)\\1c&H00D0FF&\\fscx0\\t(0,2500,\\fscx3)\\p1}m 0 0 l 740 0 l 740 56 l 0 56{\\p0}')
D(0,t(19),t(21.5),'Txt','',0,0,0,'','{\\pos(540,1080)\\fs60\\c&HBBBBBB&}Time left: 9 h 12 min')
D(2,t(21.6),t(26),'Big','',0,0,0,'','{\\pos(540,1180)\\fscx40\\fscy40\\t(0,180,\\fscx110\\fscy110)\\t(180,300,\\fscx100\\fscy100)}9 MORE\\NHOURS?!')
D(1,t(23.6),t(26),'Cta','',0,0,0,'','{\\fad(200,0)}HOW LONG DID YOU WAIT?')
open('us.ass','w').write(hdr+'\n'.join(ev)+'\n')
print(len(ev),'events')
