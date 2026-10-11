"""
Coral Health Visualization
Visualizes health assessment results.
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class CoralHealthVisualization:
    def __init__(self, output_dir='health_visualizations'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def plot_kbi_by_site(self, kbi_data, output_name='kbi_by_site'):
        """Plot KBI values by site."""
        fig, ax = plt.subplots(figsize=(12, 6))

        sites = kbi_data['site'].unique()
        colors = plt.cm.RdYlGn_r(np.linspace(0, 1, len(sites)))

        for i, site in enumerate(sites):
            site_data = kbi_data[kbi_data['site'] == site]
            ax.bar(i, site_data['kbi'].mean(), color=colors[i],
                   yerr=site_data['kbi'].std(), capsize=5)

        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(sites, rotation=45, ha='right')
        ax.set_ylabel('KBI', fontsize=12)
        ax.set_title('Kuantan Bleaching Index by Site', fontsize=14, fontweight='bold')
        ax.axhline(y=0.2, color='green', linestyle='--', label='Healthy threshold')
        ax.axhline(y=0.4, color='orange', linestyle='--', label='Mild bleaching threshold')
        ax.axhline(y=0.6, color='red', linestyle='--', label='Severe bleaching threshold')
        ax.legend(fontsize=10)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def create_interactive_kbi_chart(self, kbi_data):
        """Create interactive KBI chart."""
        fig = px.bar(
            kbi_data,
            x='site',
            y='kbi',
            color='kbi',
            color_continuous_scale='RdYlGn_r',
            title='Kuantan Bleaching Index by Site',
            labels={'kbi': 'KBI', 'site': 'Site'}
        )

        fig.add_hline(y=0.2, line_dash="dash", line_color="green",
                     annotation_text="Healthy")
        fig.add_hline(y=0.4, line_dash="dash", line_color="orange",
                     annotation_text="Mild Bleaching")
        fig.add_hline(y=0.6, line_dash="dash", line_color="red",
                     annotation_text="Severe Bleaching")

        return fig

    def plot_temporal_trend(self, temporal_data, output_name='temporal_trend'):
        """Plot temporal trend in KBI."""
        fig, ax = plt.subplots(figsize=(12, 6))

        for site in temporal_data['site'].unique():
            site_data = temporal_data[temporal_data['site'] == site]
            ax.plot(site_data['date'], site_data['kbi'], marker='o', label=site)

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('KBI', fontsize=12)
        ax.set_title('Temporal Bleaching Trend by Site', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'
