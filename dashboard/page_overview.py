import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('<div class="module-header">MODULE 01 · OVERVIEW</div>', unsafe_allow_html=True)
st.title("Reef network pulse")
st.markdown("Aggregated indicators across monitoring sites. Updated continuously from in-situ loggers and satellite feeds.")

# KPI Panels
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="panel"><div class="panel-title">TOTAL COLONIES DETECTED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FF7043;">263</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="panel"><div class="panel-title">MEAN BLEACHING INDEX (KBI)</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FFB74D;">0.50</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="panel"><div class="panel-title">SITES MONITORED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#4DD0E1;">1</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">KBI HEATMAP · INDICATORS × SITES</div>', unsafe_allow_html=True)
        sites = ["Pulau Tioman", "Pulau Seri Buat", "Raja Muda"]
        health_scores = [0.15, 0.22, 0.55]
        fig1 = px.bar(x=sites, y=health_scores, color=health_scores, color_continuous_scale=[(0.0, '#66BB6A'), (0.5, '#FFB74D'), (1.0, '#E57373')])
        
        # UPDATED AXIS STYLING
        fig1.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', showlegend=False, margin=dict(t=10, b=10, l=10, r=10), 
            xaxis=dict(
                showgrid=False, 
                title=dict(text="Reef Site", font=dict(color='#64748B', size=14)),
                tickfont=dict(color='#E2E8F0', size=12)
            ), 
            yaxis=dict(
                showgrid=True, gridcolor='#1E293B',
                title=dict(text="KBI Score", font=dict(color='#64748B', size=14)),
                tickfont=dict(color='#E2E8F0', size=12)
            )
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with col_chart2:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">SPECIES DISTRIBUTION</div>', unsafe_allow_html=True)
        species_df = pd.DataFrame({"Species": ["Dipsastraea", "Porites", "Acropora"], "Count": [107, 77, 45]})
        fig2 = px.pie(species_df, values='Count', names='Species', color='Species', color_discrete_sequence=['#00E5FF', '#FF7043', '#64748B'], hole=0.4)
        
        # UPDATED LEGEND/TEXT STYLING (Pie charts don't have X/Y axes, but we can style the legend)
        fig2.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(font=dict(color='#E2E8F0', size=12))
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})