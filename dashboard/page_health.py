import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 03 · HEALTH</div>', unsafe_allow_html=True)
st.title("Health & bleaching assessment")
st.markdown("Bleaching severity index (KBI 0–4 scale) over time, with distribution of observed severity classes and per-site stress diagnostics.")

# 1. LOAD REAL DATA
crca_dir = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\crca")
data = []

if crca_dir.exists():
    for file in crca_dir.glob("*.json"):
        try:
            with open(file, "r") as f:
                d = json.load(f)
                data.append({
                    "image": d.get("image", "Unknown"),
                    "species": d.get("class", "Unknown"),
                    "paleness": d.get("paleness", 0)
                })
        except Exception:
            pass

df = pd.DataFrame(data)

# KPI Stats
total_colonies = len(df)
mean_kbi = df['paleness'].mean() if not df.empty else 0
high_risk = len(df[df['paleness'] > 0.6]) if not df.empty else 0

# 2. KPI CARDS
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="panel"><div class="panel-title">TOTAL COLONIES ASSESSED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FF7043;">{total_colonies}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="panel"><div class="panel-title">MEAN BLEACHING INDEX</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FFB74D;">{mean_kbi:.2f}</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="panel"><div class="panel-title">COLONIES AT RISK (&gt;0.6)</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#E57373;">{high_risk}</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. CHARTS
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    if not df.empty:
        counts, bins = pd.cut(df['paleness'], bins=20, retbins=True, include_lowest=True)
        hist_counts = counts.value_counts().sort_index()
        bin_centers = [(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)]
        
        df_hist = pd.DataFrame({"Paleness Bin Center": bin_centers, "Colony Count": hist_counts.values})
        
        fig1 = go.Figure()

        fig1.add_trace(go.Bar(
            x=bin_centers,
            y=hist_counts.values,
            width=[bins[i+1]-bins[i] for i in range(len(bins)-1)],
            marker=dict(
                color=bin_centers,
                colorscale=[
                    [0.0, '#66BB6A'], [0.2, '#66BB6A'],
                    [0.2, '#FFB74D'], [0.4, '#FFB74D'],
                    [0.4, '#FF7043'], [0.6, '#FF7043'],
                    [0.6, '#E57373'], [1.0, '#E57373']
                ],
                cmin=0, cmax=1
            ),
            showlegend=False
        ))

        legend_items = [
            ("Healthy (0.0 - 0.2)", "#66BB6A"),
            ("Moderate (0.2 - 0.4)", "#FFB74D"),
            ("High (0.4 - 0.6)", "#FF7043"),
            ("Severe (0.6+)", "#E57373")
        ]
        
        for name, color in legend_items:
            fig1.add_trace(go.Scatter(
                x=[None], y=[None], 
                mode='markers', 
                marker=dict(size=10, color=color, symbol='square'),
                name=name,
                showlegend=True
            ))

        fig1.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
            font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(showgrid=False, title=dict(text="Paleness Score", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12), range=[0, 0.8]), 
            yaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="Colony Count", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color='#E2E8F0', size=12), bgcolor='rgba(0,0,0,0)'),
            height=350
        )
        
        chart_card("BLEACHING SEVERITY DISTRIBUTION", fig1, df_hist)
    else:
        st.error("No data found.")

with col_chart2:
    if not df.empty:
        df_species = df.groupby('species').agg(Mean_Paleness=('paleness', 'mean'), Count=('paleness', 'count')).reset_index()
        
        fig2 = px.box(df, x="species", y="paleness", color="species", color_discrete_sequence=['#FF7043', '#00E5FF'])
        
        fig2.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
            font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(showgrid=False, title=dict(text="", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)), 
            yaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="Paleness", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)),
            legend=dict(font=dict(color='#E2E8F0', size=12)),
            height=320
        )
        
        chart_card("OBSERVED SEVERITY BY SPECIES", fig2, df_species)
    else:
        st.error("No data found.")