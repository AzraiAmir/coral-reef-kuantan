"""
Connectivity Network
Generates connectivity network graphs.
"""

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class ConnectivityNetwork:
    def __init__(self, output_dir='connectivity_network'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def create_network(self, connectivity_df, threshold=0.05):
        """Create connectivity network from matrix."""
        G = nx.DiGraph()

        for source in connectivity_df.index:
            G.add_node(source, type='source')
        for sink in connectivity_df.columns:
            G.add_node(sink, type='sink')

        for source in connectivity_df.index:
            for sink in connectivity_df.columns:
                strength = connectivity_df.loc[source, sink]
                if strength > threshold:
                    G.add_edge(source, sink, weight=strength)

        return G

    def plot_network(self, G, output_name='network'):
        """Plot network graph."""
        fig, ax = plt.subplots(figsize=(12, 8))

        pos = nx.spring_layout(G, seed=42)

        source_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'source']
        sink_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'sink']

        nx.draw_networkx_nodes(G, pos, nodelist=source_nodes, node_color='blue',
                               node_size=500, label='Source', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=sink_nodes, node_color='red',
                               node_size=500, label='Sink', ax=ax)

        edges = G.edges()
        weights = [G[u][v]['weight'] * 5 for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=weights, alpha=0.6,
                               edge_color='gray', ax=ax)

        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

        ax.set_title('Larval Connectivity Network', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def calculate_network_metrics(self, G):
        """Calculate network metrics."""
        metrics = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
            'betweenness_centrality': nx.betweenness_centrality(G),
            'degree_centrality': nx.degree_centrality(G),
        }

        return metrics
