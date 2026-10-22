import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import chart_card

st.markdown('<div class="module-header">MODULE 06 · TEMPORAL</div>', unsafe_allow_html=True)
st.title("Long-term temporal trends")
st.markdown("Decadal shifts in ecological indicators with least-squares trend lines highlighting rate of change per metric.")

# 1. DATA (Mock for now, ready for Campaign C2/C3)
years = [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024]
kbi_scores = [0.15, 0.18, 0.22, 0.45, 0.38, 0.42, 0.50, 0.48]
coral_cover = [45, 44, 43, 35, 38, 36, 34, 33]

df = pd.DataFrame({
    "Year": years, 
    "KBI": kbi_scores, 
    "Coral Cover (%)": coral_cover
})

# 2. CREATE CHART WITH SECONDARY Y-AXIS
fig = go.Figure()

# Add Coral Cover trace (Left Y-axis)
fig.add_trace(go.Scatter(
    x=df["Year"], 
    y=df["Coral Cover (%)"], 
    mode='lines+markers', 
    name='Coral Cover (%)',
    line=dict(color='#00E5FF', width=2),
    marker=dict(size=8, color='#00E5FF')
))

# Add KBI trace (Right Y-axis)
fig.add_trace(go.Scatter(
    x=df["Year"], 
    y=df["KBI"], 
    mode='lines+markers', 
    name='KBI (Bleaching Index)',
    line=dict(color='#FF7043', width=2, dash='dot'),
    marker=dict(size=8, color='#FF7043'),
    yaxis='y2' # Assigns this trace to the right axis
))

# 3. LAYOUT AND AXIS STYLING
fig.update_layout(
    paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
    font_color='#E2E8F0', 
    margin=dict(t=10, b=10, l=10, r=10),
    height=500,
    
    # Left Y-axis (Coral Cover)
    yaxis=dict(
        title=dict(text="Coral Cover (%)", font=dict(color='#64748B', size=14)),
        tickfont=dict(color='#E2E8F0', size=12),
        gridcolor='#1E293B',
        showgrid=True,
        range=[0, 50] # Fixed scale for percentage
    ),
    
    # Right Y-axis (KBI)
    yaxis2=dict(
        title=dict(text="KBI Score", font=dict(color='#64748B', size=14)),
        tickfont=dict(color='#E2E8F0', size=12),
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, 1] # Fixed scale for KBI
    ),
    
    # X-axis (Years)
    xaxis=dict(
        title=dict(text="Year", font=dict(color='#64748B', size=14)),
        tickfont=dict(color='#E2E8F0', size=12),
        showgrid=False,
        tickmode='array',
        tickvals=years
    ),
    
    # Legend
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.02, 
        xanchor="right", 
        x=1, 
        font=dict(color='#E2E8F0', size=12)
    )
)

# 4. RENDER WITH CHART CARD
chart_card("ANNUAL SUMMARY · 2010 → 2025", fig, df)