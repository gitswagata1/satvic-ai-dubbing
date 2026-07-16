# Dubbing Satvic Movement into Regional India 🇮🇳

**Creative Retreat · Founder's Office — AI Specialist submission**

Dub an existing Hindi long-form YouTube video into **Telugu and Malayalam**, in the
creator's **own cloned voice**, using AI — good enough to actually publish.

**Result:** two watchable, verified-clean dubbed videos, produced for **₹0** of the ₹2,500
budget, on a fully local open-source pipeline — plus a repeatable system for the whole library.

Video dubbed: *"Heal Constipation Permanently (5 Cures Nobody Talks About)"* (Hindi, 16:12).

---

## Why this matters (the 30-second version)

YouTube's free auto-dubbing **cannot** produce Telugu, Malayalam or Kannada from a Hindi
video. So the ~190 million people who speak those languages are invisible to the channel
today — not for lack of interest, but for lack of an audio track. Custom dubbed tracks in
Subah's voice are the only way to reach them, and almost no Hindi-first channel has done it.
That's the opening.

## Repository map

| Folder | What's inside |
|---|---|
| [`1_Final_Videos/`](1_Final_Videos/) | The two dubbed videos + YouTube-ready audio tracks *(media not committed — see folder README)* |
| [`2_Process_and_Reasoning/`](2_Process_and_Reasoning/) | **[PROCESS.md](2_Process_and_Reasoning/PROCESS.md)** (the main writeup), the presentation script, and QC results |
| [`3_Accuracy_Review_Kit/`](3_Accuracy_Review_Kit/) | Native-speaker review sheets (460 lines, back-translated, health-claims flagged), instructions, glossary |
| [`4_Audio_Samples/`](4_Audio_Samples/) | 20-second previews of each final dub + early quality-gate clips |
| [`5_Pipeline_Workspace/`](5_Pipeline_Workspace/) | The full reproducible pipeline: scripts, translations, transcript *(large binaries gitignored — regenerable)* |
| [`SUBMISSION.md`](SUBMISSION.md) | The one-document executive summary of the whole engagement |
| `Pitch_Deck.pptx` | The slide deck: technical workflow + business case |

## The pipeline in one diagram

```
YouTube (Hindi 16:12)
  │ yt-dlp
  ├─ audio ─► Whisper ─► 230 timestamped Hindi segments
  │             └─► transcript repair ─► glossary-locked translation (Te / Ml)
  │                    │  colloquial register · numbers as words · back-translated
  │                    ▼  ─► native-speaker review sheets
  ├─ Demucs ─► clean voice stem ─► voice-clone reference (Subah)
  │        └─► music/SFX bed
  │             ▼
  │   IndicF5 (AI4Bharat) zero-shot clone ─► each segment in Subah's voice
  │             ▼  ─► leak scan + trim (content-based) ─► 0 leaks / 460 segments
  └─ ffmpeg ─► fit timing + remix music bed ─► dubbed track (−14 LUFS)
                 ▼
        H.264 video + WAV track for YouTube multi-audio upload
```

Every tool is free/open-source. Total spend: **₹0**. The ₹2,500 budget became a priced
escalation ladder (ElevenLabs) that quality never forced us onto.

## Reproduce it

```bash
cd 5_Pipeline_Workspace
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # + ffmpeg, yt-dlp
# then, per language:
.venv/bin/python scripts/synth_full.py ml     # voice-clone every segment
.venv/bin/python scripts/leak_trim.py  ml     # detect + trim reference-echo leaks
.venv/bin/python scripts/assemble.py   ml     # fit timing, remix music, mux video
```
Full run order and gotchas: [`5_Pipeline_Workspace/README.md`](5_Pipeline_Workspace/README.md).

## The honest part

Two reference-echo bugs slipped past automated checks and were caught by a **native
listener** — both are documented as the headline lessons in PROCESS.md. Accuracy sign-off
is the native review (kit in folder 3), not the machine. That discipline is the point:
for health content, a smooth-sounding wrong dub is worse than no dub.

## Credits & licenses
Pipeline code: MIT ([LICENSE](LICENSE)). Models: [AI4Bharat IndicF5](https://huggingface.co/ai4bharat/IndicF5),
[OpenAI Whisper](https://github.com/openai/whisper), [Demucs](https://github.com/adefossez/demucs).
Source content © Satvic Movement (not redistributed).
