# Demo clip (before / after)

Use **your own voice** or **royalty-free audio** only. The Satvic source video is third-party content and is not included.

1. Record 10–20 s of Hindi speech, e.g. on your phone, and save it as `demo/input_hi.wav`.
2. Write the reviewed Telugu translation into `demo/translation_te.txt`.
3. Run:
   ```bash
   cd 5_Pipeline_Workspace
   python pipeline.py ../demo/input_hi.wav --lang te --translation ../demo/translation_te.txt --out ../demo/output_te
   ```
4. Before = `demo/input_hi.wav`, after = `demo/output_te/dub_te.wav`, timings = `demo/output_te/timings.json`.

Existing "after" samples from the original authorised run: `4_Audio_Samples/FINAL_telugu_first20s.wav`, `FINAL_malayalam_first20s.wav`.
