import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown('<div class="module-header">MODULE 07 · EXPORT</div>', unsafe_allow_html=True)
st.title("Data export portal")
st.markdown("Pull curated tabular datasets as CSV or request georeferenced rasters as GeoTIFF for GIS workflows.")

col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">CSV DATASETS</div>', unsafe_allow_html=True)
        st.write("<br>**Reef sites index**", unsafe_allow_html=True)
        try:
            csv_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\site_summary.csv")
            with open(csv_path, "rb") as f:
                st.download_button(label="Download CSV", data=f, file_name="site_summary.csv", mime="text/csv", key="dl1")
        except FileNotFoundError:
            st.error("File not found.")
            
        st.markdown("---")
        st.write("**Connectivity matrix**")
        try:
            conn_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\connectivity_matrix.csv")
            with open(conn_path, "rb") as f:
                st.download_button(label="Download CSV", data=f, file_name="connectivity_matrix.csv", mime="text/csv", key="dl2")
        except FileNotFoundError:
            st.error("File not found.")

with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">GEOTIFF RASTERS</div>', unsafe_allow_html=True)
        st.write("<br>Georeferenced imagery for GIS", unsafe_allow_html=True)
        st.info("🚧 Raster exports will be available once GPS coordinates are integrated into Phase C/D.")