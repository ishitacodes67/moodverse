import cv2
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image

from src.detector import detect, annotate
from src.theme import apply_theme

st.set_page_config(page_title="MoodVerse", page_icon="🎭", layout="wide")

if "history" not in st.session_state:   # Day 2: replace with CSV/SQLite
    st.session_state.history = []

st.sidebar.title("⚙️ Settings")
privacy = st.sidebar.checkbox("🔒 Privacy mode (blur face)", value=False)
st.sidebar.caption("Images are processed in memory and never stored.")

st.title("🎭 MoodVerse")
st.caption("An emotion-aware companion that reacts to how you feel.")

source = st.radio("Input", ["📷 Camera", "🖼️ Upload"], horizontal=True)
file = st.camera_input("Take a snapshot") if source.startswith("📷") else \
    st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

mood = "No face"
annotated_rgb = None
if file is not None:
    rgb = np.array(Image.open(file).convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    results = detect(bgr)
    if results:
        top = max(results, key=lambda r: r.box[2] * r.box[3])   # largest face
        mood, conf = top.emotion, top.confidence
        st.session_state.history.append(
            {"time": datetime.now().strftime("%H:%M:%S"), "mood": mood, "confidence": round(conf, 2)})
    annotated_rgb = cv2.cvtColor(annotate(bgr, results, blur=privacy), cv2.COLOR_BGR2RGB)

theme = apply_theme(mood)
col1, col2 = st.columns([3, 2])
with col1:
    if annotated_rgb is not None:
        st.image(annotated_rgb, use_container_width=True)
with col2:
    st.markdown(f"<div class='mood-card'><div class='mood-emoji'>{theme['emoji']}</div>"
                f"<h2>{mood}</h2><p>{theme['msg']}</p></div>", unsafe_allow_html=True)

st.subheader("🕒 Session log")
if st.session_state.history:
    st.dataframe(st.session_state.history[::-1], use_container_width=True)
else:
    st.info("Take a snapshot to start logging your mood.")
