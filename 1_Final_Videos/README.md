# Final Videos

The two dubbed deliverables (Subah's cloned voice, H.264 1080p, original music bed intact,
exactly 972s to match the source, verified 0 reference-leaks):

| File | Language | Loudness |
|---|---|---|
| `Satvic_Constipation_Telugu.mp4` | Telugu | −14.3 LUFS |
| `Satvic_Constipation_Malayalam.mp4` | Malayalam | −14.2 LUFS |
| `YouTube_Audio_Tracks/*.wav` | 48 kHz stereo tracks for YouTube multi-audio upload | |

> **Note:** the `.mp4` / `.wav` files are ~339 MB / ~178 MB each and exceed GitHub's 100 MB
> file limit, so they are **not committed to the repo**. They are delivered alongside this
> repository (shared drive / GitHub Release). A 20-second preview of each dub — with the
> music bed — is committed under [`../4_Audio_Samples/`](../4_Audio_Samples/) as proof.
>
> To regenerate the videos from source, run the pipeline in
> [`../5_Pipeline_Workspace/`](../5_Pipeline_Workspace/) (see its README).

**To publish on YouTube:** upload each `_audiotrack.wav` to the existing video via
Studio → Languages → Add language → Dub → Upload. The dubbed track replaces the full mix,
which is why each track already contains the original music bed.
