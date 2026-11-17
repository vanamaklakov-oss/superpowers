import numpy as np, wave, sys
SR=48000; BPM=128; B=60/BPM; NB=40; DROP=6
T=int(SR*(NB*B+1.5)); L=np.zeros(T); R=np.zeros(T)
rng=np.random.default_rng(7)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),T-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*gain*(1-max(0,pan)); R[i:i+n]+=sig[:n]*gain*(1+min(0,pan))
def lp(x,c):
    a=np.exp(-2*np.pi*c/SR); y=np.zeros_like(x); s=0.0
    for k in range(len(x)): s=(1-a)*x[k]+a*s; y[k]=s
    return y
def hp(x,c): return x-lp(x,c)
def kick():
    t=np.arange(int(SR*0.45))/SR; f=45+80*np.exp(-t*28)
    ph=2*np.pi*np.cumsum(f)/SR; s=np.sin(ph)*np.exp(-t*7)
    s+=0.3*np.exp(-t*300)*rng.standard_normal(len(t)); return np.tanh(1.6*s)
def clap():
    t=np.arange(int(SR*0.25))/SR; n=rng.standard_normal(len(t))
    env=np.exp(-t*22)+0.6*np.exp(-((t-0.012)*400)**2)+0.5*np.exp(-((t-0.024)*400)**2)
    return hp(lp(n,4000),900)*env*0.9
def hat(d=0.06):
    t=np.arange(int(SR*d))/SR; return hp(rng.standard_normal(len(t)),7000)*np.exp(-t*60)*0.35
def saw(f,dur,det=(0,)):
    t=np.arange(int(SR*dur))/SR; s=np.zeros(len(t))
    for d in det: ph=(t*f*(1+d)+rng.random())%1; s+=2*ph-1
    return s/len(det)
def note(m): return 440*2**((m-69)/12)
chords=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]]  # Am F C G
bass=[45,41,48,43]
kenv=np.ones(T)
for b in range(NB):
    t0=b*B; bar=b//4; ch=chords[bar%4]
    if b>=DROP and b<NB-2:
        add(kick(),t0,0.9)
        i=int(t0*SR); n=int(0.3*SR); kenv[i:i+n]=np.minimum(kenv[i:i+n],1-0.75*np.exp(-np.arange(n)/SR*12))
        if b%2==1: add(clap(),t0,0.55)
        add(hat(),t0+B/2,0.6,0.3); add(hat(0.03),t0+B*0.75,0.3,-0.3)
        bl=lp(saw(note(bass[bar%4]),B*0.45,(0,0.004)),500)*np.exp(-np.arange(int(SR*B*0.45))/SR*4)
        add(np.tanh(2*bl)*0.5,t0+B/2,0.6)
    if b<DROP:
        add(hat(0.03),t0,0.25+0.05*b,0.2); add(hat(0.03),t0+B/2,0.2,-0.2)
    if b%4==0 and b<NB-2:
        dur=4*B; pad=sum(saw(note(m+12),dur,(-0.01,-0.004,0.004,0.01)) for m in ch)/3
        cut=900 if b<DROP else 2600
        pad=lp(pad,cut); env=np.minimum(1,np.arange(len(pad))/SR*8)*np.minimum(1,(len(pad)-np.arange(len(pad)))/SR*6)
        add(pad*env*0.22,t0,1,0.25); add(pad*env*0.22,t0+0.012,1,-0.25)
    if b>=DROP and b<NB-2 and b%2==0:
        st=sum(saw(note(m+24),B*0.35,(-0.006,0.006)) for m in ch)/3
        st=lp(st,3500)*np.exp(-np.arange(len(st))/SR*9); add(st*0.18,t0+B*0.5,1)
# riser into drop
rd=DROP*B-1.6; n=int(1.6*SR); t=np.arange(n)/SR
rs=hp(rng.standard_normal(n),300)*(t/1.6)**2*0.35; add(rs,rd,1)
sw=np.sin(2*np.pi*np.cumsum(200+1800*(t/1.6)**2)/SR)*(t/1.6)**2*0.08; add(sw,rd,1)
# impact at drop and at end
for tt in (DROP*B,(NB-2)*B):
    k=kick(); add(k,tt,0.6)
    n=int(1.4*SR); tt2=np.arange(n)/SR; add(lp(rng.standard_normal(n),2500)*np.exp(-tt2*3)*0.25,tt,1)
    sub=np.sin(2*np.pi*42*tt2)*np.exp(-tt2*2.5)*0.6; add(sub,tt,1)
# sidechain pads/bass already summed: apply mild duck to everything except kicks is complex; apply global light duck
L*=0.75+0.25*kenv; R*=0.75+0.25*kenv
out=np.stack([L,R],1); out/=np.max(np.abs(out))*1.12; out=np.tanh(out*1.3)/np.tanh(1.3)*0.9
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
print('len',T/SR)
