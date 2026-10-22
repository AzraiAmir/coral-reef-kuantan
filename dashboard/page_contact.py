import streamlit as st
import textwrap

st.markdown('<div class="module-header">MODULE 08 · CONTACT</div>', unsafe_allow_html=True)
st.title("Contact Us")
st.markdown("For inquiries regarding the Azr.AI Coral Reef Monitoring project, please reach out to the research team.")

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 1: PRINCIPAL INVESTIGATOR ---
with st.container(border=False):
    html_pi = """
    <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 30px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 20px; flex: 1;">
            <div style="color: #00E5FF;">
                <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <h2 style="margin: 0; color: #00E5FF; font-family: 'Space Mono', monospace; font-size: 1.5rem;">Muhammad Azrai bin Amir</h2>
        </div>
        <div style="width: 1px; height: 90px; background-color: #334155; margin: 0 30px;"></div>
        <div style="text-align: left; flex: 1.5;">
            <p style="margin: 0 0 8px 0; color: #94A3B8; font-size: 18px;">Principal Investigator / PhD Candidate</p>
            <p style="margin: 0 0 15px 0; color: #64748B; font-size: 16px;">International Islamic University Malaysia (IIUM)</p>
            <p style="margin: 0; font-size: 16px; color: #E2E8F0;"><b>📧 Email:</b> <a href="mailto:azrai_amir@live.iium.edu.my" style="color: #FF7043; text-decoration: none;">azrai_amir@live.iium.edu.my</a></p>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html_pi), unsafe_allow_html=True)

# --- ROW 2: SUPERVISORS (Side by Side) ---
col1, col2 = st.columns(2)

with col1:
    # Set a fixed height so both cards match perfectly
    with st.container(border=False, height=220):
        html_sup1 = """
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 25px 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 15px; flex: 1.2;">
                <div style="color: #FFB74D;">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <h3 style="margin: 0; color: #FFB74D; font-family: 'Space Mono', monospace; font-size: 1.1rem; line-height: 1.3;">Prof. Ir. Dr. Siti Fauziah Binti Toha@Tohara</h3>
            </div>
            <div style="width: 1px; height: 100px; background-color: #334155; margin: 0 20px;"></div>
            <div style="text-align: left; flex: 1.5;">
                <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 16px;">Professor</p>
                <p style="margin: 0 0 15px 0; color: #64748B; font-size: 15px;">Department of Mechatronics, Kulliyyah of Engineering, IIUM</p>
                <p style="margin: 0; font-size: 15px; color: #E2E8F0;"><b>📧 Email:</b> <br><a href="mailto:tsfauziah@iium.edu.my" style="color: #FF7043; text-decoration: none;">tsfauziah@iium.edu.my</a></p>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(html_sup1), unsafe_allow_html=True)

with col2:
    # Set the same fixed height here
    with st.container(border=False, height=220):
        html_sup2 = """
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; display: flex; align-items: center; padding: 25px 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 15px; flex: 1.2;">
                <div style="color: #AB47BC;">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <h3 style="margin: 0; color: #AB47BC; font-family: 'Space Mono', monospace; font-size: 1.1rem; line-height: 1.3;">Dr. Muhammad Faiz Bin Mohd Hanapiah</h3>
            </div>
            <div style="width: 1px; height: 100px; background-color: #334155; margin: 0 20px;"></div>
            <div style="text-align: left; flex: 1.5;">
                <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 16px;">Co-Supervisor / Marine Biologist</p>
                <p style="margin: 0 0 15px 0; color: #64748B; font-size: 15px;">Department of Marine Science, Kulliyyah of Science, IIUM</p>
                <p style="margin: 0; font-size: 15px; color: #E2E8F0;"><b>📧 Email:</b> <br><a href="mailto:faizhanapiah@iium.edu.my" style="color: #FF7043; text-decoration: none;">faizhanapiah@iium.edu.my</a></p>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(html_sup2), unsafe_allow_html=True)

# --- INTELLECTUAL PROPERTY NOTICE ---
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px; border-top: 1px solid #334155; margin-top: 30px; background-color: #0F172A; border-radius: 8px;">
    <p style="color: #94A3B8; font-size: 14px; margin-bottom: 5px;">
        <b>© 2026 Muhammad Azrai bin Amir.</b> All Rights Reserved.
    </p>
    <p style="color: #64748B; font-size: 12px; margin: 0;">
        The Azr.AI framework, source code, and visualizations are the intellectual property of the author.<br>
        Developed at the International Islamic University Malaysia (IIUM).<br>
        Unauthorized reproduction or distribution of this material is strictly prohibited.
    </p>
</div>
""", unsafe_allow_html=True)