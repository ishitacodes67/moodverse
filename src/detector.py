import cv2
import numpy as np
import streamlit as st
from fer.fer import FER

# 1. CACHE THE MODEL: This prevents Streamlit from reloading the heavy AI on every click
@st.cache_resource
def load_model():
    # Using mtcnn=False makes it much lighter and faster for the cloud
    return FER(mtcnn=False)

emotion_detector = load_model()

def detect(image: np.ndarray):
    if image is None:
        return "Neutral", 0.0, None, {}

    if image.dtype != np.uint8:
        image = np.clip(image, 0, 255).astype(np.uint8)

    # 2. DOWNSCALE THE IMAGE: Webcam images are huge. We shrink them to save CPU.
    height, width = image.shape[:2]
    if width > 800:
        scale = 800 / width
        new_dim = (800, int(height * scale))
        image = cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)

    results = emotion_detector.detect_emotions(image)

    if not results:
        return "Neutral", 0.0, image, {}

    face = results[0]
    box = face["box"]
    emotions = face["emotions"]

    raw_mood = max(emotions, key=emotions.get)
    confidence = float(emotions[raw_mood])

    # --- AGGRESSIVE NEUTRAL OVERRIDE ---
    if raw_mood == "neutral":
        sad_score = emotions.get("sad", 0)
        happy_score = emotions.get("happy", 0)
        angry_score = emotions.get("angry", 0)
        
        if happy_score < 0.05 and sad_score > 0.05:
            raw_mood = "sad"
            confidence = float(sad_score)
        elif angry_score > 0.15:
            raw_mood = "angry"
            confidence = float(angry_score)

    mood = raw_mood.capitalize()
    if mood == "Surprise":
        mood = "Surprised"

    annotated_img = annotate(image.copy(), box, mood)
    
    return mood, confidence, annotated_img, emotions

def annotate(img, box, mood):
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, mood, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return img