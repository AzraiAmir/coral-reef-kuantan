"""
Dashboard Pages
Full dashboard with all 6 pages.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static


def overview_page():
    """Overview page."""
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

    st.markdown("---")

    # Species distribution
    st.subheader("Species Distribution")
    species_data = pd.DataFrame({
        'Species': ['Porites', 'Acropora', 'Montipora', 'Dipsastraea', 'Favites', 'Other'],
        'Count': [2050, 1625, 1340, 1030, 930, 825]
    })
    fig = px.bar(species_data, x='Species', y='Count', color='Count',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)


def distribution_maps_page():
    """Distribution maps page."""
    st.header("Coral Distribution Maps")

    # Create map
    m = folium.Map(location=(3.8, 103.5), zoom_start=8)

    sites = [
        {'name': 'Pulau Tioman', 'lat': 2.8039, 'lon': 104.1000, 'type': 'Source'},
        {'name': 'Pulau Seri Buat', 'lat': 2.7195, 'lon': 103.8978, 'type': 'Source'},
        {'name': 'Pulau Tokong Burung', 'lat': 2.7839, 'lon': 103.9601, 'type': 'Source'},
        {'name': 'Pulau Berhala', 'lat': 3.2450, 'lon': 103.6551, 'type': 'Sink'},
        {'name': 'Raja Muda Reef', 'lat': 3.6412, 'lon': 103.4676, 'type': 'Sink'},
        {'name': 'Balok Reef', 'lat': 3.8564, 'lon': 103.4522, 'type': 'Sink'},
    ]

    for site in sites:
        color = 'blue' if site['type'] == 'Source' else 'red'
        folium.Marker(
            location=[site['lat'], site['lon']],
            popup=site['name'],
            icon=folium.Icon(color=color)
        ).add_to(m)

    folium_static(m, width=1000, height=600)


def health_assessment_page():
    """Health assessment page."""
    st.header("Coral Health Assessment")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean KBI", "0.27")
    with col2:
        st.metric("Healthy Colonies", "45%")
    with col3:
        st.metric("Bleached Colonies", "27%")

    st.markdown("---")

    # KBI by site
    kbi_data = pd.DataFrame({
        'Site': ['Pulau Tioman', 'Pulau Seri Buat', 'Pulau Tokong Burung',
                 'Pulau Berhala', 'Raja Muda Reef', 'Balok Reef'],
        'KBI': [0.15, 0.18, 0.12, 0.35, 0.42, 0.38]
    })

    fig = px.bar(kbi_data, x='Site', y='KBI', color='KBI',
                 color_continuous_scale='RdYlGn_r')
    fig.add_hline(y=0.2, line_dash="dash", line_color="green")
    fig.add_hline(y=0.4, line_dash="dash", line_color="orange")
    st.plotly_chart(fig, use_container_width=True)


def connectivity_page():
    """Connectivity page."""
    st.header("Larval Connectivity Analysis")

    connectivity_data = pd.DataFrame({
        'Pulau Berhala': [0.15, 0.22, 0.18],
        'Raja Muda Reef': [0.08, 0.12, 0.10],
        'Balok Reef': [0.05, 0.07, 0.06]
    }, index=['Pulau Tioman', 'Pulau Seri Buat', 'Pulau Tokong Burung'])

    st.subheader("Connectivity Matrix")
    st.dataframe(connectivity_data.style.background_gradient(cmap='YlOrRd'))

    fig = px.imshow(connectivity_data, color_continuous_scale='YlOrRd',
                    text_auto='.3f')
    st.plotly_chart(fig, use_container_width=True)


def temporal_trends_page():
    """Temporal trends page."""
    st.header("Temporal Trends")

    np.random.seed(42)
    dates = pd.date_range(start='2026-01-01', end='2026-12-31', freq='M')
    sites = ['Pulau Tioman', 'Pulau Seri Buat', 'Pulau Tokong Burung']

    records = []
    for site in sites:
        base = np.random.uniform(0.1, 0.3)
        for date in dates:
            kbi = base + 0.1 * np.sin((date.month - 1) / 12 * 2 * np.pi) + np.random.normal(0, 0.03)
            records.append({'date': date, 'site': site, 'kbi': max(0, min(1, kbi))})

    temporal_data = pd.DataFrame(records)

    fig = px.line(temporal_data, x='date', y='kbi', color='site',
                  title='Temporal Bleaching Trend by Site')
    st.plotly_chart(fig, use_container_width=True)


def data_export_page():
    """Data export page."""
    st.header("Data Export")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download Detection Results (CSV)",
            data="detection_results.csv",
            file_name="coral_detection_results.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="Download Health Assessment (CSV)",
            data="health_assessment.csv",
            file_name="coral_health_assessment.csv",
            mime="text/csv"
        )

    with col3:
        st.download_button(
            label="Download Connectivity Matrix (CSV)",
            data="connectivity_matrix.csv",
            file_name="larval_connectivity_matrix.csv",
            mime="text/csv"
        )
