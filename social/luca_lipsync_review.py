#!/usr/bin/env python3
"""Cloud-only visual QA of actual audio-driven lip-sync clips.

Creates a review contact sheet for each existing MP4 on a GitHub runner,
never on the owner's Mac. Requires ffmpeg and Pillow.
This does not replace human review or a learned audiovisual sync score.
"""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageStat
def run(*args):return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def main():
    root=Path("social/lipsync/2026-11-11")
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",22)
    processed=0
    for name in ["ryan","serena"]:
        p=root/name
        status=p/"status.json"
        if not status.is_file():print("SKIP",name,": no real verified video yet");continue
        meta=json.loads(status.read_text())
        vid=p/meta["output"]
        assert vid.stat().st_size>90000
        probe=json.loads(run("ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height","-of","json",str(vid)).stdout)
        dur=float(probe["format"]["duration"])
        assert 2<=dur<=15,dur
        assert any(v.get("codec_type")=="audio" for v in probe["streams"])
        with tempfile.TemporaryDirectory(prefix="sitolume-avqa-") as tmp:
            frames=[]
            for i,t in enumerate((.25,.65,1.05,1.45,1.85)):
                f=Path(tmp)/f"frame-{i:02d}.png"
                run("ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(min(t,dur-.1)),"-i",str(vid),"-frames:v","1",str(f))
                im=Image.open(f).convert("RGB")
                im.thumbnail((320,560))
                frames.append(im.copy())
        w=frames[0].width;h=frames[0].height
        sheet=Image.new("RGB",(w*len(frames),h+56),(15,15,18))
        draw=ImageDraw.Draw(sheet)
        for i,img in enumerate(frames):
            sheet.paste(img,(w*i,52))
            draw.text((w*i+12,14),f"{name.upper()}  {(.5,1.25,2.0,2.75,3.5)[i]}s",font=font,fill=(233,194,112))
        movement=[]
        for a,b in zip(frames[:-1],frames[1:]):
            diff=ImageChops.difference(a,b)
            movement.append(sum(ImageStat.Stat(diff).mean)/3)
        # Check frame variation; note that variation alone is not a guarantee of lip sync.
        if max(movement)<.06:raise RuntimeError("Static repeated image; no visible frame change")
        path=p/f"review-{name}-frames.jpg"
        sheet.save(path,quality=91,optimize=True)
        meta["review_sheet"]=path.name
        meta["frame_variation_qa"]="non_static_frames_detected"
        meta["human_lip_sync_review"]="pending"
        status.write_text(json.dumps(meta,indent=2)+"\n")
        print(name,"review contact sheet",path,"duration",round(dur,2),"variation",movement)
        processed+=1
    if not processed:raise RuntimeError("No generated lipsync output ready to review")
if __name__=="__main__":main()
