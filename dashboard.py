"""
Interactive Dashboard
Streamlit application for visualizing coral reef monitoring results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static


def main():
    st.set_page_config(
        page_title="Coral Reef Monitoring Dashboard",
        page_icon="🪸",
        layout="wide"
    )

    st.title("🪸 Coral Reef Monitoring Dashboard")
    st.markdown("### Kuantan Coastal Waters, Pahang, Malaysia")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Distribution Maps", "Health Assessment",
         "Connectivity", "Temporal Trends", "Data Export"]
    )

    if page == "Overview":
        st.header("Research Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Images Analyzed", "19,500")
        with col2:
            st.metric("Coral Species Detected", "33")
        with col3:
            st.metric("Mean Bleaching Index", "0.27")
        with col4:
            st.metric("Connectivity Score", "0.67")


if __name__ == "__main__":
    main()
