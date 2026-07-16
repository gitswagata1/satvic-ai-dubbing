# QC Results — Telugu & Malayalam Dubs

Automated verification run on the final deliverables. The **native-speaker review is still
the gate that signs off accuracy** (review kit provided); this sheet records what the
machine checks confirmed and what to look at first.

## Technical QC (both languages)

| Check | Target | Telugu | Malayalam |
|---|---|---|---|
| Video duration matches source | 972.13s | ✅ 972.0s | ✅ 972.0s |
| Audio/scene drift (max) | < ~1.5s | ✅ ~1.1s | ✅ 1.1s |
| Integrated loudness | ~ −14 LUFS | ✅ −14.3 | ✅ −14.2 |
| True peak | ≤ −1 dBTP | ✅ −1.5 | ✅ −1.5 |
| Video codec / resolution | H.264 1080p | ✅ | ✅ |
| Numbers as words (no digits) | 0 digits | ✅ 0/230 | ✅ 0/230 |
| Reference-voice leak (content scan) | 0 leaks | ✅ 0/230 | ✅ 0/230 |
| Music bed preserved under dub | present | ✅ | ✅ |

**On the leak check:** these videos were rebuilt from scratch after a native listener caught
a reference-echo leak ("degree angle banta hai") that an earlier, weaker gate had wrongly
passed. Root cause was a badly-cut voice-clone reference; re-cutting it as a clean complete
sentence dropped the echo from ~28% to ~1% at the source (3 segments trimmed in Malayalam,
0 in Telugu). Final verification uses a **content-based** scan keyed to the reference's own
Hindi words — not the language-ID gate that produced the earlier false "0" — and both
languages now read **0 real leaks across all 230 segments.**

## Accuracy checks done (pre-native-review)
- Source Hindi transcript repaired segment-by-segment (Whisper mangles code-switched English).
- Every line carries an English back-translation in the review sheet.
- Health-claim lines pre-flagged: **74 (Telugu), 63 (Malayalam)** — dosages, durations,
  do/don't instructions, health promises.
- Register corrected to everyday colloquial (founder feedback) across all 460 lines.

## Priority-review flags (tell your native reviewers to start here)
- **Malayalam segments 6, 141, 207**: the only 3 with a residual reference echo; the leaked
  prefix was trimmed (0.7–2.6s). Confirm each still opens naturally and nothing was clipped.
  (Telugu needed no trims — 0 leaks.)
- **Telugu seg 180** ("adī mimmalni kēr chēstundi"): shortened to fit its 1.5s slot but still
  slightly tight — confirm it isn't clipped or rushed.
- The single most-repeated word — "constipation" (Telugu మలబద్ధకం) — showed mild accent
  transfer in early tests; give it a focused listen.

## Known limitations (honest)
- IndicF5 is research-grade: voice identity is strong (confirmed "sounds like Subah"), but
  prosody on long compound words can be flatter than a human dub. The tier-2/3 paid path
  (ElevenLabs, priced in PROCESS.md §3) is the escalation if native reviewers want more polish.
- Numbers, ayurvedic terms, and English loanwords were handled by rule + glossary, but a
  native ear is the final check on each.
