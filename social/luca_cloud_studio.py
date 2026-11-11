#!/usr/bin/env python3
"""Luca Cloud Studio: original visual assets for Sito Lume; no local Mac usage.
Requires Pillow. 1080x1350 feed / carousel, 1080x1920 story and reel frames.
Never publishes to Instagram. Promotional examples only; no fake client proof.
"""
import argparse, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

C = {"bg": (10,20,17), "panel": (23,39,32), "lime": (213,255,102),
     "white": (246,249,244), "muted": (171,189,176), "gold": (180,151,99)}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CONTENT = [
  {"number":"01","eyebrow":"PRESENZA DIGITALE","title":["IL TUO SITO","LAVORA PER TE?"],"highlight":1,"body":"Un bel sito non basta. Deve aiutare le persone a capire cosa offri.","pill":"SCOPRI I 3 ERRORI PIU COMUNI"},
  {"number":"02","eyebrow":"ERRORE N. 1","title":["NON SI CAPISCE","COSA OFFRI"],"highlight":1,"body":"Chi visita da smartphone deve capire il tuo servizio in pochi secondi.","pill":"CHIAREZZA PRIMA DI TUTTO"},
  {"number":"03","eyebrow":"ERRORE N. 2","title":["TROPPI CLICK","PER CONTATTARTI"],"highlight":1,"body":"Un percorso semplice verso chiamata e preventivo migliora l'esperienza.","pill":"SEMPLIFICA IL CONTATTO"},
  {"number":"04","eyebrow":"ERRORE N. 3","title":["NESSUNA FIDUCIA","A PRIMA VISTA"],"highlight":1,"body":"Testi leggibili, servizi chiari e design curato contano davvero.","pill":"RENDi IL VALORE VISIBILE"},
  {"number":"05","eyebrow":"SITO LUME • ITALIA","title":["UN SITO CHE","TI RAPPRESENTA"],"highlight":1,"body":"Progettiamo esperienze web professionali per attivita in tutta Italia.","pill":"SCRIVICI DAL SITO"},
]
CAPTION = ("Hai un'attivita e vuoi capire se il tuo sito comunica davvero il tuo valore?\n\n"
 "Ecco 3 errori comuni: messaggio poco chiaro, contatto complicato e mancanza di fiducia visiva.\n\n"
 "In Sito Lume progettiamo siti professionali pensati per essere chiari, accessibili e coerenti con la tua attivita. "
 "La prima valutazione parte da una conversazione concreta.\n\n"
 "Scopri di piu dal link in bio.\n\n#SitoLume #SitiWeb #WebDesignItalia #PiccoleImprese #PresenzaOnline")
VOICE_TEXT = (
 "Un sito web bello non basta. Deve farti capire al primo sguardo. "
 "Se i servizi sono confusi, i contatti nascosti e il design poco curato, "
 "le persone possono andarsene. Sito Lume: siti web professionali per attivita in tutta Italia. "
 "Scopri il nostro lavoro dal link in bio."
)

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, int(size))

def fit(draw,text,limit,start=71):
    sz=start
    while sz>30 and draw.textlength(text,font=font(sz,True))>limit: sz-=2
    return font(sz,True)

def background(w,h,seed):
    rng=random.Random(seed)
    bg=Image.new("RGB",(w,h),C["bg"])
    glows=Image.new("RGBA",(w,h),(0,0,0,0))
    d=ImageDraw.Draw(glows)
    for x,y,r,col in [(w*.89,h*.10,w*.68,(75,135,81,115)),
                       (-w*.20,h*.72,w*.64,(50,92,69,90)),
                       (w*.65,h*.86,w*.51,(47,72,49,60))]:
        d.ellipse((int(x-r),int(y-r),int(x+r),int(y+r)),fill=col)
    bg=Image.alpha_composite(bg.convert("RGBA"),glows.filter(ImageFilter.GaussianBlur(125))).convert("RGB")
    b=ImageDraw.Draw(bg)
    for j in range(0,w,61):
        b.line((j,0,j,h),fill=(17,30,23),width=1)
    for j in range(0,h,61):
        b.line((0,j,w,j),fill=(17,30,23),width=1)
    for _ in range(55):
        x=rng.randrange(75,w-75);y=rng.randrange(100,h-100)
        b.ellipse((x,y,x+1,y+1),fill=(62,86,67))
    return bg

def brand(draw,w,h,scale):
    pad=round(82*scale)
    draw.rounded_rectangle((pad,pad,pad+52*scale,pad+52*scale),radius=12*scale,fill=C["lime"])
    draw.text((pad+15*scale,pad+10*scale),"S",font=font(29*scale,True),fill=C["bg"])
    draw.text((pad+67*scale,pad+8*scale),"SITO LUME",font=font(24*scale,True),fill=C["white"])
    draw.text((pad+68*scale,pad+40*scale),"STUDIO DIGITALE",font=font(14*scale),fill=C["muted"])

def slide(item,w,h,seed):
    scale=w/1080
    im=background(w,h,seed)
    d=ImageDraw.Draw(im)
    brand(d,w,h,scale)
    pad=round(86*scale);mid=int(h*.53)
    d.rounded_rectangle((pad,int(h*.22),w-pad,int(h*.79)),radius=28*scale,fill=C["panel"],outline=(51,70,55),width=2)
    d.rounded_rectangle((pad+36*scale,int(h*.29),pad+172*scale,int(h*.29)+6*scale),radius=3*scale,fill=C["lime"])
    d.text((pad+36*scale,int(h*.315)),item["eyebrow"],font=font(21*scale,True),fill=C["lime"])
    y=int(h*.394)
    for idx,t in enumerate(item["title"]):
        f=fit(d,t,w-2*pad-70*scale,start=69*scale)
        color=C["lime"] if idx==item["highlight"] else C["white"]
        d.text((pad+35*scale,y),t,font=f,fill=color)
        y+=88*scale
    body=item["body"]
    words=body.split();lines=[];current=""
    for word in words:
        nxt=(current+" "+word).strip()
        if d.textlength(nxt,font=font(29*scale))>w-2*pad-92*scale and current:
            lines.append(current);current=word
        else:current=nxt
    if current:lines.append(current)
    for i,line in enumerate(lines[:4]):
        d.text((pad+37*scale,int(h*.605)+43*scale*i),line,font=font(29*scale),fill=C["muted"])
    pill=item["pill"].upper()
    by=int(h*.73)
    d.rounded_rectangle((pad+35*scale,by,w-pad-35*scale,by+58*scale),radius=16*scale,outline=(125,165,88),width=2)
    pf=fit(d,pill,w-2*pad-114*scale,start=22*scale)
    d.text((pad+57*scale,by+17*scale),pill,font=pf,fill=C["lime"])
    d.text((pad,int(h*.905)),item["number"]+" / 05",font=font(24*scale,True),fill=C["lime"])
    d.text((w-pad-530*scale,int(h*.91)),"sitolume-studio.pages.dev",font=font(20*scale),fill=C["muted"])
    return im

def story(w=1080,h=1920):
    im=background(w,h,88);d=ImageDraw.Draw(im)
    brand(d,w,h,1)
    d.rounded_rectangle((80,490,w-80,1500),radius=35,fill=C["panel"],outline=(51,73,56),width=3)
    d.text((123,620),"UN SITO",font=font(108,True),fill=C["white"])
    d.text((123,790),"CHE PARLA",font=font(100,True),fill=C["lime"])
    d.text((123,960),"DI TE.",font=font(125,True),fill=C["lime"])
    d.text((123,1180),"Siti web professionali",font=font(34),fill=C["muted"])
    d.text((123,1230),"per aziende in tutta Italia.",font=font(34),fill=C["muted"])
    d.rounded_rectangle((122,1350,650,1440),radius=20,fill=C["lime"])
    d.text((158,1377),"SCOPRI SITO LUME",font=font(31,True),fill=C["bg"])
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);a=p.parse_args()
    root=Path(a.out);root.mkdir(parents=True,exist_ok=True)
    for i,item in enumerate(CONTENT):
        im=slide(item,1080,1350,i+41)
        im.save(root/f"carousel-{i+1:02d}.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    slide(CONTENT[0],1080,1350,101).save(root/"post-01.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    story().save(root/"story-01.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    # Vertical motion frames are assets for cloud Reel video build, not a published Reel.
    for i,item in enumerate([CONTENT[0],CONTENT[1],CONTENT[3],CONTENT[4]]):
        v=slide(item,1080,1920,i+71)
        v.save(root/f"reel-frame-{i+1:02d}.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    manifest={"account":"sitolume_studio","format":"cloud-first","approved_for_publishing":False,
              "story":"story-01.jpg","post":"post-01.jpg",
              "carousel":[f"carousel-{i:02d}.jpg" for i in range(1,6)],
              "reel_frames":[f"reel-frame-{i:02d}.jpg" for i in range(1,5)],
              "voices":{"male":"Ryan","female":"Serena","model":"Qwen3-TTS"},
              "caption":CAPTION,"tts_script":VOICE_TEXT,
              "status":"visual-assets-only-until-voice-and-review"}
    (root/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print("Luca Cloud Studio: 6 feed JPG, 1 story JPG, 4 motion frames + manifest")
if __name__=="__main__": main()
