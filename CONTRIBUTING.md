# Contributing to Satvic AI Dubbing

Thanks for your interest! This project is an open-source AI dubbing pipeline that translates Hindi audio to Telugu and Malayalam using voice cloning — all at zero cost.

## How to contribute

1. **Fork** this repo and clone your fork
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes and test locally
4. Push and open a **Pull Request**

## Good first issues

Look for issues labeled [`good first issue`](https://github.com/gitswagata1/satvic-ai-dubbing/labels/good%20first%20issue) — these are beginner-friendly tasks.

## Areas where help is needed

- **New language support** — extend the pipeline to additional Indic languages
- **Audio quality improvements** — better denoising, voice cloning fidelity
- **Pipeline optimization** — reduce processing time, memory usage
- **Documentation** — improve setup guides, add architecture diagrams
- **Testing** — add automated tests for pipeline stages

## Tech stack

- **Whisper** — speech-to-text transcription
- **Demucs** — audio source separation
- **IndicF5** — Indic language text-to-speech with voice cloning
- **ffmpeg** — audio/video processing

## Code style

- Use consistent Python formatting (PEP 8)
- Write descriptive commit messages
- Keep PRs focused — one feature or fix per PR
