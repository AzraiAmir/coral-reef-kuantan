"""
Environmental Correlation
Correlates health metrics with environmental parameters.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


class EnvironmentalCorrelation:
    def __init__(self, health_data, environmental_data):
        self.health_data = health_data
        self.environmental_data = environmental_data
        self.results = {}

    def merge_data(self):
        """Merge health and environmental data."""
        merged = pd.merge(
            self.health_data,
            self.environmental_data,
            on=['site_id', 'campaign']
        )
        return merged

    def correlate_kbi_temperature(self):
        """Correlate KBI with temperature."""
        merged = self.merge_data()
        corr, p_value = stats.pearsonr(merged['kbi'], merged['temperature_c'])

        self.results['kbi_temperature'] = {
            'correlation': corr,
            'p_value': p_value,
            'significant': p_value < 0.05,
        }

        return self.results['kbi_temperature']

    def correlate_kbi_salinity(self):
        """Correlate KBI with salinity."""
        merged = self.merge_data()
        corr, p_value = stats.pearsonr(merged['kbi'], merged['salinity_psu'])

        self.results['kbi_salinity'] = {
            'correlation': corr,
            'p_value': p_value,
            'significant': p_value < 0.05,
        }

        return self.results['kbi_salinity']

    def correlate_kbi_ph(self):
        """Correlate KBI with pH."""
        merged = self.merge_data()
        corr, p_value = stats.pearsonr(merged['kbi'], merged['ph'])

        self.results['kbi_ph'] = {
            'correlation': corr,
            'p_value': p_value,
            'significant': p_value < 0.05,
        }

        return self.results['kbi_ph']

    def plot_correlation(self, variable, output_name='environmental_correlation'):
        """Plot correlation between KBI and environmental variable."""
        merged = self.merge_data()

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(merged[variable], merged['kbi'], alpha=0.5)

        # Fit line
        z = np.polyfit(merged[variable], merged['kbi'], 1)
        p = np.poly1d(z)
        x_range = np.linspace(merged[variable].min(), merged[variable].max(), 100)
        ax.plot(x_range, p(x_range), 'r-', label=f'Fit: y={z[0]:.2f}x+{z[1]:.2f}')

        ax.set_xlabel(variable, fontsize=12)
        ax.set_ylabel('KBI', fontsize=12)
        ax.set_title(f'KBI vs {variable}', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{output_name}.png'
