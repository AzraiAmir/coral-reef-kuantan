"""
Bleaching Severity Map
Generates bleaching severity maps from KBI values.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


class BleachingSeverityMap:
    def __init__(self, output_dir='bleaching_maps'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def create_heatmap(self, kbi_data, output_name='bleaching_heatmap'):
        """Create bleaching severity heatmap."""
        fig, ax = plt.subplots(figsize=(10, 8))

        scatter = ax.scatter(
            kbi_data['longitude'],
            kbi_data['latitude'],
            c=kbi_data['kbi'],
            cmap='RdYlGn_r',
            s=200,
            edgecolor='black',
            vmin=0,
            vmax=1
        )

        plt.colorbar(scatter, ax=ax, label='KBI')

        for idx, row in kbi_data.iterrows():
            ax.annotate(
                row['site'],
                (row['longitude'], row['latitude']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8
            )

        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title('Bleaching Severity Map (KBI)', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def create_health_classification_map(self, kbi_data, output_name='health_classification'):
        """Create health classification map."""
        def classify(kbi):
            if kbi < 0.2:
                return 'Healthy'
            elif kbi < 0.4:
                return 'Mild Bleaching'
            elif kbi < 0.6:
                return 'Moderate Bleaching'
            elif kbi < 0.8:
                return 'Severe Bleaching'
            else:
                return 'Critical Bleaching'

        kbi_data['health_status'] = kbi_data['kbi'].apply(classify)

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = {
            'Healthy': 'green',
            'Mild Bleaching': 'yellow',
            'Moderate Bleaching': 'orange',
            'Severe Bleaching': 'red',
            'Critical Bleaching': 'darkred',
        }

        for status, color in colors.items():
            subset = kbi_data[kbi_data['health_status'] == status]
            if len(subset) > 0:
                ax.scatter(
                    subset['longitude'],
                    subset['latitude'],
                    c=color,
                    s=200,
                    label=status,
                    edgecolor='black'
                )

        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title('Health Classification Map', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'
