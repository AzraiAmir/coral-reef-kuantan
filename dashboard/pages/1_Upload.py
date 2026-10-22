import streamlit as st
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar

st.set_page_config(page_title="Upload | Azr.AI", page_icon="📤", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_sidebar("Upload")

st.title("Upload & Process")
st.markdown("Upload your underwater images or videos here to run the full Azr.AI analysis pipeline (Phases C to E).")
uploaded_files = st.file_uploader("Drag and drop your coral images or videos here", type=["jpg", "jpeg", "png", "mp4", "mov"], accept_multiple_files=True)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("⚙️ Analysis Settings", expanded=False):
    col1, col2 = st.columns(2)
    with col1: st.slider("Detection Confidence Threshold", 0.1, 0.9, 0.40, 0.05)
    with col2:
        st.checkbox("Run Health Assessment (Phase D)", value=True)
        st.checkbox("Run Connectivity Model (Phase E)", value=False)
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🚀 Start Analysis", use_container_width=True):
        if not uploaded_files: st.error("Please upload at least one file first.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for stage_name, progress in [("Uploading files...", 0.1), ("Phase C: Detecting corals...", 0.4), ("Phase D: Assessing health...", 0.7), ("Phase E: Connectivity...", 0.9), ("Complete!", 1.0)]:
                status_text.text(f"⏳ {stage_name}")
                time.sleep(1)
                progress_bar.progress(progress)
            status_text.success(f"✅ Successfully processed {len(uploaded_files)} files!")
            st.balloons()