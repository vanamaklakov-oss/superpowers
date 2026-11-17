import numpy as np, wave, sys
SR=48000; TOT=39.0; N=int(SR*TOT); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(11)
def add(s,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(s),N-i)
    if n>0: L[i:i+n]+=s[:n]*g*(1-max(0,pan)); R[i:i+n]+=s[:n]*g*(1+min(0,pan))
def hz(m): return 440*2**((m-69)/12)
def lp(x,a):
    y=np.empty_like(x); s=0.0
    for k in range(len(x)): s=a*s+(1-a)*x[k]; y[k]=s
    return y
B=0.5
def ep(m,d,v):  # electric-piano-ish
    t=np.arange(int(SR*d))/SR; f=hz(m)
    return (np.sin(2*np.pi*f*t+0.8*np.sin(2*np.pi*f*2*t)*np.exp(-t*3)))*np.exp(-t*1.6)*np.minimum(1,t*300)*v
prog=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]
bars=int(TOT/(4*B))+1
for b in range(bars):
    t0=b*4*B; ch=prog[b%4]
    for j,m in enumerate(ch): add(ep(m+12,2.2,0.07),t0+j*0.012,1,0.3*(j-1.5)/1.5)
    add(ep(ch[0]-12,1.6,0.16),t0); add(ep(ch[0]-12,1.0,0.1),t0+2*B)
    for q in range(4):
        tt=t0+q*B
        k=np.arange(int(SR*0.3))/SR; kick=np.sin(2*np.pi*np.cumsum(50+60*np.exp(-k*30))/SR)*np.exp(-k*9)
        if q in (0,2): add(kick,tt,0.35)
        h=np.arange(int(SR*0.04))/SR; hat=(rng.standard_normal(len(h)))*np.exp(-h*90); hat=hat-lp(hat,0.6)
        add(hat,tt+B/2,0.05,0.4)
        if q in (1,3):
            s=np.arange(int(SR*0.18))/SR; sn=rng.standard_normal(len(s))*np.exp(-s*25); add(sn-lp(sn,0.85),tt,0.06)
# eraser swishes at chapter changes (frames /30)
for f in (140,270,455,640,790,955,1060):
    n=int(SR*0.45); t=np.arange(n)/SR; x=rng.standard_normal(n); x=lp(x,0.7)-lp(x,0.97)
    env=np.sin(np.pi*t/0.45)**1.5; add(x*env*0.5,f/30-0.02,1,0.0)
fade=np.ones(N); i=int((TOT-2.5)*SR); fade[i:]=np.linspace(1,0,N-i); L*=fade; R*=fade
out=np.stack([L,R],1); out/=np.max(np.abs(out))*1.15
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
