"""Detect + trim the reference-echo leak in both refs (rectum tail AND neutral 'degree angle
banta hai' tail). Distinctive markers are HINDI function words a clean Telugu/Malayalam
segment never contains — so legitimate content mentioning 'degree/angle' is NOT touched.
Trims using word-level timestamps; verifies the new start is leak-free."""
import sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, whisper

LANG = sys.argv[1]
SR = 24000
asr = whisper.load_model("small")
segs = json.load(open(f"data/segments_{LANG}.json"))

# HINDI-only leak signatures (won't appear in clean te/ml).
# Current reference tail = "...apne pehle tool se" -> pehle/shuru/karte/aaiye/apne.
# Old-reference tails kept as a safety net (rectum / 'degree angle banta hai').
MARK = ['pehle','shuru','karte','aaiye','apne','tool se',
        'पहले','शुरू','करते','आइए','अपने','टूल से',
        'banta','bantha','banda','bandha','बनता','बन्ता','नब्बे','nabbe','ऐसे','aise nab',
        'रहता है','रेक्टम','rectum','रेट्टम','degree angle','ninety degree']

def head_words(a, secs):
    sf.write("/tmp/hw.wav", a[:int(secs*SR)], SR)
    return asr.transcribe("/tmp/hw.wav", fp16=False, verbose=False, word_timestamps=True)

def marked(t):
    tl = t.lower()
    return any(m.lower() in tl for m in MARK)

def lid_hi(a, secs=2.5):
    sf.write("/tmp/hl.wav", a[:int(secs*SR)], SR)
    mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(whisper.load_audio("/tmp/hl.wav"))).to(asr.device)
    _, p = asr.detect_language(mel)
    return max(p, key=p.get) == "hi" or p.get("hi", 0) >= 0.40

fixed = []
for s in segs:
    sid = s["id"]; path = f"segment_audio/synth_{LANG}/seg_{sid:03d}.wav"
    a, _ = sf.read(path, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
    if len(a) < int(0.5*SR): continue
    r = head_words(a, 3.2)
    # PRECISE detection: only the reference-tail markers (Hindi function words that never
    # appear in clean Telugu/Malayalam). LID is NOT used — Whisper misreads clean Dravidian
    # audio as Hindi far too often, causing false positives that would trim real content.
    leak = marked(r["text"])
    if not leak:
        continue
    # trim to the end of the last Hindi-marker word within the first ~3.2s
    cut = 0.0
    for seg in r.get("segments", []):
        for wd in seg.get("words", []):
            if wd.get("end", 9) <= 3.4 and marked(wd["word"]):
                cut = max(cut, wd["end"])
    if cut <= 0:               # marker/LID said leak but no word boundary — iterative fallback
        cut = 0.4
        while cut < 3.4:
            sub = a[int(cut*SR):]
            rr = head_words(sub, 2.0)
            if not marked(rr["text"]): break
            cut += 0.4
    trimmed = a[int((cut+0.03)*SR):]
    n = int(0.015*SR)
    if len(trimmed) > n: trimmed[:n] = trimmed[:n]*np.linspace(0,1,n)
    # verify
    stillbad = marked(head_words(trimmed, 2.0)["text"])
    sf.write(path, trimmed, SR)
    fixed.append((sid, round(cut,2), "STILL-BAD" if stillbad else "ok"))
    print(f"seg {sid}: trimmed {cut:.2f}s -> {'STILL-BAD' if stillbad else 'clean'} dur={len(trimmed)/SR:.1f}s", flush=True)

bad = [f[0] for f in fixed if f[2] == "STILL-BAD"]
print(f"{LANG}: trimmed {len(fixed)} segments; residual still-bad={bad}", flush=True)
