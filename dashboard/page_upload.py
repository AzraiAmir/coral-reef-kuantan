import streamlit as st
import time

st.markdown('<div class="module-header">MODULE 00 · INGEST</div>', unsafe_allow_html=True)
st.title("Upload & Process")
st.markdown("Ingest raw underwater imagery for automated detection and health assessment.")

with st.container(border=True):
    st.markdown('<div class="panel-title">DATA INGESTION</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Drag and drop coral images here", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    with st.expander("⚙️ Pipeline Settings"):
        col1, col2 = st.columns(2)
        with col1: st.slider("Detection Confidence Threshold", 0.1, 0.9, 0.40, 0.05)
        with col2:
            st.checkbox("Run Health Assessment (Phase D)", value=True)
            st.checkbox("Run Connectivity Model (Phase E)", value=False)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Analysis", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one image.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for stage_name, progress in [("Ingesting raw data...", 0.2), ("Running YOLOv8...", 0.5), ("Assessing health...", 0.8), ("Complete!", 1.0)]:
                status_text.text(f"⏳ {stage_name}")
                time.sleep(1.5)
                progress_bar.progress(progress)
            status_text.success(f"✅ Successfully processed {len(uploaded_files)} files!")
            st.balloons()