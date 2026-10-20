import folium
import pandas as pd

def create_map(df, default_location=(19.8762, 75.3433)):
    located = df.dropna(subset=["latitude", "longitude"]) if not df.empty else pd.DataFrame()
    center = (located["latitude"].mean(), located["longitude"].mean()) if not located.empty else default_location
    
    m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")
    
    for _, row in located.iterrows():
        folium.Marker(
            location=(row["latitude"], row["longitude"]),
            popup=f"{row['mood']} ({row['timestamp'].strftime('%Y-%m-%d %H:%M')})",
            icon=folium.Icon(color="green" if row["mood"] in ["Happy", "Surprised"] else "blue")
        ).add_to(m)
    return m