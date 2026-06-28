import os, zipfile, numpy as np
from PIL import Image
import chargen as cg
from export import slug

S=6; HH=cg.H+2; W=cg.W
BG=(244,243,238)

def frame(recipe, dy=0, blink=False, legph=0, armph=0):
    a=cg.compose(recipe, blink=blink, legph=legph, armph=armph)
    canvas=np.zeros((HH,W,4),np.uint8)
    yo=1-dy
    canvas[yo:yo+cg.H,:,:]=a
    return canvas

# (dy, blink, legph, armph)
IDLE=[(0,False,0,0),(1,False,0,0),(1,True,0,0),(0,False,0,0)]
IDLE_MS=[260,260,140,260]
WALK=[(1,False,1,1),(0,False,0,0),(1,False,2,2),(0,False,0,0)]
WALK_MS=[130,130,130,130]

def up(arr,s=S):
    return Image.fromarray(arr,'RGBA').resize((arr.shape[1]*s,arr.shape[0]*s),Image.NEAREST)

def to_gif(frames_rgba, durs, path, bg=BG):
    imgs=[]
    for fr in frames_rgba:
        im=up(fr).convert('RGBA')
        base=Image.new('RGBA',im.size,bg+(255,)); base.alpha_composite(im)
        imgs.append(base.convert('P',palette=Image.ADAPTIVE))
    imgs[0].save(path,save_all=True,append_images=imgs[1:],duration=durs,loop=0,disposal=2)

def strip(frames_rgba, path):
    n=len(frames_rgba); cell=up(frames_rgba[0]).size
    sheet=Image.new('RGBA',(cell[0]*n,cell[1]),(0,0,0,0))
    for i,fr in enumerate(frames_rgba):
        sheet.alpha_composite(up(fr),(i*cell[0],0))
    sheet.save(path)

os.makedirs('/home/claude/anim',exist_ok=True)
for nm,rc in cg.ALL.items():
    sg=slug(nm)
    idle=[frame(rc,*p) for p in IDLE]
    walk=[frame(rc,*p) for p in WALK]
    to_gif(idle,IDLE_MS,f'/home/claude/anim/{sg}_idle.gif')
    to_gif(walk,WALK_MS,f'/home/claude/anim/{sg}_walk.gif')
    strip(idle,f'/home/claude/anim/{sg}_idle_strip.png')
    strip(walk,f'/home/claude/anim/{sg}_walk_strip.png')
print('per-character anim done')

# combined preview grid GIF (idle), grouped order
names=list(cg.ALL.keys()); cols=6; rows=(len(names)+cols-1)//cols
cw,chh=W*S, HH*S
gframes=[]
for fi in range(len(IDLE)):
    canvas=Image.new('RGBA',(cols*cw, rows*chh),BG+(255,))
    for i,nm in enumerate(names):
        fr=frame(cg.ALL[nm],*IDLE[fi]); r,c=divmod(i,cols)
        canvas.alpha_composite(up(fr),(c*cw,r*chh))
    gframes.append(canvas.convert('P',palette=Image.ADAPTIVE))
gframes[0].save('/mnt/user-data/outputs/ada-turbo-idle-preview.gif',save_all=True,append_images=gframes[1:],duration=IDLE_MS,loop=0,disposal=2)
print('preview gif done')

with zipfile.ZipFile('/mnt/user-data/outputs/ada-turbo-animasyonlar.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('/home/claude/anim')):
        z.write(f'/home/claude/anim/{f}',f'anim/{f}')
    z.write('/home/claude/chargen.py','chargen.py')
    z.write('/home/claude/anim.py','anim.py')
print('zipped', len(os.listdir('/home/claude/anim')),'files')
