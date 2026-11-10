import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path
from utils import chart_card # Assuming you use this for charts

st.markdown('<div class="module-header">MODULE 02 · DISTRIBUTION</div>', unsafe_allow_html=True)
st.title("Spatial distribution maps")
st.markdown("Geo-referenced coral cover and density across the surveyed reefs. Toggle layers for point density.")

# --- 1. DEFINE PATHS & LOAD DATA ---
BASE_DIR = Path(__file__).parent
site_summary_path = BASE_DIR / "data" / "site_summary.csv"

if site_summary_path.exists():
    df = pd.read_csv(site_summary_path)
    
    # Example Map Generation (Adjust to your actual map code)
    m = folium.Map(location=[3.0, 103.0], zoom_start=7) # Roughly Kuantan/Tioman area
    
    for idx, row in df.iterrows():
        # Assuming your CSV has 'lat', 'lon', and 'site_name' columns
        if 'lat' in row and 'lon' in row:
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=5,
                color='#00E5FF',
                fill=True,
                popup=row.get('site_name', 'Reef Site')
            ).add_to(m)
            
    st_folium(m, use_container_width=True, height=500)
else:
    st.error("site_summary.csv not found in the data folder.")
