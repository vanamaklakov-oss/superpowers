import json,re
ST={1:0.2,2:5.85,3:13.95,4:24.0,5:28.1,6:34.45,7:37.95,8:42.75}
KEY={'gta','6','pc','ps5','eight','zen','2','3.5','gigahertz','ryzen','3700x','10.3','teraflops','rx','6700','rtx','2070','super','3060','16','gigs','ram','ssd','5.5','nvme','minimum','1080p','30','fps','60','4070','32','estimates','specs'}
lines={int(l.split('|')[0]):l.split('|',1)[1].strip() for l in open('lines.txt',encoding='utf-8')}
t=lambda x:'%d:%02d:%05.2f'%(x//3600,(x%3600)//60,x%60)
out=[]
for n,st in ST.items():
    w=json.load(open(f'v{n}.mp3.json')); toks=lines[n].split(); assert len(toks)>=len(w)
    # align spoken words to the written tokens (keep punctuation)
    words=[]; j=0
    for x in w:
        while j<len(toks) and toks[j].strip('.,!?:;"').lower()!=x['w'].lower().strip('.,!?'): j+=1
        words.append((toks[j] if j<len(toks) else x['w'],x['s'],x['s']+x['d'])); j+=1
    chunks=[];cur=[]
    for wd in words:
        cur.append(wd)
        if len(cur)==3 or wd[0][-1] in '.,:?!' : chunks.append(cur);cur=[]
    if cur: chunks.append(cur)
    for i,c in enumerate(chunks):
        a=st+c[0][1]; b=st+(chunks[i+1][0][1] if i+1<len(chunks) else c[-1][2]+0.3)
        txt=' '.join(('{\\c&H0000E1FF&}'+s.upper()+'{\\c&HFFFFFF&}') if s.strip('.,!?:;"').lower() in KEY else s.upper() for s,_,_ in c)
        out.append(f'Dialogue: 0,{t(a)},{t(b)},Cap,,0,0,0,,{{\\fscx120\\fscy120\\t(0,110,\\fscx100\\fscy100)}}'+txt)
hdr='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,8,4,2,70,70,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
open('caps.ass','w').write(hdr+'\n'.join(out)+'\n'); print(len(out),'captions')
