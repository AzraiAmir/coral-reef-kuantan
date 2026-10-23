import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 04 · ENVIRONMENTAL</div>', unsafe_allow_html=True)
st.title("Physicochemical & satellite feeds")
st.markdown("In-situ logger streams fused with satellite-derived sea-surface temperature and current rose diagnostics.")

# --- GENERATE DYNAMIC MOCK DATA ---
site_summary_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\site_summary.csv")
if site_summary_path.exists():
    df_sites = pd.read_csv(site_summary_path)
    site_list = df_sites.iloc[:, 0].tolist()
    num_sites = len(site_list)
else:
    site_list = ['Tioman', 'Seri Buat', 'Berhala', 'Raja Muda', 'Balok']
    num_sites = 5

np.random.seed(num_sites) 
sst_data = {'Site': site_list}
for i in range(5): 
    sst_data[f'Run_{i}'] = np.random.normal(loc=28.5 + (num_sites * 0.1), scale=0.3, size=num_sites)

df_sst = pd.DataFrame(sst_data).melt(id_vars='Site', var_name='Run', value_name='SST (°C)')

col1, col2 = st.columns(2, vertical_alignment="top")

# --- LEFT BOX ---
with col1:
    # Reduced to 420px to fit on screen
    with st.container(border=True, height=420):
        fig1 = px.box(df_sst, x='Site', y='SST (°C)', color_discrete_sequence=['#00E5FF'])
        
        fig1.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(showgrid=False, title=dict(text="Reef Site", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)), 
            yaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="SST (°C)", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)),
            height=340
        )
        
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">SST DISTRIBUTION BY SITE</div>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

# --- RIGHT BOX ---
with col2:
    with st.container(border=True, height=420):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        speeds = np.random.randint(3, 18, size=8).tolist() 
        df_rose = pd.DataFrame({'Direction': directions, 'Speed': speeds})
        
        fig2 = px.bar_polar(
            df_rose, r='Speed', theta='Direction', color='Speed', 
            color_continuous_scale=['#005B66', '#00E5FF', '#FF7043', '#E57373'] 
        )
        
        fig2.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', 
            margin=dict(t=40, b=20, l=40, r=40),
            polar=dict(
                bgcolor='#111A22', 
                radialaxis=dict(showline=False, showticklabels=True, gridcolor='#334155', tickfont=dict(color='#E2E8F0', size=10), angle=45, tickangle=0, range=[0, 20]), 
                angularaxis=dict(tickfont=dict(color='#E2E8F0', size=14, family="Space Mono"), gridcolor='#1E293B')
            ),
            coloraxis_showscale=False,
            height=340
        )
        
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">CURRENT ROSE · DIRECTION × SPEED</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        # Adjusted legend margin to match new height
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.75rem; font-family: 'Inter', sans-serif; padding-bottom: 5px; color: #B0BEC5; margin-top: -35px; position: relative; z-index: 10;">
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #005B66; border-radius: 2px;"></div> Slow</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #00E5FF; border-radius: 2px;"></div> Moderate</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #FF7043; border-radius: 2px;"></div> Fast</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #E57373; border-radius: 2px;"></div> Very Fast</div>
        </div>
        """, unsafe_allow_html=True)