"""
GIS Mapping
Generates distribution maps, health heatmaps, and connectivity visualizations.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx


class GISMapper:
    def __init__(self, output_dir='maps'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def create_distribution_map(self, data, output_name='distribution_map'):
        """Create species distribution map."""
        gdf = gpd.GeoDataFrame(
            data,
            geometry=[Point(lon, lat) for lon, lat in zip(data['longitude'], data['latitude'])],
            crs='EPSG:4326'
        )

        fig, ax = plt.subplots(figsize=(12, 8))

        gdf.plot(
            ax=ax,
            column='live_coral_cover',
            cmap='Greens',
            legend=True,
            markersize=100,
            edgecolor='black'
        )

        for idx, row in gdf.iterrows():
            ax.annotate(
                row['site'],
                (row.geometry.x, row.geometry.y),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8
            )

        ax.set_title('Live Coral Cover by Site', fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Distribution map saved to {self.output_dir}/{output_name}.png")

    def create_health_heatmap(self, health_data, output_name='health_heatmap'):
        """Create health heatmap."""
        fig, ax = plt.subplots(figsize=(10, 6))

        im = ax.imshow(
            health_data.values,
            cmap='RdYlGn_r',
            aspect='auto'
        )

        ax.set_xticks(range(len(health_data.columns)))
        ax.set_yticks(range(len(health_data.index)))
        ax.set_xticklabels(health_data.columns, rotation=45, ha='right')
        ax.set_yticklabels(health_data.index)

        plt.colorbar(im, ax=ax, label='KBI')

        ax.set_title('Coral Health Heatmap (KBI)', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Health heatmap saved to {self.output_dir}/{output_name}.png")
