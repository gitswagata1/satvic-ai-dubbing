# Screen-Recording Presentation Script (~6–8 minutes)

---

**[0:00 — The gap]**
"Before picking any AI tool, I asked why this problem even exists — YouTube dubs videos for
free now. The answer: from a Hindi video, YouTube cannot auto-dub into Telugu, Malayalam or
Kannada. At all. And where it can dub, it uses a generic robot voice — not Subah's. For a
health channel, the voice *is* the trust. That's the gap, and that's why this is worth doing."

**[1:00 — The tool hunt, honestly]** *(show PROCESS.md §3 table)*
"I compared eleven tools. My first pick, Sarvam AI — India-trained, purpose-built — turned
out to be waitlist-gated. My second pick, ElevenLabs, would've cost ₹1,950 of the ₹2,500
budget. Then I asked a different question: what would this cost at zero? IIT Madras'
AI4Bharat lab open-sourced IndicF5 — voice cloning plus native Telugu and Malayalam, running
on my own laptop. The final spend was zero rupees, with ElevenLabs priced and held as a
fallback in case quality demanded it. I got to keep the budget as an escalation ladder
instead of an invoice."

**[2:30 — The pipeline]** *(show PROCESS.md §4 diagram)*
"Five free tools chained: yt-dlp pulls the video, Whisper transcribes the Hindi into 230
timestamped segments, Demucs separates Subah's voice from the music — which gives me both a
clean 6.6-second clone reference AND the original music bed to remix under each dub, because
YouTube's multi-audio track replaces the whole mix. Translation happens *outside* the
dubbing tool, on purpose: for health content, every word gets frozen and reviewed before
any audio exists."

**[3:30 — Play the samples]** *(play samples/test_te.wav, then test_ml.wav)*
"This is Subah's cloned voice speaking Telugu... and Malayalam. Cloned from six and a half
seconds of her existing videos, by a free model."

**[4:00 — What didn't work]** *(show PROCESS.md §5)*
"The dead ends taught the most. Whisper mangled every English word inside the Hindi —
'constipation' became कुन्स्टिपेशन — so transcript repair became step one of QC. My first
translation draft was too *pure* — textbook language — and got rewritten to everyday
YouTuber register, which is now a locked rule in the glossary. And the best one: my Telugu
audio kept failing its automated check... until I discovered the *checker* was broken, not
the audio. Whisper is nearly deaf to Telugu. A Telugu-specialist model heard it perfectly.
Lesson: when you QC a low-resource language, first validate the validator."

**[5:30 — Verification]** *(show review-kit/: a review sheet CSV + instructions)*
"Accuracy isn't vibes. Every one of the 460 translated lines carries an English
back-translation, and every health claim — 74 in Telugu, 63 in Malayalam — is pre-flagged:
dosages, durations, do's and don'ts. A native speaker of each language works through this
sheet, then watches the full dub. A dub that sounds fluent but says the wrong thing about
someone's health is worse than no dub — so the human review is the gate that decides
whether the free tier ships or we escalate to the paid one."

**[6:30 — At scale]** *(show PROCESS.md §7)*
"For the full library: the pipeline is already a script, so machines do the repetitive work
and humans concentrate where judgment lives — script review and native watch-down. Pick
videos by watch-time analytics, pick languages by audience geography, let the glossary
compound with every reviewed video, keep YouTube's free auto-dub for the sixteen languages
it does cover, and spend effort only where the platform is blind: Telugu, Malayalam,
Kannada, Tamil. The cost at scale isn't compute — it's native QC, and for a health channel
that's exactly the right place for the money to go."

**[7:30 — Close]** *(show videos/ folder)*
"Two dubbed videos, Subah's voice, zero rupees, and a process where every failure made the
system smarter. That's the how."
