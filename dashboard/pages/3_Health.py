import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar

st.set_page_config(page_title="Health | Azr.AI", page_icon="🩺", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar("Health")

st.title("🩺 Health Assessment")
st.markdown("Quantitative coral bleaching severity (KBI) and disease prevalence.")
st.info("🚧 This page will display the Phase D health metrics, including KBI heatmaps and D_toWhite scatter plots.")