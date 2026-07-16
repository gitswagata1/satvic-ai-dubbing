"""Detection-only report. Flags segments whose FIRST 2.5s looks like the reference-echo leak
(neutral tail 'ninety degree angle banta hai' OR old rectum tail), while EXCLUDING the few
segments whose own translation legitimately discusses the 90-degree angle."""
import sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, whisper

LANG = sys.argv[1]; SR = 24000
asr = whisper.load_model("small")
segs = json.load(open(f"data/segments_{LANG}.json"))

# leak markers seen in the echoed tail (English-translated OR Devanagari OR romanized)
LEAK = ['degree','angle','ninety','nabbe','banta','bantha','banda','western','vestern',
        'बनता','बन्ता','नब्बे','डिग्री','एंगल','आंगल','रेक्टम','rectum','रहता']
# a segment legitimately about the angle if its OWN translation mentions angle/degree/ninety
LEGIT = ['degree','angle','ninety',' డిగ్రీ','కోణం','తొంబై','డിഗ്രി','ആംഗിൾ','കോൺ','തൊണ്ണൂറ്','९०','90']

def has(t, words):
    tl = t.lower(); return any(w.lower() in tl for w in words)

def devanagari(t): return any('ऀ' <= c <= 'ॿ' for c in t)

flagged, legit_hits = [], []
for s in segs:
    sid = s["id"]
    a, _ = sf.read(f"segment_audio/synth_{LANG}/seg_{sid:03d}.wav", dtype="float32")
    a = a.mean(1) if a.ndim > 1 else a
    if len(a) < int(0.5*SR): continue
    sf.write("/tmp/d.wav", a[:int(2.5*SR)], SR)
    txt = asr.transcribe("/tmp/d.wav", task="transcribe", fp16=False, verbose=False)["text"]
    mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(whisper.load_audio("/tmp/d.wav"))).to(asr.device)
    _, p = asr.detect_language(mel)
    is_hi = max(p, key=p.get) == "hi" or p.get("hi",0) >= 0.40
    looks_leak = has(txt, LEAK) or devanagari(txt) or is_hi
    own_legit = has(s.get(LANG,""), LEGIT) or has(s.get("bt",""), ['degree','angle','ninety'])
    if looks_leak and not own_legit:
        flagged.append(sid); print(f"LEAK seg {sid}: hi={p.get('hi',0):.2f} :: {txt.strip()[:65]}", flush=True)
    elif looks_leak and own_legit:
        legit_hits.append(sid)
print(f"{LANG}: {len(flagged)} leaking, {len(legit_hits)} legit-angle-excluded {legit_hits}", flush=True)
print("IDS:", ",".join(map(str, flagged)), flush=True)
