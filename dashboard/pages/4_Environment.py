import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar

st.set_page_config(page_title="Environment | Azr.AI", page_icon="🌡️", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar("Environment")

st.title("🌡️ Environmental Parameters")
st.markdown("Physicochemical and satellite-derived environmental drivers of coral health.")
st.info("🚧 This page will display time-series charts for SST, salinity, pH, and turbidity.")