import streamlit as st

st.markdown('<div class="module-header">MODULE 09 · FAQ</div>', unsafe_allow_html=True)
st.title("Frequently Asked Questions")
st.markdown("Find answers to common questions regarding the Azr.AI system, model capabilities, and dashboard features.")

# ==========================================
# FAQ CARD CSS
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
    summary::-webkit-details-marker {
        display: none;
    }
    summary::before {
        content: "›";
        color: #E2E8F0;
        font-size: 1.5rem;
        font-weight: bold;
        margin-right: 15px;
        transition: transform 0.2s ease;
        line-height: 1;
    }
    details[open] summary::before {
        transform: rotate(90deg);
    }
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

# Helper function to create the HTML cards
def faq_card(question, answer):
    st.markdown(f"""
    <details>
        <summary>{question}</summary>
        <div class="faq-answer">{answer}</div>
    </details>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECTION 1: AI MODEL & DETECTION
# ==========================================
st.markdown("### <span style='color:#00E5FF'>◈ AI Model & Detection</span>", unsafe_allow_html=True)

faq_card("What species can the model currently detect?", "The current trained model is capable of detecting <b>Dipsastraea</b> and <b>Porites</b>. If the system is shown an untrained species (e.g., Montipora), it will likely either ignore it or misclassify it.")
faq_card("Do I need to retrain the model if I want to detect new species?", "<b>Yes.</b> The system cannot learn new species on the fly. To detect a new coral species, a new dataset must be annotated and the model must be retrained.")
faq_card("Can I upload videos instead of images?", "<b>Yes.</b> The system accepts both images (JPG, PNG) and videos (MP4, MOV). For videos, the system extracts frames at a specified interval to perform the analysis without overwhelming your computer's memory.")

# ==========================================
# SECTION 2: DATA & UPLOADS
# ==========================================
st.markdown("### <span style='color:#FFB74D'>◈ Data & Uploads</span>", unsafe_allow_html=True)

faq_card("Do I need to rename my files to a specific format before uploading?", "<b>No.</b> You can upload images with any filename (e.g., IMG_2026.jpg). The system analyzes the visual content of the image, not the filename.")
faq_card("Is there a limit to the file size or resolution I can upload?", "<b>Yes.</b> To prevent the server from crashing, the system limits individual files to <b>50 MB</b>. For videos, we recommend 1080p resolution rather than 4K.")
faq_card("Does the system automatically assess coral health (KBI) when I upload?", "No, the Upload page is designed solely for fast detection. The health assessment requires a specific color-reference workflow, which can be viewed on the <b>Health Assessment</b> page.")

# ==========================================
# SECTION 3: DASHBOARD & VISUALIZATION
# ==========================================
st.markdown("### <span style='color:#AB47BC'>◈ Dashboard & Visualization</span>", unsafe_allow_html=True)

faq_card("Why do some charts show simulated or limited data?", "The dashboard is continuously updated as new field data becomes available. Currently, the <b>Environment</b> and <b>Temporal Trends</b> charts display simulated data while the project awaits additional campaign data.")
faq_card("What does the Dispersal Potential Index (DPI) mean?", "The DPI measures how important a specific reef is as a 'source' of coral larvae. A high DPI indicates that a reef exports a large number of larvae to nearby reefs, making it a critical area for conservation.")
faq_card("How do I download the charts and data?", "Look for the <b>⚙ gear icon</b> in the top right corner of most charts. Clicking it opens a menu that allows you to download the chart as an image (PNG) or the underlying data as a spreadsheet (CSV).")

# ==========================================
# SECTION 4: TROUBLESHOOTING
# ==========================================
st.markdown("### <span style='color:#E57373'>◈ Troubleshooting</span>", unsafe_allow_html=True)

faq_card("The detection model is not loading. What should I do?", "If the system cannot load the AI model, ensure that the model file has been properly placed in the <code>models/trained/</code> directory. If the issue persists, try refreshing the page.")
faq_card("The map is blank or grey. How do I fix it?", "The interactive map requires an active internet connection to load the background map tiles. If you are offline or behind a strict firewall, the map may appear as a blank grey box.")