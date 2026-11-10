import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
import numpy as np
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 05 · CONNECTIVITY</div>', unsafe_allow_html=True)
st.title("Source-sink dynamics")
st.markdown("Modelled larval connectivity between reef nodes. Edges indicate exchange probability; node colour denotes dominant role.")

# 1. LOAD REAL DATA
BASE_DIR = Path(__file__).parent
matrix_path = BASE_DIR / "data" / "connectivity_matrix.csv"
dpi_path = BASE_DIR / "data" / "dpi.json"

df_matrix = pd.DataFrame()
dpi_data = {}

if matrix_path.exists():
    df_matrix = pd.read_csv(matrix_path, index_col=0)

if dpi_path.exists():
    with open(dpi_path, "r") as f:
        dpi_data = json.load(f)

col1, col2 = st.columns([1.5, 1], vertical_alignment="top")

# --- LEFT COLUMN: NETWORK GRAPH ---
with col1:
    with st.container(border=True, height=560):
        if not df_matrix.empty:
            G = nx.DiGraph()
            sources = df_matrix.index.tolist()
            sinks = df_matrix.columns.tolist()
            
            for node in set(sources + sinks):
                G.add_node(node)
                
            for source in sources:
                for sink in sinks:
                    weight = df_matrix.loc[source, sink]
                    if weight > 0.05:
                        G.add_edge(source, sink, weight=weight)

            pos = nx.circular_layout(G)
            
            edge_x, edge_y = [], []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color='#64748B'), hoverinfo='none', mode='lines')

            node_x, node_y, node_text, node_color = [], [], [], []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                
                clean_name = node.replace("_", " ")
                if " " in clean_name:
                    parts = clean_name.split(" ", 1)
                    display_text = f"<span style='text-align:center'>{parts[0]}<br>{parts[1]}</span>"
                else:
                    display_text = f"<span style='text-align:center'>{clean_name}</span>"
                    
                node_text.append(display_text)
                node_color.append('#00E5FF' if node in sources else '#FF7043')

            node_trace = go.Scatter(
                x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="bottom center",
                textfont=dict(size=11, color='#E2E8F0'), hoverinfo='text',
                marker=dict(showscale=False, color=node_color, size=20, line_width=2, line_color='#111A22'))

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                showlegend=False, hovermode='closest', margin=dict(b=40, l=20, r=20, t=20), 
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', height=480))
            
            st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">NETWORK GRAPH · LARVAL FLOW</div>', unsafe_allow_html=True)
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True, 
                'displaylogo': False, 
                'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'], 
                'modeBarButtonsToAdd': ['resetScale2d']
            })

# --- RIGHT COLUMN: DPI BAR CHART ---
with col2:
    with st.container(border=True, height=560):
        if dpi_data:
            dpi_df = pd.DataFrame(list(dpi_data.items()), columns=['Site', 'DPI'])
            dpi_df['Site'] = dpi_df['Site'].str.replace("_", " ")
            dpi_df = dpi_df.sort_values(by='DPI', ascending=True)
            dpi_df['Role'] = dpi_df['Site'].apply(lambda x: 'Source (MPA)' if x == 'Pulau Tioman' else 'Sink (Nearshore)')
            
            fig_dpi = px.bar(dpi_df, x='DPI', y='Site', orientation='h', color='Role', color_discrete_map={'Source (MPA)': '#00E5FF', 'Sink (Nearshore)': '#FF7043'})
            
            fig_dpi.update_layout(
                paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
                font_color='#E2E8F0', 
                margin=dict(t=20, b=10, l=10, r=40), 
                xaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="DPI Score", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12), range=[0, 1.15]), 
                yaxis=dict(showgrid=False, title="", tickfont=dict(color='#E2E8F0', size=12)),
                height=480, 
                showlegend=False,
                bargap=0.3 
            )
            
            fig_dpi.update_traces(texttemplate='%{x:.2f}', textposition='outside', textfont_color='#E2E8F0', textfont_size=12, cliponaxis=False)
            
            st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">DISPERSAL POTENTIAL INDEX</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_dpi, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("dpi.json not found in the data folder.")

st.markdown("<br>", unsafe_allow_html=True)

# --- FULL WIDTH: MATRIX HEATMAP ---
if not df_matrix.empty:
    fig_matrix = px.imshow(df_matrix, text_auto=".2f", aspect="auto", color_continuous_scale=[[0.0, '#1E293B'], [0.1, '#1E293B'], [0.5, '#005B66'], [1.0, '#FF7043']])
    
    fig_matrix.update_layout(
        paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, title=dict(text="Sink Reefs (Receiving)", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=13), side="bottom"), 
        yaxis=dict(showgrid=False, title=dict(text="Source Reefs (Exporting)", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=13)),
        coloraxis_colorbar=dict(title="Probability", tickfont=dict(color='#94A3B8'))
    )
    
    fig_matrix.update_traces(xgap=2, ygap=2, textfont=dict(color='#111A22'))
    
    chart_card("CONNECTIVITY MATRIX (PROBABILITY)", fig_matrix, df_matrix)
else:
    st.error("Matrix data unavailable. Make sure connectivity_matrix.csv is in the data folder.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# ROW 3: PLD & LARVAL RETENTION (Mock Data)
# ==========================================
col3, col4 = st.columns(2, vertical_alignment="top")

with col3:
    df_pld = pd.DataFrame({'Species': ['Porites', 'Dipsastraea'], 'PLD_Days': [8, 14]})
    fig_pld = px.bar(df_pld, x='PLD_Days', y='Species', orientation='h', color_discrete_sequence=['#AB47BC'])
    fig_pld.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=True, gridcolor='#1E293B', title="Days"), yaxis=dict(showgrid=False, title="Species"), height=330)
    chart_card("PELAGIC LARVAE DURATION [MOCK DATA]", fig_pld, df_pld)

with col4:
    df_ret = pd.DataFrame({'Status': ['Retained (Self-Seeding)', 'Exported'], 'Percentage': [72.3, 27.7]})
    fig_ret = px.pie(df_ret, names='Status', values='Percentage', hole=0.4, color_discrete_sequence=['#66BB6A', '#FF7043'])
    fig_ret.update_traces(textposition='inside', textinfo='percent', insidetextfont=dict(color='#111A22', size=16))
    fig_ret.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), legend=dict(font=dict(color='#E2E8F0', size=12)), height=330)
    chart_card("LARVAL RETENTION [MOCK DATA]", fig_ret, df_ret)
