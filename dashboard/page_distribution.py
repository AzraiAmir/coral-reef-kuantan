import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 02 · DISTRIBUTION</div>', unsafe_allow_html=True)
st.title("Spatial distribution maps")
st.markdown("Geo-referenced coral cover and density across the surveyed reefs. Toggle layers for point density.")

# 1. LOAD GPS DATA
gps_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\gps_coordinates.csv")

if gps_path.exists():
    df_gps = pd.read_csv(gps_path)
    
    if not df_gps.empty:
        col_map, col_stats = st.columns([2, 1], vertical_alignment="top")
        
        with col_map:
            fig = px.scatter_map(
                df_gps, 
                lat="latitude", 
                lon="longitude", 
                hover_name="image_name",
                zoom=7, 
                height=360, # REDUCED HEIGHT TO PREVENT SCROLLBAR
                color_discrete_sequence=["#00E5FF"]
            )
            
            fig.update_layout(
                map=dict(
                    style="carto-darkmatter",
                    center=dict(lat=df_gps["latitude"].mean(), lon=df_gps["longitude"].mean()),
                    zoom=7
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='#111A22'
            )
            
            fig.update_traces(marker=dict(size=16, opacity=0.9))
            chart_card("REEF SITES · GPS LOCATIONS", fig, df_gps)
            
        with col_stats:
            # 1. Sites Mapped
            st.markdown(f'<div class="panel" style="margin-bottom: 10px; padding: 15px;"><div class="panel-title" style="font-size: 11px;">SITES MAPPED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#00E5FF; font-size: 1.8rem;">{len(df_gps)}</h2></div>', unsafe_allow_html=True)
            
            # 2. Latitude
            st.markdown(f'<div class="panel" style="margin-bottom: 10px; padding: 15px;"><div class="panel-title" style="font-size: 11px;">LATITUDE RANGE</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FFB74D; font-size: 1.3rem;">{df_gps["latitude"].min():.3f}° to {df_gps["latitude"].max():.3f}°</h2></div>', unsafe_allow_html=True)
            
            # 3. Longitude
            st.markdown(f'<div class="panel" style="margin-bottom: 10px; padding: 15px;"><div class="panel-title" style="font-size: 11px;">LONGITUDE RANGE</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FF7043; font-size: 1.3rem;">{df_gps["longitude"].min():.3f}° to {df_gps["longitude"].max():.3f}°</h2></div>', unsafe_allow_html=True)
            
            # 4. Data Source (Padding removed to keep it compact)
            st.markdown('<div class="panel" style="padding: 15px; background-color: #1E293B; border: 1px solid #334155;"><div class="panel-title" style="font-size: 11px;">DATA SOURCE</div><p style="color: #94A3B8; font-size: 13px; margin-top: 5px; line-height: 1.4;">GPS EXIF extracted from raw imagery. Map centered on Pahang Coastal Region.</p></div>', unsafe_allow_html=True)

    else:
        st.warning("The GPS CSV exists but contains no data.")
else:
    st.warning("No GPS data found. Please run the EXIF extraction script first.")