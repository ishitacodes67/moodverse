import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

MOOD_SCORES = {"Happy": 5, "Surprised": 4, "Neutral": 3, "Tired": 2, "Sad": 1, "Angry": 1}
MOOD_COLORS = {"Happy": "#FFD93D", "Neutral": "#6BCB77", "Tired": "#4D96FF", "Surprised": "#FF6B6B"}

def create_timeline(df):
    if df.empty or len(df) < 2: return None
    df["score"] = df["mood"].map(MOOD_SCORES).fillna(3)
    fig = px.line(df, x="timestamp", y="score", markers=True, text="mood",
                  title="Your Mood Journey", color_discrete_sequence=["#6BCB77"])
    fig.update_traces(textposition="top center", marker=dict(size=10, color=[MOOD_COLORS.get(m, "#888") for m in df["mood"]]))
    fig.update_layout(yaxis=dict(tickvals=[1,2,3,4,5], ticktext=["Low", "Tired", "Neutral", "Good", "Great"]))
    return fig

def create_heatmap(df):
    if df.empty or len(df) < 3: return None
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day_name()
    df["score"] = df["mood"].map(MOOD_SCORES).fillna(3)
    
    df["time_of_day"] = pd.cut(df["hour"], bins=[0, 6, 12, 18, 24], 
                               labels=["Night", "Morning", "Afternoon", "Evening"], include_lowest=True)
    
    pivot = df.pivot_table(values="score", index="day", columns="time_of_day", aggfunc="mean")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn", vmin=1, vmax=5, ax=ax)
    ax.set_title("Mood by Day & Time")
    ax.set_ylabel("")
    ax.set_xlabel("")
    return fig