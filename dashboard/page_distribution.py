import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('<div class="module-header">MODULE 02 · DISTRIBUTION</div>', unsafe_allow_html=True)
st.title("Spatial distribution maps")
st.markdown("Geo-referenced coral cover and density across the surveyed reefs. Toggle layers for choropleth and point density.")

col_map, col_stats = st.columns([3, 1])

with col_map:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">REEF SITES · CHOROPLETH + HEATMAP</div>', unsafe_allow_html=True)
        map_data = pd.DataFrame({
            'lat': [2.8, 2.7, 3.2, 3.6, 3.8],
            'lon': [104.1, 103.9, 103.6, 103.4, 103.3],
            'site': ['Pulau Tioman', 'Pulau Seri Buat', 'Pulau Berhala', 'Raja Muda', 'Balok']
        })
        fig = px.scatter_map(map_data, lat="lat", lon="lon", hover_name="site", 
                             zoom=7, height=500, color_discrete_sequence=["#00E5FF"])
        fig.update_layout(
            map_style="carto-darkmatter",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='#111A22'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_stats:
    st.markdown('''
    <div class="panel">
        <div class="panel-title">SITE INDEX</div>
        <br>
        <p><b>5</b> active sites</p>
        <p><b>263</b> colonies mapped</p>
        <p><b>C1</b> survey campaign</p>
    </div>
    ''', unsafe_allow_html=True)