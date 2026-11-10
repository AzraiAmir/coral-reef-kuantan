import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 02 · DISTRIBUTION</div>', unsafe_allow_html=True)
st.title("Spatial distribution maps")
st.markdown("Geo-referenced coral cover and density across the surveyed reefs. Toggle layers for point density.")

# 1. LOAD GPS DATA FROM SITE SUMMARY
BASE_DIR = Path(__file__).parent
csv_path = BASE_DIR / "data" / "site_summary.csv"

# Assuming you are using pandas:
df = pd.read_csv(csv_path) 

if site_summary_path.exists():
    df_gps = pd.read_csv(site_summary_path)
    
    # If the columns don't exist, show a warning
    if 'Latitude' not in df_gps.columns or 'Longitude' not in df_gps.columns:
        st.warning("Latitude/Longitude columns missing. Please check your CSV file.")
    else:
        # Force to numeric, replacing any text with 0.0
        df_gps['Latitude'] = pd.to_numeric(df_gps['Latitude'], errors='coerce').fillna(0.0)
        df_gps['Longitude'] = pd.to_numeric(df_gps['Longitude'], errors='coerce').fillna(0.0)
        
        # Filter out 0.0 coordinates
        valid_gps = df_gps[(df_gps['Latitude'] != 0.0) & (df_gps['Longitude'] != 0.0)]
        
        if not valid_gps.empty:
            col_map, col_stats = st.columns([2, 1], vertical_alignment="top")
            
            with col_map:
                fig = px.scatter_map(
                    valid_gps, 
                    lat="Latitude", 
                    lon="Longitude", 
                    hover_name=valid_gps.columns[0],
                    zoom=7, 
                    height=520, 
                    color_discrete_sequence=["#00E5FF"]
                )
                
                fig.update_layout(
                    map=dict(
                        style="carto-darkmatter",
                        center=dict(lat=valid_gps["Latitude"].mean(), lon=valid_gps["Longitude"].mean()),
                        zoom=7
                    ),
                    margin=dict(t=10, b=10, l=10, r=10),
                    paper_bgcolor='#111A22'
                )
                
                fig.update_traces(marker=dict(size=16, opacity=0.9))
                chart_card("REEF SITES · GPS LOCATIONS", fig, valid_gps, height=520)
                
            with col_stats:
                st.markdown(f'<div class="panel" style="margin-bottom: 15px; padding: 15px;"><div class="panel-title" style="font-size: 12px;">SITES MAPPED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#00E5FF; font-size: 1.8rem;">{len(valid_gps)}</h2></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="panel" style="margin-bottom: 15px; padding: 15px;"><div class="panel-title" style="font-size: 12px;">LATITUDE RANGE</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FFB74D; font-size: 1.3rem;">{valid_gps["Latitude"].min():.3f}° to {valid_gps["Latitude"].max():.3f}°</h2></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="panel" style="margin-bottom: 15px; padding: 15px;"><div class="panel-title" style="font-size: 12px;">LONGITUDE RANGE</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FF7043; font-size: 1.3rem;">{valid_gps["Longitude"].min():.3f}° to {valid_gps["Longitude"].max():.3f}°</h2></div>', unsafe_allow_html=True)
                st.markdown('<div class="panel" style="padding: 15px; background-color: #1E293B; border: 1px solid #334155;"><div class="panel-title" style="font-size: 12px;">DATA SOURCE</div><p style="color: #94A3B8; font-size: 13px; margin-top: 5px; line-height: 1.4;">GPS dynamically mapped from Uploaded Sites. Sites with (0,0) are hidden.</p></div>', unsafe_allow_html=True)
        else:
            st.info("No valid GPS coordinates found in the CSV. Please update the coordinates in site_summary.csv.")
else:
    st.warning("site_summary.csv not found.")
