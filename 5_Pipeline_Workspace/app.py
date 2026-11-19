"""Minimal UI for the dubbing pipeline.  Run:  streamlit run app.py"""

import json
import tempfile
from pathlib import Path

import streamlit as st

from pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT.parent / "4_Audio_Samples"
LANGS = {"Telugu": "te", "Malayalam": "ml"}
ICON = {"pending": "⏳", "running": "🔄", "ok": "✅", "skipped": "⏭️", "failed": "❌"}

st.set_page_config(page_title="AI Dubbing Pipeline", page_icon="🎙️", layout="wide")
st.title("🎙️ Hindi → Telugu / Malayalam AI dubbing")
st.caption("Demucs → Whisper → translation (human-reviewed) → IndicF5 voice clone → ffmpeg · runs locally, ₹0 API cost")

run_tab, prev_tab = st.tabs(["▶ Run on a clip", "📼 Previous full run (Satvic assignment)"])

with run_tab:
    st.info("Use only audio you own (e.g. your own voice) or royalty-free audio. "
            "Stages whose models are not installed are shown as skipped, never faked.")
    c1, c2 = st.columns([2, 1])
    up = c1.file_uploader("Hindi audio or video clip (≤ 30 s recommended)", type=["wav", "mp3", "m4a", "mp4", "mov"])
    lang_name = c2.radio("Target language", list(LANGS))
    whisper_model = c2.selectbox("Whisper model", ["tiny", "base", "small", "medium"], index=2)
    translation = st.text_area(f"Reviewed {lang_name} text for this clip (translation step is human-in-the-loop)",
                               height=90, placeholder="Paste the reviewed translation here")

    if st.button("Run pipeline", type="primary", disabled=up is None):
        tmp = Path(tempfile.mkdtemp())
        src = tmp / up.name
        src.write_bytes(up.getvalue())
        st.audio(str(src))
        board = st.empty()

        def paint(results):
            rows = [{"": ICON[r.status], "stage": r.name, "tool": r.tool, "status": r.status,
                     "time (s)": f"{r.seconds:.2f}" if r.status not in ("pending", "running") else "",
                     "note": r.note} for r in results]
            board.dataframe(rows, hide_index=True, use_container_width=True)

        pipe = Pipeline(src, LANGS[lang_name], tmp / "out", translation or None, whisper_model, on_update=paint)
        results = pipe.run_all()
        total = sum(r.seconds for r in results)
        st.metric("Total pipeline time", f"{total:.1f} s")
        if pipe.ctx.get("transcript"):
            st.subheader("Whisper transcript (Hindi)")
            st.write(pipe.ctx["transcript"])
        final = next((r.outputs.get("final") for r in results if r.outputs.get("final")), None)
        if final:
            st.subheader(f"Dubbed output · {lang_name}")
            st.audio(final)
        st.download_button("Download timings.json", (tmp / "out" / "timings.json").read_bytes(),
                           file_name="timings.json")

with prev_tab:
    st.markdown(
        "Outputs from the full 16-minute run made for Satvic Movement's assignment "
        "(see `SUBMISSION.md`): **230 segments per language**, **0 reference-leaks across 460 segments** "
        "(language-ID scan), CPU synthesis ≈ **2 h per video-language on a MacBook** (`PROCESS.md`).")
    c1, c2 = st.columns(2)
    for col, (name, f) in zip((c1, c2), [("Telugu", "FINAL_telugu_first20s.wav"), ("Malayalam", "FINAL_malayalam_first20s.wav")]):
        col.subheader(f"After · {name} (first 20 s, music bed kept)")
        p = SAMPLES / f
        if p.exists():
            col.audio(str(p))
        else:
            col.warning(f"{f} not found")
    st.caption("The original Hindi source video belongs to Satvic Movement and is not redistributed here.")

    lang = LANGS[st.radio("Show segments for", list(LANGS), horizontal=True, key="seg_lang")]
    segs = json.loads((ROOT / "data" / f"segments_{lang}.json").read_text(encoding="utf-8"))
    st.subheader("Segment table: Hindi → target → back-translation (first 12 of 230)")
    st.dataframe([{"t (s)": f"{s['start']:.1f}–{s['end']:.1f}", "Hindi": s.get("hi_clean", ""),
                   "target": s.get(lang, ""), "back-translation": s.get("bt", ""), "flag": s.get("flag", "")}
                  for s in segs[:12]], hide_index=True, use_container_width=True)
