import numpy as np
from PIL import Image, ImageDraw, ImageFont
import chargen as cg

SCALE=5
def F(sz):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
    except: return ImageFont.load_default()

def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c[:3])

def char_img(recipe):
    a=cg.compose(recipe)
    return Image.fromarray(a,'RGBA')

# ---------- furniture (drawn on a logical RGBA ImageDraw) ----------
def plankfloor(d,w,h,base,y0):
    d.rectangle([0,y0,w,h],fill=base+(255,))
    dk=shade(base,0.93)
    for y in range(y0,h,16): d.line([(0,y),(w,y)],fill=dk+(255,))
    for x in range(0,w,16): d.line([(x,y0),(x,h)],fill=dk+(255,))

def wall(d,w,wallc,y1):
    d.rectangle([0,0,w,y1],fill=wallc+(255,))
    d.rectangle([0,y1-3,w,y1],fill=shade(wallc,0.82)+(255,))  # baseboard

def window(d,x,y,wc=(150,205,235)):
    d.rectangle([x,y,x+22,y+14],fill=shade((90,110,130),1.0)+(255,))
    d.rectangle([x+1,y+1,x+21,y+13],fill=wc+(255,))
    d.line([(x+11,y+1),(x+11,y+13)],fill=(235,245,250,255))
    d.line([(x+1,y+7),(x+21,y+7)],fill=(235,245,250,255))

def wallart(d,x,y,col):
    d.rectangle([x,y,x+16,y+12],fill=(70,60,55,255))
    d.rectangle([x+1,y+1,x+15,y+11],fill=col+(255,))

def plant(d,x,y):
    d.rectangle([x+2,y+8,x+8,y+13],fill=(150,95,60,255))      # pot
    d.rectangle([x+3,y+9,x+7,y+12],fill=(120,75,48,255))
    d.ellipse([x,y,x+10,y+8],fill=(80,165,90,255))
    d.ellipse([x+2,y-3,x+8,y+3],fill=(70,150,80,255))
    d.ellipse([x+4,y+1,x+11,y+7],fill=(95,180,100,255))

def rug(d,x0,y0,x1,y1,col):
    d.rectangle([x0,y0,x1,y1],fill=col+(255,))
    d.rectangle([x0+3,y0+3,x1-3,y1-3],outline=shade(col,0.85)+(255,),width=1)

def chair(d,cx,by,col=(60,62,72)):
    d.rectangle([cx-6,by-4,cx+6,by+4],fill=col+(255,))
    d.rectangle([cx-6,by-12,cx+6,by-4],fill=shade(col,1.15)+(255,))

def desk(d,cx,by,wood=(150,110,70)):
    d.rectangle([cx-18,by-6,cx+18,by-2],fill=shade(wood,1.1)+(255,))   # top
    d.rectangle([cx-18,by-2,cx+18,by+12],fill=wood+(255,))             # front
    d.rectangle([cx-18,by-6,cx+18,by-6],fill=shade(wood,0.7)+(255,))
    d.line([(cx-18,by+12),(cx+18,by+12)],fill=shade(wood,0.7)+(255,))

def monitor(d,cx,by,screen=(120,170,210)):
    d.rectangle([cx-7,by-16,cx+7,by-7],fill=(40,42,50,255))
    d.rectangle([cx-6,by-15,cx+6,by-8],fill=screen+(255,))
    d.rectangle([cx-1,by-7,cx+1,by-6],fill=(40,42,50,255))

def mug(d,cx,by,col=(210,90,70)):
    d.rectangle([cx-2,by-9,cx+2,by-6],fill=col+(255,)); d.point((cx+3,by-8),fill=col+(255,))

def papers(d,cx,by):
    d.rectangle([cx-4,by-8,cx+3,by-6],fill=(240,240,235,255))
    d.line([(cx-3,by-7),(cx+1,by-7)],fill=(150,150,150,255))

def deskplant(d,cx,by):
    d.rectangle([cx-2,by-8,cx+2,by-6],fill=(150,95,60,255)); d.ellipse([cx-3,by-12,cx+3,by-7],fill=(80,165,90,255))

# zone-special props
def whiteboard(d,x,y):
    d.rectangle([x,y,x+34,y+20],fill=(60,60,66,255)); d.rectangle([x+1,y+1,x+33,y+19],fill=(245,245,242,255))
    d.line([(x+4,y+5),(x+20,y+5)],fill=(80,140,210,255)); d.line([(x+4,y+9),(x+26,y+9)],fill=(70,160,90,255))
    d.line([(x+4,y+13),(x+16,y+13)],fill=(210,90,70,255))
def serverrack(d,x,y):
    d.rectangle([x,y,x+14,y+30],fill=(45,47,55,255))
    for yy in range(y+2,y+30,4):
        d.rectangle([x+2,yy,x+12,yy+2],fill=(70,72,82,255)); d.point((x+11,yy),fill=(90,230,140,255))
def vault(d,x,y):
    d.rectangle([x,y,x+22,y+24],fill=(80,82,92,255)); d.rectangle([x+2,y+2,x+20,y+22],fill=(110,112,122,255))
    d.ellipse([x+7,y+8,x+15,y+16],fill=(60,62,70,255)); d.ellipse([x+9,y+10,x+13,y+14],fill=(240,200,64,255))
def alarm(d,x,y):
    d.rectangle([x+1,y+4,x+7,y+8],fill=(60,60,66,255)); d.ellipse([x,y,x+8,y+6],fill=(230,70,60,255)); d.ellipse([x+2,y+1,x+6,y+4],fill=(255,150,140,255))
def easel(d,x,y):
    d.line([(x,y+24),(x+6,y)],fill=(120,85,55,255),width=1); d.line([(x+14,y+24),(x+8,y)],fill=(120,85,55,255),width=1)
    d.rectangle([x,y,x+14,y+14],fill=(245,245,240,255),outline=(120,85,55,255))
    d.rectangle([x+3,y+3,x+7,y+7],fill=(210,90,120,255)); d.rectangle([x+8,y+7,x+11,y+10],fill=(80,140,210,255))
def chessboard(d,x,y):
    for i in range(4):
        for j in range(4):
            c=(235,225,200) if (i+j)%2==0 else (90,70,55)
            d.rectangle([x+i*4,y+j*4,x+i*4+3,y+j*4+3],fill=c+(255,))
def coffee(d,x,y):
    d.rectangle([x,y+6,x+16,y+20],fill=(70,72,80,255)); d.rectangle([x+2,y,x+14,y+8],fill=(95,98,108,255))
    d.rectangle([x+4,y+10,x+12,y+16],fill=(40,42,48,255)); d.point((x+8,y+3),fill=(220,220,220,255))

ZONE_LABELS=["Strateji ve marka","Yaratıcı ekip","Pazarlama ve büyüme","Müşteri ve operasyon","Analitik, ürün ve teknik"]

def specials(d,zi,Wpx,WALLY,Hpx):
    if zi==0:
        wallart(d,Wpx//2-8,9,(150,170,210))
        d.rectangle([Wpx-72,WALLY+44,Wpx-34,WALLY+54],fill=(150,115,75,255))
        chessboard(d,Wpx-68,WALLY+26)
    elif zi==1:
        wallart(d,40,9,(230,150,180)); wallart(d,Wpx-58,9,(250,200,120))
        easel(d,14,WALLY+26)
    elif zi==2:
        whiteboard(d,Wpx//2-17,6)
        coffee(d,8,WALLY+24)
    elif zi==3:
        wallart(d,Wpx//2-8,9,(240,160,90)); alarm(d,Wpx-34,9)
        coffee(d,8,WALLY+24)
    elif zi==4:
        whiteboard(d,Wpx//2-17,6); serverrack(d,6,WALLY+16); vault(d,Wpx-30,WALLY+20)

def render_zone(zi):
    dn,dc,ags=cg.DOMAINS[zi]
    n=len(ags)
    cols = 4 if n>4 else max(2,n)
    rows=(n+cols-1)//cols
    floor_light = tuple(int(v*0.35+200*0.65) for v in dc)
    rugc = tuple(int(v*0.55+255*0.45) for v in dc)
    wallc=(214,210,200)
    Wpx = max(cols*64+24, 280)
    WALLY=30
    Hpx = WALLY + rows*82 + 24
    img=Image.new('RGBA',(Wpx,Hpx),(0,0,0,0))
    d=ImageDraw.Draw(img)
    plankfloor(d,Wpx,Hpx,floor_light,WALLY-3)
    wall(d,Wpx,wallc,WALLY)
    window(d,18,8); window(d,Wpx-40,8)
    rug(d,12,WALLY+6,Wpx-12,Hpx-10,rugc)
    specials(d,zi,Wpx,WALLY,Hpx)
    plant(d,4,Hpx-18); plant(d,Wpx-14,Hpx-18)
    for i,(nm,rc) in enumerate(ags):
        r,c=divmod(i,cols)
        cx=24+32 + c*64
        by=WALLY+58 + r*82
        chair(d,cx,by+6)
        img.alpha_composite(char_img(rc),(cx-16, by-34))
        desk(d,cx,by, wood=(150,115,75))
        monitor(d,cx-9,by, screen=tuple(int(v*0.5+150*0.5) for v in dc))
        mug(d,cx+10,by); papers(d,cx+2,by); deskplant(d,cx+14,by)
    return img

def finalize(zi):
    img=render_zone(zi)
    big=img.resize((img.width*SCALE,img.height*SCALE),Image.NEAREST)
    out=Image.new('RGBA',(big.width, big.height+50),(247,246,241,255))
    out.alpha_composite(big,(0,50))
    dd=ImageDraw.Draw(out)
    dc=cg.DOMAINS[zi][1]
    dd.rectangle([18,15,30,40],fill=dc+(255,))
    dd.text((42,16),ZONE_LABELS[zi],fill=(45,45,52,255),font=F(26))
    n=len(cg.DOMAINS[zi][2])
    dd.text((42,40),f"{n} ajan",fill=(120,120,128,255),font=F(15))
    return out.convert('RGB')

if __name__=='__main__':
    import os
    os.makedirs('/home/claude/ofis',exist_ok=True)
    slugs=['strateji-marka','yaratici','pazarlama','musteri-operasyon','analitik-teknik']
    imgs=[]
    for zi in range(5):
        im=finalize(zi); imgs.append(im)
        im.save(f'/home/claude/ofis/zon-{zi+1}-{slugs[zi]}.png')
        print('zone',zi+1,im.size)
    # overview: stack
    Wm=max(i.width for i in imgs); tot=sum(i.height for i in imgs)+ (len(imgs)+1)*16
    ov=Image.new('RGB',(Wm+32, tot),(239,238,232))
    y=16
    for im in imgs:
        ov.paste(im,(16,y)); y+=im.height+16
    ov.save('/home/claude/ofis/_ofis-tam.png'); print('overview',ov.size)
