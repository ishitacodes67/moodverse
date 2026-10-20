# 🎭 MoodVerse
An emotion-aware companion built with Python: it detects your mood from a snapshot and reacts with a mood-themed UI, voice, charts, maps and art.

> Status: **Day 1 of 4** – detection + mood-reactive UI.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Roadmap
- [x] Day 1: Detection, mood-reactive UI, privacy mode, session log
- [ ] Day 2: Persistent logging, Plotly timeline, Seaborn heatmap, Folium mood map
- [ ] Day 3: Voice (gTTS), mood card (Pillow), generative art (Matplotlib), badges
- [ ] Day 4: Deploy, README GIF, report

## Privacy
Images are processed in memory and never saved. Privacy mode blurs faces.
Emotion output is a heuristic estimate, not a medical or psychological assessment.
