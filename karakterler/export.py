import unicodedata, os, zipfile
from PIL import Image, ImageDraw, ImageFont
import chargen as cg

def slug(s):
    s=s.replace('İ','I').replace('ı','i').replace('ş','s').replace('Ş','s').replace('ğ','g').replace('Ğ','g')
    s=s.replace('ç','c').replace('Ç','c').replace('ö','o').replace('Ö','o').replace('ü','u').replace('Ü','u')
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return s.lower().replace(' / ','-').replace(' ','-')

def font(sz):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
    except: return ImageFont.load_default()

def wrap(d,txt,fnt,maxw):
    words=txt.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=fnt)<=maxw: cur=t
        else: 
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ---------- presentable grouped roster ----------
SC=5; CW=190; SP=24; FS=17
fnt=font(FS); hf=font(20)
BG=(244,243,238,255)
# compute height
tmp=Image.new('RGBA',(10,10)); td=ImageDraw.Draw(tmp)
sections=[]
for dn,dc,ags in cg.DOMAINS:
    cols=min(4,len(ags)); rows=(len(ags)+cols-1)//cols
    sections.append((dn,dc,ags,cols,rows))
width=4*CW+SP*2
total_h=SP
for dn,dc,ags,cols,rows in sections:
    total_h+=40+ rows*(cg.H*SC+54)+SP
img=Image.new('RGBA',(width,total_h),BG)
d=ImageDraw.Draw(img)
y=SP
for dn,dc,ags,cols,rows in sections:
    d.rectangle([SP,y,SP+8,y+26],fill=dc+(255,))
    d.text((SP+18,y+3),dn,fill=(45,45,52,255),font=hf)
    y+=40
    for i,(nm,rc) in enumerate(ags):
        r,c=divmod(i,cols)
        a=cg.compose(rc)
        sp=Image.fromarray(a,'RGBA').resize((cg.W*SC,cg.H*SC),Image.NEAREST)
        cx=SP + c*CW + (CW-cg.W*SC)//2
        cy=y + r*(cg.H*SC+54)
        img.alpha_composite(sp,(cx,cy))
        for li,line in enumerate(wrap(d,nm,fnt,CW-10)):
            tw=d.textlength(line,font=fnt)
            d.text((SP+c*CW+(CW-tw)//2, cy+cg.H*SC+4+li*19),line,fill=(55,55,62,255),font=fnt)
    y+=rows*(cg.H*SC+54)+SP
img.convert('RGB').save('/mnt/user-data/outputs/ada-turbo-karakterler.png')
print('roster', img.size)

# ---------- transparent individual sprites + sheet ----------
os.makedirs('/home/claude/sprites',exist_ok=True)
SSC=6
for nm,rc in cg.ALL.items():
    a=cg.compose(rc)
    Image.fromarray(a,'RGBA').resize((cg.W*SSC,cg.H*SSC),Image.NEAREST).save(f'/home/claude/sprites/{slug(nm)}.png')
# transparent sheet 6 cols
names=list(cg.ALL.keys()); cols=6; rows=(len(names)+cols-1)//cols
sheet=Image.new('RGBA',(cols*cg.W*SSC, rows*cg.H*SSC),(0,0,0,0))
for i,nm in enumerate(names):
    a=cg.compose(cg.ALL[nm]); r,c=divmod(i,cols)
    sheet.alpha_composite(Image.fromarray(a,'RGBA').resize((cg.W*SSC,cg.H*SSC),Image.NEAREST),(c*cg.W*SSC,r*cg.H*SSC))
sheet.save('/home/claude/sprites/_spritesheet.png')
print('sprites', len(names))

# zip
with zipfile.ZipFile('/mnt/user-data/outputs/ada-turbo-sprites.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('/home/claude/sprites')):
        z.write(f'/home/claude/sprites/{f}', f'sprites/{f}')
    z.write('/home/claude/chargen.py','chargen.py')
print('zipped')
