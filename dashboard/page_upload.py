import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO
from pathlib import Path
import io
import tempfile
import os

st.markdown('<div class="module-header">MODULE 00 · INGEST</div>', unsafe_allow_html=True)
st.title("Upload & Process")
st.markdown("Ingest raw underwater imagery or video for automated detection and health assessment.")

# Load YOLO Model
@st.cache_resource
def load_model():
    model_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\models\trained\yolov8s_coral\best.pt")
    if model_path.exists():
        return YOLO(str(model_path))
    else:
        st.error(f"Model not found at {model_path}.")
        return None

model = load_model()

with st.container(border=True):
    st.markdown('<div class="panel-title">DATA INGESTION</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Drag and drop coral images or videos here (Max 50MB per file)", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], accept_multiple_files=True)

    with st.expander("⚙️ Pipeline Settings"):
        col1, col2 = st.columns(2)
        with col1: 
            conf_threshold = st.slider("Detection Confidence Threshold", 0.1, 0.9, 0.40, 0.05)
        with col2:
            frame_skip = st.slider("Video Frame Skip (Process 1 frame every X seconds)", 1, 5, 2)
            st.checkbox("Run Health Assessment (Phase D)", value=False, disabled=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Analysis", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one file.")
        elif model is None:
            st.error("Cannot run analysis: Model file missing.")
        else:
            # --- FILE SIZE VALIDATION ---
            MAX_FILE_SIZE_MB = 50
            valid_files = []
            
            for file in uploaded_files:
                # Convert file size to MB
                file_size_mb = file.size / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    st.error(f"❌ File '{file.name}' is too large ({file_size_mb:.1f} MB). Max allowed is {MAX_FILE_SIZE_MB} MB.")
                else:
                    valid_files.append(file)
            
            if not valid_files:
                st.stop() # Stop execution if no valid files remain
            
            # --- PROCESSING LOOP ---
            progress_bar = st.progress(0)
            status_text = st.empty()
            all_results = []
            
            for i, uploaded_file in enumerate(valid_files):
                status_text.text(f"⏳ Processing {uploaded_file.name} ({i+1}/{len(valid_files)})...")
                progress_bar.progress((i + 1) / len(valid_files))
                
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                # IMAGE PROCESSING
                if file_extension in ['jpg', 'jpeg', 'png']:
                    image_bytes = uploaded_file.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    results = model(image, conf=conf_threshold)
                    res = results[0]
                    res_rgb = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
                    
                    for box in res.boxes:
                        cls_id = int(box.cls[0].item())
                        all_results.append({
                            "File": uploaded_file.name,
                            "Type": "Image",
                            "Species": model.names[cls_id],
                            "Confidence": round(float(box.conf[0].item()), 3)
                        })
                    
                    st.markdown(f"**{uploaded_file.name}**")
                    col1, col2 = st.columns(2)
                    col1.image(image, caption="Original", use_container_width=True)
                    col2.image(res_rgb, caption=f"Detected: {len(res.boxes)}", use_container_width=True)

                # VIDEO PROCESSING
                elif file_extension in ['mp4', 'mov', 'avi']:
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}")
                    tfile.write(uploaded_file.read())
                    tfile.close()
                    
                    cap = cv2.VideoCapture(tfile.name)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_jump = int(fps * frame_skip) 
                    
                    frame_count = 0
                    processed_frames = 0
                    video_st_results = []
                    
                    st.markdown(f"**{uploaded_file.name}** (Video)")
                    cols = st.columns(3)
                    
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                            
                        if frame_count % frame_jump == 0:
                            processed_frames += 1
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = model(frame_rgb, conf=conf_threshold)
                            res = results[0]
                            
                            for box in res.boxes:
                                cls_id = int(box.cls[0].item())
                                video_st_results.append({
                                    "File": uploaded_file.name,
                                    "Type": "Video",
                                    "Frame": processed_frames,
                                    "Species": model.names[cls_id],
                                    "Confidence": round(float(box.conf[0].item()), 3)
                                })
                            
                            if processed_frames <= 3:
                                annotated_frame = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
                                with cols[processed_frames - 1]:
                                    st.image(annotated_frame, caption=f"Frame {processed_frames}", use_container_width=True)
                                    
                        frame_count += 1
                        
                    cap.release()
                    os.remove(tfile.name)
                    all_results.extend(video_st_results)
                    st.success(f"Processed {processed_frames} frames from video. Found {len(video_st_results)} instances.")

            status_text.success(f"✅ Successfully processed {len(valid_files)} files!")
            
            if all_results:
                df = pd.DataFrame(all_results)
                st.markdown("### Detection Results")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="▤  Download Results as CSV",
                    data=csv,
                    file_name="yolo_detections.csv",
                    mime="text/csv",
                    use_container_width=True
                )