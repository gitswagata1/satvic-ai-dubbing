# Final Videos

The two dubbed deliverables (Subah's cloned voice, H.264 1080p, original music bed intact,
exactly 972s to match the source, verified 0 reference-leaks):

| File | Language | Loudness |
|---|---|---|
| `Satvic_Constipation_Telugu.mp4` | Telugu | −14.3 LUFS |
| `Satvic_Constipation_Malayalam.mp4` | Malayalam | −14.2 LUFS |
| `YouTube_Audio_Tracks/*.wav` | 48 kHz stereo tracks for YouTube multi-audio upload | |

> **Where to find the media.** The full-resolution `.mp4` (≈339 MB) and `.wav` tracks
> (≈178 MB) are the canonical deliverables and live in this folder locally / on the shared
> drive — they're too large to commit to git.
>
> The **[GitHub Release](../../releases/latest)** carries watchable copies you can grab
> without cloning:
> - `*_480p.mp4` — full-length watchable video previews of each dub
> - `*_audiotrack.mp3` — the complete dubbed audio (256 kbps) for a full listen
> - `Pitch_Deck.pptx` and `SUBMISSION.pdf`
>
> A 20-second WAV snippet of each dub is also committed under
> [`../4_Audio_Samples/`](../4_Audio_Samples/). To regenerate the full-res videos from
> source, run the pipeline in [`../5_Pipeline_Workspace/`](../5_Pipeline_Workspace/).

**To publish on YouTube:** upload each `_audiotrack.wav` to the existing video via
Studio → Languages → Add language → Dub → Upload. The dubbed track replaces the full mix,
which is why each track already contains the original music bed.
