"""Clip-level dubbing pipeline with per-stage status and timing.

    python pipeline.py <input audio/video> --lang te|ml [--translation file.txt] [--out output/clip]

Stages: normalize (ffmpeg) -> separate (Demucs) -> transcribe (Whisper)
        -> translate (human-in-the-loop text) -> synthesize (IndicF5) -> assemble (ffmpeg)

A stage whose model is not installed is reported as SKIPPED with the reason; nothing
is faked. Every run writes <out>/timings.json and prints a summary table.
Use only audio you own or that is royalty-free (see ../demo/README.md).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class StageResult:
    name: str
    tool: str
    status: str = "pending"  # ok | skipped | failed
    seconds: float = 0.0
    note: str = ""
    outputs: dict = field(default_factory=dict)


def has(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True, text=True)


class Pipeline:
    STAGES = [
        ("normalize", "ffmpeg"),
        ("separate", "Demucs htdemucs"),
        ("transcribe", "Whisper"),
        ("translate", "human-in-the-loop text"),
        ("synthesize", "IndicF5 (AI4Bharat)"),
        ("assemble", "ffmpeg"),
    ]

    def __init__(self, src: Path, lang: str, out: Path, translation: str | None = None,
                 whisper_model: str = "small", on_update=None):
        self.src, self.lang, self.out = src, lang, out
        self.translation = translation
        self.whisper_model = whisper_model
        self.on_update = on_update or (lambda results: None)
        self.results = [StageResult(n, t) for n, t in self.STAGES]
        self.ctx: dict = {}
        out.mkdir(parents=True, exist_ok=True)

    # ---------------- stages ----------------
    def normalize(self, r: StageResult):
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg not on PATH")
        wav = self.out / "input_44k.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(self.src), "-ac", "2", "-ar", "44100", str(wav)])
        self.ctx["input_wav"] = wav
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(wav)], capture_output=True, text=True)
        self.ctx["duration_s"] = float(probe.stdout.strip() or 0)
        r.note = f"{self.ctx['duration_s']:.1f}s audio, 44.1 kHz stereo"
        r.outputs["input"] = str(wav)

    def separate(self, r: StageResult):
        if not has("demucs"):
            return self._skip(r, "demucs not installed (pip install demucs)")
        run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-o", str(self.out / "stems"),
             str(self.ctx["input_wav"])])
        d = next((self.out / "stems").glob("*/input_44k"))
        self.ctx["vocals"], self.ctx["music"] = d / "vocals.wav", d / "no_vocals.wav"
        r.note = "vocals / music bed split"
        r.outputs.update(vocals=str(self.ctx["vocals"]), music=str(self.ctx["music"]))

    def transcribe(self, r: StageResult):
        if not has("whisper"):
            return self._skip(r, "openai-whisper not installed")
        import whisper
        model = whisper.load_model(self.whisper_model)
        audio = str(self.ctx.get("vocals", self.ctx["input_wav"]))
        res = model.transcribe(audio, language="hi")
        self.ctx["transcript"] = res["text"].strip()
        self.ctx["segments"] = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                                for s in res["segments"]]
        (self.out / "transcript_hi.json").write_text(json.dumps(self.ctx["segments"], ensure_ascii=False, indent=1))
        r.note = f"{len(self.ctx['segments'])} segments, model={self.whisper_model}"
        r.outputs["transcript"] = self.ctx["transcript"]

    def translate(self, r: StageResult):
        # The original project translated with an LLM under a glossary, then native review.
        # For a new clip we take the reviewed target-language text as input.
        if not self.translation:
            return self._skip(r, "no target-language text supplied (paste reviewed translation)")
        self.ctx["target_text"] = self.translation.strip()
        r.note = f"{len(self.ctx['target_text'])} chars of {self.lang} text"

    def synthesize(self, r: StageResult):
        if "target_text" not in self.ctx:
            return self._skip(r, "needs translated text")
        if not (has("transformers") and has("f5_tts")):
            return self._skip(r, "IndicF5 not installed (gated HF model ai4bharat/IndicF5)")
        if "transcript" not in self.ctx:
            return self._skip(r, "needs Whisper transcript for the voice reference text")
        import numpy as np
        import soundfile as sf
        from transformers import AutoModel
        ref = self.out / "ref_8s.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(self.ctx.get("vocals", self.ctx["input_wav"])),
             "-t", "8", "-ac", "1", "-ar", "24000", str(ref)])
        ref_text = self.ctx["segments"][0]["text"] if self.ctx.get("segments") else self.ctx["transcript"]
        model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
        a = np.asarray(model(self.ctx["target_text"], ref_audio_path=str(ref), ref_text=ref_text), dtype=np.float32)
        if np.abs(a).max() > 1.5:
            a = a / 32768.0
        speech = self.out / f"speech_{self.lang}.wav"
        sf.write(speech, a, 24000)
        self.ctx["speech"] = speech
        r.note = f"voice-cloned {len(a) / 24000:.1f}s of speech"
        r.outputs["speech"] = str(speech)

    def assemble(self, r: StageResult):
        if "speech" not in self.ctx:
            return self._skip(r, "no synthesized speech to assemble")
        final = self.out / f"dub_{self.lang}.wav"
        if "music" in self.ctx:
            run(["ffmpeg", "-y", "-v", "error", "-i", str(self.ctx["speech"]), "-i", str(self.ctx["music"]),
                 "-filter_complex", "[0:a]aresample=44100,volume=1.0[s];[1:a]volume=0.8[m];[s][m]amix=inputs=2:duration=longest",
                 str(final)])
            r.note = "speech + original music bed"
        else:
            run(["ffmpeg", "-y", "-v", "error", "-i", str(self.ctx["speech"]), "-ar", "44100", str(final)])
            r.note = "speech only (no music stem)"
        r.outputs["final"] = str(final)

    # ---------------- runner ----------------
    def _skip(self, r: StageResult, why: str):
        r.status, r.note = "skipped", why
        return "skipped"

    def run_all(self) -> list[StageResult]:
        for r in self.results:
            r.status = "running"
            self.on_update(self.results)
            t0 = time.perf_counter()
            try:
                if getattr(self, r.name)(r) != "skipped":
                    r.status = "ok"
            except Exception as e:  # noqa: BLE001 - report any stage failure
                r.status, r.note = "failed", f"{type(e).__name__}: {e}"[:300]
            r.seconds = round(time.perf_counter() - t0, 2)
            self.on_update(self.results)
            if r.status == "failed":
                break
        (self.out / "timings.json").write_text(json.dumps(
            {"input": str(self.src), "lang": self.lang, "stages": [asdict(x) for x in self.results]},
            ensure_ascii=False, indent=2))
        return self.results


def summary_table(results: list[StageResult]) -> str:
    rows = [f"{'stage':<11} {'tool':<24} {'status':<8} {'time (s)':>8}  note", "-" * 78]
    rows += [f"{r.name:<11} {r.tool:<24} {r.status:<8} {r.seconds:>8.2f}  {r.note}" for r in results]
    rows += ["-" * 78, f"{'total':<11} {'':<24} {'':<8} {sum(r.seconds for r in results):>8.2f}"]
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("--lang", choices=["te", "ml"], required=True)
    ap.add_argument("--translation", help="path to a UTF-8 text file with the reviewed translation")
    ap.add_argument("--out", type=Path, default=Path("output/clip"))
    ap.add_argument("--whisper-model", default="small")
    a = ap.parse_args()
    text = Path(a.translation).read_text(encoding="utf-8") if a.translation else None
    res = Pipeline(a.input, a.lang, a.out, text, a.whisper_model).run_all()
    print(summary_table(res))
    print(f"\ntimings written to {a.out / 'timings.json'}")


if __name__ == "__main__":
    main()
