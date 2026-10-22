import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 05 · CONNECTIVITY</div>', unsafe_allow_html=True)
st.title("Source-sink dynamics")
st.markdown("Modelled larval connectivity between reef nodes. Edges indicate exchange probability; node colour denotes dominant role.")

# 1. LOAD REAL DATA
matrix_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\connectivity_matrix.csv")
dpi_path = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\dpi.json")

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
    # Keep height at 520
    with st.container(border=True, height=520):
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

            source_x, source_y, source_text = [], [], []
            sink_x, sink_y, sink_text = [], [], []
            
            for node in G.nodes():
                x, y = pos[node]
                clean_name = node.replace("_", " ")
                if " " in clean_name:
                    parts = clean_name.split(" ", 1)
                    display_text = f"<span style='text-align:center'>{parts[0]}<br>{parts[1]}</span>"
                else:
                    display_text = f"<span style='text-align:center'>{clean_name}</span>"
                
                if node in sources:
                    source_x.append(x)
                    source_y.append(y)
                    source_text.append(display_text)
                else:
                    sink_x.append(x)
                    sink_y.append(y)
                    sink_text.append(display_text)

            edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color='#64748B'), hoverinfo='none', mode='lines', showlegend=False)

            source_trace = go.Scatter(
                x=source_x, y=source_y, mode='markers+text', text=source_text, textposition="bottom center",
                textfont=dict(size=11, color='#E2E8F0'), hoverinfo='text', name='Source Reef (MPA)',
                marker=dict(showscale=False, color='#00E5FF', size=20, line_width=2, line_color='#111A22'))

            sink_trace = go.Scatter(
                x=sink_x, y=sink_y, mode='markers+text', text=sink_text, textposition="bottom center",
                textfont=dict(size=11, color='#E2E8F0'), hoverinfo='text', name='Sink Reef (Nearshore)',
                marker=dict(showscale=False, color='#FF7043', size=20, line_width=2, line_color='#111A22'))

            # THE FIX: Reduced bottom margin (b=10) and adjusted legend y-position
            fig = go.Figure(data=[edge_trace, source_trace, sink_trace],
                            layout=go.Layout(
                                showlegend=True, hovermode='closest', margin=dict(b=10, l=20, r=20, t=20), 
                                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(color='#E2E8F0', size=12)),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', height=440))
            
            st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">NETWORK GRAPH · LARVAL FLOW</div>', unsafe_allow_html=True)
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True, 
                'displaylogo': False, 
                'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'], 
                'modeBarButtonsToAdd': ['resetScale2d']
            })

# --- RIGHT COLUMN: DPI BAR CHART ---
with col2:
    # Keep height at 520
    with st.container(border=True, height=520):
        if dpi_data:
            dpi_df = pd.DataFrame(list(dpi_data.items()), columns=['Site', 'DPI'])
            dpi_df['Site'] = dpi_df['Site'].str.replace("_", " ")
            dpi_df = dpi_df.sort_values(by='DPI', ascending=True)
            dpi_df['Role'] = dpi_df['Site'].apply(lambda x: 'Source (MPA)' if x == 'Pulau Tioman' else 'Sink (Nearshore)')
            
            fig_dpi = px.bar(dpi_df, x='DPI', y='Site', orientation='h', color='Role', color_discrete_map={'Source (MPA)': '#00E5FF', 'Sink (Nearshore)': '#FF7043'})
            
            # THE FIX: Reduced bottom margin to pull the x-axis closer to the edge
            fig_dpi.update_layout(
                paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
                font_color='#E2E8F0', 
                margin=dict(t=0, b=10, l=10, r=40), # Reduced bottom margin from 20 to 10
                xaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="DPI Score", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12), range=[0, 1.15]), 
                yaxis=dict(showgrid=False, title="", tickfont=dict(color='#E2E8F0', size=12)),
                height=440, 
                showlegend=False,
                bargap=0.3 
            )
            
            fig_dpi.update_traces(texttemplate='%{x:.2f}', textposition='outside', textfont_color='#E2E8F0', textfont_size=12, cliponaxis=False)
            
            st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">DISPERSAL POTENTIAL INDEX</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_dpi, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("dpi.json not found.")

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
    st.error("Matrix data unavailable.")