<div align="center">

[![header](https://capsule-render.vercel.app/api?type=waving&color=0:141e30,50:e44d26,100:f7b733&height=200&section=header&text=Satvic%20AI%20Dubbing&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Zero-cost%20AI%20dubbing%20%E2%80%94%20Hindi%20to%20Telugu%20%26%20Malayalam&descAlignY=55&descSize=18&descColor=f0e6d3)](https://github.com/gitswagata1/satvic-ai-dubbing)

**Dub Hindi audio into Telugu and Malayalam in the creator's cloned voice — fully open-source, zero API cost.**

<br/>

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/gitswagata1/satvic-ai-dubbing?style=for-the-badge&color=f7b733)](https://github.com/gitswagata1/satvic-ai-dubbing/stargazers)
[![Forks](https://img.shields.io/github/forks/gitswagata1/satvic-ai-dubbing?style=for-the-badge&color=70a5fd)](https://github.com/gitswagata1/satvic-ai-dubbing/network/members)
[![Issues](https://img.shields.io/github/issues/gitswagata1/satvic-ai-dubbing?style=for-the-badge&color=e44d26)](https://github.com/gitswagata1/satvic-ai-dubbing/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## What is this?

An end-to-end AI dubbing pipeline that takes Hindi video/audio and produces dubbed versions in **Telugu** and **Malayalam** — using the original speaker's cloned voice. Every component is open-source:

| Step | Model / Tool | What it does |
|------|-------------|-------------|
| **Voice separation** | [Demucs](https://github.com/facebookresearch/demucs) | Separates vocals from background music/noise |
| **Transcription** | [OpenAI Whisper](https://github.com/openai/whisper) | Transcribes Hindi speech to text |
| **Translation** | Translation pipeline | Hindi text to Telugu / Malayalam |
| **Voice synthesis** | [IndicF5 TTS](https://github.com/ai4bharat/IndicF5) | Clones the speaker's voice in the target language |
| **Assembly** | [ffmpeg](https://ffmpeg.org/) | Merges dubbed audio back with original background |

**Total API cost: Rs. 0** — everything runs locally on your GPU.

---

## Pipeline Architecture

```
Input Audio/Video
       |
       v
+----------------+
|    Demucs      |---- Background track (preserved)
|   Separation   |
+-------+--------+
        | Vocals only
        v
+----------------+
|    Whisper     |
|  Transcription |
+-------+--------+
        | Hindi text
        v
+----------------+
|  Translation   |
|  Hindi -> TG   |
|  Hindi -> ML   |
+-------+--------+
        | Target language text
        v
+----------------+
|  IndicF5 TTS   |---- Voice cloning from original speaker
|   Synthesis    |
+-------+--------+
        | Dubbed audio
        v
+----------------+
|    ffmpeg      |<--- Background track (from Demucs)
|   Assembly     |
+----------------+
        |
        v
  Final Dubbed Video
```

---

## Project Structure

```
satvic-ai-dubbing/
├── 1_Final_Videos/              # Output dubbed videos
├── 2_Process_and_Reasoning/     # Documentation of the dubbing process
├── 3_Accuracy_Review_Kit/       # QC sheets and reviewer instructions
├── 4_Audio_Samples/             # Sample audio clips for testing
├── 5_Pipeline_Workspace/        # Main pipeline code
│   ├── scripts/                 # Core pipeline scripts
│   │   ├── synth_full.py        # Full synthesis pipeline
│   │   ├── assemble.py          # Audio assembly
│   │   ├── detect_report.py     # Detection and reporting
│   │   ├── fix_leaks.py         # Audio leak fixing
│   │   └── ...
│   ├── requirements.txt         # Python dependencies
│   └── data/                    # Input data
├── Pitch_Deck.pdf               # Project pitch deck
├── SUBMISSION.md                # Detailed submission document
├── Dockerfile                   # Container image
├── Makefile                     # Dev commands
└── LICENSE                      # MIT
```

---

## Quickstart

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended: 8GB+ VRAM)
- ffmpeg installed and on PATH

### Installation

```bash
# Clone the repository
git clone https://github.com/gitswagata1/satvic-ai-dubbing.git
cd satvic-ai-dubbing

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r 5_Pipeline_Workspace/requirements.txt
```

### Run the pipeline

```bash
cd 5_Pipeline_Workspace

# Full synthesis — dub a Hindi audio file to Telugu
python scripts/synth_full.py --input data/input.wav --lang telugu

# Assemble final output with background audio
python scripts/assemble.py --dubbed output/dubbed.wav --bg output/background.wav
```

### Docker

```bash
docker build -t satvic-dubbing .
docker run --gpus all -v $(pwd)/data:/app/data satvic-dubbing
```

---

## Supported Languages

| Source | Target | Status |
|--------|--------|--------|
| Hindi | Telugu | Production |
| Hindi | Malayalam | Production |
| Hindi | Tamil | Planned |
| Hindi | Kannada | Planned |

---

## Quality Assurance

The `3_Accuracy_Review_Kit/` directory contains:
- **Reviewer instructions** for linguistic accuracy checks
- **Review sheets** (CSV) for Telugu and Malayalam output scoring
- **Glossary** of domain-specific terms

---

## Roadmap

- [ ] **Tamil language support** — extend pipeline to Tamil TTS
- [ ] **Batch processing** — dub multiple files in one run
- [ ] **Progress bar** — visual feedback for long dubbing jobs
- [ ] **Web UI** — Gradio/Streamlit interface for non-technical users
- [ ] **Lip sync** — basic visual alignment for video dubbing

See the [open issues](https://github.com/gitswagata1/satvic-ai-dubbing/issues) for community-requested features.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push and open a Pull Request

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Demucs](https://github.com/facebookresearch/demucs) by Meta Research — audio source separation
- [OpenAI Whisper](https://github.com/openai/whisper) — speech recognition
- [IndicF5](https://github.com/ai4bharat/IndicF5) by AI4Bharat — Indic language TTS
- [ffmpeg](https://ffmpeg.org/) — multimedia processing

---

<div align="center">

**Built by [Swagata Banerjee](https://github.com/gitswagata1)**

*Zero-cost AI dubbing for Indian languages.*

[![footer](https://capsule-render.vercel.app/api?type=waving&color=0:f7b733,50:e44d26,100:141e30&height=100&section=footer)](https://github.com/gitswagata1/satvic-ai-dubbing)

</div>
