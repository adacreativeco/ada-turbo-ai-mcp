from PIL import Image, ImageDraw, ImageFont
import env, chargen as cg

SCALE=4
def Ft(s):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
    except: return ImageFont.load_default()
def sh(c,f): return tuple(max(0,min(255,int(v*f))) for v in c[:3])

# building geometry (logical px)
LEFTW=6; ROOMX0=LEFTW; ROOMW=300; ROOMX1=ROOMX0+ROOMW
IWALL=4; CORX0=ROOMX1+IWALL; CORW=46; CORX1=CORX0+CORW; RIGHTW=6
BUILDW=CORX1+RIGHTW
FH=84; SLAB=10
# floor plan: (kind, dept_index)
FLOORS=[('dept',0),('dept',1),('meeting',None),('dept',2),('dept',3),('dept',4)]
NF=len(FLOORS)
TOTH=SLAB+NF*(FH+SLAB)

WALLC=(206,202,192); SLABC=(150,146,138); CORC=(196,198,205)

def win(d,x,y):
    d.rectangle([x,y,x+18,y+12],fill=(70,90,110,255))
    d.rectangle([x+1,y+1,x+17,y+11],fill=(150,205,235,255))
    d.line([(x+9,y+1),(x+9,y+11)],fill=(235,245,250,255))
    d.line([(x+1,y+6),(x+17,y+6)],fill=(235,245,250,255))

def door(d,x,y,h,col=(150,110,70)):
    d.rectangle([x,y,x+IWALL+1,y+h],fill=sh(col,0.7)+(255,))      # frame
    d.rectangle([x,y+2,x+IWALL+1,y+h-2],fill=col+(255,))          # open leaf
    d.point((x+IWALL-1,y+h//2),fill=(240,220,120,255))            # handle

def floor_room(d,img,i):
    kind,di=FLOORS[i]
    y0=SLAB + i*(FH+SLAB)
    yr=y0; yb=y0+FH
    dc = cg.DOMAINS[di][1] if di is not None else (120,120,130)
    tint = tuple(int(v*0.30+205*0.70) for v in dc)
    # floor surface
    d.rectangle([ROOMX0,yr,ROOMX1,yb],fill=tint+(255,))
    for x in range(ROOMX0,ROOMX1,16): d.line([(x,yr),(x,yb)],fill=sh(tint,0.94)+(255,))
    # back wall strip
    d.rectangle([ROOMX0,yr,ROOMX1,yr+10],fill=WALLC+(255,))
    d.rectangle([ROOMX0,yr+9,ROOMX1,yr+10],fill=sh(WALLC,0.8)+(255,))
    # windows -> LEFT side of back wall
    win(d,ROOMX0+6,yr-1); win(d,ROOMX0+28,yr-1)
    # right wall + door to corridor
    d.rectangle([ROOMX1,yr,ROOMX1+IWALL,yb],fill=sh(WALLC,0.85)+(255,))
    door(d,ROOMX1,yb-30,28,col=sh(dc,1.0))
    # dept sign near door
    if di is not None:
        d.rectangle([ROOMX1-26,yr+14,ROOMX1-6,yr+22],fill=dc+(255,))

    feet=yb-4
    if kind=='dept':
        ags=cg.DOMAINS[di][2]; n=len(ags)
        # back counter desks under windows (decor)
        env.coffee(d, ROOMX0+60, yr+12)
        env.plant(d, ROOMX1-44, yb-16)
        step=(ROOMW-40)/max(1,n)
        for k,(nm,rc) in enumerate(ags):
            cx=int(ROOMX0+26+step*k+step/2-step/2)+10
            cx=int(ROOMX0+24+ (k+0.5)*((ROOMW-60)/n))
            img.alpha_composite(cg.char_img(rc) if hasattr(cg,'char_img') else env.char_img(rc),(cx-16,feet-34))
        # small desks row near front
    else:
        # meeting room
        env.whiteboard(d, ROOMX0+10, yr-2)
        # long table center
        tx0=ROOMX0+90; tx1=ROOMX1-70; tcy=yr+46
        d.rectangle([tx0,tcy-12,tx1,tcy+12],fill=(150,115,75,255))
        d.rectangle([tx0,tcy-12,tx1,tcy-10],fill=(175,140,95,255))
        d.rectangle([tx0,tcy+10,tx1,tcy+12],fill=(120,90,58,255))
        env.plant(d, ROOMX1-46, yb-16)
        # seated managers around table (representative)
        seats=['Müdür','CEO / Ürün','Strateji Direktörü','Yaratıcı Direktör','CFO']
        sx=[tx0+18,tx0+70,tx0+122,tx0+150,tx0+100]
        # top side (behind table -> occluded by table front)
        topx=[tx0+24,tx0+78,tx0+132]
        for j,nm in enumerate(seats[:3]):
            img.alpha_composite(env.char_img(cg.ALL[nm]),(topx[j]-16, tcy-12-30))
        # redraw table front to occlude their lower bodies
        d.rectangle([tx0,tcy-2,tx1,tcy+12],fill=(150,115,75,255))
        d.rectangle([tx0,tcy+10,tx1,tcy+12],fill=(120,90,58,255))
        # bottom side (in front of table)
        botx=[tx0+50,tx0+108]
        for j,nm in enumerate(seats[3:5]):
            img.alpha_composite(env.char_img(cg.ALL[nm]),(botx[j]-16, tcy+12-30+6))

def corridor(d,img):
    d.rectangle([CORX0,0,CORX1,TOTH],fill=CORC+(255,))
    for y in range(0,TOTH,16): d.line([(CORX0,y),(CORX1,y)],fill=sh(CORC,0.95)+(255,))
    # stairs zigzag down the corridor
    for i in range(NF):
        y0=SLAB+i*(FH+SLAB)
        for s in range(6):
            yy=y0+10+s*11
            d.rectangle([CORX0+6+s*5,yy,CORX0+6+s*5+8,yy+6],fill=sh(CORC,0.8)+(255,))
    # a person in corridor
    img.alpha_composite(env.char_img(cg.ALL['Proje Yöneticisi']),(CORX0+CORW//2-16, SLAB+2*(FH+SLAB)+FH-4-34))

def render_building():
    img=Image.new('RGBA',(BUILDW,TOTH),(0,0,0,0))
    d=ImageDraw.Draw(img)
    # outer shell
    d.rectangle([0,0,BUILDW-1,TOTH-1],fill=WALLC+(255,))
    # slabs
    for i in range(NF+1):
        y=i*(FH+SLAB)
        d.rectangle([0,y,BUILDW,y+SLAB],fill=SLABC+(255,))
    # exterior left wall
    d.rectangle([0,0,LEFTW,TOTH],fill=sh(WALLC,0.9)+(255,))
    for i in range(NF):
        floor_room(d,img,i)
    corridor(d,img)
    # outer outline
    d.rectangle([0,0,BUILDW-1,TOTH-1],outline=(70,68,64,255),width=1)
    return img

def finalize():
    img=render_building()
    big=img.resize((img.width*SCALE,img.height*SCALE),Image.NEAREST)
    GUT=176
    out=Image.new('RGBA',(big.width+GUT, big.height+40),(247,246,241,255))
    out.alpha_composite(big,(GUT,20))
    dd=ImageDraw.Draw(out)
    labels=[]
    for i,(kind,di) in enumerate(FLOORS):
        if kind=='dept':
            nm=env.ZONE_LABELS[di]; cnt=f"{len(cg.DOMAINS[di][2])} ajan"; col=cg.DOMAINS[di][1]
        else:
            nm="Toplantı odası"; cnt="orta kat"; col=(120,120,130)
        cy=20+ (SLAB+i*(FH+SLAB)+FH//2)*SCALE
        dd.rectangle([14,cy-14,26,cy+14],fill=col+(255,))
        dd.text((34,cy-16),nm,fill=(45,45,52,255),font=Ft(20))
        dd.text((34,cy+6),cnt,fill=(120,120,128,255),font=Ft(14))
    dd.text((GUT,2),"ADA Turbo — departman binası",fill=(45,45,52,255),font=Ft(16))
    return out.convert('RGB')

if __name__=='__main__':
    finalize().save('/home/claude/bina.png'); print('bina ok')
