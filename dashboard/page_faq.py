import streamlit as st

st.markdown('<div class="module-header">MODULE 09 · FAQ</div>', unsafe_allow_html=True)
st.title("Frequently Asked Questions")
st.markdown("Find answers to common questions regarding the Azr.AI system, model capabilities, and dashboard features.")

# ==========================================
# CUSTOM CSS FOR FAQ CARDS
# ==========================================
st.markdown("""
<style>
    details {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        margin-bottom: 15px;
        overflow: hidden;
    }
    summary {
        font-size: 1.15rem;
        font-weight: 600;
        color: #E2E8F0;
        padding: 15px 20px;
        cursor: pointer;
        list-style: none;
        display: flex;
        align-items: center;
    }
    summary::-webkit-details-marker { display: none; }
    summary::before {
        content: "›";
        color: #E2E8F0;
        font-size: 1.5rem;
        font-weight: bold;
        margin-right: 15px;
        transition: transform 0.2s ease;
        line-height: 1;
    }
    details[open] summary::before { transform: rotate(90deg); }
    .faq-answer {
        font-size: 1.05rem;
        color: #94A3B8;
        line-height: 1.6;
        padding: 0 20px 15px 45px;
        background-color: #1E293B;
        border-top: 1px solid #334155;
        padding-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

def faq_card(question, answer):
    st.markdown(f"""
    <details>
        <summary>{question}</summary>
        <div class="faq-answer">{answer}</div>
    </details>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECTION 0: ABOUT THE DASHBOARD
# ==========================================
st.markdown("### <span style='color:#00E5FF'>◈ About the System</span>", unsafe_allow_html=True)

faq_card(
    "What is this dashboard about?", 
    "This dashboard is the frontend interface for the <b>Azr.AI Coral Health Monitoring System</b>. It integrates deep learning (YOLOv8), colour analysis, and hydrodynamic modelling to monitor coral reef health in Kuantan. You can upload raw underwater imagery/video to detect species, calculate bleaching severity (KBI), and visualise spatial and connectivity data."
)

faq_card(
    "What are the phases processed in this pipeline?",
    "<b>Phase B (Enhancement)</b>, <b>Phase C (Detection)</b>, and <b>Phase D (Health Assessment)</b>.<br><br>"
    "<ul>"
    "<li><b>Phase B (Enhancement):</b> Restores underwater colors and contrast before detection using three algorithms:"
    "<ul>"
    "<li><b>RCC (Red Channel Compensation):</b> Restores the red light that is lost underwater due to depth.</li>"
    "<li><b>Gray-World:</b> Neutralizes unnatural color casts (e.g., if the whole image looks too blue or green).</li>"
    "<li><b>CLAHE (Contrast Limited Adaptive Histogram Equalization):</b> Boosts local contrast to make coral textures and edges pop.</li>"
    "</ul></li>"
    "<li><b>Phase C (Detection):</b> Runs the YOLOv8 AI model to find, count, and label the coral species.</li>"
    "<li><b>Phase D (Health Assessment):</b> Crops each coral to calculate its Bleaching Index (KBI) and color distance to white (D_to_White).</li>"
    "<li><b>Phase F (Dashboard):</b> Immediately updates the charts and database with the new results.</li>"
    "</ul>"
)

faq_card(
    "Does the Upload page run all phases from A to F?",
    "<b>No.</b> The dashboard only runs the computational phases (B, C, D) on uploaded media. It does <b>not</b> run Phase A (field data collection) or Phase E (ocean current simulation), as those require manual fieldwork and heavy hydrodynamic modelling (MIKE 21) done offline."
)

# ==========================================
# SECTION 1: DATA & UPLOADS
# ==========================================
st.markdown("### <span style='color:#FFB74D'>◈ Data & Uploads</span>", unsafe_allow_html=True)

faq_card(
    "What species can the AI model currently detect?",
    "The AI model is a <b>dynamic classifier</b> that detects the coral genera present in its training dataset. Because it continuously learns from the annotated data it is given, the range of detectable species expands as new annotations are added to the system. However, if the system is shown a species that was not included in its training data, it will likely ignore it or misclassify it."
)

faq_card(
    "Do I need to retrain the model if I want to detect new species?",
    "<b>Yes.</b> The system cannot learn new species on the fly. To detect a new coral species, a new dataset must be annotated and the model must be retrained using the YOLOv8 architecture."
)

faq_card(
    "Is there a limit to the file size or resolution I can upload?",
    "<b>Yes.</b> To prevent the server from crashing, the system limits individual files to <b>50 MB</b>. For videos, we recommend 1080p resolution rather than 4K to ensure smooth processing."
)

faq_card(
    "Can I upload videos instead of images?",
    "<b>Yes.</b> The system accepts both images (JPG, PNG) and videos (MP4, MOV). For videos, the system extracts frames at a specified interval (e.g., every 2 seconds) to perform the analysis without overwhelming your computer's memory."
)

# ==========================================
# SECTION 2: DASHBOARD & VISUALIZATION
# ==========================================
st.markdown("### <span style='color:#AB47BC'>◈ Dashboard & Visualization</span>", unsafe_allow_html=True)

faq_card(
    "Why do some charts show simulated or limited data?",
    "The <b>Environment</b> and <b>Temporal Trends</b> charts currently use simulated data while the project awaits additional campaign data (Phase A) and oceanographic satellite files (MODIS/NOAA)."
)

faq_card(
    "Why does the Connectivity page not update after I upload images?",
    "Connectivity (Phase E) is based on ocean physics (currents and tides), not coral images. It requires running the MIKE 21 hydrodynamic simulation offline. Uploading an image does not change the ocean currents."
)

faq_card(
    "What does the Dispersal Potential Index (DPI) mean?",
    "The DPI measures how important a specific reef is as a 'source' of coral larvae. A high DPI indicates that a reef exports a large number of larvae to nearby reefs, making it a critical area for conservation."
)

faq_card(
    "How do I download the charts and data?",
    "Look for the <b>⚙ gear icon</b> in the top right corner of most charts. Clicking it opens a menu that allows you to download the chart as an image (PNG) or the underlying data as a spreadsheet (CSV)."
)

# ==========================================
# SECTION 3: TROUBLESHOOTING
# ==========================================
st.markdown("### <span style='color:#E57373'>◈ Troubleshooting</span>", unsafe_allow_html=True)

faq_card(
    "I uploaded images, but the KBI chart shows a blank space for my new site.",
    "This happens if you uploaded a site that already exists in the database but had empty (NaN) data. To fix this, ensure your <code>site_summary.csv</code> has '0' instead of blank spaces, or clear the file and re-upload."
)

faq_card(
    "The detection model is not loading. What should I do?",
    "Ensure that the model file <code>best.pt</code> has been properly placed in the <code>models/trained/yolov8s_coral/</code> directory."
)

faq_card(
    "The map is blank or grey. How do I fix it?",
    "The interactive map requires an active internet connection to load the background map tiles. If you are offline or behind a strict firewall, the map may appear as a blank grey box."
)