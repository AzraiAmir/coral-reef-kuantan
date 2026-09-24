"""
Dispersal Potential Index (DPI) Calculator
Calculates DPI for each source site based on four factors.
"""

import numpy as np
import pandas as pd


class DPICalculator:
    def __init__(self):
        self.weights = {
            'adult_coral_cover': 0.3,
            'pld': 0.3,
            'current_speed': 0.2,
            'depth_variation': 0.2,
        }

    def calculate_dpi(self, adult_coral_cover, pld, current_speed, depth_variation):
        """Calculate Dispersal Potential Index (DPI)."""
        normalized_cover = adult_coral_cover / 100.0
        normalized_pld = min(pld / 20.0, 1.0)
        normalized_speed = min(current_speed / 1.0, 1.0)
        normalized_depth = min(depth_variation / 10.0, 1.0)

        dpi = (
            self.weights['adult_coral_cover'] * normalized_cover +
            self.weights['pld'] * normalized_pld +
            self.weights['current_speed'] * normalized_speed +
            self.weights['depth_variation'] * normalized_depth
        )

        return dpi

    def calculate_all_sites(self, site_data):
        """Calculate DPI for all source sites."""
        results = []
        for site_name, data in site_data.items():
            dpi = self.calculate_dpi(
                data['adult_coral_cover'],
                data['pld'],
                data['current_speed'],
                data['depth_variation']
            )
            results.append({
                'site': site_name,
                'adult_coral_cover': data['adult_coral_cover'],
                'pld': data['pld'],
                'current_speed': data['current_speed'],
                'depth_variation': data['depth_variation'],
                'dpi': dpi,
            })

        df = pd.DataFrame(results)
        df = df.sort_values('dpi', ascending=False)

        return df
