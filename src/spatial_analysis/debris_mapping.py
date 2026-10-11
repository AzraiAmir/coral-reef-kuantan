"""
Debris Mapping
Generates debris distribution maps.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


class DebrisMapper:
    def __init__(self, output_dir='debris_maps'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def create_debris_map(self, debris_data, output_name='debris_map'):
        """Create debris distribution map."""
        fig, ax = plt.subplots(figsize=(12, 8))

        scatter = ax.scatter(
            debris_data['longitude'],
            debris_data['latitude'],
            c=debris_data['density'],
            cmap='Reds',
            s=100,
            edgecolor='black'
        )

        plt.colorbar(scatter, ax=ax, label='Debris Density (items/km²)')

        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title('Anthropogenic Debris Distribution', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def calculate_debris_density(self, debris_data, area_km2):
        """Calculate debris density per unit area."""
        total_debris = len(debris_data)
        density = total_debris / area_km2

        return {
            'total_debris': total_debris,
            'area_km2': area_km2,
            'density': density,
        }
