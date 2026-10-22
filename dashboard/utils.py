import streamlit as st

st.markdown('<div class="module-header">MODULE 09 · FAQ</div>', unsafe_allow_html=True)
st.title("Frequently Asked Questions")
st.markdown("Find answers to common questions regarding the Azr.AI system, model capabilities, and dashboard features.")

# ==========================================
# CUSTOM CSS FOR FAQ CARDS
# ==========================================
st.markdown("""
<style>
    /* Target the expander container */
    div[data-testid="stExpander"] {
        background-color: #1E293B !important; /* Deep Ocean background */
        border: 1px solid #334155 !important; /* Panel Border */
        border-radius: 8px !important;
        margin-bottom: 15px !important;
    }
    
    /* Target the expander summary (the clickable question part) */
    div[data-testid="stExpander"] summary {
        font-size: 1.1rem !important; /* Bigger question font */
        font-weight: 600 !important;
        color: #E2E8F0 !important; /* Foam White */
        padding: 12px 15px !important;
    }

    /* Target the text inside the expander (the answer part) */
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.05rem !important; /* Bigger answer font */
        color: #94A3B8 !important; /* Mist Gray */
        line-height: 1.6 !important;
        padding-bottom: 10px !important;
    }

    /* Change the expander arrow icon to a monotone symbol */
    div[data-testid="stExpander"] summary svg {
        fill: #00E5FF !important; /* Cyan icon */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECTION 1: AI MODEL & DETECTION
# ==========================================
st.markdown("### <span style='color:#00E5FF'>◈ AI Model & Detection</span>", unsafe_allow_html=True)

with st.expander("What species can the model currently detect?"):
    st.markdown("""
    The current trained model (`yolov8s_coral`) is only capable of detecting the species it was trained on. 
    Based on the Phase C/D datasets, this currently includes **Dipsastraea** and **Porites**. 
    If the model is shown an untrained species (e.g., Montipora), it will likely either ignore it or misclassify it.
    """)

with st.expander("Do I need to retrain the model if I want to detect new species?"):
    st.markdown("""
    **Yes.** Deep learning models do not learn "on the fly" inside the dashboard. 
    To add a new species, you must:
    1. Annotate images of the new species using CVAT.
    2. Add them to your training dataset.
    3. Retrain the YOLOv8 model in Phase C.
    4. Replace the `best.pt` file in the `models/trained/` folder.
    """)

with st.expander("How does the system handle videos?"):
    st.markdown("""
    For videos, the system does not process every single frame (which would crash a normal laptop). 
    Instead, the user selects a "Frame Skip" rate (e.g., every 2 seconds). The system extracts those specific frames, runs the YOLO inference, and aggregates the findings. It then displays a preview of the first 3 processed frames.
    """)

# ==========================================
# SECTION 2: DATA & UPLOADS
# ==========================================
st.markdown("### <span style='color:#FFB74D'>◈ Data & Uploads</span>", unsafe_allow_html=True)

with st.expander("Does the user need to rename files to a standard format before uploading?"):
    st.markdown("""
    **No.** The system analyzes the visual pixels, not the filename. You can upload `IMG_2026.jpg` or `coral_pic.png`. 
    However, the CSV output will record whatever the original filename was. If strict naming conventions (e.g., `[Site]_[Depth].jpg`) are required for your thesis, they must be applied before uploading.
    """)

with st.expander("What is the maximum file size for uploads?"):
    st.markdown("""
    By default, Streamlit limits uploads to **200MB per file**. If a 4K video exceeds this, it will be rejected. You can increase this limit by editing your `.streamlit/config.toml` file, but it is generally not recommended for browser-based applications.
    """)

with st.expander("Why is there no automatic Health Assessment (KBI) on the Upload page?"):
    st.markdown("""
    The Upload page performs bounding-box detection (finding where the coral is). 
    The KBI Health Assessment (Phase D) requires cropping the coral, applying a colour reference chart (Coral-CRCA), and calculating paleness. Because this is computationally heavy, it is isolated on the Health Assessment page to keep the Upload pipeline fast.
    """)

# ==========================================
# SECTION 3: DASHBOARD & VISUALIZATION
# ==========================================
st.markdown("### <span style='color:#AB47BC'>◈ Dashboard & Visualization</span>", unsafe_allow_html=True)

with st.expander("Why are some charts using mock data?"):
    st.markdown("""
    The **Environment** and **Temporal Trends** pages currently use simulated data. 
    *   Environment: Waiting for the Phase A multiprobe CSV and Aqua MODIS `.nc` files.
    *   Temporal: Requires Campaign 2 and Campaign 3 field data to show multi-year trends.
    """)

with st.expander("Why do some maps show no GPS data or only 6 points?"):
    st.markdown("""
    During Phase B, the drone's GPS EXIF tags were stripped or missing from the raw imagery. 
    To ensure the Distribution Map still functioned for the thesis demo, 6 known reef coordinates (Tioman, Seri Buat, Tokong Burung, Berhala, Raja Muda, Balok) were manually injected into `gps_coordinates.csv`.
    """)

with st.expander("How does the Connectivity page calculate the DPI?"):
    st.markdown("""
    The Dispersal Potential Index (DPI) is calculated from the `connectivity_matrix.csv` (generated in Phase E via Parcels and MIKE 21). 
    It represents the probability of larvae exporting from a Source Reef (like Tioman) to a Sink Reef (like Balok). The higher the DPI, the more critical that reef is as a larval source.
    """)

with st.expander("Why do some charts have a ⚙ gear menu?"):
    st.markdown("""
    The gear menu is a custom utility (`utils.py`) applied to most charts. It allows you to:
    1. Download the chart as a high-res PNG.
    2. Download the raw data as a CSV.
    3. Toggle "Full Screen" mode (expands the chart to 800px height for presentations).
    """)

# ==========================================
# SECTION 4: TROUBLESHOOTING
# ==========================================
st.markdown("### <span style='color:#E57373'>◈ Troubleshooting</span>", unsafe_allow_html=True)

with st.expander("I got a 'Model not found' error. What do I do?"):
    st.markdown("""
    This means the dashboard cannot find the `best.pt` file. 
    Ensure that your trained model is saved exactly at: `C:\\Users\\[Username]\\Downloads\\coral-reef-kuantan\\models\\trained\\yolov8s_coral\\best.pt`.
    """)

with st.expander("The map is a blank grey box. How do I fix it?"):
    st.markdown("""
    This usually happens if the browser blocks Mapbox tile requests. 
    We bypassed this by using `scatter_map` with the free `carto-darkmatter` style. If it still fails, try refreshing the browser or checking your internet connection (the map requires loading external tiles).
    """)