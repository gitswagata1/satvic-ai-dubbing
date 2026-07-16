import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, whisper, json
LANG=sys.argv[1]; SR=24000; asr=whisper.load_model("small")
segs=json.load(open(f"data/segments_{LANG}.json"))
bad=[]
for s in segs:
    a,_=sf.read(f"segment_audio/synth_{LANG}/seg_{s['id']:03d}.wav",dtype="float32"); a=a.mean(1) if a.ndim>1 else a
    if len(a)<int(0.5*SR): continue
    sf.write("/tmp/f.wav", a[:int(2.5*SR)], SR)
    mel=whisper.log_mel_spectrogram(whisper.pad_or_trim(whisper.load_audio("/tmp/f.wav"))).to(asr.device)
    _,p=asr.detect_language(mel)
    if max(p,key=p.get)=="hi" or p.get("hi",0)>=0.35: bad.append((s['id'],round(p.get("hi",0),2)))
print(f"{LANG} FINAL: {len(bad)} leaking:", bad)
