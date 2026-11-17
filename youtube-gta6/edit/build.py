import subprocess, sys
B=60/128; FPS=30
W='../wait/'
dur={1:3.7,2:2.205,3:4.109,4:1.833,5:3.668,6:1.867,7:1.8,8:3.033}
segs=[(8,1.47,3),(1,0.37,3),(3,1.5,4),(1,2.03,3),(2,0,4),(5,0,2),(5,1.13,5),(6,0,4),(7,0,2),(7,0.87,2),(3,0,3),(8,0,3)]
end_t=20.0
inputs=[];fil=[];t=0.0;labels=[]
for k,(c,s,b) in enumerate(segs+[(4,0,None)]):
    st=t; en=end_t if b is None else t+b*B
    nf=round(en*FPS)-round(st*FPS); need=nf/FPS
    if b is None: src_end=dur[c]-0.02
    else:
        src_end=min(dur[c]-0.02, s+need) if c!=7 or s>0 else 0.86
        if c==7 and s>0: src_end=dur[c]-0.02
        if c==3 and s==0: src_end=min(src_end,1.49)
    avail=src_end-s; fac=max(1.0,need/avail)
    inputs+=['-i',W+f'w{c}.mov']
    flash = 0.22 if k==2 else (0.12 if k>=1 else 0)
    punch = k>=2
    z = "if(lte(on,6),1.14-0.14*on/6,1)" if punch else "1+0.0015*on"
    chain=(f"[{k}:v:0]trim={s}:{src_end},setpts=(PTS-STARTPTS)*{fac:.4f},fps={FPS},"
           f"tpad=stop_mode=clone:stop_duration=1,trim=end_frame={nf},setpts=PTS-STARTPTS,"
           f"scale=1920:1080,setsar=1,split[a{k}][b{k}];"
           f"[a{k}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.2[bg{k}];"
           f"[b{k}]scale=1500:844,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1500x844:fps={FPS},crop=1080:844[fg{k}];"
           f"[bg{k}][fg{k}]overlay=0:(H-h)/2,format=yuv420p")
    if flash: chain+=f",fade=t=in:st=0:d={flash}:color=white"
    if b is None: chain+=f",fade=t=out:st={need-0.35:.3f}:d=0.35"
    chain+=f"[v{k}]"
    fil.append(chain); labels.append(f"[v{k}]"); t=en
    print(k,c,round(st,3),round(en,3),'fac',round(fac,3),file=sys.stderr)
n=len(labels)
fil.append("".join(labels)+f"concat=n={n}:v=1:a=0,subtitles=subs.ass[v]")
cmd=['ffmpeg','-loglevel','error','-y']+inputs+['-i','beat.wav','-filter_complex',";".join(fil),
 '-map','[v]','-map',f'{n}:a','-t',str(end_t),'-af','afade=t=out:st=19.2:d=0.8,loudnorm=I=-14:TP=-1.2',
 '-c:v','libx264','-preset','slow','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','/home/user/gta6_edit.mp4']
subprocess.run(cmd,check=True)
