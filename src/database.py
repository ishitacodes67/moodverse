import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "moodverse.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            mood TEXT NOT NULL,
            confidence REAL,
            latitude REAL,
            longitude REAL
        )
    """)
    conn.commit()
    conn.close()

def log_mood(mood, confidence, lat=None, lon=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO mood_logs (timestamp, mood, confidence, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), mood, confidence, lat, lon)
    )
    conn.commit()
    conn.close()

def get_all_logs():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM mood_logs ORDER BY timestamp ASC", conn)
    conn.close()
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df