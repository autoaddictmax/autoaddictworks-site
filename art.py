"""Procedural atmosphere art (no stock photos). Replace with real shop photos in static/img/photos/."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
rng=np.random.default_rng(7)
def save(a,name,q=82):
    Image.fromarray(np.clip(a,0,255).astype('uint8')).save(f'static/img/art/{name}',quality=q,optimize=True,progressive=True)
def base(W,H,top=(11,12,14),bot=(20,21,24)):
    y=np.linspace(0,1,H)[:,None,None]
    return np.ones((H,W,3))*(np.array(top)*(1-y)+np.array(bot)*y)
def glow(W,H,cx,cy,rx,ry,col,amt):
    yy,xx=np.mgrid[0:H,0:W]
    d=((xx-cx)/rx)**2+((yy-cy)/ry)**2
    return np.exp(-d)[:,:,None]*np.array(col)[None,None,:]*amt
def grain(a,s=5):
    return a+rng.normal(0,s,a.shape[:2])[:,:,None]
def vignette(a,k=0.55):
    H,W=a.shape[:2];yy,xx=np.mgrid[0:H,0:W]
    d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    return a*(1-k*np.clip(d-0.35,0,1)[:,:,None])

# ---- HERO: night workshop — perspective ceiling light bars, glossy floor, gold spotlight
W,H=2400,1300
a=base(W,H,(8,9,11),(16,17,20))
layer=Image.new('RGB',(W,H),0);d=ImageDraw.Draw(layer)
vpx,vpy=W*0.66,H*0.50   # vanishing point
for row in range(9):
    t=row/8.0; y=vpy-60-(1-t)**1.8*520
    span=40+ (1-t)**1.8*900; h=max(3,16*(1-t)**1.6)
    for col in (-1.0,-0.35,0.35,1.0):
        x=vpx+col*span; w=max(10,190*(1-t)**1.7)
        d.rectangle([x-w/2,y,x+w/2,y+h],fill=(235,240,245))
# side pillars (blue-grey steel)
for k,x in enumerate([W*0.08,W*0.30,W*0.88,W*0.98]):
    d.rectangle([x,H*0.12,x+(26 if k in(1,2) else 40),H*0.72],fill=(44,48,54))
L=np.asarray(layer.filter(ImageFilter.GaussianBlur(3))).astype(float)
Lb=np.asarray(layer.filter(ImageFilter.GaussianBlur(26))).astype(float)
a+=L*0.55+Lb*0.5
# floor: reflection of lights (flipped, stretched, blurred)
fl=np.flipud(L+Lb)[:, :, :]
mask=np.clip((np.arange(H)-vpy)/(H-vpy),0,1)[:,None,None]
refl=np.asarray(Image.fromarray(np.clip(fl,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(14))).astype(float)
shift=int(H*0.0)
a+=refl*0.45*mask*(np.arange(H)[:,None,None]>vpy)
# floor horizon line & sheen
a+=glow(W,H,vpx,vpy+40,W*0.55,40,(180,190,200),0.18)
# gold spotlight pool where car/emblem sits
a+=glow(W,H,W*0.68,H*0.78,W*0.26,H*0.10,(201,179,138),0.55)
a+=glow(W,H,W*0.68,H*0.45,W*0.30,H*0.35,(201,179,138),0.10)
a=vignette(grain(a,4),0.6)
save(a,'hero.jpg',80)

# ---- Generic tiles (services / approach / band)
def tile(name,W,H,cx,cy,col=(201,179,138),streak=True,seed=0):
    r=np.random.default_rng(seed)
    a=base(W,H,(11,12,14),(22,23,26))
    a+=glow(W,H,W*cx,H*cy,W*0.45,H*0.35,col,0.32)
    if streak:
        lay=Image.new('RGB',(W,H),0);dd=ImageDraw.Draw(lay)
        for i in range(7):
            y=H*(0.15+0.1*i)+r.normal(0,8); x0=r.uniform(-0.2,0.4)*W
            dd.line([x0,y,x0+W*r.uniform(0.6,1.2),y-H*0.18],fill=(220,200,160),width=int(r.uniform(1,3)))
        S=np.asarray(lay.filter(ImageFilter.GaussianBlur(2))).astype(float)
        a+=S*0.25
    a=vignette(grain(a,5),0.5); save(a,name,78)
tile('tile-1.jpg',900,640,.7,.6,seed=1)
tile('tile-2.jpg',900,640,.3,.4,seed=2)
tile('tile-3.jpg',900,640,.6,.3,seed=3)
tile('tile-4.jpg',900,640,.5,.7,seed=4)
tile('approach.jpg',1400,900,.35,.55,(150,155,165),seed=5)
# band: sweeping track curve
W,H=2400,700
a=base(W,H,(13,14,17),(8,9,11))
lay=Image.new('RGB',(W,H),0);dd=ImageDraw.Draw(lay)
import math
for k,(off,wid,c) in enumerate([(0,70,(52,56,62)),(60,10,(201,179,138)),(-60,6,(241,235,223))]):
    pts=[(W*0.55+ (t*W*0.6)+off, H*1.1 - (t**0.6)*H*1.3) for t in np.linspace(0,1,60)]
    dd.line(pts,fill=c,width=wid,joint='curve')
S=np.asarray(lay.filter(ImageFilter.GaussianBlur(4))).astype(float)
a+=S*0.8; a+=glow(W,H,W*0.85,H*0.2,W*0.3,H*0.5,(201,179,138),0.25)
a=vignette(grain(a,4),0.5); save(a,'band.jpg',78)
