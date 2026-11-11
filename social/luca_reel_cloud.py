#!/usr/bin/env python3
"""Convert Sito Lume original vertical motion boards + original narration into Reel draft.
Runs only in cloud CI; never uploads or publishes. No music with unclear rights.
"""
import argparse, os, json, math, subprocess, shutil
from pathlib import Path
from PIL import Image
import soundfile as sf

def run(args):
    subprocess.run(args,check=True,timeout=350,stdout=subprocess.DEVNULL)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--assets',required=True)
    p.add_argument('--voice',required=True)
    p.add_argument('--out',required=True)
    a=p.parse_args()
    root=Path(a.assets).resolve()
    voice=Path(a.voice).resolve()
    dst=Path(a.out).resolve()
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg not installed on cloud runner")
    with sf.SoundFile(str(voice)) as audio:
        sec=audio.frames/audio.samplerate
    if not (5<sec<80):raise RuntimeError(f"Invalid voice duration: {sec}s")
    frames=[root/f'reel-frame-{j:02d}.jpg' for j in range(1,5)]
    for f in frames:
        if not f.exists():raise FileNotFoundError(f)
        with Image.open(f) as im:
            if im.size!=(1080,1920):raise RuntimeError(f"Wrong frame size: {f}")
    # One gently moving zoom per frame. Explicit duration for deterministic output.
    per=sec/len(frames)
    segments=[]
    for i,img in enumerate(frames):
        seg=dst.parent/f'clip-{i+1:02d}.mp4'
        # input is 24fps duplicated still. zoompan uses stateful zoom for subtle camera movement.
        vf=("scale=1120:1992,crop=1080:1920:"
            "x='(iw-ow)*min(t/10,1)':y='(ih-oh)/2',"
            "eq=contrast=1.035:saturation=1.04,"
            "format=yuv420p")
        run(["ffmpeg","-y","-hide_banner","-loglevel","error",
             "-loop","1","-framerate","24","-t",f"{per:.3f}",
             "-i",str(img),"-vf",vf,"-r","24",
             "-c:v","libx264","-preset","veryfast","-crf","19",
             "-pix_fmt","yuv420p","-an",str(seg)])
        segments.append(seg)
    concat=dst.parent/"reel_concat.txt"
    concat.write_text("".join(f"file '{f.name}'\n" for f in segments))
    temp=dst.parent/"silent_reel.mp4"
    run(["ffmpeg","-y","-hide_banner","-loglevel","error",
         "-f","concat","-safe","0","-i",str(concat),"-c","copy",str(temp)])
    run(["ffmpeg","-y","-hide_banner","-loglevel","error",
         "-i",str(temp),"-i",str(voice),
         "-map","0:v:0","-map","1:a:0","-c:v","copy",
         "-c:a","aac","-b:a","160k","-af","loudnorm=I=-16:TP=-1.5:LRA=11",
         "-movflags","+faststart","-shortest",str(dst)])
    result=subprocess.check_output(["ffprobe","-v","error","-show_entries",
       "stream=codec_type,width,height","-of","json",str(dst)],text=True)
    info=json.loads(result)['streams']
    assert any(s.get('codec_type')=='video' and s.get('width')==1080 and s.get('height')==1920 for s in info)
    assert any(s.get('codec_type')=='audio' for s in info)
    print(f"Reel draft verified: {dst.name}; {sec:.1f}s; 1080x1920, voice over.")
    for seg in segments:seg.unlink(missing_ok=True)
    concat.unlink(missing_ok=True)
    temp.unlink(missing_ok=True)

if __name__=="__main__":main()
