import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('<div class="module-header">MODULE 04 · ENVIRONMENTAL</div>', unsafe_allow_html=True)
st.title("Physicochemical & satellite feeds")
st.markdown("In-situ logger streams fused with satellite-derived sea-surface temperature and current rose diagnostics.")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">SST DISTRIBUTION BY SITE</div>', unsafe_allow_html=True)
        df_sst = pd.DataFrame({'Site': ['Tioman', 'Seri Buat', 'Berhala', 'Raja Muda', 'Balok'], 'SST (°C)': [28.5, 28.7, 29.2, 29.5, 29.8]})
        fig1 = px.box(df_sst, x='Site', y='SST (°C)', color_discrete_sequence=['#00E5FF'])
        
        # UPDATED AXIS STYLING
        fig1.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(
                showgrid=False,
                title=dict(text="Reef Site", font=dict(color='#64748B', size=14)),
                tickfont=dict(color='#E2E8F0', size=12)
            ), 
            yaxis=dict(
                showgrid=True, gridcolor='#1E293B',
                title=dict(text="SST (°C)", font=dict(color='#64748B', size=14)),
                tickfont=dict(color='#E2E8F0', size=12)
            )
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">CURRENT ROSE · DIRECTION × SPEED</div>', unsafe_allow_html=True)
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        speeds = [12, 15, 8, 5, 3, 4, 7, 10]
        fig2 = px.bar_polar(r=speeds, theta=directions, color_discrete_sequence=['#FF7043'])
        
        # UPDATED POLAR AXIS STYLING
        fig2.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            polar=dict(
                bgcolor='#111A22', 
                radialaxis=dict(showline=False, gridcolor='#1E293B', tickfont=dict(color='#E2E8F0', size=12), title=dict(text="Speed (m/s)", font=dict(color='#64748B', size=14))),
                angularaxis=dict(tickfont=dict(color='#E2E8F0', size=12))
            )
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})