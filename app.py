import streamlit as st
import cv2
import numpy as np
from src.detector import detect

# Try to import theme colors/emojis safely
try:
    from src.theme import MOOD_EMOJIS
except ImportError:
    # Fallback if not found in theme.py
    MOOD_EMOJIS = {"Happy": "😊", "Neutral": "😐", "Tired": "😴", "Surprised": "😲"}

# --- Page Config ---
st.set_page_config(page_title="MoodVerse", page_icon="🎭", layout="wide")

# --- Sidebar ---
st.sidebar.title("MoodVerse 🎭")
st.sidebar.caption("Your Emotion-Aware Companion")
st.sidebar.header("⚙️ Settings")
privacy_mode = st.sidebar.checkbox("🔒 Privacy mode (blur face)", value=False)
st.sidebar.write("Images are processed in memory and never stored.")

# --- Main UI ---
st.title("Mood Detection")
st.write("Take a photo to detect your mood.")

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # 1. Convert Streamlit image to OpenCV format
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # 2. Run detection
    mood, confidence, annotated_img = detect(img_rgb)
    
    # 3. Display results
    if confidence == 0.0:
        st.warning("No face detected. Please try again with better lighting.")
        st.image(img_rgb, channels="RGB")
    else:
        st.success(f"Detected Mood: **{mood}** {MOOD_EMOJIS.get(mood, '')} (Confidence: {confidence:.2f})")
        
        # 4. Handle Privacy Mode
        if privacy_mode:
            # Apply a heavy blur to the whole image
            blurred_img = cv2.GaussianBlur(annotated_img, (99, 99), 30)
            st.image(blurred_img, channels="RGB", caption="Privacy Mode ON (Face Blurred)")
        else:
            st.image(annotated_img, channels="RGB", caption="Annotated Image")
            
        # 5. Session Log
        if "log" not in st.session_state:
            st.session_state.log = []
        
        # Add to log (only if it's a new detection)
        if not st.session_state.log or st.session_state.log[-1]["mood"] != mood:
            st.session_state.log.append({"mood": mood, "confidence": round(confidence, 2)})
        
        st.write("### Session Log")
        st.dataframe(st.session_state.log, use_container_width=True)