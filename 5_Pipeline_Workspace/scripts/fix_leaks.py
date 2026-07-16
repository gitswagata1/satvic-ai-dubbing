import sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf
from transformers import AutoModel
import whisper

LANG = sys.argv[1]                     # 'ml' or 'te'
MODE = sys.argv[2] if len(sys.argv) > 2 else "scan"   # "scan" (all) or comma ids
MAX_ROUNDS = 8
SR = 24000
REF_AUDIO = "references/ref_neutral.wav"
REF_TEXT = "आजकल हम वेस्टर्न टॉयलेट्स यूज़ करने लगे हैं जिसमें आपकी बॉडी और नीज़ का ऐसे नब्बे डिग्री एंगल बनता है."

seg_list = json.load(open(f"data/segments_{LANG}.json"))
SEGS = {s["id"]: s for s in seg_list}

print(f"[{LANG}] loading models...", flush=True)
model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
asr = whisper.load_model("small")

def synth(sid):
    s = SEGS[sid]; text = s[LANG].strip()
    path = f"segment_audio/synth_{LANG}/seg_{sid:03d}.wav"
    if not text:
        sf.write(path, np.zeros(int(0.1*SR), dtype=np.float32), SR); return
    a = np.asarray(model(text, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT), dtype=np.float32)
    if np.abs(a).max() > 1.5: a = a / 32768.0
    sf.write(path, a, SR)

def is_leak(sid, secs=2.5):
    """Leak = first `secs` detected as Hindi (a regional dub start never should be)."""
    a, _ = sf.read(f"segment_audio/synth_{LANG}/seg_{sid:03d}.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    if len(a) < 0.4*SR: return False
    sf.write("/tmp/lidchk.wav", a[: int(secs*SR)], SR)
    audio = whisper.pad_or_trim(whisper.load_audio("/tmp/lidchk.wav"))
    mel = whisper.log_mel_spectrogram(audio).to(asr.device)
    _, probs = asr.detect_language(mel)
    top = sorted(probs.items(), key=lambda x: -x[1])
    hi = probs.get("hi", 0.0)
    return top[0][0] == "hi" or hi >= 0.35

if MODE == "scan":
    t0 = time.time()
    working = [s["id"] for s in seg_list if is_leak(s["id"])]
    print(f"[{LANG}] LID scan of {len(seg_list)}: {len(working)} leaking "
          f"({(time.time()-t0)/60:.0f}m) ids={working}", flush=True)
else:
    working = [int(x) for x in MODE.split(",") if x.strip()]

for rnd in range(1, MAX_ROUNDS+1):
    t0 = time.time()
    for sid in working: synth(sid)
    residual = [sid for sid in working if is_leak(sid)]
    print(f"[{LANG}] round {rnd}: {len(working)} -> {len(residual)} leaking "
          f"({(time.time()-t0)/60:.0f}m) residual={residual}", flush=True)
    working = residual
    if not working:
        print(f"[{LANG}] ALL CLEAN after round {rnd}", flush=True); break
else:
    print(f"[{LANG}] STOPPED, residual={working}", flush=True)
