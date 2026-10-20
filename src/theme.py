# src/theme.py

MOOD_COLORS = {
    "Happy": "#FFD93D",      # Yellow
    "Neutral": "#6BCB77",    # Green
    "Tired": "#4D96FF",      # Blue
    "Surprised": "#FF6B6B",  # Red
    "Sad": "#9B59B6",        # Purple
    "Angry": "#E74C3C"       # Dark Red
}

MOOD_EMOJIS = {
    "Happy": "😊",
    "Neutral": "😐",
    "Tired": "😴",
    "Surprised": "😲",
    "Sad": "😢",
    "Angry": "😠"
}

MOOD_MESSAGES = {
    "Happy": "You're glowing! Keep doing what you're doing.",
    "Neutral": "A calm and steady state. Take a moment to breathe.",
    "Tired": "You seem tired. Maybe it's time for a short break or some water.",
    "Surprised": "Whoa! Something caught your attention.",
    "Sad": "It's okay to feel down. Be kind to yourself today.",
    "Angry": "Take a deep breath. Step away for a minute if you can."
}

def get_mood_theme(mood):
    """
    Returns the color, emoji, and message for a given mood.
    Falls back to Neutral if the mood is not found.
    """
    return {
        "color": MOOD_COLORS.get(mood, "#6BCB77"),
        "emoji": MOOD_EMOJIS.get(mood, "😐"),
        "message": MOOD_MESSAGES.get(mood, "Mood recorded.")
    }