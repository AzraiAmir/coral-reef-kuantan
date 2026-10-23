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
        
        st.write("<br>**Reef Sites Health Summary (with KBI & D_to_White)**", unsafe_allow_html=True)
        csv_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\site_summary.csv")
        if csv_path.exists():
            with open(csv_path, "rb") as f:
                st.download_button(label="Download Site Summary CSV", data=f, file_name="site_summary.csv", mime="text/csv", key="dl1", use_container_width=True)
        else:
            st.error("site_summary.csv not found.")
            
        st.markdown("---")
        
        st.write("**Connectivity Matrix**")
        conn_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\connectivity_matrix.csv")
        if conn_path.exists():
            with open(conn_path, "rb") as f:
                st.download_button(label="Download Connectivity CSV", data=f, file_name="connectivity_matrix.csv", mime="text/csv", key="dl2", use_container_width=True)
        else:
            st.error("connectivity_matrix.csv not found.")

with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">RAW UPLOADED DETECTIONS</div>', unsafe_allow_html=True)
        
        st.write("<br>**Latest YOLO Upload Results**", unsafe_allow_html=True)
        # This file is generated when users upload images on Page 2
        upload_csv = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\uploaded_detections.csv")
        if upload_csv.exists():
            with open(upload_csv, "rb") as f:
                st.download_button(label="Download Raw Detections CSV", data=f, file_name="uploaded_detections.csv", mime="text/csv", key="dl3", use_container_width=True)
        else:
            st.info("No new uploads detected yet. Upload images on the 'Upload & Process' page first.")
            
        st.markdown("---")
        
        st.write("**GeoTIFF Rasters**")
        st.info("🚧 Raster exports will be available once GPS coordinates are fully integrated.")