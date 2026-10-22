import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="Azr.AI | Coral Health", 
    page_icon="dashboard/assets/favicon.png",
    layout="wide"
)

# 1. LOAD CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 2. HIDE SCROLLBARS GLOBALLY & REDUCE PADDING
st.markdown("""
<style>
    /* Reduce the massive default top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Hide the sidebar scrollbar */
    section[data-testid="stSidebar"] > div {
        overflow-y: hidden !important;
    }

    /* Hide scrollbar for Chrome, Safari and Opera */
    div[data-testid="stVerticalBlock"] > div[style*="height"]::-webkit-scrollbar {
        display: none;
    }
    /* Hide scrollbar for IE, Edge and Firefox */
    div[data-testid="stVerticalBlock"] > div[style*="height"] {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }

    /* ==========================================
       FLOATING SCROLL BUTTON (Global CSS)
       ========================================== */
    .floating-scroll-btn {
        position: fixed !important;
        bottom: 40px !important;
        right: 40px !important;
        width: 55px !important;
        height: 55px !important;
        border-radius: 50% !important;
        background-color: #1E293B !important;
        color: #00E5FF !important;
        border: 2px solid #334155 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        z-index: 9999999 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
    }

    .floating-scroll-btn:hover {
        border-color: #00E5FF !important;
        color: #FFFFFF !important;
        transform: scale(1.1) !important;
    }
    /* Force the Streamlit iframe to float */
    iframe[title="streamlit_component"] {
        position: fixed !important;
        bottom: 40px !important;
        right: 40px !important;
        width: 60px !important;
        height: 60px !important;
        z-index: 999999 !important;
        border: none !important;
        box-shadow: none !important;
        pointer-events: none;
    }
    iframe[title="streamlit_component"] * {
        pointer-events: auto;
    }
    /* 
       Target the Streamlit link button specifically. 
       We find the exact link (#top-anchor) and force it to float.
    */
    div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stMarkdownContainer"] a[href="#top-anchor"]) {
        position: fixed !important;
        bottom: 40px !important;
        right: 40px !important;
        z-index: 9999999 !important;
        width: 55px !important;
    }

    /* Style the actual link button to be a circular icon */
    a[href="#top-anchor"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 55px !important;
        height: 55px !important;
        border-radius: 50% !important;
        background-color: #1E293B !important;
        color: #00E5FF !important;
        border: 2px solid #334155 !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
    }

    a[href="#top-anchor"]:hover {
        border-color: #00E5FF !important;
        color: #FFFFFF !important;
        transform: scale(1.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGATION
pg = st.navigation([
    st.Page("page_overview.py", title="Overview", icon="🏠", default=True),
    st.Page("page_upload.py", title="Upload & Process", icon="📤"),
    st.Page("page_distribution.py", title="Distribution Maps", icon="🗺️"),
    st.Page("page_health.py", title="Health Assessment", icon="🩺"),
    st.Page("page_environment.py", title="Environment", icon="🌡️"),
    st.Page("page_connectivity.py", title="Connectivity", icon="🕸️"),
    st.Page("page_temporal.py", title="Temporal Trends", icon="📈"),
    st.Page("page_export.py", title="Data Export", icon="💾"),
    st.Page("page_faq.py", title="FAQ", icon="❓"),
    st.Page("page_contact.py", title="Contact Us", icon="✉️"),
], position="hidden")

current_page = pg.title

# 4. SIDEBAR
with st.sidebar:
    logo_path = Path(__file__).parent / "assets" / "logo_full.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f: logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<div style="text-align: center; margin-bottom: 30px;"><img src="data:image/png;base64,{logo_b64}" style="width: 140px;"></div>', unsafe_allow_html=True)
    
    def get_class(title):
        return "nav-link active" if current_page == title else "nav-link"

    st.markdown(f"""
    <div class="nav-container">
        <a href="/" target="_self" class="{get_class('Overview')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>Overview</span>
        </a>
        <a href="/page_upload" target="_self" class="{get_class('Upload & Process')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
            <span>Upload & Process</span>
        </a>
        <a href="/page_distribution" target="_self" class="{get_class('Distribution Maps')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
            <span>Distribution Maps</span>
        </a>
        <a href="/page_health" target="_self" class="{get_class('Health Assessment')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
            <span>Health Assessment</span>
        </a>
        <a href="/page_environment" target="_self" class="{get_class('Environment')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"></path></svg>
            <span>Environment</span>
        </a>
        <a href="/page_connectivity" target="_self" class="{get_class('Connectivity')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
            <span>Connectivity</span>
        </a>
        <a href="/page_temporal" target="_self" class="{get_class('Temporal Trends')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
            <span>Temporal Trends</span>
        </a>
        <a href="/page_export" target="_self" class="{get_class('Data Export')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            <span>Data Export</span>
        </a>
        <a href="/page_faq" target="_self" class="{get_class('FAQ')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            <span>FAQ</span>
        </a>
        <a href="/page_contact" target="_self" class="{get_class('Contact Us')}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
            <span>Contact Us</span>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # --- FOOTER ---
    iium_logo_path = Path(__file__).parent / "assets" / "iium_logo.png"
    if iium_logo_path.exists():
        with open(iium_logo_path, "rb") as f: 
            iium_b64 = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <div class="floating-footer" style="text-align: center;">
            <img src="data:image/png;base64,{iium_b64}">
            <hr style="width: 80%; margin: 10px auto; border-color: #334155;">
            <p style="margin: 0; font-size: 12px; color: #E2E8F0;">v1.0.0 | PhD Research</p>
            <p style="margin: 5px 0 0 0; font-size: 10px; color: #64748B; line-height: 1.2;">
                © 2026 M. Azrai Amir.<br>All Rights Reserved.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("IIUM Logo not found.")

# 5. TOP HEADER
acri_path = Path(__file__).parent / "assets" / "acri_logo.png"
marine_path = Path(__file__).parent / "assets" / "marine_ai_logo.png"

acri_b64 = ""
marine_b64 = ""

if acri_path.exists():
    with open(acri_path, "rb") as f: 
        acri_b64 = base64.b64encode(f.read()).decode()
if marine_path.exists():
    with open(marine_path, "rb") as f: 
        marine_b64 = base64.b64encode(f.read()).decode()

header_html = """
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0px 20px 0px; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
    <h1 style="color: #E2E8F0; font-family: 'Space Mono', monospace; font-size: 1.2rem; letter-spacing: 1px; margin: 0; white-space: nowrap;">
        <span style="color: #00E5FF;">AZR.AI</span> | Automated Zonation & Reef Artificial Intelligence
    </h1>
    <div style="display: flex; gap: 15px; align-items: center;">
        <img src="data:image/png;base64,{ACRI_IMG}" style="height: 80px; object-fit: contain;">
        <img src="data:image/png;base64,{MARINE_IMG}" style="height: 80px; object-fit: contain;">
    </div>
</div>
""".format(ACRI_IMG=acri_b64, MARINE_IMG=marine_b64)

st.markdown(header_html, unsafe_allow_html=True)

# 6. RUN THE PAGE
pg.run()