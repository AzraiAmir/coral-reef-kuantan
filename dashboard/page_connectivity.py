import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
from pathlib import Path

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

col1, col2 = st.columns([1.5, 1])

# --- LEFT COLUMN: NETWORK GRAPH ---
with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">NETWORK GRAPH · LARVAL FLOW</div>', unsafe_allow_html=True)
        
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

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1.5, color='#64748B'),
                hoverinfo='none',
                mode='lines')

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
                x=node_x, y=node_y,
                mode='markers+text',
                text=node_text,
                textposition="bottom center",
                textfont=dict(size=11, color='#E2E8F0'),
                hoverinfo='text',
                marker=dict(
                    showscale=False,
                    color=node_color,
                    size=20,
                    line_width=2,
                    line_color='#111A22'))

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20, l=20, r=20, t=20), 
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.3, 1.3]), 
                                paper_bgcolor='#111A22', plot_bgcolor='#111A22',
                                font_color='#E2E8F0',
                                height=400
                            ))
            
            # THE FIX: Enable the modebar and position it at the top right
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': True, 
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'], # Clean up the UI
                    'modeBarButtonsToAdd': ['resetScale2d'] # Add a reset button
                }
            )
            
            # Custom CSS to make the modebar dark and match the theme
            st.markdown("""
            <style>
            /* Target the modebar container */
            div[data-testid="stPlotlyChart"] .modebar {
                background-color: #111A22 !important; /* Dark background */
                border-radius: 4px;
                top: 10px; /* Push down from the very top edge */
            }
            /* Target the icons */
            div[data-testid="stPlotlyChart"] .modebar-btn path {
                fill: #94A3B8 !important; /* Slate grey by default */
            }
            /* Target the icons on hover */
            div[data-testid="stPlotlyChart"] .modebar-btn:hover path {
                fill: #00E5FF !important; /* Cyan on hover */
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.75rem; font-family: 'Inter', sans-serif; padding-bottom: 15px; color: #B0BEC5;">
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background-color: #00E5FF; border-radius: 50%;"></div> Source Reef (MPA)
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="width: 12px; height: 12px; background-color: #FF7043; border-radius: 50%;"></div> Sink Reef (Nearshore)
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("connectivity_matrix.csv not found.")

# --- RIGHT COLUMN: DPI BAR CHART ---
with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">DISPERSAL POTENTIAL INDEX</div>', unsafe_allow_html=True)
        
        if dpi_data:
            dpi_df = pd.DataFrame(list(dpi_data.items()), columns=['Site', 'DPI'])
            dpi_df = dpi_df.sort_values(by='DPI', ascending=True)
            
            # Assign color based on site name
            dpi_df['Role'] = dpi_df['Site'].apply(lambda x: 'Source (MPA)' if x in ['Pulau_Tioman'] else 'Sink (Nearshore)')
            
            fig_dpi = px.bar(
                dpi_df, 
                x='DPI', 
                y='Site', 
                orientation='h', 
                color='Role',
                color_discrete_map={
                    'Source (MPA)': '#00E5FF',
                    'Sink (Nearshore)': '#FF7043'
                }
            )
            
            fig_dpi.update_layout(
                paper_bgcolor='#111A22', plot_bgcolor='#111A22', 
                font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=30), # Increased right margin for text
                xaxis=dict(showgrid=True, gridcolor='#1E293B', title="DPI Score", range=[0, 1.15]), # Increased to 1.15 so text fits
                yaxis=dict(showgrid=False, title=""),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    title=None, font=dict(size=11)
                ),
                height=400,
                showlegend=True
            )
            
            # THE FIX: Text outside the bar, colored white for high contrast
            fig_dpi.update_traces(
                texttemplate='%{x:.2f}', 
                textposition='outside', 
                textfont_color='#E2E8F0', 
                textfont_size=12,
                cliponaxis=False # Prevents text from being cut off at the edge
            )
            
            st.plotly_chart(fig_dpi, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("dpi.json not found.")

st.markdown("<br>", unsafe_allow_html=True)

# --- FULL WIDTH: MATRIX HEATMAP ---
with st.container(border=True):
    st.markdown('<div class="panel-title" style="padding: 15px 15px 0 15px;">CONNECTIVITY MATRIX (PROBABILITY)</div>', unsafe_allow_html=True)
    
    if not df_matrix.empty:
        fig_matrix = px.imshow(
            df_matrix, 
            text_auto=".2f", 
            aspect="auto",
            color_continuous_scale=[
                [0.0, '#1E293B'],  
                [0.1, '#1E293B'],  
                [0.5, '#005B66'],  
                [1.0, '#FF7043']   
            ]
        )
        
        fig_matrix.update_layout(
            paper_bgcolor='#111A22', plot_bgcolor='#111A22',
            font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(
                showgrid=False, 
                title=dict(
                    text="Sink Reefs (Receiving)", 
                    font=dict(color='#64748B', size=14) # Increased title size
                ),
                tickfont=dict(color='#E2E8F0', size=13), # Increased tick size
                side="bottom"
            ), 
            yaxis=dict(
                showgrid=False, 
                title=dict(
                    text="Source Reefs (Exporting)",
                    font=dict(color='#64748B', size=14) # Increased title size
                ),
                tickfont=dict(color='#E2E8F0', size=13) # Increased tick size
            ),
            coloraxis_colorbar=dict(
                title="Probability", 
                tickfont=dict(color='#94A3B8')
            )
        )
        
        fig_matrix.update_traces(
            xgap=2, 
            ygap=2,
            textfont=dict(color='#111A22') 
        )
        
        st.plotly_chart(fig_matrix, use_container_width=True, config={'displayModeBar': False})
    else:
        st.error("Matrix data unavailable.")