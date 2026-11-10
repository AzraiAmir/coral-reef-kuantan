import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown('<div class="module-header">MODULE 07 · EXPORT</div>', unsafe_allow_html=True)
st.title("Data export portal")
st.markdown("Pull curated tabular datasets as CSV or request georeferenced rasters as GeoTIFF for GIS workflows.")

# --- DEFINE PATHS ---
BASE_DIR = Path(__file__).parent
summary_path = BASE_DIR / "data" / "site_summary.csv"
matrix_path = BASE_DIR / "data" / "connectivity_matrix.csv"

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### CSV DATASETS")
        
        # 1. Site Summary
        st.markdown("**Reef Sites Health Summary (with KBI & D_to_White)**")
        if summary_path.exists():
            with open(summary_path, "rb") as file:
                st.download_button(
                    label="Download site_summary.csv",
                    data=file,
                    file_name="site_summary.csv",
                    mime="text/csv"
                )
        else:
            st.error("site_summary.csv not found in data folder.")
            
        st.markdown("---")
        
        # 2. Connectivity Matrix
        st.markdown("**Connectivity Matrix**")
        if matrix_path.exists():
            with open(matrix_path, "rb") as file:
                st.download_button(
                    label="Download connectivity_matrix.csv",
                    data=file,
                    file_name="connectivity_matrix.csv",
                    mime="text/csv"
                )
        else:
            st.error("connectivity_matrix.csv not found in data folder.")

with col2:
    with st.container(border=True):
        st.markdown("#### RAW UPLOADED DETECTIONS")
        st.info("No new uploads detected yet.")
        
        st.markdown("---")
        
        st.markdown("#### GeoTIFF Rasters")
        st.info("Raster exports will be available once GPS coordinates are fully integrated.")
