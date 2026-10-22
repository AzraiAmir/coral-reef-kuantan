import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar

st.set_page_config(page_title="Connectivity | Azr.AI", page_icon="🕸️", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar("Connectivity")

st.title("🕸️ Connectivity Modelling")
st.markdown("Source-sink dynamics of coral larvae between MPAs and nearshore reefs.")
st.info("🚧 This page will display the Phase E network graph, connectivity matrix, and Dispersal Potential Index (DPI).")