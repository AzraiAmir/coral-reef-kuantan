import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 04 · ENVIRONMENTAL</div>', unsafe_allow_html=True)
st.title("Physicochemical & satellite feeds")
st.markdown("In-situ logger streams fused with satellite-derived sea-surface temperature and current rose diagnostics.")

# Generate Mock Sites
site_list = ['Tioman', 'Seri Buat', 'Berhala', 'Raja Muda', 'Balok']
num_sites = 5

# ==========================================
# SECTION 1: SST & ROSE (Real/Mock Layout)
# ==========================================
col1, col2 = st.columns(2, vertical_alignment="top")
with col1:
    with st.container(border=True, height=400):
        np.random.seed(42)
        df_sst = pd.DataFrame({'Site': site_list, 'SST': np.random.normal(29, 0.5, num_sites)})
        fig1 = px.box(df_sst, x='Site', y='SST', color_discrete_sequence=['#00E5FF'])
        fig1.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#1E293B'), height=320)
        chart_card("SST DISTRIBUTION [MOCK DATA]", fig1, df_sst)

with col2:
    with st.container(border=True, height=400):
        df_rose = pd.DataFrame({'Direction': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], 'Speed': np.random.randint(3, 18, 8)})
        fig2 = px.bar_polar(df_rose, r='Speed', theta='Direction', color='Speed', color_continuous_scale=['#005B66', '#00E5FF', '#FF7043', '#E57373'])
        fig2.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=40, b=20, l=40, r=40), polar=dict(bgcolor='#111A22', radialaxis=dict(showline=False, gridcolor='#334155'), angularaxis=dict(gridcolor='#1E293B')), coloraxis_showscale=False, height=320)
        chart_card("CURRENT ROSE [MOCK DATA]", fig2, df_rose)

# ==========================================
# SECTION 2: MISSING IN-SITU CHARTS
# ==========================================
st.markdown("### <span style='color:#FFB74D'>◈ In-Situ Physicochemical Parameters</span>", unsafe_allow_html=True)
col3, col4 = st.columns(2, vertical_alignment="top")

with col3:
    with st.container(border=True, height=350):
        df_temp = pd.DataFrame({'Time': pd.date_range(start='2024-01-01', periods=30), 'Temperature': np.random.normal(28.5, 1, 30)})
        fig3 = px.line(df_temp, x='Time', y='Temperature', color_discrete_sequence=['#FF7043'])
        fig3.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#1E293B'), height=280)
        chart_card("TEMPERATURE TIME-SERIES [MOCK DATA]", fig3, df_temp)

with col4:
    with st.container(border=True, height=350):
        df_turb = pd.DataFrame(np.random.rand(5, 5), columns=['S1','S2','S3','S4','S5'], index=['Jan','Feb','Mar','Apr','May'])
        fig4 = px.imshow(df_turb, text_auto=".2f", color_continuous_scale='Teal')
        fig4.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), height=280)
        chart_card("TURBIDITY HEATMAP [MOCK DATA]", fig4, df_turb)

# ==========================================
# SECTION 3: MISSING SATELLITE/HYDRO CHARTS
# ==========================================
st.markdown("### <span style='color:#AB47BC'>◈ Satellite & Hydrodynamic Parameters</span>", unsafe_allow_html=True)
col5, col6 = st.columns(2, vertical_alignment="top")

with col5:
    with st.container(border=True, height=350):
        x, y = np.mgrid[-5:5:100j, -5:5:100j]
        z = np.sin(np.sqrt(x**2 + y**2))
        fig5 = go.Figure(data=go.Contour(z=z, colorscale='Blues'))
        fig5.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), height=280)
        chart_card("DO CONTOUR MAP [MOCK DATA]", fig5)

with col6:
    with st.container(border=True, height=350):
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=[1, 2], y=[1, 2], mode='lines+markers', line=dict(color='#00E5FF'), marker=dict(symbol='arrow', size=15, angleref='previous')))
        fig6.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), height=280)
        chart_card("CURRENT VECTOR MAP [MOCK DATA]", fig6)