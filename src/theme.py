"""Mood -> colors/emoji/message. Add new moods here only."""
import streamlit as st

MOODS = {
    "Happy":   {"emoji": "😄", "bg": "#2b2a12", "accent": "#FFD43B", "msg": "You're glowing! Great time for a creative task."},
    "Neutral": {"emoji": "😐", "bg": "#14202b", "accent": "#74C0FC", "msg": "Steady and calm. Good time for focused work."},
    "Tired":   {"emoji": "😴", "bg": "#1f1a2e", "accent": "#B197FC", "msg": "You look tired. Consider a 5-minute break."},
    "No face": {"emoji": "🔍", "bg": "#1a1a1a", "accent": "#868E96", "msg": "No face found. Face the camera in good light."},
    "Surprised": {"emoji": "😲", "bg": "#FF6B6B", "accent": "#FFD43B", "msg": "Wow! That's unexpected!"}
}


def apply_theme(mood: str) -> dict:
    m = MOODS.get(mood, MOODS["No face"])
    st.markdown(
        f"""<style>
        .stApp {{ background: {m['bg']}; transition: background 0.6s; }}
        h1, h2, h3 {{ color: {m['accent']} !important; }}
        .mood-card {{ border: 2px solid {m['accent']}; border-radius: 16px;
                      padding: 1rem; text-align: center; }}
        .mood-emoji {{ font-size: 4rem; }}
        </style>""",
        unsafe_allow_html=True,
    )
    return m
