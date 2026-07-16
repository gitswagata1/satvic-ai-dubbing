# dub-project — the AI dubbing pipeline (working directory)

This is the **engine room** for the Satvic dubbing task. The polished deliverables live in
the sibling submission folders (`../1_Final_Videos`, etc.); this folder is the reusable pipeline that produced them.

Everything is free/local: **yt-dlp · Whisper · Demucs · IndicF5 (AI4Bharat) · ffmpeg**.

## Folder layout

```
dub-project/
├── scripts/          the pipeline (run from THIS root: `python scripts/xxx.py <lang>`)
├── inputs/           source_video.mp4, source_audio.m4a  (from YouTube)
├── references/       voice-clone samples of Subah
│                       ref_subah.wav  — original (its text mentions "rectum"; caused leaks)
│                       ref_neutral.wav — leak-safe replacement (no medical words)
├── data/             segments_hi/te/ml.json, glossary.md, transcript/, stems/
│                       stems/ = Demucs output: vocals.wav + no_vocals.wav (music bed)
├── segment_audio/    synth_ml/, synth_te/  — 230 voice-cloned clips per language
├── output/           speech_*.wav, dub_*.mp4 (AV1 pre-transcode), dub_*_track.wav, review sheets
└── requirements.txt  pinned deps (env removed to save space — recreate below)
```

## Recreate the environment
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # transformers==4.49, openai-whisper, demucs, torch, soundfile
```
Also needs the CLI tools `ffmpeg` and `yt-dlp` (e.g. `brew install ffmpeg yt-dlp`), plus a
HuggingFace token with gated-repo access for `ai4bharat/IndicF5`.

## The pipeline, in order

| # | Command | What it does |
|---|---------|--------------|
| 0 | `yt-dlp` + `whisper` + `demucs` | download → Hindi transcript → split voice/music (done; outputs in data/) |
| — | *(translate)* | `data/segments_hi.json` → `segments_te/ml.json` per `data/glossary.md` (LLM + native review) |
| 1 | `python scripts/synth_full.py <te\|ml>` | voice-clone every segment with IndicF5 → `segment_audio/synth_<lang>/` |
| 2 | `python scripts/fix_leaks.py <lang> scan` | LID-scan all segments; regenerate any that **start in Hindi** (reference-echo leak), loop to zero |
| 3 | `python scripts/trim2.py <lang> <id,id,...>` | last resort: trim the Hindi prefix off stubborn leak segments |
| 4 | `python scripts/final_scan.py <lang>` | verify **0 / 230** segments leak |
| 5 | `python scripts/assemble.py <lang>` | fit each clip to its time slot, remix the music bed, mux → `output/dub_<lang>.mp4` + `_track.wav` |
| 6 | `ffmpeg ... libx264` | transcode AV1→H.264 for the deliverable (see PROCESS.md) |

`fix_leaks.py <lang> <id,id>` (instead of `scan`) re-synths a specific set — used after
shortening over-length segments, so the regenerated ones get leak-checked too.

## Key gotchas (baked into the scripts / learned the hard way)
- **Reference-echo leak**: IndicF5 echoes the reference line's tail into ~25% of segments.
  Fixed by neutral reference + terminal punctuation + LID scan-and-regenerate loop. Detect
  with *language ID*, not word-matching (ASR spells the echo differently each time).
- **Numbers as words**: digits garble in Indic TTS — translations spell every number out.
- **Length**: Dravidian runs ~40% longer than Hindi; `assemble.py` time-fits (≤1.3×) and
  over-length lines get shortened upstream, then re-synth'd via `fix_leaks.py <lang> <ids>`.
- **Run from this root**, not from `scripts/` — all paths are root-relative.

See `../2_Process_and_Reasoning/PROCESS.md` for the full reasoning.
