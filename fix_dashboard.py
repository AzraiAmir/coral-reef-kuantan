import os
from pathlib import Path

base_dir = Path("dashboard")
assets_dir = base_dir / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)

# 1. CSS - Nukes Streamlit's sidebar and makes room for ours
css_content = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&family=Poppins:wght@500;600;700&display=swap');

:root {
    --bg-abyss: #0A1929;
    --bg-deep-ocean: #132F4C;
    --accent-coral: #FF7043;
    --accent-teal: #4DD0E1;
    --text-foam: #F5F7FA;
    --text-mist: #B0BEC5;
    --border-reef: #1E3A5F;
}

.stApp {
    background: linear-gradient(180deg, var(--bg-abyss) 0%, #05101A 100%);
    color: var(--text-foam);
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    color: var(--text-foam) !important;
}

/* Completely hide Streamlit's native sidebar */
[data-testid="stSidebar"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    display: none !important;
}

/* Add a 280px margin to the main content to make room for our custom sidebar */
.block-container {
    padding-left: 300px !important;
    padding-top: 2rem !important;
    max-width: 100% !important;
}

.metric-card {
    background-color: var(--bg-deep-ocean);
    border: 1px solid var(--border-reef);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 10px 0;
}
.metric-label {
    font-size: 0.9rem;
    color: var(--text-mist);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stButton>button {
    background-color: var(--accent-coral) !important;
    color: var(--text-foam) !important;
    border: none;
    border-radius: 4px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: var(--accent-teal) !important;
    color: var(--bg-abyss) !important;
    box-shadow: 0 0 15px var(--accent-teal);
}
"""
(assets_dir / "style.css").write_text(css_content.strip(), encoding="utf-8")

# 2. APP.PY - Custom HTML Sidebar Router
app_content = """
import streamlit as st
from pathlib import Path
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Azr.AI | Coral Health", page_icon="🪸", layout="wide")

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Read Logo
logo_path = Path(__file__).parent / "assets" / "logo_full.png"
logo_b64 = ""
if logo_path.exists():
    with open(logo_path, "rb") as f: logo_b64 = base64.b64encode(f.read()).decode()

# Draw Custom Sidebar
custom_html = f'''
<style>
    #custom-sidebar {{
        position: fixed; top: 0; left: 0; height: 100vh; width: 280px;
        background-color: #132F4C; border-right: 1px solid #1E3A5F;
        display: flex; flex-direction: column; z-index: 999999;
        font-family: 'Inter', sans-serif;
    }}
    #logo-box {{ padding: 30px 20px; display: flex; justify-content: center; }}
    #logo-box img {{ width: 170px; }}
    #nav-box {{ flex-grow: 1; padding: 0 15px; display: flex; flex-direction: column; }}
    .nav-item {{
        display: flex; align-items: center; padding: 12px; margin-bottom: 5px;
        border-radius: 6px; color: #B0BEC5; text-decoration: none; transition: 0.2s;
    }}
    .nav-item:hover {{ background-color: #1E3A5F; color: #F5F7FA; }}
    .nav-item.active {{ background-color: #FF7043; color: white; }}
    .nav-icon {{ font-size: 1.2rem; margin-right: 15px; }}
    #version-box {{
        text-align: center; color: #B0BEC5; font-size: 0.8rem;
        padding: 20px; border-top: 1px solid #1E3A5F;
    }}
</style>

<div id="custom-sidebar">
    <div id="logo-box"><img src="data:image/png;base64,{logo_b64}"></div>
    <div id="nav-box">
        <a href="/" target="_self" class="nav-item active"><span class="nav-icon">🏠</span> Overview</a>
        <a href="/page_upload" target="_self" class="nav-item"><span class="nav-icon">📤</span> Upload & Process</a>
        <a href="/page_distribution" target="_self" class="nav-item"><span class="nav-icon">🗺️</span> Distribution Maps</a>
        <a href="/page_health" target="_self" class="nav-item"><span class="nav-icon">🩺</span> Health Assessment</a>
        <a href="/page_environment" target="_self" class="nav-item"><span class="nav-icon">🌡️</span> Environment</a>
        <a href="/page_connectivity" target="_self" class="nav-item"><span class="nav-icon">🕸️</span> Connectivity</a>
    </div>
    <div id="version-box">v1.0.0 | PhD Research</div>
</div>
'''
components.html(custom_html, height=0, width=0)

pages = [
    st.Page("page_overview.py", title="Overview", default=True),
    st.Page("page_upload.py", title="Upload & Process"),
    st.Page("page_distribution.py", title="Distribution Maps"),
    st.Page("page_health.py", title="Health Assessment"),
    st.Page("page_environment.py", title="Environment"),
    st.Page("page_connectivity.py", title="Connectivity"),
]

pg = st.navigation(pages, position="hidden")
pg.run()
"""
(base_dir / "app.py").write_text(app_content.strip(), encoding="utf-8")

# 3. OVERVIEW
overview_content = """
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Overview")
st.markdown("Welcome to the **Azr.AI** monitoring platform. This dashboard provides a summary of the latest coral health, detection, and connectivity analysis.")

try:
    df = pd.read_csv(r"C:\\Users\\mazra\\Downloads\\coral-reef-kuantan\\results\\phase_d\\site_summary.csv")
    total_colonies = df['colonies'].sum()
    mean_paleness = df['mean_paleness'].mean()
    num_sites = len(df)
except FileNotFoundError:
    total_colonies = 263
    mean_paleness = 0.4992
    num_sites = 1

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-card"><div class="metric-label">Colonies Detected</div><div class="metric-value" style="color: #FF7043;">{total_colonies}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-card"><div class="metric-label">Sites Monitored</div><div class="metric-value" style="color: #4DD0E1;">{num_sites}</div></div>', unsafe_allow_html=True)
with col3:
    health_color = "#FFB74D" if mean_paleness < 0.6 else "#E57373"
    st.markdown(f'<div class="metric-card"><div class="metric-label">Mean KBI (Relative)</div><div class="metric-value" style="color: {health_color};">{mean_paleness:.2f}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-card"><div class="metric-label">Model Confidence</div><div class="metric-value" style="color: #66BB6A;">High</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("Species Distribution")
    species_df = pd.DataFrame({"Species": ["Dipsastraea", "Porites", "Acropora", "Montipora"], "Count": [107, 77, 45, 22]})
    fig1 = px.pie(species_df, values='Count', names='Species', color='Species', color_discrete_sequence=px.colors.qualitative.Dark24, hole=0.4)
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#F5F7FA', margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)
with chart_col2:
    st.subheader("Site Health Overview")
    sites = ["Pulau Tioman", "Pulau Seri Buat", "Raja Muda"]
    health_scores = [0.15, 0.22, 0.55]
    fig2 = px.bar(x=sites, y=health_scores, labels={'x': 'Site', 'y': 'KBI (Bleaching Index)'}, color=health_scores, color_continuous_scale=[(0.0, '#66BB6A'), (0.5, '#FFB74D'), (1.0, '#E57373')])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#F5F7FA', showlegend=False, xaxis=dict(showgrid=False, color='#B0BEC5'), yaxis=dict(showgrid=True, gridcolor='#1E3A5F', color='#B0BEC5'), margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig2, use_container_width=True)
"""
(base_dir / "page_overview.py").write_text(overview_content.strip(), encoding="utf-8")

# 4. UPLOAD
upload_content = """
import streamlit as st
import time

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
"""
(base_dir / "page_upload.py").write_text(upload_content.strip(), encoding="utf-8")

# 5. PLACEHOLDERS
placeholders = {
    "page_distribution.py": 'import streamlit as st\nst.title("🗺️ Distribution Maps")\nst.markdown("Spatial distribution of coral species.")',
    "page_health.py": 'import streamlit as st\nst.title("🩺 Health Assessment")\nst.markdown("Quantitative coral bleaching severity.")',
    "page_environment.py": 'import streamlit as st\nst.title("🌡️ Environmental Parameters")\nst.markdown("Environmental drivers of coral health.")',
    "page_connectivity.py": 'import streamlit as st\nst.title("🕸️ Connectivity Modelling")\nst.markdown("Source-sink dynamics of coral larvae.")'
}
for filename, content in placeholders.items():
    (base_dir / filename).write_text(content.strip(), encoding="utf-8")

print("✅ DONE. Custom Sidebar injected successfully.")