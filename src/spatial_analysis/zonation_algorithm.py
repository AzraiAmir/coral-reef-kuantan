"""
Zonation Algorithm
Conservation value zonation algorithm.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


class ZonationAlgorithm:
    def __init__(self):
        self.criteria_weights = {
            'live_coral_cover': 0.25,
            'coral_genera_richness': 0.20,
            'sensitive_taxa': 0.15,
            'structural_complexity': 0.15,
            'disturbance_absence': 0.10,
            'recruitment_potential': 0.10,
            'connectivity': 0.05,
        }

    def normalize_criteria(self, data):
        """Normalize criteria to 0-1 scale."""
        normalized = {}
        for criterion, weight in self.criteria_weights.items():
            values = data[criterion].values
            min_val, max_val = values.min(), values.max()

            if max_val - min_val > 0:
                normalized[criterion] = (values - min_val) / (max_val - min_val)
            else:
                normalized[criterion] = np.zeros_like(values)

        return normalized

    def calculate_conservation_value(self, data):
        """Calculate conservation value for each site."""
        normalized = self.normalize_criteria(data)

        conservation_value = np.zeros(len(data))
        for criterion, weight in self.criteria_weights.items():
            conservation_value += weight * normalized[criterion]

        return conservation_value

    def classify_conservation_value(self, conservation_value):
        """Classify conservation value into categories."""
        categories = []
        for value in conservation_value:
            if value >= 0.75:
                categories.append('High')
            elif value >= 0.50:
                categories.append('Medium')
            elif value >= 0.25:
                categories.append('Low')
            else:
                categories.append('Degraded')

        return categories

    def generate_zonation_map(self, data, output_name='zonation_map'):
        """Generate conservation value zonation map."""
        data['conservation_value'] = self.calculate_conservation_value(data)
        data['conservation_category'] = self.classify_conservation_value(data['conservation_value'])

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 8))

        colors = {
            'High': 'darkgreen',
            'Medium': 'yellowgreen',
            'Low': 'orange',
            'Degraded': 'red',
        }

        for category, color in colors.items():
            subset = data[data['conservation_category'] == category]
            if len(subset) > 0:
                ax.scatter(
                    subset['longitude'],
                    subset['latitude'],
                    c=color,
                    s=200,
                    label=category,
                    edgecolor='black'
                )

        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title('Conservation Value Zonation Map', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return data
