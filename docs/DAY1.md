# Day 1 – Setup, Detection, Mood-Reactive UI (about 4-5 hours)

Libraries: OpenCV, Streamlit, Pillow, NumPy  |  Manual: Exp 1, 4, 7, 8

## Step 1 – Environment (20 min)
1. Install Python 3.10+ and Git. Check: `python --version`, `git --version`.
2. Unzip `moodverse.zip`, open the folder in VS Code.
3. `python -m venv .venv` then activate it.
4. `pip install -r requirements.txt`

## Step 2 – GitHub repo (15 min)
1. On github.com create an EMPTY repo named `moodverse` (no README, no .gitignore).
2. In the project folder:
```bash
git init
git branch -M main
git add .
git commit -m "chore: initial project skeleton"
git remote add origin https://github.com/<your-username>/moodverse.git
git push -u origin main
```

## Step 3 – Run the app (15 min)
`streamlit run app.py` -> take a snapshot or upload a photo.
Expected: face box, mood label, theme color changes, row added to session log.

## Step 4 – Understand the code (45 min)
- `src/detector.py`: Haar cascade finds face; smile in lower half = Happy; no eyes in upper half = Tired; else Neutral.
- `src/theme.py`: one dict controls emoji, color, message per mood.
- `app.py`: input, detect, annotate, theme, log.
Write 3-4 lines in your own words about each file. You need this for the report and interviews.

## Step 5 – Make it yours (60-90 min) – commit after each
1. Add a 5th mood in `theme.py` (e.g. "Surprised") -> `git commit -m "feat: add surprised mood"`
2. Tune detection in `detector.py` (try smile `minNeighbors` 15-30; test with 5+ photos in different light) -> `git commit -m "tune: smile threshold"`
3. Add your name/college to the sidebar -> `git commit -m "feat: sidebar branding"`
4. Test privacy mode and confirm the face is blurred.

## Step 6 – Tests (15 min)
`pip install pytest` then `python -m pytest -q tests` -> 2 passed.

## Step 7 – Screenshots + push (20 min)
Save 3 screenshots (Happy, Neutral/Tired, privacy mode) in `docs/screens/` (create folder).
```bash
git add .
git commit -m "docs: day 1 screenshots"
git push
```

## Known limits (be honest in your report)
- Haar detection is a heuristic; glasses, dim light, or tilted faces reduce accuracy.
- Only 3 real moods now. Day 2/3 can swap in an ONNX model.

## ✅ Day 1 DONE checklist – message me "Day 1 done" only when ALL are true
- [ ] App runs with `streamlit run app.py`, no errors
- [ ] Face detected; mood label + theme change
- [ ] Privacy mode blurs the face
- [ ] Session log fills up
- [ ] `pytest` shows 2 passed
- [ ] Repo on GitHub with 4+ meaningful commits
- [ ] 3 screenshots saved
- [ ] You can explain detector.py in 1 minute

When done, send: "Day 1 done" + any bug/accuracy problem you noticed. Then I give you Day 2.
