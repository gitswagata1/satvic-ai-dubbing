#!/bin/bash
# finalize a language end-to-end: trim residual leaks -> verify -> assemble -> transcode deliverable
set -e
LANG=$1          # te | ml
NAME=$2          # Telugu | Malayalam
cd "$(dirname "$0")/.."

echo "[$LANG] 1/4 trimming any residual reference-echo leaks..."
.venv/bin/python scripts/leak_trim.py "$LANG"

echo "[$LANG] 2/4 independent verification scan..."
.venv/bin/python scripts/detect_report.py "$LANG" 2>/dev/null | tail -2

echo "[$LANG] 3/4 assembling (fit timing + music bed + mux)..."
.venv/bin/python scripts/assemble.py "$LANG" | tail -2

echo "[$LANG] 4/4 transcoding H.264 deliverable..."
ffmpeg -y -v error -i "output/dub_${LANG}.mp4" -c:v libx264 -preset medium -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k "../1_Final_Videos/Satvic_Constipation_${NAME}.mp4"
cp "output/dub_${LANG}_track.wav" "../1_Final_Videos/YouTube_Audio_Tracks/Satvic_Constipation_${NAME}_audiotrack.wav"
echo "[$LANG] DONE -> ../1_Final_Videos/Satvic_Constipation_${NAME}.mp4"
