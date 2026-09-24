"""
Temporal Trend Analysis
Analyses temporal trends in KBI and environmental parameters.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


class TemporalTrendAnalysis:
    def __init__(self, data):
        self.data = data
        self.results = {}

    def calculate_trend(self, variable, time_column='date'):
        """Calculate temporal trend for a variable."""
        # Convert date to numeric
        time_numeric = pd.to_datetime(self.data[time_column]).astype(int) / 10**9

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            time_numeric, self.data[variable]
        )

        self.results[f'{variable}_trend'] = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'std_err': std_err,
            'trend': 'increasing' if slope > 0 else 'decreasing',
        }

        return self.results[f'{variable}_trend']

    def seasonal_decomposition(self, variable, period=12):
        """Perform seasonal decomposition."""
        from statsmodels.tsa.seasonal import seasonal_decompose

        series = self.data.set_index('date')[variable]
        decomposition = seasonal_decompose(series, model='additive', period=period)

        return decomposition

    def plot_temporal_trend(self, variable, output_name='temporal_trend'):
        """Plot temporal trend."""
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(self.data['date'], self.data[variable], 'b-', label='Observed', linewidth=2)

        # Add trend line
        time_numeric = pd.to_datetime(self.data['date']).astype(int) / 10**9
        z = np.polyfit(time_numeric, self.data[variable], 1)
        p = np.poly1d(z)
        ax.plot(self.data['date'], p(time_numeric), 'r--', label='Trend', linewidth=2)

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(variable, fontsize=12)
        ax.set_title(f'Temporal Trend: {variable}', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{output_name}.png'
