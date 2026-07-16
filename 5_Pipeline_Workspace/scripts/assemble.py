import sys, os, json, subprocess
import numpy as np, soundfile as sf

LANG = sys.argv[1]
SR = 24000
MAX_TEMPO = 1.30          # max speed-up to fit a slot
SEGS = json.load(open(f"data/segments_{LANG}.json"))
DUR = 972.126621          # exact source duration

canvas = np.zeros(int(DUR * SR) + 5 * SR, dtype=np.float32)
write_head = 0.0      # earliest time the next segment may start (no overlaps, ever)
max_drift = 0.0
GAP = 0.12            # minimal breath gap between cascaded segments

for i, s in enumerate(SEGS):
    path = f"segment_audio/synth_{LANG}/seg_{s['id']:03d}.wav"
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    # trim leading/trailing synthesis silence (keep 60ms breath)
    nz = np.where(np.abs(a) > 0.005)[0]
    if len(nz):
        pad = int(0.06 * SR)
        a = a[max(0, nz[0] - pad): min(len(a), nz[-1] + pad)]
    nominal = s["start"]
    start = max(nominal, write_head)          # cascade: start late rather than overlap
    slot_end = SEGS[i + 1]["start"] if i + 1 < len(SEGS) else DUR
    slot = slot_end - start
    dur = len(a) / SR
    if dur > slot and slot > 0.3:
        tempo = min(dur / slot, MAX_TEMPO)
        tmp_in, tmp_out = f"/tmp/fit_in.wav", f"/tmp/fit_out.wav"
        sf.write(tmp_in, a, SR)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp_in,
                        "-filter:a", f"atempo={tempo:.4f}", tmp_out], check=True)
        a, _ = sf.read(tmp_out, dtype="float32")
        dur = len(a) / SR
    p0 = int(start * SR)
    if p0 < len(canvas):
        end = min(p0 + len(a), len(canvas))
        canvas[p0:end] += a[: end - p0]
    write_head = start + dur + GAP
    max_drift = max(max_drift, start - nominal)

sf.write(f"output/speech_{LANG}.wav", canvas[: int(DUR * SR)], SR)
tail_over = max(0.0, write_head - GAP - DUR)
print(f"speech track written; max drift from timestamps {max_drift:.2f}s; tail overrun {tail_over:.2f}s")

# mix with music bed, normalize to -14 LUFS, encode outputs
base = f"output/dub_{LANG}"
subprocess.run(["ffmpeg", "-y", "-v", "error",
    "-i", f"output/speech_{LANG}.wav",
    "-i", "data/stems/htdemucs/source_audio/no_vocals.wav",
    "-filter_complex",
    "[0:a]aresample=48000[sp];[1:a]aresample=48000,volume=0.9[bed];"
    "[sp][bed]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]",
    "-map", "[out]", "-ar", "48000", "-ac", "2", f"{base}_track.wav"], check=True)
print(f"{base}_track.wav written (48k stereo, -14 LUFS)")

subprocess.run(["ffmpeg", "-y", "-v", "error",
    "-i", "inputs/source_video.mp4", "-i", f"{base}_track.wav",
    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "-shortest", f"{base}.mp4"], check=True)
print(f"{base}.mp4 written")
