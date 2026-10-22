import streamlit.components.v1 as components
import base64
from pathlib import Path

def render_sidebar(active_page="Overview"):
    # Read the logo
    logo_path = Path(__file__).parent / "assets" / "logo_full.png"
    logo_b64 = ""
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

    # Helper to set the active class
    def get_class(page_name):
        return "nav-item active" if page_name == active_page else "nav-item"

    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');
        
        body {{ margin: 0; padding: 0; background: transparent; }}
        
        #sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 280px;
            background-color: #132F4C;
            border-right: 1px solid #1E3A5F;
            display: flex;
            flex-direction: column;
            transition: width 0.3s ease;
            font-family: 'Inter', sans-serif;
            z-index: 999999;
        }}

        #sidebar.collapsed {{
            width: 80px;
        }}

        #logo-container {{
            padding: 20px;
            text-align: center;
            height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: height 0.3s ease;
        }}

        #logo-container img {{
            width: 160px;
            transition: opacity 0.3s ease;
        }}

        #sidebar.collapsed #logo-container img {{
            display: none;
        }}

        #nav-container {{
            flex-grow: 1;
            padding: 0 15px;
            overflow: hidden;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 5px;
            border-radius: 6px;
            color: #B0BEC5;
            text-decoration: none;
            transition: background 0.2s;
            white-space: nowrap;
        }}

        .nav-item:hover {{ background-color: #1E3A5F; color: #F5F7FA; }}
        .nav-item.active {{ background-color: #FF7043; color: white; }}

        .nav-icon {{ font-size: 1.2rem; margin-right: 15px; min-width: 24px; text-align: center; }}
        .nav-text {{ font-size: 1rem; font-weight: 500; }}
        
        #sidebar.collapsed .nav-text {{
            display: none;
        }}

        #sidebar.collapsed .nav-item {{
            justify-content: center;
        }}

        #sidebar.collapsed .nav-icon {{
            margin-right: 0;
        }}

        #version-text {{
            text-align: center;
            color: #B0BEC5;
            font-size: 0.8rem;
            padding: 20px;
            border-top: 1px solid #1E3A5F;
            white-space: nowrap;
        }}

        #sidebar.collapsed #version-text {{
            font-size: 0;
        }}

        #sidebar.collapsed #version-text::after {{
            content: "v1.0";
            font-size: 0.8rem;
        }}

        #toggle-btn {{
            position: absolute;
            top: 20px;
            right: -15px;
            background-color: #FF7043;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            font-weight: bold;
        }}
    </style>

    <div id="sidebar">
        <button id="toggle-btn" onclick="toggleSidebar()">«</button>
        
        <div id="logo-container">
            <img src="data:image/png;base64,{logo_b64}">
        </div>

        <div id="nav-container">
            <a href="/" target="_self" class="{get_class('Overview')}">
                <span class="nav-icon">🏠</span><span class="nav-text">Overview</span>
            </a>
            <a href="/Upload" target="_self" class="{get_class('Upload')}">
                <span class="nav-icon">📤</span><span class="nav-text">Upload & Process</span>
            </a>
            <a href="/Distribution" target="_self" class="{get_class('Distribution')}">
                <span class="nav-icon">🗺️</span><span class="nav-text">Distribution Maps</span>
            </a>
            <a href="/Health" target="_self" class="{get_class('Health')}">
                <span class="nav-icon">🩺</span><span class="nav-text">Health Assessment</span>
            </a>
            <a href="/Environment" target="_self" class="{get_class('Environment')}">
                <span class="nav-icon">🌡️</span><span class="nav-text">Environment</span>
            </a>
            <a href="/Connectivity" target="_self" class="{get_class('Connectivity')}">
                <span class="nav-icon">🕸️</span><span class="nav-text">Connectivity</span>
            </a>
        </div>

        <div id="version-text">v1.0.0 | PhD Research</div>
    </div>

    <script>
        function toggleSidebar() {{
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('collapsed');
            const btn = document.getElementById('toggle-btn');
            btn.innerText = sidebar.classList.contains('collapsed') ? '»' : '«';
        }}
    </script>
    """
    components.html(html, height=0, width=0)