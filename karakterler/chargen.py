#!/usr/bin/env python3
"""ADA Turbo — parça-bazlı piksel karakter üreteci."""
import numpy as np
from PIL import Image

W, H = 32, 36
OUTLINE = (26, 26, 32)

# ---- palette ----
SKINS = [(244,206,168),(232,180,140),(208,150,110),(176,120,84),(250,220,190)]
def shade(c, f):
    return (max(0,min(255,int(c[0]*f))), max(0,min(255,int(c[1]*f))), max(0,min(255,int(c[2]*f))))

def new():
    return np.zeros((H, W, 4), np.uint8)

def rgba(c):
    return (c[0], c[1], c[2], 255) if len(c) == 3 else c

def ps(a, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        a[y, x] = rgba(c)

def rect(a, x0, y0, x1, y1, c):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            ps(a, x, y, c)

# ================= HEAD / FACE =================
def face(a, skin):
    x0,x1,y0,y1 = 9,17,6,15
    rect(a,x0,y0,x1,y1,skin)
    for cx,cy in [(x0,y0),(x1,y0),(x0,y1),(x1,y1)]:
        a[cy,cx]=(0,0,0,0)
    # neck
    rect(a,11,15,15,16,shade(skin,0.92))
    # ears
    ps(a,x0-1,11,skin); ps(a,x1+1,11,skin)

def eyes(a, skin, glasses=False, sun=False, brow=False, blink=False):
    if sun:
        rect(a,10,10,12,12,(28,28,34)); rect(a,14,10,16,12,(28,28,34))
        ps(a,13,11,(28,28,34))
        ps(a,10,10,(120,120,140)); ps(a,14,10,(120,120,140))
        return
    if glasses:
        for x in (10,11,12): ps(a,x,10,(45,45,52)); ps(a,x,12,(45,45,52))
        for x in (14,15,16): ps(a,x,10,(45,45,52)); ps(a,x,12,(45,45,52))
        ps(a,10,11,(45,45,52)); ps(a,12,11,(45,45,52))
        ps(a,14,11,(45,45,52)); ps(a,16,11,(45,45,52))
        ps(a,13,11,(45,45,52))
    if blink:
        rect(a,10,11,12,11,shade(skin,0.62)); rect(a,14,11,16,11,shade(skin,0.62))
    else:
        ps(a,11,11,(40,40,48)); ps(a,15,11,(40,40,48))
    if brow:
        rect(a,10,9,12,9,(70,50,40)); rect(a,14,9,16,9,(70,50,40))

def mouth(a, smile=True):
    if smile:
        rect(a,12,13,14,13,(150,80,80)); ps(a,11,12,(150,80,80)); ps(a,15,12,(150,80,80))
    else:
        rect(a,12,13,14,13,(120,70,70))

# ================= HAIR / HEADGEAR =================
def hair_short(a,c):
    rect(a,9,5,17,7,c); ps(a,8,7,c); ps(a,18,7,c); rect(a,9,8,9,9,c); rect(a,17,8,17,9,c)
    rect(a,10,5,16,5,shade(c,1.15))
def hair_messy(a,c):
    rect(a,9,5,17,7,c)
    for x in (9,11,13,15,17): ps(a,x,4,c)
    ps(a,8,7,c); ps(a,18,7,c); rect(a,9,8,9,10,c); rect(a,17,8,17,10,c)
def hair_long(a,c):
    rect(a,9,5,17,7,c); ps(a,8,6,c); ps(a,18,6,c)
    rect(a,8,7,9,16,c); rect(a,17,7,18,16,c)
    rect(a,10,5,16,5,shade(c,1.15))
def hair_bun(a,c):
    rect(a,10,4,16,7,c); rect(a,12,1,15,3,c); rect(a,13,0,14,0,c)
    ps(a,9,7,c); ps(a,17,7,c)
def slick(a,c):
    rect(a,9,5,17,6,c); rect(a,9,7,10,8,c); rect(a,16,7,17,8,c)
    rect(a,10,5,16,5,shade(c,1.2))
def bald(a,skin):
    rect(a,10,5,16,6,shade(skin,1.04))

def beret(a,c):
    rect(a,9,4,16,6,c); rect(a,10,3,15,3,c); ps(a,17,5,c); ps(a,16,3,shade(c,0.8))
    ps(a,9,4,shade(c,1.2))
def cap_back(a,c):
    rect(a,9,4,17,6,c); rect(a,10,3,16,3,c); rect(a,7,5,8,6,shade(c,0.85))  # back strap
    rect(a,11,5,15,5,shade(c,1.15))
def deerstalker(a,c):
    rect(a,9,4,17,6,c); rect(a,10,3,16,3,c)
    rect(a,8,7,10,7,shade(c,0.85)); rect(a,16,7,18,7,shade(c,0.85))  # brims
    ps(a,9,8,c); ps(a,17,8,c)  # ear flaps
def hardhat(a,c):
    rect(a,9,4,17,6,c); rect(a,11,2,15,3,c); rect(a,7,6,19,6,shade(c,0.9))  # brim
    rect(a,12,4,14,4,shade(c,1.2)); ps(a,13,2,shade(c,1.2))
def crown(a):
    g=(240,196,64)
    rect(a,9,3,17,6,g)
    ps(a,9,1,g); ps(a,13,1,g); ps(a,17,1,g)
    ps(a,9,2,g); ps(a,13,2,g); ps(a,17,2,g)
    ps(a,11,4,(220,80,80)); ps(a,15,4,(80,140,220)); ps(a,13,4,(80,180,120))
def headset(a,c=(40,40,48)):
    rect(a,9,3,17,4,c)  # band
    rect(a,7,6,8,9,c); rect(a,18,6,19,9,c)  # earcups
    # mic boom
    ps(a,8,10,c); ps(a,9,11,c); ps(a,10,12,(60,200,120))
def trenchhat(a,c):
    rect(a,7,6,19,6,shade(c,0.85))  # brim
    rect(a,9,3,17,5,c); rect(a,9,5,17,5,shade(c,0.8))

def hair_under_hat(a,c):
    rect(a,8,7,9,9,c); rect(a,17,7,18,9,c)

# ================= OUTFITS (torso) =================
def legs_pants(a,c,ph=0):
    if ph==1:
        rect(a,9,28,12,32,c); rect(a,15,28,18,30,c)
        rect(a,9,33,12,33,(40,40,46)); rect(a,15,31,18,31,(40,40,46))
    elif ph==2:
        rect(a,9,28,12,30,c); rect(a,15,28,18,32,c)
        rect(a,9,31,12,31,(40,40,46)); rect(a,15,33,18,33,(40,40,46))
    else:
        rect(a,9,28,12,31,c); rect(a,15,28,18,31,c)
        rect(a,9,32,12,33,(40,40,46)); rect(a,15,32,18,33,(40,40,46))
def legs_skirt(a,c,ph=0):
    rect(a,8,28,19,30,c)
    rect(a,9,31,11,32,SKINS[0]); rect(a,16,31,18,32,SKINS[0])
    if ph==1:
        rect(a,9,33,11,33,(40,40,46)); rect(a,16,32,18,32,(40,40,46))
    elif ph==2:
        rect(a,9,32,11,32,(40,40,46)); rect(a,16,33,18,33,(40,40,46))
    else:
        rect(a,9,33,11,33,(40,40,46)); rect(a,16,33,18,33,(40,40,46))
def legs_long(a,c,ph=0):
    rect(a,8,28,18,31,c)
    rect(a,9,32,12,33,(40,40,46)); rect(a,15,32,18,33,(40,40,46))

def arms(a,c,skin,ph=0):
    loff = {0:0,1:1,2:-1}[ph]; roff = {0:0,1:-1,2:1}[ph]
    rect(a,6,17,7,23+loff,c); ps(a,6,24+loff,skin); ps(a,7,24+loff,skin)
    rect(a,19,17,20,23+roff,c); ps(a,19,24+roff,skin); ps(a,20,24+roff,skin)

def torso_base(a,c):
    rect(a,8,16,18,27,c)

def blazer(a,c,shirt=(238,238,240),tie=None):
    torso_base(a,c)
    rect(a,12,16,14,22,shirt)  # shirt placket
    ps(a,11,16,shade(c,0.8)); ps(a,15,16,shade(c,0.8))  # lapels
    ps(a,12,17,shade(c,0.8)); ps(a,14,17,shade(c,0.8))
    if tie: rect(a,13,17,13,22,tie)
def turtleneck(a,c):
    torso_base(a,c); rect(a,11,15,15,16,shade(c,1.1))
def hoodie(a,c):
    rect(a,7,5,18,8,shade(c,0.9))  # hood behind head sides
    rect(a,8,7,9,9,shade(c,0.85)); rect(a,17,7,18,9,shade(c,0.85))
    torso_base(a,c)
    rect(a,12,16,14,17,shade(c,1.1))  # collar
    ps(a,12,18,(250,250,250)); ps(a,14,18,(250,250,250))  # drawstrings
    rect(a,11,23,15,25,shade(c,0.88))  # pocket
def apron(a,c,shirt=(220,220,225),splatter=False):
    torso_base(a,shirt)
    rect(a,10,18,16,27,c)  # apron panel
    ps(a,11,16,c); ps(a,15,16,c); rect(a,11,16,11,18,c); rect(a,15,16,15,18,c)  # straps
    if splatter:
        for sx,sy,col in [(11,20,(220,80,80)),(14,22,(80,140,220)),(12,24,(240,200,60)),(15,25,(80,180,120))]:
            ps(a,sx,sy,col)
def vest(a,c,shirt=(232,232,236)):
    torso_base(a,shirt)
    rect(a,8,16,10,27,c); rect(a,16,16,18,27,c)  # vest sides
    rect(a,13,17,13,24,(60,60,68))  # buttons line on shirt
def cardigan(a,c):
    torso_base(a,c); rect(a,13,16,13,27,shade(c,0.8))
    for y in (18,21,24): ps(a,13,y,(240,240,240))
def trench(a,c):
    rect(a,8,16,18,31,c)  # long
    rect(a,13,16,13,31,shade(c,0.85)); rect(a,8,22,18,22,shade(c,0.85))  # belt
    ps(a,11,16,shade(c,0.8)); ps(a,15,16,shade(c,0.8))
def military(a,c):
    torso_base(a,c)
    rect(a,8,16,10,17,shade(c,1.2)); rect(a,16,16,18,17,shade(c,1.2))  # epaulettes
    for y in (18,20,22,24): ps(a,13,y,(240,200,64))  # gold buttons
def tee(a,c):
    torso_base(a,c)

# ================= PROPS (right side ~ x21..30) =================
def pr_flag(a):
    c=(120,90,210)
    rect(a,22,14,22,27,(150,120,90))  # pole
    rect(a,23,14,28,18,c); rect(a,23,15,27,17,(240,240,250))
def pr_gem(a):
    c=(120,200,230)
    rect(a,23,18,27,18,c); rect(a,22,19,28,20,c); rect(a,23,21,27,21,c); rect(a,24,22,26,22,c); ps(a,25,23,c)
    ps(a,24,19,(240,255,255))
def pr_megaphone(a):
    c=(230,150,60)
    rect(a,22,18,23,22,c); rect(a,24,16,26,24,c); rect(a,27,15,28,25,shade(c,0.9))
def pr_pen(a):
    for i in range(6): ps(a,22+i,24-i,(60,60,70)); ps(a,23+i,24-i,(210,160,60))
    ps(a,22,24,(240,240,240))
def pr_palette(a):
    c=(200,160,110)
    rect(a,22,20,27,24,c); a[24,27]=(0,0,0,0)
    ps(a,23,21,(220,80,80)); ps(a,25,21,(80,140,220)); ps(a,24,23,(240,200,60)); ps(a,26,22,(80,180,120))
    rect(a,26,18,27,20,(120,90,60))  # brush
def pr_clapper(a):
    rect(a,22,19,28,24,(40,40,48)); 
    for x in range(22,29,2): ps(a,x,19,(240,240,240))
    for x in range(23,29,2): ps(a,x,20,(240,240,240))
def pr_target(a):
    rect(a,22,17,27,22,(220,80,80)); rect(a,23,18,26,21,(245,245,245)); rect(a,24,19,25,20,(220,80,80))
def pr_magnifier(a):
    c=(80,80,90)
    rect(a,22,16,26,16,c); rect(a,22,20,26,20,c); rect(a,22,17,22,19,c); rect(a,26,17,26,19,c)
    rect(a,23,17,25,19,(180,220,240))
    ps(a,27,21,c); ps(a,28,22,c); ps(a,29,23,c)
def pr_envelope(a):
    c=(230,200,120)
    rect(a,22,18,28,24,c); rect(a,22,18,28,18,shade(c,0.8))
    ps(a,23,19,shade(c,0.7)); ps(a,27,19,shade(c,0.7)); rect(a,24,20,26,21,shade(c,0.7))
def pr_rocket(a):
    rect(a,24,15,26,21,(230,230,235)); ps(a,25,14,(220,80,80))
    rect(a,24,16,26,16,(80,140,220)); rect(a,23,20,23,22,(220,80,80)); rect(a,27,20,27,22,(220,80,80))
    ps(a,24,22,(240,160,40)); ps(a,26,22,(240,160,40)); ps(a,25,23,(240,200,60))
def pr_bubble(a):
    c=(80,180,140)
    rect(a,22,16,28,21,c); rect(a,24,22,25,23,c); rect(a,23,17,27,20,(245,245,245))
def pr_book(a):
    c=(180,100,70)
    rect(a,22,17,28,24,c); rect(a,23,18,27,23,(245,245,240)); rect(a,25,18,25,23,c)
def pr_star(a):
    g=(240,200,64)
    ps(a,25,15,g); rect(a,24,16,26,16,g); rect(a,22,17,28,17,g); rect(a,23,18,27,18,g)
    rect(a,24,19,26,19,g); ps(a,23,20,g); ps(a,27,20,g)
def pr_tv(a):
    rect(a,22,16,29,23,(60,60,70)); rect(a,23,17,28,22,(150,200,230)); rect(a,24,24,27,24,(60,60,70))
def pr_briefcase(a):
    c=(120,80,50)
    rect(a,22,19,28,25,c); rect(a,24,18,26,18,c); rect(a,22,21,28,21,shade(c,0.8)); ps(a,25,21,(220,220,220))
def pr_clipboard(a):
    rect(a,22,17,28,25,(200,160,110)); rect(a,23,18,27,24,(245,245,240)); rect(a,24,16,26,17,(120,120,130))
    rect(a,24,19,26,19,(120,120,130)); rect(a,24,21,26,21,(120,120,130))
def pr_heart(a):
    r=(225,90,110)
    rect(a,22,18,23,19,r); rect(a,26,18,27,19,r); rect(a,22,18,27,20,r); rect(a,23,21,26,21,r); rect(a,24,22,25,22,r)
def pr_flame(a):
    rect(a,24,16,25,16,(225,90,60)); rect(a,23,17,26,18,(225,90,60))
    rect(a,23,19,26,21,(240,160,40)); rect(a,24,20,25,21,(245,220,80)); rect(a,23,22,26,22,(225,90,60))
def pr_mic(a):
    c=(70,70,80)
    rect(a,24,16,26,19,c); rect(a,24,16,26,16,(160,160,170)); rect(a,25,20,25,23,c); rect(a,23,24,27,24,c)
def pr_chart(a):
    rect(a,22,22,23,25,(80,140,220)); rect(a,24,19,25,25,(80,180,120)); rect(a,26,16,27,25,(240,180,60))
def pr_coin(a):
    g=(240,200,64)
    rect(a,23,18,27,18,g); rect(a,22,19,28,23,g); rect(a,23,24,27,24,g)
    rect(a,24,19,26,23,shade(g,0.85)); rect(a,25,19,25,23,g)
def pr_gear(a):
    c=(140,140,150)
    rect(a,23,17,27,17,c); rect(a,22,18,28,22,c); rect(a,23,23,27,23,c)
    ps(a,23,16,c); ps(a,27,16,c); ps(a,22,23,c); ps(a,28,23,c)
    rect(a,24,19,26,21,(60,60,70))
def pr_shield(a):
    c=(90,150,220)
    rect(a,23,17,27,17,c); rect(a,22,18,28,21,c); rect(a,23,22,27,23,c); rect(a,24,24,26,24,c); ps(a,25,25,c)
    rect(a,24,18,26,20,(240,240,250))
def pr_binoc(a):
    c=(50,50,60)
    rect(a,22,18,24,22,c); rect(a,26,18,28,22,c); rect(a,24,19,26,19,c)
    ps(a,23,19,(150,200,230)); ps(a,27,19,(150,200,230))
def pr_baton(a):
    rect(a,22,24,28,24,(220,220,225)); ps(a,28,23,(240,200,64))  # baton
    # medallion on chest handled by outfit; here a small wand

def outline(a, col=OUTLINE):
    op = a[:,:,3] > 0
    out = np.zeros_like(op)
    out[1:,:]  |= op[:-1,:]
    out[:-1,:] |= op[1:,:]
    out[:,1:]  |= op[:,:-1]
    out[:,:-1] |= op[:,1:]
    edge = out & ~op
    a[edge] = (col[0],col[1],col[2],255)

# ================= COMPOSITION =================
def compose(recipe, blink=False, legph=0, armph=0):
    a = new()
    skin = SKINS[recipe.get('skin',0)]
    out = recipe['outfit']
    ocol = out[1]
    legs = recipe.get('legs', legs_pants)
    legcol = recipe.get('legcol',(70,80,110))
    # legs
    if out[0]=='trench':
        legs_long(a,ocol,legph)
    else:
        legs(a,legcol,legph)
    # arms behind torso
    arms(a,recipe.get('armcol',ocol),skin,armph)
    # torso/outfit
    OUTF[out[0]](a, *out[1:])
    if recipe.get('pinstripe'):
        for x in (10,13,16):
            for y in range(17,27):
                if tuple(a[y,x][:3])==tuple(shade(out[1],1.0))[:3] or a[y,x][3]>0:
                    pass
        for x in (10,16):
            for y in range(17,26,2): ps(a,x,y,shade(out[1],1.35))
    if recipe.get('medallion'):
        g=(240,200,64)
        rect(a,12,20,14,21,g); ps(a,13,22,g); a[20,12]=(0,0,0,0); a[20,14]=(0,0,0,0)
    # head
    face(a,skin)
    eyes(a, skin, glasses=recipe.get('glasses',False), sun=recipe.get('sun',False), brow=recipe.get('brow',False), blink=blink)
    mouth(a, recipe.get('smile',True))
    # hair/hat
    recipe['head'](a)
    # prop
    if recipe.get('prop'): recipe['prop'](a)
    outline(a)
    return a

def hoodie_pre(a,c):
    pass

OUTF = {
 'blazer':blazer,'turtleneck':turtleneck,'hoodie':hoodie,'apron':apron,
 'vest':vest,'cardigan':cardigan,'trench':trench,'military':military,'tee':tee,
}

def hoodie_hair(a): rect(a,9,5,17,7,(50,40,32)); ps(a,8,7,(50,40,32)); ps(a,18,7,(50,40,32))
def earrings(a,c=(240,200,64)): ps(a,8,12,c); ps(a,18,12,c)

# ---- head recipes (hair + headgear) ----
def H_strateji(a): slick(a,(55,42,32))
def H_marka(a): hair_bun(a,(40,30,48)); earrings(a)
def H_yaratici(a): hair_short(a,(40,35,40)); beret(a,(40,40,52))
def H_copy(a): hair_messy(a,(64,46,32))
def H_art(a): hair_messy(a,(40,35,45)); beret(a,(205,60,82))
def H_yapim(a): hair_under_hat(a,(40,30,24)); cap_back(a,(70,120,90))
def H_perf(a): hair_short(a,(50,40,30)); headset(a)
def H_seo(a): hair_under_hat(a,(72,56,40)); deerstalker(a,(150,128,86))
def H_email(a): hair_short(a,(72,52,36))
def H_growth(a): hair_messy(a,(38,34,30))
def H_sosyal(a): hair_long(a,(60,40,28)); earrings(a)
def H_icerik(a): hair_bun(a,(60,46,34))
def H_inf(a): hair_long(a,(74,46,30))
def H_medya(a): slick(a,(40,35,40))
def H_hesap(a): slick(a,(58,44,34))
def H_proje(a): hair_short(a,(40,35,30))
def H_cs(a): hair_short(a,(74,52,36)); headset(a)
def H_kriz(a): hair_under_hat(a,(40,35,30)); hardhat(a,(240,180,40))
def H_pr(a): hair_bun(a,(50,38,30)); earrings(a)
def H_analitik(a): hair_short(a,(42,42,48))
def H_cfo(a): slick(a,(70,70,76))
def H_ceo(a): slick(a,(58,44,34)); crown(a)
def H_cto(a): hoodie_hair(a); headset(a)
def H_cos(a): hair_short(a,(40,35,30))
def H_intel(a): hair_under_hat(a,(40,35,32)); trenchhat(a,(62,62,76))
def H_mudur(a): slick(a,(46,36,30))

DOMAINS = [
 ("Strateji ve marka", (111,90,214), [
   ("Strateji Direktörü", dict(outfit=('blazer',(96,74,150),(238,238,240),(150,120,210)), head=H_strateji, brow=True, skin=1, legcol=(50,42,80), prop=pr_flag)),
   ("Marka Stratejisti", dict(outfit=('turtleneck',(120,86,168)), head=H_marka, skin=4, prop=pr_gem)),
 ]),
 ("Yaratıcı ekip", (216,86,143), [
   ("Yaratıcı Direktör", dict(outfit=('turtleneck',(206,74,120)), head=H_yaratici, skin=2, prop=pr_megaphone)),
   ("Copywriter", dict(outfit=('hoodie',(150,120,140)), head=H_copy, glasses=True, skin=0, legcol=(60,55,65), prop=pr_pen)),
   ("Art Director", dict(outfit=('apron',(120,80,150),(225,225,228),True), head=H_art, skin=0, legcol=(60,60,70), prop=pr_palette)),
   ("Yapımcı", dict(outfit=('vest',(70,120,90),(232,232,236)), head=H_yapim, skin=3, legcol=(50,52,60), prop=pr_clapper)),
 ]),
 ("Pazarlama ve büyüme", (60,157,110), [
   ("Performans Pazarlama", dict(outfit=('tee',(70,170,120)), head=H_perf, skin=1, legcol=(50,55,65), prop=pr_target)),
   ("SEO", dict(outfit=('trench',(150,128,86)), head=H_seo, glasses=True, skin=1, prop=pr_magnifier)),
   ("E-posta / CRM", dict(outfit=('cardigan',(80,150,120)), head=H_email, skin=2, legcol=(60,60,70), prop=pr_envelope)),
   ("Growth Hacker", dict(outfit=('hoodie',(64,150,96)), head=H_growth, skin=0, legcol=(50,55,62), prop=pr_rocket)),
   ("Sosyal Medya", dict(outfit=('turtleneck',(72,168,150)), head=H_sosyal, skin=3, prop=pr_bubble)),
   ("İçerik Stratejisti", dict(outfit=('cardigan',(96,140,90)), head=H_icerik, glasses=True, skin=4, legcol=(60,60,68), prop=pr_book)),
   ("Influencer", dict(outfit=('turtleneck',(230,150,180)), head=H_inf, sun=True, skin=4, prop=pr_star)),
   ("Medya Planlama", dict(outfit=('blazer',(56,120,96),(238,238,240),None), head=H_medya, skin=1, legcol=(45,55,60), prop=pr_tv)),
 ]),
 ("Müşteri ve operasyon", (224,138,46), [
   ("Hesap Yöneticisi", dict(outfit=('blazer',(168,112,52),(240,240,242),(120,80,40)), head=H_hesap, skin=2, legcol=(70,55,40), prop=pr_briefcase)),
   ("Proje Yöneticisi", dict(outfit=('vest',(210,150,60),(235,235,238)), head=H_proje, skin=1, legcol=(60,58,64), prop=pr_clipboard)),
   ("Müşteri Başarısı", dict(outfit=('cardigan',(232,168,80)), head=H_cs, skin=0, legcol=(70,60,52), prop=pr_heart)),
   ("Kriz İletişimi", dict(outfit=('vest',(232,120,40),(60,60,70)), head=H_kriz, smile=False, skin=3, legcol=(50,50,58), prop=pr_flame)),
   ("PR", dict(outfit=('blazer',(210,140,70),(240,240,242),(150,90,50)), head=H_pr, skin=4, legcol=(70,55,42), prop=pr_mic)),
 ]),
 ("Analitik, ürün ve teknik", (58,134,200), [
   ("Analitik", dict(outfit=('cardigan',(70,120,190)), head=H_analitik, glasses=True, skin=1, legcol=(50,55,70), prop=pr_chart)),
   ("CFO", dict(outfit=('blazer',(40,52,84),(238,238,240),(120,140,200)), head=H_cfo, glasses=True, skin=2, legcol=(38,44,66), pinstripe=True, prop=pr_coin)),
   ("CEO / Ürün", dict(outfit=('blazer',(46,56,92),(238,238,240),(180,50,50)), head=H_ceo, brow=True, skin=1, legcol=(40,45,70), prop=None)),
   ("CTO", dict(outfit=('hoodie',(72,82,98)), head=H_cto, skin=2, legcol=(50,55,65), prop=pr_gear)),
   ("Kurmay Başkanı", dict(outfit=('military',(54,72,128)), head=H_cos, skin=3, legcol=(40,48,80), prop=pr_shield)),
   ("İstihbarat", dict(outfit=('trench',(70,74,92)), head=H_intel, sun=True, skin=1, prop=pr_binoc)),
   ("Müdür", dict(outfit=('blazer',(60,90,150),(238,238,240),(240,200,64)), head=H_mudur, skin=2, legcol=(45,55,90), medallion=True, prop=pr_baton)),
 ]),
]

ALL = {}
for _dn,_dc,_ags in DOMAINS:
    for _nm,_rc in _ags:
        ALL[_nm]=_rc

def render_sheet(items, cols=3, scale=11, pad=6, label=True):
    from PIL import ImageDraw, ImageFont
    names=list(items.keys()); n=len(names); rows=(n+cols-1)//cols
    cellw, cellh = W, H+ (8 if label else 0)
    sheet = Image.new('RGBA',(cols*cellw*scale + (cols+1)*pad*scale, rows*cellh*scale+(rows+1)*pad*scale),(245,244,238,255))
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9*scale//2)
    except: font=ImageFont.load_default()
    d=ImageDraw.Draw(sheet)
    for i,nm in enumerate(names):
        a=compose(items[nm])
        img=Image.fromarray(a,'RGBA').resize((W*scale,H*scale),Image.NEAREST)
        r,c=divmod(i,cols)
        x=pad*scale + c*(cellw*scale+pad*scale); y=pad*scale + r*(cellh*scale+pad*scale)
        sheet.alpha_composite(img,(x,y))
        if label:
            d.text((x+2, y+H*scale+2), nm, fill=(40,40,46,255), font=font)
    return sheet

if __name__=='__main__':
    sheet=render_sheet(ALL, cols=6, scale=9)
    sheet.convert('RGB').save('/home/claude/full_roster.png')
    print('saved', sheet.size, '| agents:', len(ALL))
