"""
Interactive Dashboard — Azr.AI
Coral reef monitoring visualization with coral-ocean theme.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from pathlib import Path

from src.visualization.dashboard_pages import (
    overview_page,
    distribution_maps_page,
    health_assessment_page,
    connectivity_page,
    temporal_trends_page,
    data_export_page,
)


# Coral-ocean color palette (used in charts)
COLORS = {
    "abyss":     "#0A1929",
    "ocean":     "#132F4C",
    "coral":     "#FF7043",
    "teal":      "#4DD0E1",
    "kelp":      "#66BB6A",
    "sand":      "#FFB74D",
    "bleached":  "#E57373",
    "foam":      "#F5F7FA",
    "mist":      "#B0BEC5",
    "line":      "#1E3A5F",
}


def load_theme():
    """Load custom CSS theme."""
    css_path = Path(__file__).parent / "theme.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Azr.AI — Coral Reef Monitoring",
        page_icon="🪸",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_theme()

    # Header with gradient
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #FF7043 0%, #4DD0E1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0;
        ">
            🪸 Azr.AI — Coral Reef Monitoring
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='color: #B0BEC5; margin-top: 0;'>"
        "Automated Zonation & Reef Artificial Intelligence — "
        "Kuantan Coastal Waters, Pahang, Malaysia"
        "</p>",
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    st.sidebar.markdown(
        "<h3 style='color: #FF7043;'>Navigation</h3>",
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio(
        "Select View",
        [
            "Overview",
            "Distribution Maps",
            "Health Assessment",
            "Connectivity",
            "Temporal Trends",
            "Data Export",
        ],
        label_visibility="collapsed",
    )

    # Footer brand
    st.sidebar.markdown(
        "<hr style='border-color: #1E3A5F;'>"
        "<p style='color: #B0BEC5; font-size: 0.75rem;'>"
        "Azr.AI v0.1.0<br>"
        "Muhammad Azrai bin Amir<br>"
        "IIUM · 2026"
        "</p>",
        unsafe_allow_html=True,
    )

    # Route to selected page
    if page == "Overview":
        overview_page()
    elif page == "Distribution Maps":
        distribution_maps_page()
    elif page == "Health Assessment":
        health_assessment_page()
    elif page == "Connectivity":
        connectivity_page()
    elif page == "Temporal Trends":
        temporal_trends_page()
    elif page == "Data Export":
        data_export_page()


if __name__ == "__main__":
    main()