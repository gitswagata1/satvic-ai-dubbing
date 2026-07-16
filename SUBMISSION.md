# Creative Retreat — Final Submission
## Dubbing Satvic Movement into Regional India, with AI

**Role:** Founder's Office — AI Specialist  
**Task:** Dub an existing Hindi long-form video into two regional languages, in the creator's
own voice, using AI — genuinely watchable and accurate, not just technically possible.  
**Video dubbed:** *Heal Constipation Permanently (5 Cures Nobody Talks About)* — Hindi, 16:12.

---

## 1. What was delivered

| Deliverable | Where |
|---|---|
| **Telugu dub** — Subah's cloned voice, H.264 1080p, music bed intact, 972s | `1_Final_Videos/Satvic_Constipation_Telugu.mp4` |
| **Malayalam dub** — same spec | `1_Final_Videos/Satvic_Constipation_Malayalam.mp4` |
| **YouTube multi-audio tracks** (WAV, 48 kHz, −14 LUFS) | `1_Final_Videos/YouTube_Audio_Tracks/` |
| **Process & reasoning** (this doc + the deep writeup) | `2_Process_and_Reasoning/PROCESS.md` |
| **Pitch deck** (technical workflow + business case) | `Pitch_Deck.pptx` |
| **Native-speaker review kit** (460 lines, back-translated, health-claims flagged) | `3_Accuracy_Review_Kit/` |
| **Reproducible pipeline** (scripts, translations, transcript) | `5_Pipeline_Workspace/` |

**Cost: ₹0** of the ₹2,500 budget. **Verification: 0 reference-leaks across all 460 segments.**

> The final videos are ~339 MB each and are shared alongside this repository (drive / release);
> 20-second previews with the music bed are in `4_Audio_Samples/`.

---

## 2. The strategic insight (why this is worth doing at all)

Before choosing any tool, I checked what YouTube already does for free — because a paid
pipeline has to justify itself against the platform.

**YouTube's free auto-dubbing cannot produce Telugu, Malayalam, or Kannada from a Hindi
video.** Kannada isn't an auto-dub target from *any* language, and where auto-dub does exist
it uses a generic synthetic voice, not the creator's. So the ~190 million people who speak
these three languages are invisible to the channel today — purely for lack of an audio track.

Custom, voice-cloned multi-audio tracks are the **only** route to that audience, and almost no
Hindi-first channel has taken it. That is the reach opportunity, and it's a durable one.

---

## 3. Which tools, and why (the brief's core question)

| Step | Tool chosen | Why |
|---|---|---|
| Download | **yt-dlp** | Pulls video + original audio track cleanly. Free. |
| Transcribe | **OpenAI Whisper (medium)** | Timestamped Hindi transcript as the translation source of truth. Local, free. |
| Voice / music separation | **Demucs** | Splits Subah's voice (clone reference) from the music bed (needed because YouTube's dubbed track replaces the *entire* mix). |
| Translation | **LLM + a locked glossary + native review** | Kept *outside* the dubbing tool so every word is reviewable before synthesis. |
| Voice clone + TTS | **IndicF5 (AI4Bharat / IIT-Madras)** | Open-source, zero-shot voice cloning, native Telugu + Malayalam, runs locally. |
| Assemble | **ffmpeg** | Fits each line to timing, remixes the music bed, muxes the video, normalizes loudness. |

**Why IndicF5 over the alternatives — and the two pivots to get there:**

1. **Sarvam AI Dub** won the on-paper comparison (purpose-built for Indic dubbing with voice
   cloning) — but its dubbing product is **waitlist-gated**, not self-serve. A tool you can't
   access loses to one you can.
2. **ElevenLabs** has the best clone fidelity and supports both languages, but costs ~₹1,950.
   I kept it as a **priced fallback**, not the default.
3. **IndicF5** — India's own open-source model — does the exact job (Hindi→Te/Ml with voice
   cloning) for **₹0**, locally. It became Tier 1; ElevenLabs Starter (~₹450) and Creator
   (~₹1,950) are Tiers 2–3, priced but never needed.

The ₹2,500 budget stopped being a spend and became **an escalation ladder we priced but never
had to climb** — the decision to move up it is the native reviewer's, not a default.

Tools evaluated and rejected for this pilot: Rask (no free plan), Camb.ai (self-serve dubbing
minutes near-useless), HeyGen/Vozo/Murf (cost or Te/Ml-dub coverage), Dubverse (budget math),
and the DIY route (Google/Azure/Bhashini TTS) — cheapest per minute but you assemble the whole
STT→MT→TTS→sync chain yourself, which is essentially what IndicF5 + this pipeline already is.

---

## 4. What didn't work (the honest part)

- **YouTube's caption track** was auto-generated junk and rate-limited; Whisper on the real
  Hindi audio replaced it.
- **Whisper mangles code-switched English** inside Hindi ("constipation" → कुन्स्टिपेशन) — so
  transcript repair became step one, before any translation.
- **The first translation was too "pure"** — literary/Sanskritized. Founder feedback corrected
  it to everyday colloquial (how a Telugu/Malayalam YouTuber actually speaks); all 460 lines
  were rewritten and the rule locked into the glossary.
- **The reference-voice leak — caught by a native ear, twice.** IndicF5 occasionally echoes its
  voice-clone reference into a segment's start. My reference clip's tail ("…rectum bent rehta
  hai", then a "neutral" one whose tail was "…degree angle banta hai") bled into the dub.
  Worse: because the second leak was partly English, a language-ID scan reported a **false
  "0 leaks."** A native listener caught what the automation missed. Root cause turned out to be
  a **badly-cut reference clip**; re-cutting it as a clean, complete sentence dropped the leak
  rate from **~28% to ~1%** at the source. Both languages were then re-synthesized and verified
  with a **content-based** detector — final state **0 / 460**.

**The lesson threaded through all of these:** a detector's green light means nothing until it's
stress-tested for false positives *and* false negatives — and for a health channel, the human
ear is the ground truth. Which is exactly why the native review is the gate, not the machine.

---

## 5. How accuracy was verified

Layered, cheapest-first:

1. **Glossary lock** — brand/ayurvedic terms transliterated, English loanwords kept, all
   numbers spelled out as words (Indic TTS garbles digits), respectful register.
2. **Source-transcript repair** — every ASR error fixed before translation.
3. **Back-translation on every line** — each of 460 segments carries a literal English
   back-translation in the review sheet, so meaning is auditable without reading both scripts.
4. **Health-claim flags** — 74 Telugu / 63 Malayalam lines pre-flagged (dosages, durations,
   do/don't instructions, health promises) for priority review.
5. **Native-speaker watch-down** — script review, then a full watch of the dub. **This is the
   sign-off.** The review kit (`3_Accuracy_Review_Kit/`) makes it a ~40-minute job.
6. **Technical QC** — duration match, sync, −14 LUFS loudness, music bed intact, 0 leaks
   (`2_Process_and_Reasoning/QC_RESULTS.md`).

**Please still run the native review before publishing** — Satvic's team, or an arranged native
speaker per language. The pipeline gets it fluent and clean; a native ear confirms it's *right*.

---

## 6. If we did this at scale (the full library)

- **The pipeline is a queue.** Everything is scripted; human time concentrates only on
  script-review and the native watch-down — hire one freelance native reviewer per language.
- **Order by analytics, not alphabet** — dub top watch-time videos first; pick languages from
  YouTube Geography data.
- **The glossary compounds** — every reviewed video shrinks the next one's review time. It's the moat.
- **Keep YouTube's free auto-dub** for the 16 languages it covers from Hindi; spend custom-dub
  effort only where the platform is blind — Telugu, Malayalam, Kannada, Tamil.
- **Cost inverts nicely** — one GPU collapses synthesis to minutes; the real cost is native QC
  (~₹2–3k/video), which is exactly where a wellness brand should spend.
- **Formalize the voice** — one consented, verified clone per language in a Satvic-controlled
  account, replacing per-video zero-shot cloning (consistency + clean rights).

---

## 7. Rights & consent

Voice cloning used Subah's own published audio, for Satvic's own content, at Satvic's
invitation — and IndicF5's license itself requires permission for any cloned voice, which this
use has by construction. For a production rollout: record Subah's formal voice-consent statement
and keep the voice assets in a Satvic-controlled account.

---

## 8. How to navigate this submission

Start with this document, then:
- **`Pitch_Deck.pptx`** — the presentation (technical workflow + business case).
- **`2_Process_and_Reasoning/PROCESS.md`** — the full detailed writeup, dead ends and all.
- **`2_Process_and_Reasoning/PRESENTATION_SCRIPT.md`** — talking track for the screen recording.
- **`3_Accuracy_Review_Kit/`** — hand to a native speaker to verify accuracy.
- **`5_Pipeline_Workspace/`** — the reproducible pipeline (run order in its README).

*Two clean dubs today, in Subah's voice, for ₹0 — and a repeatable system ready for the library.*
