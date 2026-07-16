# Dubbing Satvic Movement into Regional India — Process, Reasoning & Results

**Task:** Dub *"Heal Constipation Permanently (5 Cures Nobody Talks About)"* (Hindi, 16:12)
into two regional languages, in Subah's own voice, using AI.

**Result:** Telugu + Malayalam dubs, voice-cloned from Subah's own audio, produced for
**₹0 of the ₹2,500 budget** — with a priced escalation path if native reviewers demand it.

---

## 1. The strategic insight that shaped everything

Before touching any dubbing tool, I checked what YouTube itself now offers — because if the
platform dubs for free, a paid pipeline has to justify its existence.

Finding (verified against YouTube's official docs, July 2026):

- YouTube auto-dubbing is free and covers 27 languages, **but from a Hindi source video the
  supported targets do NOT include Telugu, Malayalam or Kannada.** Kannada isn't an auto-dub
  target from *any* source language.
- Even where auto-dub exists (e.g., English→Telugu), it uses a generic synthetic voice —
  "expressive speech" (which preserves the creator's vocal character) does not cover
  Dravidian target languages.
- YouTube's multi-language audio feature lets a creator upload custom dubbed tracks to an
  existing video (Studio → Languages → Add language → Dub), and custom tracks coexist with /
  override auto-dubs.

**So for exactly the audience Satvic wants to reach, there is no free platform path.**
Custom dubbed tracks in Subah's cloned voice are the *only* way — and because most
Hindi-first channels haven't realised this, it's an open reach opportunity. Trust in a
health channel lives in the teacher's voice; a generic TTS voice would spend that trust,
a cloned one carries it across languages.

## 2. Language choice: Telugu + Malayalam

| | Telugu | Malayalam | Kannada |
|---|---|---|---|
| Native speakers | ~96M (largest of the three) | ~38M | ~59M |
| Auto-dub from Hindi | ✗ | ✗ | ✗ |
| Auto-dub from English | ✓ (generic voice) | ✗ | ✗ |

Telugu is the largest unreached audience; Malayalam adds Kerala's famously health-conscious
viewership — a natural fit for Satvic content. At scale, the second-language choice should
come from YouTube Analytics geography data, not intuition (see §7).

## 3. Tool research — the market, and why the winner changed twice

Criteria: (a) Hindi → Te/Ml actually supported, (b) clones Subah's voice, (c) fits ₹2,500,
(d) translation editable *before* audio synthesis (non-negotiable for health content),
(e) automatable beyond one video.

| Tool | Hi→Te/Ml | Voice clone | ₹2,500 verdict | Notes |
|---|---|---|---|---|
| **IndicF5** (AI4Bharat, IIT-M) | ✓ | ✓ zero-shot | **✓ ₹0 — final choice** | Open-source, runs locally, trained on 1,417h of Indian speech |
| **Sarvam AI Dub** (India) | ✓ purpose-built | ✓ | ✗ **waitlist-gated** | On-paper winner; dubbing product not self-serve |
| **ElevenLabs** | ✓ (Eleven v3: `tel`, `mal`) | ✓ best fidelity | ✓ $5–22 | Held as priced fallback (Tier 2/3) |
| Dubverse (India) | ✓ | ✓ Supreme plan | ~at ceiling | Unique: publishes straight to YT multi-audio |
| HeyGen | ✓ | ✓ | ✗ $29, just over | Unlimited audio dubs on paid — best value if budget flexes |
| Rask.ai | ✓ | ✓ | ✗ $50 minimum | |
| Camb.ai | ✓ | ✓ | ✗ ~3 dubbing min at $20 self-serve | Enterprise-oriented |
| Vozo / Murf | partial/unclear | ✓ | ✗ points model / Te-Ml dub unconfirmed | |
| Google TTS / Azure / Bhashini | pieces only | gated/none | pennies but DIY, no clone | |
| YouTube auto-dub | ✗ for these languages | ✗ | free | The gap that makes this task matter |

**The decision changed twice, and that's the honest story:**
1. *Sarvam Dub* won the comparison table — purpose-built, India-trained, ₹1,000 free credits.
   Then it turned out to be **waitlist/enterprise-gated**. A tool that wins on paper but can't
   be accessed today loses to one that can.
2. *ElevenLabs Creator* (₹1,950) became the plan — until asking "what would this cost at ₹0?"
   surfaced **IndicF5**: open-source, from India's own AI4Bharat lab, zero-shot voice cloning,
   native Telugu/Malayalam support, running locally on a MacBook.

**Final architecture — a quality ladder that starts at ₹0:**
- **Tier 1 (shipped): IndicF5** + fully-local pipeline. Total spend: ₹0.
- **Tier 2 (~₹450): ElevenLabs Starter** if native listeners judge the clone insufficient.
- **Tier 3 (~₹1,950): ElevenLabs Creator** for maximum fidelity + headroom.

The budget's job changed from "what we spend" to "the escalation path we priced but didn't
need." The quality gate that decides tier promotion is the native-speaker review — designed
in, not bolted on.

## 4. The pipeline (what actually ran)

```
YouTube video (Hindi, 16:12)
  │ yt-dlp (free)
  ├── audio ──► Whisper medium, local (free) ──► 230 timestamped Hindi segments
  │                     │
  │                     ▼
  │        Transcript repair + glossary-locked translation (LLM)  ◄── glossary.md (locked FIRST)
  │                     │   Telugu & Malayalam, segment-by-segment,
  │                     │   colloquial register, numbers as words,
  │                     ▼   every line back-translated to English
  │        Review sheets (CSV) ──► native-speaker verification
  │                     │
  ├── Demucs (free) ──► clean voice stem ──► 6.6s reference clip of Subah
  │                └──► music/SFX bed
  │                     ▼
  │        IndicF5 zero-shot clone (free, local):
  │        cloned voice speaks each reviewed segment (~2h CPU per language)
  │                     ▼
  └── ffmpeg: segments placed on original timeline + music bed,
        loudness-normalised ──► full-mix track (exact source duration)
        ──► dubbed MP4 preview + WAV for YouTube multi-audio upload
```

Two design decisions worth defending:

**Why not feed the video to an end-to-end dubbing tool?**
For health content, the script must be frozen, glossary-checked and human-reviewed *before*
any audio exists — end-to-end tools hide translation inside the black box, and every fix
after synthesis costs a re-render. Keeping translation outside the tool also means the
translation layer is portable across TTS engines (the tier ladder above).

**Why source-separate the audio?**
YouTube's multi-audio track replaces the *entire* mix. A dub without Satvic's music bed
feels like a different, cheaper video. Demucs gives us the music bed to remix under every
language — and, as a bonus, a studio-clean voice stem that makes a far better voice-clone
reference than the mixed audio.

## 5. What didn't work — dead ends, kept honest

- **YouTube caption rip**: the video's caption track kept rate-limiting (HTTP 429) and turned
  out to be auto-generated from an en-IN base — unusable as a translation source of truth.
  Whisper on the actual Hindi audio replaced it.
- **Whisper's Hindi ASR mangles code-switched English** — कुन्स्टिपेशन (constipation),
  आश्कार्ड (ash gourd), ध्रिफला (Triphala), दब्यूसी (WC). ~40 such per video. This is why
  "validate the source transcript" is step one of QC: every segment's Hindi was repaired
  from context before translation, recorded in a `hi_clean` field.
- **Demucs produced nothing on first run** — its audio writer needed an undeclared extra
  package (torchcodec). Free local tools: ₹0 in money, paid in patience.
- **Sarvam Dub, the on-paper winner, is waitlist-gated** (see §3).
- **IndicF5 fought back three times**: (a) its HuggingFace repo is consent-gated — an account
  must explicitly agree to clone only voices it has permission for (ethically, a point in its
  favour); (b) HuggingFace's new Xet download backend failed repeatedly until disabled;
  (c) it crashes on current `transformers` (meta-device init) — downgrading to the 4.x
  series it was built for fixed it. Version drift is the tax on research-grade tools.
- **First translation draft was too "pure"** — literary/Sanskritized register. Founder
  feedback caught it: Subah's Hindi is everyday Hinglish, and the dub must sound like a
  Telugu/Malayalam YouTuber talking at home. The register rule was locked into the glossary
  (with a concrete test: *would a casual native health YouTuber say this line aloud?*) and
  all 460 segments were rewritten. This is now a permanent, reusable rule for every future video.
- **Whisper is an unreliable judge of Telugu.** Our Telugu test clip round-tripped as
  *silence* through generic Whisper — twice. A controlled experiment (Hindi through the same
  pipeline: near-perfect; the same clip through IIT-M's Telugu-finetuned Whisper: near
  word-perfect) proved the checker was broken, not the audio. **Lesson: never QC a
  low-resource language with a judge that's weak in that language — validate the validator.**
- **The reference-voice leak — the most important failure, and a native ear caught it.**
  IndicF5 (like the F5-TTS family it's built on) intermittently *echoes the tail of the
  voice-clone reference line* at the start of a generated segment. My reference clip was
  Subah saying a Hindi sentence ending "...रेक्टम बेंट रहता है" — so that Hindi phrase was
  bleeding into the *start* of many Malayalam segments. My early spot-checks happened to land
  on clean segments and missed it; a native listener flagged it immediately ("there's a
  repeated word — rectum bent raha tha"). An automated ASR scan of all 230 segments then
  quantified it: **~28% of segments had the leak.** Getting to a genuine fix took several
  wrong turns worth recording:
  - **Wrong detector #1 — word-matching the leaked Hindi.** ASR spells the mangled echo
    differently every time, so exact-match waved through segments that were still leaking.
  - **Wrong detector #2 — Hindi language-ID.** "First 2.5s reads as Hindi" caught the *rectum*
    leak, but when I switched references to a "neutral" line, its tail was "...ninety **degree
    angle banta hai**" — and because "degree angle" is English, those segments read as
    English, sailed past the Hindi detector, and a scan reported a false **"0 leaks."** The
    native listener caught it again. Lesson burned in: **a green light from a detector you
    haven't stress-tested is worth nothing.**
  - **Wrong detector #3 — "any Devanagari / reads as Hindi = leak."** This over-flagged wildly:
    Whisper-small renders *clean* Malayalam into Devanagari-looking text and often misreads it
    as Hindi, so it flagged 53 clean segments. Trimming those would have *damaged* good content.
  - **Root cause, finally.** The echo wasn't inherent — it was caused by a **badly-cut
    reference** (mine ended mid-sentence). Re-cutting the reference as a **clean, complete,
    silence-trimmed sentence** dropped the echo from ~28% to **~1%** (3 of 230 in Malayalam).
  - **The fix that shipped:** (1) clean-sentence reference → almost no echo at the source;
    (2) re-synthesize both languages fresh; (3) a **precise** detector keyed to the reference's
    own Hindi function words (which never occur in clean Telugu/Malayalam) — not language-ID,
    not Devanagari-presence; (4) deterministic prefix-trim on the handful of genuine residuals,
    content ASR-checked afterwards.
  **Lessons: (a) the human ear is the ground truth — it caught this twice when automation
  didn't; (b) fix root cause (reference quality) over symptoms (chasing leaks downstream);
  (c) a detector must be validated against both false negatives AND false positives before you
  trust its "0"; (d) a voice-clone reference should be a clean, complete, topic-neutral
  sentence — whatever it says, and however it's cut, can surface in the output.**
- **Dravidian languages run ~40% longer than Hindi, and that breaks lip/scene sync.** The
  first full Malayalam assembly drifted up to 3.3 seconds behind the picture in a dense
  explanatory stretch, because translated lines were simply longer than their source slots.
  Two-part fix: (1) a small time-stretch (≤1.3×) per segment, and (2) for the worst 39
  segments, a targeted *re-translation to be shorter* — cutting discourse fillers and padding
  while protecting every dosage, duration and instruction. **This is the real lesson for
  scale: translation length is a first-class constraint in dubbing, not an afterthought. The
  brief to a translator (human or AI) must include the time budget per line**, or every dub
  needs a fixing pass. Our review sheets now carry a `length-risk` flag for exactly this.

## 6. Verification — how accuracy was actually checked

Layered, cheapest-first (modelled on the premix/postmix discipline used in professional
dubbing QC):

1. **Glossary lock before translation** — brand terms, ayurvedic terms transliterated not
   translated, English loanwords natives keep, ALL numbers spelled out as words (Indic TTS
   garbles digits), respectful మీరు/നിങ്ങൾ register, colloquial-not-pure rule.
2. **Source-transcript repair** — every Whisper mangling fixed from context before
   translation; unrecoverable lines flagged `unclear-source` rather than guessed silently.
3. **Machine-checkable rules enforced in code** — zero digits in 460 translated segments,
   segment counts and timestamps verified identical to source.
4. **Back-translation on every line** — each Telugu/Malayalam segment carries a literal
   English back-translation in the review sheet, so a reviewer (or Satvic's team) can audit
   meaning without reading both scripts.
5. **ASR round-trip on synthesized audio** — the dub is transcribed back by a speech
   recognizer and compared to the intended text (using language-appropriate checkers — see §5).
   Caught a real finding: mild accent-transfer slur on మలబద్ధకాన్ని (the word "constipation"!),
   flagged for the native pronunciation pass.
6. **Native-speaker review — the step that actually decides.** Each reviewer gets a
   timestamped CSV (230 rows: Hindi | translation | back-translation | auto-flags) with
   **74 health-claim lines (Telugu) / 63 (Malayalam)** pre-flagged: dosages, durations,
   do/don't instructions, health promises. Severity taxonomy: blocker / issue / preference.
   Then a full watch-down of the dubbed video for pronunciation, glitches, sync.
   (Review kit included in this folder; Satvic's offer to verify samples plugs in exactly here.)
7. **Technical pass** — duration matches source within tolerance, loudness normalised to
   YouTube's ~-14 LUFS, no clipping, music bed intact.
8. **In-player check after upload** — switch audio tracks in a real player, confirm sync and
   localized title/description.

## 7. At scale — what changes across the full library

1. **Order by analytics, not alphabet.** Dub the top-20 watch-time videos first; pick
   languages from Analytics geography + subscriber requests. One probe video per language,
   read 28-day watch time, then commit.
2. **The pipeline is already a queue.** Every step above is scripted; human time concentrates
   exactly where it should: script review and native watch-down. One freelance native
   reviewer per language (~₹2–3k/video) working from CSV sheets — 10× cheaper than fixing
   audio after synthesis.
3. **The glossary compounds.** Every reviewed video grows the locked per-language glossary,
   shrinking future review time. The glossary *is* the moat — it encodes how Satvic speaks
   Telugu and Malayalam.
4. **Formalise the voice.** One professionally-verified clone per language with Subah's
   recorded consent, living in a Satvic-controlled account, instead of per-video zero-shot
   cloning — consistency plus a clean rights posture.
5. **Hardware beats APIs at library scale.** CPU synthesis costs ~2h per video-language.
   A single GPU (rented at ~₹25–50/hr, or Sarvam's API once off the waitlist) collapses that
   to minutes. At 200 videos × 3 languages, the compute bill is trivial either way — the real
   cost is human QC, which is exactly where a health channel *should* spend.
6. **Keep auto-dub ON** for the ~16 languages YouTube covers from Hindi for free (English,
   Bengali, Punjabi, Spanish...); spend custom-dub effort only where the platform is blind:
   Telugu, Malayalam, Kannada, Tamil.
7. **Localize metadata at scale** — titles/descriptions per language (bulk CSV via Content
   Manager); it's what makes dubbed tracks *discoverable*, not just available.

## 8. Rights & consent

Voice cloning used Subah's own published audio, for Satvic Movement's own content, at
Satvic's invitation. The IndicF5 license itself requires explicit permission for any cloned
voice — which this use case has by construction. For production rollout: record Subah's
formal consent statement and keep the voice assets in a Satvic-controlled account.

## 9. Costs

| Item | Cost |
|---|---|
| yt-dlp, Whisper, Demucs, ffmpeg, IndicF5, translation, QC tooling | ₹0 |
| ElevenLabs fallback (priced, not needed) | ₹450–1,950 |
| **Total spent of ₹2,500 budget** | **₹0** |

Both final videos passed technical QC (duration, sync < 0.6s, −14 LUFS, zero reference-leak
across 460 segments) — see QC_RESULTS.md. Accuracy sign-off is the native-speaker review,
for which the review kit is provided.
