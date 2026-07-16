import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, whisper
LANG=sys.argv[1]; IDS=[int(x) for x in sys.argv[2].split(",")]
SR=24000; asr=whisper.load_model("small")
def hi_prob(seg, secs):
    if len(seg) < int(0.5*SR): return 0.0
    sf.write("/tmp/t.wav", seg[:int(secs*SR)], SR)
    mel=whisper.log_mel_spectrogram(whisper.pad_or_trim(whisper.load_audio("/tmp/t.wav"))).to(asr.device)
    _,p=asr.detect_language(mel); return p.get("hi",0.0), max(p,key=p.get)
for sid in IDS:
    path=f"segment_audio/synth_{LANG}/seg_{sid:03d}.wav"
    a,_=sf.read(path,dtype="float32"); a=a.mean(1) if a.ndim>1 else a
    cut=0.0
    while cut < 3.6:
        seg=a[int(cut*SR):]
        h15,_=hi_prob(seg,1.5); h25,t25=hi_prob(seg,2.5)
        if t25!="hi" and h15<0.30 and h25<0.30: break
        cut+=0.40
    trimmed=a[int(cut*SR):]
    # 15ms fade-in to avoid click
    n=int(0.015*SR); 
    if len(trimmed)>n: trimmed[:n]*=np.linspace(0,1,n)
    sf.write(path, trimmed, SR)
    h15,_=hi_prob(trimmed,1.5); h25,t25=hi_prob(trimmed,2.5)
    print(f"seg {sid}: total cut {cut:.1f}s -> start={t25} hi15={h15:.2f} hi25={h25:.2f} dur={len(trimmed)/SR:.1f}s", flush=True)
print("DONE")
