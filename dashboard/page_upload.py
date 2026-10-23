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
import time
import json
from geopy.geocoders import Nominatim

st.markdown('<div class="module-header">MODULE 00 · INGEST</div>', unsafe_allow_html=True)
st.title("Upload & Process")
st.markdown("Ingest raw underwater imagery or video for automated detection and health assessment.")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    [data-testid="stFileUploader"] button svg { fill: #00E5FF !important; stroke: #00E5FF !important; }
    [data-testid="stFileUploader"] section { background-color: #1E293B !important; border: 1px dashed #334155 !important; }
    div.stButton > button { color: #00E5FF !important; border: 1px solid #334155 !important; background-color: #1E293B !important; }
    div.stButton > button:hover { color: #FFFFFF !important; border-color: #00E5FF !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\models\trained\yolov8s_coral\best.pt")
    if model_path.exists():
        return YOLO(str(model_path))
    else:
        st.error(f"Model not found at {model_path}.")
        return None

model = load_model()

def apply_enhancement(img):
    if img is None or img.size == 0: return img
    b, g, r = cv2.split(img)
    r_comp = cv2.add(r, 50) 
    r_comp = np.clip(r_comp, 0, 255).astype(np.uint8)
    b_mean, g_mean, r_mean = np.mean(b), np.mean(g), np.mean(r_comp)
    avg = (b_mean + g_mean + r_mean) / 3
    b = cv2.add(b, (avg - b_mean) * 0.5)
    g = cv2.add(g, (avg - g_mean) * 0.5)
    r_comp = cv2.add(r_comp, (avg - r_mean) * 0.5)
    balanced_img = cv2.merge([np.clip(b, 0, 255).astype(np.uint8), np.clip(g, 0, 255).astype(np.uint8), r_comp])
    lab = cv2.cvtColor(balanced_img, cv2.COLOR_BGR2LAB)
    l, a, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced_lab = cv2.merge([l, a, b_channel])
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

def analyze_coral_health(cropped_img):
    if cropped_img is None or cropped_img.size == 0: return None
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    mean_v = hsv[:, :, 2].mean()
    paleness = mean_v / 255.0 
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    if gray.max() > 0:
        thresh = np.percentile(gray, 95)
        bright_mask = gray >= thresh
        white_ref_bgr = cropped_img[bright_mask].mean(axis=0)
        coral_lab = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2LAB)
        white_lab = cv2.cvtColor(np.uint8([[white_ref_bgr]]), cv2.COLOR_BGR2LAB)[0][0]
        dists = np.linalg.norm(coral_lab.astype(float) - white_lab.astype(float), axis=2)
        mean_dwhite = dists.mean()
    else:
        mean_dwhite = 0.0
    return {"mean_paleness": round(paleness, 4), "mean_d_to_white": round(mean_dwhite, 2)}

with st.container(border=True):
    st.markdown('<div class="panel-title">DATA INGESTION</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Drag and drop coral images or videos here (Max 50MB per file)", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], accept_multiple_files=True)

    with st.expander("⚙️ Pipeline Settings"):
        col1, col2 = st.columns(2)
        with col1: 
            conf_threshold = st.slider("Detection Confidence Threshold", 0.1, 0.9, 0.60, 0.05)
        with col2:
            enable_enhancement = st.checkbox("Enable Phase B Enhancement (RCC + CLAHE)", value=True)
            
    st.markdown("### Site Information")
    col_site, col_lat, col_lon = st.columns(3)
    
    with col_site:
        site_name = st.text_input("Enter Site Name (Compulsory)", placeholder="e.g., Pulau Tioman")
        
    if site_name:
        if f"geo_{site_name}" not in st.session_state:
            try:
                geolocator = Nominatim(user_agent="azrai_coral_app")
                location = geolocator.geocode(site_name + ", Malaysia", timeout=5)
                if location:
                    st.session_state[f"geo_{site_name}"] = (location.latitude, location.longitude)
                else:
                    st.session_state[f"geo_{site_name}"] = (0.0, 0.0)
            except Exception:
                st.session_state[f"geo_{site_name}"] = (0.0, 0.0)

    default_lat, default_lon = st.session_state.get(f"geo_{site_name}", (0.0, 0.0))

    with col_lat:
        lat = st.number_input("Latitude (Auto-filled)", value=float(default_lat), format="%.5f")
    with col_lon:
        lon = st.number_input("Longitude (Auto-filled)", value=float(default_lon), format="%.5f")

    if lat != 0.0 and lon != 0.0:
        st.markdown(f"**Preview Location:** Lat {lat}, Lon {lon}")
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data, zoom=10, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("▶&nbsp;&nbsp;&nbsp;&nbsp;Start Analysis", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one file.")
        elif not site_name:
            st.error("Site Name is compulsory. Please enter a location name.")
        elif model is None:
            st.error("Cannot run analysis: Model file missing.")
        else:
            MAX_FILE_SIZE_MB = 50
            valid_files = [f for f in uploaded_files if (f.size / (1024 * 1024)) <= MAX_FILE_SIZE_MB]
            if not valid_files: st.stop()
            
            all_results = []
            total_files = len(valid_files)
            
            main_progress = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(valid_files):
                status_text.markdown(f"**📁 Processing File {i+1}/{total_files}:** `{uploaded_file.name}`")
                
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension in ['jpg', 'jpeg', 'png']:
                    image_bytes = uploaded_file.read()
                    image_pil = Image.open(io.BytesIO(image_bytes))
                    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
                    
                    if enable_enhancement:
                        status_text.markdown(f"**🟡 Phase B:** Enhancing image (RCC + CLAHE)...", help="Phase B improves murky underwater images.")
                        time.sleep(0.3)
                        image_to_detect = apply_enhancement(image_cv)
                    else:
                        image_to_detect = image_cv
                        
                    status_text.markdown(f"**🔵 Phase C:** Running YOLOv8 detection...", help="Phase C uses Deep Learning to find coral species.")
                    time.sleep(0.3)
                    results = model(image_to_detect, conf=conf_threshold)
                    res = results[0]
                    res_rgb = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
                    
                    st.markdown(f"**{uploaded_file.name}**")
                    if enable_enhancement:
                        c1, c2, c3 = st.columns(3)
                        c1.image(image_pil, caption="Original", use_container_width=True)
                        c2.image(cv2.cvtColor(image_to_detect, cv2.COLOR_BGR2RGB), caption="Enhanced (Phase B)", use_container_width=True)
                        c3.image(res_rgb, caption=f"Detected: {len(res.boxes)}", use_container_width=True)
                    else:
                        c1, c2 = st.columns(2)
                        c1.image(image_pil, caption="Original", use_container_width=True)
                        c2.image(res_rgb, caption=f"Detected: {len(res.boxes)}", use_container_width=True)
                    
                    status_text.markdown(f"**🟢 Phase D:** Calculating Health Metrics (KBI & D_to_White)...", help="Phase D calculates the Bleaching Index (KBI).")
                    time.sleep(0.3)
                    for box in res.boxes:
                        cls_id = int(box.cls[0].item())
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        cropped_coral = image_to_detect[y1:y2, x1:x2]
                        health_metrics = analyze_coral_health(cropped_coral)
                        
                        if health_metrics:
                            all_results.append({
                                "site": site_name,
                                "filename": uploaded_file.name,
                                "species": model.names[cls_id],
                                "confidence": round(float(box.conf[0].item()), 3),
                                "paleness": health_metrics["mean_paleness"],
                                "d_to_white": health_metrics["mean_d_to_white"]
                            })

                elif file_extension in ['mp4', 'mov', 'avi']:
                    status_text.markdown(f"**🎥 Video Processing:** Extracting frames...")
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}")
                    tfile.write(uploaded_file.read())
                    tfile.close()
                    
                    cap = cv2.VideoCapture(tfile.name)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_jump = int(fps * 2) 
                    
                    frame_count = 0
                    processed_frames = 0
                    video_st_results = []
                    
                    st.markdown(f"**{uploaded_file.name}** (Video)")
                    cols = st.columns(3)
                    
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret: break
                            
                        if frame_count % frame_jump == 0:
                            processed_frames += 1
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = model(frame_rgb, conf=conf_threshold)
                            res = results[0]
                            
                            for box in res.boxes:
                                cls_id = int(box.cls[0].item())
                                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                                cropped_coral = frame[y1:y2, x1:x2]
                                health_metrics = analyze_coral_health(cropped_coral)
                                
                                if health_metrics:
                                    video_st_results.append({
                                        "site": site_name,
                                        "filename": uploaded_file.name,
                                        "frame": processed_frames,
                                        "species": model.names[cls_id],
                                        "confidence": round(float(box.conf[0].item()), 3),
                                        "paleness": health_metrics["mean_paleness"],
                                        "d_to_white": health_metrics["mean_d_to_white"]
                                    })
                            
                            if processed_frames <= 3:
                                annotated_frame = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
                                with cols[processed_frames - 1]:
                                    st.image(annotated_frame, caption=f"Frame {processed_frames}", use_container_width=True)
                                    
                        frame_count += 1
                        
                    cap.release()
                    os.remove(tfile.name)
                    all_results.extend(video_st_results)

                main_progress.progress((i + 1) / total_files)

            status_text.markdown("**🟢 Phase D & Database Update:** Saving results to CSV...")
            time.sleep(0.5)
            
            if all_results:
                df = pd.DataFrame(all_results)
                display_df = df.copy()
                display_df.insert(0, 'No.', range(1, len(display_df) + 1))
                st.markdown("### Detection Results")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(label="▤&nbsp;&nbsp;&nbsp;Download Results as CSV", data=csv, file_name="yolo_detections.csv", mime="text/csv", use_container_width=True)
                
                # --- UPDATE site_summary.csv ---
                site_summary_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\site_summary.csv")
                
                if site_summary_path.exists():
                    summary_df = pd.read_csv(site_summary_path)
                    
                    # Drop the duplicate 'KBI' column if it exists from previous runs
                    if 'KBI' in summary_df.columns:
                        summary_df = summary_df.drop(columns=['KBI'])
                    
                    site_col = "site"
                    colony_col = "colonies"
                    dip_col = "dip_count"
                    por_col = "por_count"
                    kbi_col = "mean_paleness"
                    dwhite_col = "mean_d_to_white"
                    
                else:
                    site_col, colony_col, dip_col, por_col, kbi_col, dwhite_col = "site", "colonies", "dip_count", "por_count", "mean_paleness", "mean_d_to_white"
                    summary_df = pd.DataFrame(columns=[site_col, colony_col, dip_col, por_col, kbi_col, dwhite_col])
                
                new_colonies = len(df)
                dip_count = len(df[df['species'].str.lower() == 'dipsastraea'])
                por_count = len(df[df['species'].str.lower() == 'porites'])
                mean_paleness = df['paleness'].mean()
                mean_dwhite = df['d_to_white'].mean()
                
                if site_name in summary_df[site_col].values:
                    idx = summary_df.index[summary_df[site_col] == site_name].tolist()[0]
                    
                    summary_df.at[idx, colony_col] += new_colonies
                    if dip_col in summary_df.columns: summary_df.at[idx, dip_col] += dip_count
                    if por_col in summary_df.columns: summary_df.at[idx, por_col] += por_count
                    
                    old_paleness = summary_df.at[idx, kbi_col]
                    if pd.isna(old_paleness) or old_paleness == 0.0:
                        summary_df.at[idx, kbi_col] = mean_paleness
                    else:
                        summary_df.at[idx, kbi_col] = (old_paleness + mean_paleness) / 2
                        
                    old_dwhite = summary_df.at[idx, dwhite_col]
                    if pd.isna(old_dwhite) or old_dwhite == 0.0:
                        summary_df.at[idx, dwhite_col] = mean_dwhite
                    else:
                        summary_df.at[idx, dwhite_col] = (old_dwhite + mean_dwhite) / 2
                else:
                    new_row = {
                        site_col: site_name, 
                        colony_col: new_colonies, 
                        dip_col: dip_count, 
                        por_col: por_count,
                        kbi_col: mean_paleness, 
                        dwhite_col: mean_dwhite, 
                        'Latitude': lat, 
                        'Longitude': lon
                    }
                    summary_df = pd.concat([summary_df, pd.DataFrame([new_row])], ignore_index=True)
                
                summary_df.to_csv(site_summary_path, index=False)
                
                crca_dir = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\crca")
                crca_dir.mkdir(parents=True, exist_ok=True)
                
                for idx, row in df.iterrows():
                    json_filename = f"{site_name}_{int(time.time())}_{idx}.json"
                    json_path = crca_dir / json_filename
                    json_data = {"image": row['filename'], "class": row['species'], "paleness": row['paleness']}
                    with open(json_path, "w") as f:
                        json.dump(json_data, f)

                st.success(f"✅ **Phase C & D Complete!** Analyzed and saved {new_colonies} colonies with health metrics (KBI & D_to_White).")