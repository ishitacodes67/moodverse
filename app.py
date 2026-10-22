import streamlit as st
import cv2
import numpy as np
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

from src.detector import detect
from src.theme import MOOD_EMOJIS
from src.database import init_db, log_mood, get_all_logs
from src.analytics import create_timeline, create_heatmap
from src.map_view import create_map
from src.features import get_suggestion, generate_voice, create_mood_card

# Init DB on start
init_db()

st.set_page_config(page_title="MoodVerse", page_icon="🎭", layout="wide")

# Sidebar
st.sidebar.title("MoodVerse 🎭")
st.sidebar.caption("Your Emotion-Aware Companion")
privacy_mode = st.sidebar.checkbox("🔒 Privacy mode (blur face)", value=False)

# Tabs
tab1, tab2, tab3 = st.tabs(["📸 Detect Mood", "📊 Analytics", "🗺️ Mood Map"])

with tab1:
    st.header("Detect Your Mood")
    
    # Tabs to switch between Live Webcam and File Upload
    input_method = st.radio("Choose Input Method:", ["Webcam", "Upload Image"], horizontal=True)
    
    img_file_buffer = None
    if input_method == "Webcam":
        img_file_buffer = st.camera_input("Take a picture")
    else:
        img_file_buffer = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        # OPTIMIZATION: Resize the image before passing it to the AI to save RAM/CPU
        img_rgb = cv2.resize(img_rgb, (400, int(400 * img_rgb.shape[0] / img_rgb.shape[1])))

        # The FER detector (now returns 4 variables)
        mood, confidence, annotated_img, raw_emotions = detect(img_rgb)
        
        if confidence == 0.0:
            st.warning("No face detected. Please try again with better lighting.")
        else:
            st.success(f"Detected Mood: **{mood}** {MOOD_EMOJIS.get(mood, '')} (Confidence: {confidence:.2f})")
            
            # AI Debug Panel (Placed correctly inside the else block)
            with st.expander("🧠 AI Brain Debug Info"):
                st.write("Here is exactly what the neural network is seeing:")
                st.json(raw_emotions)
            
            # 1. Smart Suggestion
            suggestion = get_suggestion(mood)
            st.info(f"💡 **Smart Suggestion:** {suggestion}")
            
            # 2. Voice Companion
            if st.button("🔊 Listen to Companion"):
                with st.spinner("Generating voice..."):
                    audio = generate_voice(f"I see you are feeling {mood}. {suggestion}")
                    if audio:
                        st.audio(audio, format="audio/mp3")
            
            # Location (Optional for the map)
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude (optional)", value=19.8762, format="%.4f")
            with col2:
                lon = st.number_input("Longitude (optional)", value=75.3433, format="%.4f")
            
            # Log Button
            if st.button("💾 Save Mood to Database"):
                log_mood(mood, confidence, lat, lon)
                st.success("Mood saved successfully! Check the Analytics and Map tabs.")

            st.divider()
            
            # 3. Mood Card Generator & Image Display
            col_img, col_card = st.columns(2)
            
            with col_img:
                st.subheader("Your Photo")
                if privacy_mode:
                    blurred_img = cv2.GaussianBlur(annotated_img, (99, 99), 30)
                    st.image(blurred_img, channels="RGB", caption="Privacy Mode ON")
                else:
                    st.image(annotated_img, channels="RGB")
                    
            with col_card:
                st.subheader("🎨 Mood Card")
                mood_card = create_mood_card(annotated_img, mood)
                if mood_card:
                    st.image(mood_card, caption="Right-click and 'Save image as...' to share!")

with tab2:
    st.header("📊 Your Mood Analytics")
    df = get_all_logs()
    
    if df.empty:
        st.info("No data yet. Log some moods in the Detect tab!")
    else:
        st.subheader("Mood Timeline")
        timeline_fig = create_timeline(df)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
        else:
            st.write("Need more data for a timeline.")
            
        st.subheader("When are you happiest?")
        heatmap_fig = create_heatmap(df)
        if heatmap_fig:
            st.pyplot(heatmap_fig)
        else:
            st.write("Need at least 3 logs for a heatmap.")

with tab3:
    st.header("🗺️ Where do you feel this way?")
    df = get_all_logs()
    if not df.empty and "latitude" in df.columns:
        mood_map = create_map(df)
        st_folium(mood_map, width=800, height=500)
    else:
        st.info("Log some moods with location data to see the map!")