#!/usr/bin/env python3
"""Render *new* original Qwen3-TTS Italian narrations on a cloud runner.
No fallback speaker: failure leaves the voice missing, never an invented success.
"""
import json, os, argparse
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

MODEL = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--voice",choices=["Ryan","Serena","both"],default="both")
    args=ap.parse_args()
    manifest=json.loads(Path(args.manifest).read_text())
    out=Path(args.out);out.mkdir(exist_ok=True,parents=True)
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    model=Qwen3TTSModel.from_pretrained(MODEL,device_map="cpu",
        dtype=torch.float32,attn_implementation="sdpa")
    speakers=["Ryan","Serena"] if args.voice=="both" else [args.voice]
    for speaker in speakers:
        if speaker=="Ryan":
            script=manifest["tts_script"]
        else:
            script=("Hai mai pensato a quello che un cliente vede quando apre il tuo sito? "
                    "Pochi secondi possono fare la differenza. Un messaggio chiaro, "
                    "un design curato e un contatto semplice rendono tutto piu facile. "
                    "Sito Lume, siti professionali per imprese in tutta Italia.")
        wavs,sr=model.generate_custom_voice(text=script,language="Italian",speaker=speaker)
        audio=np.asarray(wavs[0],dtype=np.float32)
        if len(audio)<int(sr*3) or len(audio)>int(sr*80):
            raise RuntimeError("TTS sample duration out of acceptable range")
        peak=float(np.max(np.abs(audio)))
        if not np.isfinite(peak) or peak<0.001:raise RuntimeError("TTS output silent or corrupt")
        path=out/f"{speaker.lower()}-it.wav"
        sf.write(path,audio,sr,subtype="PCM_16")
        with sf.SoundFile(path) as f:
            duration=round(f.frames/f.samplerate,2)
        print(f"Voice verified: {speaker} Italian, {duration}s @ {sr}Hz")
    print("Cloud Qwen voices completed")

if __name__=="__main__":main()
