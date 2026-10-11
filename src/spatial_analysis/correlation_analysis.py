"""
Correlation Analysis
Full correlation analysis suite.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


class CorrelationAnalysis:
    def __init__(self, data):
        self.data = data
        self.results = {}

    def pearson_correlation(self, var1, var2):
        """Calculate Pearson correlation."""
        corr, p_value = stats.pearsonr(self.data[var1], self.data[var2])

        self.results[f'{var1}_vs_{var2}'] = {
            'correlation': corr,
            'p_value': p_value,
            'method': 'pearson',
            'significant': p_value < 0.05,
        }

        return self.results[f'{var1}_vs_{var2}']

    def spearman_correlation(self, var1, var2):
        """Calculate Spearman correlation."""
        corr, p_value = stats.spearmanr(self.data[var1], self.data[var2])

        self.results[f'{var1}_vs_{var2}'] = {
            'correlation': corr,
            'p_value': p_value,
            'method': 'spearman',
            'significant': p_value < 0.05,
        }

        return self.results[f'{var1}_vs_{var2}']

    def point_biserial_correlation(self, binary_var, continuous_var):
        """Calculate point-biserial correlation."""
        corr, p_value = stats.pointbiserialr(self.data[binary_var], self.data[continuous_var])

        self.results[f'{binary_var}_vs_{continuous_var}'] = {
            'correlation': corr,
            'p_value': p_value,
            'method': 'point-biserial',
            'significant': p_value < 0.05,
        }

        return self.results[f'{binary_var}_vs_{continuous_var}']

    def correlation_matrix(self, variables):
        """Calculate correlation matrix."""
        corr_matrix = self.data[variables].corr()

        return corr_matrix

    def plot_correlation_matrix(self, variables, output_name='correlation_matrix'):
        """Plot correlation matrix as heatmap."""
        corr_matrix = self.correlation_matrix(variables)

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            ax=ax
        )

        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{output_name}.png'
