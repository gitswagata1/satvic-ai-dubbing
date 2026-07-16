import sys, os, json, subprocess, time
import numpy as np, soundfile as sf
from transformers import AutoModel

LANG = sys.argv[1]          # 'te' or 'ml'
SEGS = json.load(open(f"data/segments_{LANG}.json"))
OUT = f"segment_audio/synth_{LANG}"
os.makedirs(OUT, exist_ok=True)
SR = 24000
REF_AUDIO = "references/ref_clean.wav"
REF_TEXT = "आइए शुरू करते हैं अपने पहले टूल से."

model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
print(f"[{LANG}] model loaded, {len(SEGS)} segments", flush=True)

t0 = time.time()
for i, s in enumerate(SEGS):
    path = f"{OUT}/seg_{s['id']:03d}.wav"
    if os.path.exists(path):
        continue
    text = s[LANG].strip()
    if not text:
        sf.write(path, np.zeros(int(0.1*SR), dtype=np.float32), SR); continue
    a = np.asarray(model(text, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT), dtype=np.float32)
    if np.abs(a).max() > 1.5: a = a / 32768.0
    sf.write(path, a, SR)
    if i % 10 == 0:
        el = time.time()-t0
        print(f"[{LANG}] {i+1}/{len(SEGS)} elapsed {el/60:.0f}m", flush=True)
print(f"[{LANG}] SYNTH COMPLETE in {(time.time()-t0)/60:.0f}m", flush=True)
