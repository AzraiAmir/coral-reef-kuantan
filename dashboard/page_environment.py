import streamlit as st
import pandas as pd
import plotly.express as px
from utils import chart_card

st.markdown('<div class="module-header">MODULE 04 · ENVIRONMENTAL</div>', unsafe_allow_html=True)
st.title("Physicochemical & satellite feeds")
st.markdown("In-situ logger streams fused with satellite-derived sea-surface temperature and current rose diagnostics.")

col1, col2 = st.columns(2)

with col1:
    # 1. CREATE DATA AND CHART FIRST
    df_sst = pd.DataFrame({'Site': ['Tioman', 'Seri Buat', 'Berhala', 'Raja Muda', 'Balok'], 'SST (°C)': [28.5, 28.7, 29.2, 29.5, 29.8]})
    fig1 = px.box(df_sst, x='Site', y='SST (°C)', color_discrete_sequence=['#00E5FF'])
    
    fig1.update_layout(
        paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, title=dict(text="Reef Site", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)), 
        yaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="SST (°C)", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)),
        height=400
    )

    # 2. NOW BUILD THE CARD
    with st.container(border=True, height=520):
        with st.container(horizontal=True, vertical_alignment="center"):
            st.markdown('<div class="panel-title" style="margin: 0; padding-top: 10px;">SST DISTRIBUTION BY SITE</div>', unsafe_allow_html=True)
            st.space("stretch")
            
            with st.popover("⚙", help="Chart Options"):
                img_bytes = fig1.to_image(format="png", width=1200, height=800)
                st.download_button(
                    label="↓&nbsp;&nbsp;&nbsp;Download PNG",
                    data=img_bytes,
                    file_name="sst_distribution.png",
                    mime="image/png",
                    use_container_width=True,
                    key="png_sst"
                )
                csv = df_sst.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="▤&nbsp;&nbsp;&nbsp;Download CSV",
                    data=csv,
                    file_name="sst_distribution.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="csv_sst"
                )

        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with col2:
    # 1. CREATE DATA AND CHART FIRST
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    speeds = [12, 15, 8, 5, 3, 4, 7, 10]
    df_rose = pd.DataFrame({'Direction': directions, 'Speed': speeds})
    
    fig2 = px.bar_polar(
        df_rose, 
        r='Speed', 
        theta='Direction', 
        color='Speed', 
        color_continuous_scale=['#005B66', '#00E5FF', '#FF7043', '#E57373'] 
    )
    
    fig2.update_layout(
        paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', 
        margin=dict(t=10, b=10, l=10, r=10),
        polar=dict(
            bgcolor='#111A22', 
            radialaxis=dict(showline=False, showticklabels=False, gridcolor='#334155'), 
            angularaxis=dict(tickfont=dict(color='#E2E8F0', size=14, family="Space Mono"), gridcolor='#1E293B')
        ),
        coloraxis_showscale=False,
        height=400
    )

    # 2. NOW BUILD THE CARD
    with st.container(border=True, height=520):
        with st.container(horizontal=True, vertical_alignment="center"):
            st.markdown('<div class="panel-title" style="margin: 0; padding-top: 10px;">CURRENT ROSE · DIRECTION × SPEED</div>', unsafe_allow_html=True)
            st.space("stretch")
            
            with st.popover("⚙", help="Chart Options"):
                img_bytes = fig2.to_image(format="png", width=1200, height=800)
                st.download_button(
                    label="↓&nbsp;&nbsp;&nbsp;Download PNG",
                    data=img_bytes,
                    file_name="current_rose.png",
                    mime="image/png",
                    use_container_width=True,
                    key="png_rose"
                )
                csv = df_rose.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="▤&nbsp;&nbsp;&nbsp;Download CSV",
                    data=csv,
                    file_name="current_rose.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="csv_rose"
                )

        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        # Legend inside the card
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.75rem; font-family: 'Inter', sans-serif; padding-bottom: 10px; color: #B0BEC5; margin-top: -10px;">
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #005B66; border-radius: 2px;"></div> Slow (0-5 m/s)</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #00E5FF; border-radius: 2px;"></div> Moderate (5-10 m/s)</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #FF7043; border-radius: 2px;"></div> Fast (10-15 m/s)</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: #E57373; border-radius: 2px;"></div> Very Fast (15+ m/s)</div>
        </div>
        """, unsafe_allow_html=True)