import streamlit as st
import textwrap
import base64
from pathlib import Path

st.markdown('<div class="module-header">MODULE 08 · CONTACT</div>', unsafe_allow_html=True)
st.title("Contact Us")
st.markdown("For inquiries regarding the Azr.AI Coral Reef Monitoring project, please reach out to the research team.")

st.markdown("<br>", unsafe_allow_html=True)

def get_base64_image(image_filename):
    img_path = Path(__file__).parent / "assets" / image_filename
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

b64_azrai = get_base64_image("azrai.JPG")
b64_siti = get_base64_image("siti.JPG")
b64_faiz = get_base64_image("faiz.JPG")

img_pi = f'<img src="data:image/jpeg;base64,{b64_azrai}" style="width: 100%; height: 100%; object-fit: cover;">'
img_sup1 = f'<img src="data:image/jpeg;base64,{b64_siti}" style="width: 100%; height: 100%; object-fit: cover;">'
img_sup2 = f'<img src="data:image/jpeg;base64,{b64_faiz}" style="width: 100%; height: 100%; object-fit: cover;">'

# --- ROW 1: PRINCIPAL INVESTIGATOR ---
with st.container(border=False):
    html_pi = f"""
    <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 30px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 20px; flex: 1;">
            <div style="width: 80px; height: 80px; flex-shrink: 0; border-radius: 50%; background-color: #0F172A; border: 2px solid #00E5FF; display: flex; justify-content: center; align-items: center; overflow: hidden;">
                {img_pi}
            </div>
            <h2 style="margin: 0; color: #00E5FF; font-family: 'Space Mono', monospace; font-size: 1.5rem;">Muhammad Azrai bin Amir</h2>
        </div>
        <div style="width: 1px; height: 90px; background-color: #334155; margin: 0 30px;"></div>
        <div style="text-align: left; flex: 1.5;">
            <p style="margin: 0 0 8px 0; color: #94A3B8; font-size: 18px;">Principal Investigator / PhD Candidate</p>
            <p style="margin: 0 0 15px 0; color: #64748B; font-size: 16px;">Department of Mechatronics,<br>Kulliyyah of Engineering, IIUM</p>
            <p style="margin: 0; font-size: 16px; color: #E2E8F0;"><b>📧 Email:</b> <a href="mailto:azrai_amir@live.iium.edu.my" style="color: #FF7043; text-decoration: none;">azrai_amir@live.iium.edu.my</a></p>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html_pi), unsafe_allow_html=True)

# --- ROW 2: SUPERVISORS (Side by Side) ---
col1, col2 = st.columns(2)

with col1:
    with st.container(border=False, height=250):
        html_sup1 = f"""
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 25px 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 15px; flex: 1.8;">
                <div style="width: 80px; height: 80px; flex-shrink: 0; border-radius: 50%; background-color: #0F172A; border: 2px solid #FFB74D; display: flex; justify-content: center; align-items: center; overflow: hidden;">
                    {img_sup1}
                </div>
                <h3 style="margin: 0; color: #FFB74D; font-family: 'Space Mono', monospace; font-size: 1.1rem; line-height: 1.3;">Prof. Ir. Dr. Siti Fauziah Binti Toha @ Tohara</h3>
            </div>
            <div style="width: 1px; height: 100px; background-color: #334155; margin: 0 20px;"></div>
            <div style="text-align: left; flex: 1.5;">
                <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 16px;">Professor</p>
                <p style="margin: 0 0 15px 0; color: #64748B; font-size: 15px;">Department of Mechatronics,<br>Kulliyyah of Engineering, IIUM</p>
                <p style="margin: 0; font-size: 15px; color: #E2E8F0;"><b>📧 Email:</b> <br><a href="mailto:tsfauziah@iium.edu.my" style="color: #FF7043; text-decoration: none;">tsfauziah@iium.edu.my</a></p>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(html_sup1), unsafe_allow_html=True)

with col2:
    with st.container(border=False, height=250):
        html_sup2 = f"""
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 25px 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 15px; flex: 1.8;">
                <div style="width: 80px; height: 80px; flex-shrink: 0; border-radius: 50%; background-color: #0F172A; border: 2px solid #AB47BC; display: flex; justify-content: center; align-items: center; overflow: hidden;">
                    {img_sup2}
                </div>
                <h3 style="margin: 0; color: #AB47BC; font-family: 'Space Mono', monospace; font-size: 1.1rem; line-height: 1.3;">Dr. Muhammad Faiz Bin Mohd Hanapiah</h3>
            </div>
            <div style="width: 1px; height: 100px; background-color: #334155; margin: 0 20px;"></div>
            <div style="text-align: left; flex: 1.5;">
                <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 16px;">Coral Reef Ecologist</p>
                <p style="margin: 0 0 15px 0; color: #64748B; font-size: 15px;">Advanced Coastal Research and Innovation,<br>Kulliyyah of Science IIUM</p>
                <p style="margin: 0; font-size: 15px; color: #E2E8F0;"><b>📧 Email:</b> <br><a href="mailto:faizhanapiah@iium.edu.my" style="color: #FF7043; text-decoration: none;">faizhanapiah@iium.edu.my</a></p>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(html_sup2), unsafe_allow_html=True)

# --- INTELLECTUAL PROPERTY NOTICE ---
st.markdown("""
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(5px);
    border-top: 1px solid #334155;
    text-align: center;
    padding: 12px 0;
    z-index: 999;
">
    <p style="color: #94A3B8; font-size: 13px; margin: 0 0 4px 0;">
        <b>© 2026 Muhammad Azrai bin Amir.</b> All Rights Reserved.
    </p>
    <p style="color: #64748B; font-size: 11px; margin: 0; line-height: 1.4;">
        The Azr.AI framework, source code, and visualizations are the intellectual property of the author, developed at IIUM.<br>
        Unauthorized reproduction or distribution of this material is strictly prohibited.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)