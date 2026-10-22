import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar

st.set_page_config(page_title="Distribution | Azr.AI", page_icon="🗺️", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar("Distribution")

st.title("🗺️ Distribution Maps")
st.markdown("Spatial distribution of coral species across the Kuantan coastal waters.")
st.info("🚧 This page will display interactive choropleth maps and heatmaps generated from Phase C detection data.")