#!/usr/bin/env python3
"""Editorial 4:5 crops for Luca cinematic Instagram covers and carousels.
CPU-only, GitHub Actions. Does not touch videos, voices or Mac.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1350
GOLD=(235,189,107)
WHITE=(247,241,227)
MUTED=(180,171,159)
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
COPY=[
 ("IL TUO BUSINESS", "MERITA DI BRILLARE.", "Un sito professionale ti rappresenta."),
 ("NON BASTA ESSERE ONLINE.", "FATTI RICONOSCERE.", "Design chiaro, identità e fiducia."),
 ("WEB DESIGN", "PER LA TUA IMPRESA.", "Ogni dettaglio conta."),
 ("SITO LUME", "UN SITO CHE PARLA DI TE.", "Scopri il nostro studio digitale.")
]

def fit(d,text,limit,sz):
    while sz>29 and d.textlength(text,font=ImageFont.truetype(BOLD,sz))>limit:sz-=2
    return ImageFont.truetype(BOLD,sz)

def make(inp:Path, out:Path, number:int, voice:str):
    src=Image.open(inp).convert("RGB")
    assert src.size==(1080,1920)
    # Preserve actual face from top of scene; copy lower third for editorial text.
    img=src.crop((0,40,W,1390))
    # Subtle shadow for reading at the lower third.
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    od=ImageDraw.Draw(overlay)
    for y in range(830,H):
        alpha=round(250*min(1,max(0,(y-830)/220)))
        od.line((0,y,W,y),fill=(10,10,14,alpha),width=1)
    canvas=Image.alpha_composite(img.convert("RGBA"),overlay)
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((61,1060,W-61,H-58),radius=28,fill=(15,15,19,242),outline=(147,106,61,255),width=3)
    first,second,third=COPY[number]
    d.text((100,1090),first,font=fit(d,first,880,46),fill=WHITE)
    d.text((100,1160),second,font=fit(d,second,880,49),fill=GOLD)
    d.text((100,1240),third,font=ImageFont.truetype(REG,25),fill=MUTED)
    d.rectangle((0,0,W,6),fill=GOLD)
    canvas.convert("RGB").save(out,"JPEG",quality=93,optimize=True,subsampling=0)

def main():
    import argparse
    from datetime import datetime, timezone
    p=argparse.ArgumentParser()
    p.add_argument("--day",default=datetime.now(timezone.utc).date().isoformat())
    args=p.parse_args()
    root=Path("social/cinema")/args.day
    for voice in ("ryan","serena"):
        folder=root/voice
        first=folder/f"scene-{voice}-01.jpg"
        assert first.exists()
        for i in range(4):
            scene=folder/f"scene-{voice}-{i+1:02d}.jpg"
            target=folder/f"cinema-carousel-{voice}-{i+1:02d}.jpg"
            make(scene,target,i,voice)
        make(first,folder/f"cover-{voice}.jpg",0,voice)
        print(voice,"safe-frame 1080x1350 editorial covers and carousel QA passed")

if __name__=="__main__":main()
