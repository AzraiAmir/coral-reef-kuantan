"""
Connectivity Visualization
Visualizes connectivity matrix and network graphs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go


class ConnectivityVisualization:
    def __init__(self, output_dir='connectivity_visualizations'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def plot_connectivity_matrix(self, connectivity_df, output_name='connectivity_matrix'):
        """Plot connectivity matrix as heatmap."""
        fig, ax = plt.subplots(figsize=(8, 6))

        im = ax.imshow(connectivity_df.values, cmap='YlOrRd', aspect='auto')

        ax.set_xticks(range(len(connectivity_df.columns)))
        ax.set_yticks(range(len(connectivity_df.index)))
        ax.set_xticklabels(connectivity_df.columns, rotation=45, ha='right')
        ax.set_yticklabels(connectivity_df.index)

        for i in range(len(connectivity_df.index)):
            for j in range(len(connectivity_df.columns)):
                text = ax.text(j, i, f'{connectivity_df.values[i, j]:.3f}',
                              ha='center', va='center', fontsize=10,
                              color='white' if connectivity_df.values[i, j] > 0.5 else 'black')

        plt.colorbar(im, ax=ax, label='Connectivity Probability')

        ax.set_xlabel('Sink Sites', fontsize=12, fontweight='bold')
        ax.set_ylabel('Source Sites', fontsize=12, fontweight='bold')
        ax.set_title('Larval Connectivity Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def plot_connectivity_network(self, connectivity_df, output_name='connectivity_network'):
        """Plot connectivity network graph."""
        G = nx.DiGraph()

        # Add nodes
        for source in connectivity_df.index:
            G.add_node(source, type='source')
        for sink in connectivity_df.columns:
            G.add_node(sink, type='sink')

        # Add edges
        for source in connectivity_df.index:
            for sink in connectivity_df.columns:
                strength = connectivity_df.loc[source, sink]
                if strength > 0.05:
                    G.add_edge(source, sink, weight=strength)

        fig, ax = plt.subplots(figsize=(12, 8))

        pos = nx.spring_layout(G, seed=42)

        # Draw nodes
        source_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'source']
        sink_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'sink']

        nx.draw_networkx_nodes(G, pos, nodelist=source_nodes, node_color='blue',
                               node_size=500, label='Source', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=sink_nodes, node_color='red',
                               node_size=500, label='Sink', ax=ax)

        # Draw edges
        edges = G.edges()
        weights = [G[u][v]['weight'] * 5 for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=weights, alpha=0.6,
                               edge_color='gray', ax=ax)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

        ax.set_title('Larval Connectivity Network', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def create_interactive_network(self, connectivity_df):
        """Create interactive connectivity network."""
        G = nx.DiGraph()

        for source in connectivity_df.index:
            G.add_node(source, type='source')
        for sink in connectivity_df.columns:
            G.add_node(sink, type='sink')

        for source in connectivity_df.index:
            for sink in connectivity_df.columns:
                strength = connectivity_df.loc[source, sink]
                if strength > 0.05:
                    G.add_edge(source, sink, weight=strength)

        pos = nx.spring_layout(G, seed=42)

        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            weight = G[edge[0]][edge[1]]['weight']

            edge_trace.append(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=weight * 5, color='gray'),
                hoverinfo='none',
                mode='lines'
            ))

        node_trace = go.Scatter(
            x=[pos[n][0] for n in G.nodes()],
            y=[pos[n][1] for n in G.nodes()],
            mode='markers+text',
            text=list(G.nodes()),
            textposition='top center',
            marker=dict(
                size=20,
                color=['blue' if G.nodes[n]['type'] == 'source' else 'red' for n in G.nodes()]
            ),
            hoverinfo='text'
        )

        fig = go.Figure(data=edge_trace + [node_trace])
        fig.update_layout(
            title='Larval Connectivity Network',
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        return fig
