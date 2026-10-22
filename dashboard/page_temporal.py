import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('<div class="module-header">MODULE 06 · TEMPORAL</div>', unsafe_allow_html=True)
st.title("Long-term temporal trends")
st.markdown("Decadal shifts in ecological indicators with least-squares trend lines highlighting rate of change per metric.")

with st.container(border=True):
    st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">ANNUAL SUMMARY · 2010 → 2025</div>', unsafe_allow_html=True)
    years = [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024]
    kbi_scores = [0.15, 0.18, 0.22, 0.45, 0.38, 0.42, 0.50, 0.48]
    coral_cover = [45, 44, 43, 35, 38, 36, 34, 33]
    df = pd.DataFrame({"Year": years, "KBI": kbi_scores, "Coral Cover (%)": coral_cover})
    
    fig = px.line(df, x="Year", y=["KBI", "Coral Cover (%)"], markers=True, color_discrete_sequence=["#FF7043", "#00E5FF"])
    
    # UPDATED AXIS STYLING
    fig.update_layout(
        paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(
            showgrid=False,
            title=dict(text="Year", font=dict(color='#64748B', size=14)),
            tickfont=dict(color='#E2E8F0', size=12)
        ),
        yaxis=dict(
            showgrid=True, gridcolor='#1E293B',
            title=dict(text="Metric Value", font=dict(color='#64748B', size=14)),
            tickfont=dict(color='#E2E8F0', size=12)
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#E2E8F0', size=12))
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})