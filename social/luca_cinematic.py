#!/usr/bin/env python3
"""Luca Cinema Studio — CPU-only cinematic avatar reels on free GitHub runners.
Visual engine: Pillow + FFmpeg (open source). Faces: synthetic CC0 from
visualizevalue/headshots. Lip movement is NOT simulated; this is a moving
cinematic virtual-presenter composition, not photoreal lip-sync.
No local Mac storage, API secrets, paid GPU, or Instagram writes.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
BLACK = (8, 9, 12)
GOLD = (235, 189, 107)
WHITE = (248, 243, 231)
FADE = (175, 165, 153)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
HEADSHOTS = {
    "ryan": "02",    # Synthetic adult male in jacket
    "serena": "09",  # Synthetic adult female in jacket
}
CREDIT = "Synthetic personas: visualizevalue/headshots, CC0 1.0. Audio: Sito Lume original Qwen3-TTS."


def face_for(voice: str, cache: Path) -> Image.Image:
    src = f"https://raw.githubusercontent.com/visualizevalue/headshots/main/full/{HEADSHOTS[voice]}.png"
    target = cache / f"{voice}-cc0.png"
    request = urllib.request.Request(src, headers={"User-Agent": "SitoLume-LucaCinema/1.0"})
    with urllib.request.urlopen(request, timeout=40) as response:
        raw = response.read(9_000_000)
    if len(raw) < 25_000 or len(raw) > 8_000_000:
        raise ValueError("Synthetic portrait missing or unusual file size")
    target.write_bytes(raw)
    portrait = Image.open(target).convert("RGB")
    if portrait.width < 500 or portrait.height < 500:
        raise ValueError("Portrait too small for a 1080p cinematic composition")
    return portrait


def f(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else FONT, size)


def center(draw: ImageDraw.ImageDraw, y: int, label: str, size: int, color, bold=False):
    font = f(size, bold)
    box = draw.textbbox((0, 0), label, font=font, stroke_width=0)
    draw.text(((W - (box[2] - box[0])) // 2, y), label, font=font, fill=color)


def studio(seed: int) -> Image.Image:
    rng = random.Random(seed)
    im = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(im)
    for y in range(H):
        g = y / H
        d.line((0, y, W, y), fill=(int(7 + 11 * (1-g)), int(8 + 8 * (1-g)), int(11 + 7*g)))
    # 3D-like perspective grid and architectural light walls
    van = (W//2, 540)
    for x in range(-1100, 2600, 145):
        d.line((van, (x, H)), fill=(36, 30, 24), width=2)
    for y in (950, 1100, 1260, 1430, 1620, 1830):
        d.line((0,y,W,y), fill=(28, 24, 24), width=2)
    for x in (65, 80, 1000, 1016):
        d.line((x, 0, x, H), fill=(59, 41, 26), width=2)
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((450,-650,1740,740),fill=(178,110,46,100))
    gd.ellipse((-600,720,400,1750),fill=(112,78,53,55))
    glow=glow.filter(ImageFilter.GaussianBlur(175))
    im=Image.alpha_composite(im.convert("RGBA"),glow).convert("RGB")
    d=ImageDraw.Draw(im)
    for _ in range(55):
        x=rng.randint(35,W-35);y=rng.randint(250,H-160)
        r=rng.choice((1,1,2,2,3))
        d.ellipse((x-r,y-r,x+r,y+r),fill=(rng.randint(85,190),rng.randint(70,120),42))
    return im


def portrait_cutout(image: Image.Image, height=1130) -> Image.Image:
    # Soft-key CC0 headshot over white. The source face remains recognisable.
    im=image.convert("RGBA")
    if im.width>1000:
        im=im.resize((900,900),Image.Resampling.LANCZOS)
    rgb=im.convert("RGB")
    from PIL import ImageChops
    # White background removal: high mean brightness + very low color spread.
    pix=rgb.load()
    mask=Image.new("L",rgb.size,255);mp=mask.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r,g,b=pix[x,y]
            near=min(r,g,b)
            spread=max(r,g,b)-near
            if near>=246 and spread<25: a=0
            elif near>223 and spread<24: a=max(0,min(255,int((246-near)/23*255)))
            else:a=255
            mp[x,y]=a
    mask=mask.filter(ImageFilter.GaussianBlur(1.0))
    im.putalpha(mask)
    w=round(im.width*height/im.height)
    return im.resize((w,height),Image.Resampling.LANCZOS)


def emblem(d: ImageDraw.ImageDraw, y=80):
    d.rounded_rectangle((70,y,134,y+64),radius=17,fill=(31,35,42),outline=(121,91,59),width=2)
    d.text((85,y+3),"S",font=f(47,True),fill=GOLD)
    d.text((150,y+5),"SITO LUME",font=f(35,True),fill=WHITE)
    d.text((152,y+47),"DIGITAL STUDIO   •   ITALIA",font=f(16),fill=FADE)


def gold_curve(im, offset=0):
    glow=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(glow)
    for i in range(4):
        points=[]
        for x in range(-40,1130,9):
            y=int(1390+80*math.sin((x+offset)/235)+i*18)
            points.append((x,y))
        d.line(points,fill=(235,189,107,max(25,140-i*35)),width=max(1,4-i))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))


def textshadow(d, pos, txt, size, fill=WHITE):
    font=f(size,True)
    x,y=pos
    d.text((x+3,y+6),txt,font=font,fill=(0,0,0),stroke_width=1)
    d.text((x,y),txt,font=font,fill=fill)


def draw_person(im: Image.Image, face: Image.Image, x: int, y: int, height: int):
    figure=portrait_cutout(face,height)
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    ring=ImageDraw.Draw(layer)
    w=figure.width
    cx=x+w//2;cy=y+height//2
    ring.ellipse((cx-495,cy-520,cx+495,cy+515),outline=(180,139,70,120),width=7)
    layer.alpha_composite(figure,(x,y))
    im.alpha_composite(layer)


def scene(i: int, voice: str, face: Image.Image) -> Image.Image:
    im=studio(37+i*42+(0 if voice=="ryan" else 3)).convert("RGBA")
    d=ImageDraw.Draw(im)
    emblem(d)
    if i==0:
        draw_person(im,face,100,270,1070)
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((65,1390,1015,1748),radius=32,fill=(13,14,19,238),outline=(120,83,42,160),width=3)
        d.text((110,1430),"IL TUO BUSINESS",font=f(47,True),fill=WHITE)
        d.text((110,1506),"MERITA DI",font=f(57,True),fill=WHITE)
        d.text((110,1581),"BRILLARE.",font=f(79,True),fill=GOLD)
        d.line((110,1700,620,1700),fill=GOLD,width=5)
    elif i==1:
        draw_person(im,face,205,210,1050)
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((70,1340,1010,1750),radius=32,fill=(14,14,18,246),outline=(150,105,55),width=3)
        d.text((108,1391),"NON BASTA",font=f(53,True),fill=WHITE)
        d.text((108,1474),"ESSERE ONLINE.",font=f(57,True),fill=GOLD)
        d.text((110,1598),"Serve un sito chiaro, moderno",font=f(33),fill=FADE)
        d.text((110,1651),"e facile da usare.",font=f(33),fill=FADE)
    elif i==2:
        # Stylish fictional website mockup, no false client portfolio.
        d.rounded_rectangle((90,420,990,1515),radius=40,fill=(18,20,25),outline=GOLD,width=5)
        d.rounded_rectangle((120,460,960,520),radius=16,fill=(43,43,45))
        for j,c in enumerate([(224,116,94),(230,178,78),(95,176,119)]):
            x=151+j*37
            d.ellipse((x,483,x+15,498),fill=c)
        d.text((260,479),"SITO  •  LUME",font=f(20,True),fill=WHITE)
        d.rounded_rectangle((132,545,948,1025),radius=22,fill=(34,32,32))
        for y in range(545,1025):
            k=(y-545)/480
            d.line((132,y,948,y),fill=(int(26+35*k),int(28+23*k),int(33+20*k)))
        d.ellipse((510,620,800,910),outline=(210,159,75),width=15)
        d.text((185,705),"WEB DESIGN",font=f(50,True),fill=GOLD)
        d.text((188,778),"PER LA TUA",font=f(43,True),fill=WHITE)
        d.text((188,841),"IMPRESA.",font=f(53,True),fill=WHITE)
        for idx,(label,y) in enumerate([("DESIGN SU MISURA",1085),("ESPERIENZA MOBILE",1181),("CONTATTO SEMPLICE",1277)]):
            d.rounded_rectangle((145,y,930,y+73),radius=12,fill=(28,29,34),outline=(65,57,45),width=2)
            d.ellipse((166,y+20,203,y+57),fill=GOLD)
            d.text((226,y+20),label,font=f(29,True),fill=WHITE)
        d.text((100,1620),"OGNI DETTAGLIO",font=f(45,True),fill=WHITE)
        d.text((100,1695),"CONTA.",font=f(84,True),fill=GOLD)
    else:
        draw_person(im,face,130,230,950)
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((65,1300,1015,1795),radius=34,fill=(12,13,17,247),outline=(145,106,58),width=3)
        d.text((110,1360),"SITO LUME",font=f(80,True),fill=GOLD)
        d.text((110,1472),"UN SITO CHE",font=f(47,True),fill=WHITE)
        d.text((110,1548),"TI RAPPRESENTA.",font=f(50,True),fill=WHITE)
        d.rounded_rectangle((115,1655,955,1750),radius=25,fill=GOLD)
        d.text((168,1677),"SCOPRI SITO LUME",font=f(38,True),fill=(17,15,15))
    gold_curve(im,i*110)
    d=ImageDraw.Draw(im)
    d.text((75,1851), "sitolume-studio.pages.dev",font=f(22),fill=FADE)
    return im.convert("RGB")


def shell(command, timeout=600):
    subprocess.run(command,check=True,timeout=timeout)


def audio_length(path: Path) -> float:
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
       "format=duration","-of","json",str(path)],text=True))
    dur=float(data["format"]["duration"])
    if not 8<dur<85:
        raise ValueError(f"Unexpected audio duration {dur}")
    return dur


def encode(clips, audio: Path, out: Path, duration: float):
    # 4 x camera dolly clips with gentle xfade; no fake mouth synchronization.
    cross=0.38
    each=(duration+cross*3+0.28)/4
    files=[]
    for i,img in enumerate(clips):
        vid=out.parent/f".camera-{i}.mp4"
        # FFmpeg's zoompan gives subtle continuous cinematic camera push-in.
        vf=("zoompan=z='min(zoom+0.00048,1.095)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            "d=1:s=1080x1920:fps=24,format=yuv420p")
        shell(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1",
          "-framerate","24","-t",f"{each:.3f}","-i",str(img),
          "-vf",vf,"-c:v","libx264","-preset","veryfast","-crf","21",
          "-pix_fmt","yuv420p","-an",str(vid)],timeout=400)
        files.append(vid)
    filters=[]
    prior="[0:v]"
    for i in range(1,4):
        tag=f"[s{i}]"
        transition=["fadeblack","smoothleft","fade"][i-1]
        filters.append(f"{prior}[{i}:v]xfade=transition={transition}:duration={cross}:offset={(i*each-i*cross):.3f}{tag}")
        prior=tag
    filters.append(f"{prior}format=yuv420p[v]")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y"]
    for fpath in files:
        cmd.extend(["-i",str(fpath)])
    cmd.extend(["-i",str(audio),"-filter_complex",";".join(filters),
      "-map","[v]","-map","4:a:0","-c:v","libx264","-preset","veryfast",
      "-crf","20","-r","24","-pix_fmt","yuv420p",
      "-c:a","aac","-b:a","160k","-movflags","+faststart",
      "-t",f"{duration+0.12:.3f}",str(out)])
    shell(cmd,timeout=700)
    for fpath in files:fpath.unlink(missing_ok=True)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error",
       "-show_entries","stream=codec_type,width,height:format=duration",
       "-of","json",str(out)],text=True))
    assert any(s.get("codec_type")=="video" and s.get("width")==1080 and s.get("height")==1920 for s in probe["streams"])
    assert any(s.get("codec_type")=="audio" for s in probe["streams"])
    assert abs(float(probe["format"]["duration"])-duration)<1.0
    return round(float(probe["format"]["duration"]),1)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--voice",choices=("ryan","serena"),required=True)
    p.add_argument("--audio",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    wav=Path(args.audio);assert wav.is_file(), "Luca original Ryan/Serena audio missing"
    duration=audio_length(wav)
    with tempfile.TemporaryDirectory(prefix="luca-cinema-") as tmp:
        cache=Path(tmp); face=face_for(args.voice,cache)
        clips=[]
        for i in range(4):
            target=out/f"scene-{args.voice}-{i+1:02d}.jpg"
            scene(i,args.voice,face).save(target,"JPEG",quality=91,optimize=True)
            clips.append(target)
        # A reusable branded cover and carousel cards based on the cinematic scenes.
        cover=Image.open(clips[0]).crop((0,290,1080,1640))
        cover.save(out/f"cover-{args.voice}.jpg",quality=92,optimize=True)
        for i,path in enumerate(clips):
            img=Image.open(path).crop((0,285,1080,1635))
            img.save(out/f"cinema-carousel-{args.voice}-{i+1:02d}.jpg",quality=92,optimize=True)
        video=out/f"reel-{args.voice}-cinema.mp4"
        actual=encode(clips,wav,video,duration)
    status={"voice":args.voice,"avatar":"synthetic virtual presenter, portrait animation (not lipsync)",
       "video":video.name,"cover":f"cover-{args.voice}.jpg",
       "carousel":[f"cinema-carousel-{args.voice}-{i+1:02d}.jpg" for i in range(4)],
       "resolution":"1080x1920","duration_seconds":actual,
       "render":"verified","instagram_posted":False,"credit":CREDIT}
    (out/f"cinema-{args.voice}.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(status,ensure_ascii=False))


if __name__=="__main__":
    main()
