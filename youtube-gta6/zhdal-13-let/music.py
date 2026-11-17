import numpy as np, wave, sys
SR=48000; TOT=26.0; N=int(SR*TOT); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(3)
def add(s,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(s),N-i)
    if n>0: L[i:i+n]+=s[:n]*g*(1-max(0,pan)); R[i:i+n]+=s[:n]*g*(1+min(0,pan))
def hz(m): return 440*2**((m-69)/12)
def piano(m,d=2.5,v=0.5):
    t=np.arange(int(SR*d))/SR; f=hz(m)
    s=sum(a*np.sin(2*np.pi*f*k*t)*np.exp(-t*(1.2+k*0.9)) for k,a in [(1,1),(2,0.45),(3,0.2),(4,0.1)])
    s*=np.minimum(1,t*200); return s*v
def pad(ms,d,v=0.08):
    t=np.arange(int(SR*d))/SR; s=sum(np.sin(2*np.pi*hz(m)*(1+dt)*t) for m in ms for dt in (-0.003,0.003))
    env=np.minimum(1,t/1.2)*np.minimum(1,(d-t)/1.0); return s*env*v/len(ms)
B=60/72
prog=[(57,[57,60,64]),(53,[53,57,60]),(48,[52,55,60]),(55,[55,59,62])]
# waiting part 0-13s: arpeggios
t=0.0; k=0
while t<12.6:
    root,ch=prog[k%4]
    add(piano(root-12,3.5,0.35),t,1,0); add(pad(ch,4*B+0.3),t,1)
    for j,m in enumerate([ch[0],ch[1],ch[2],ch[1]+12]):
        if t+j*B<12.8: add(piano(m+12,2.2,0.22),t+j*B,1,0.3*((-1)**j))
    t+=4*B; k+=1
# calendar 13-15: heartbeat + swell
for tt in (13.1,13.45,14.1,14.45):
    tb=np.arange(int(SR*0.25))/SR; add(np.sin(2*np.pi*55*tb)*np.exp(-tb*18),tt,0.9)
sw=pad([57,64,69],2.2,0.12); add(sw*np.linspace(0.2,1.3,len(sw)),13.0,1)
# emotional 15-19: major, bigger
for j,(r,ch) in enumerate([(48,[60,64,67]),(53,[60,65,69])]):
    tt=15.0+j*2.0; add(piano(r-12,3,0.4),tt); add(pad(ch,2.3,0.13),tt)
    for q,m in enumerate([ch[0]+12,ch[1]+12,ch[2]+12]): add(piano(m,2,0.25),tt+q*0.5,1,0.2*(q-1))
fade=np.ones(N); i0=int(18.7*SR); i1=int(19.0*SR); fade[i0:i1]=np.linspace(1,0,i1-i0); fade[i1:]=0
L*=fade; R*=fade
# loading 19-21.5: UI blips + hum
for tt in (19.3,19.9,20.5,21.1):
    tb=np.arange(int(SR*0.08))/SR; add(np.sin(2*np.pi*1320*tb)*np.exp(-tb*40)*0.25,tt)
th=np.arange(int(SR*2.4))/SR; add(np.sin(2*np.pi*60*th)*0.05*np.minimum(1,th*3),19.05)
# sad trombone 21.5
def tromb(m,d,vib=False):
    t=np.arange(int(SR*d))/SR; f=hz(m)*(1+ (0.02*np.sin(2*np.pi*6*t)*np.minimum(1,t*2) if vib else 0))
    ph=2*np.pi*np.cumsum(f)/SR; s=sum(np.sin(k*ph)/k**1.2 for k in range(1,8))
    env=np.minimum(1,t*25)*np.minimum(1,(d-t)*8)*(1-0.15*t/d); return np.tanh(1.5*s)*env*0.3
tt=21.6
for m,d in [(55,0.42),(54,0.42),(53,0.42)]: add(tromb(m,d),tt); tt+=0.45
add(tromb(52,1.9,True),tt)
out=np.stack([L,R],1); out/=np.max(np.abs(out))*1.1
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
