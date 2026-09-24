"""
MIKE 21 FM Validation
Validates MIKE 21 FM hydrodynamic model against ADCP data.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


class MIKE21Validation:
    def __init__(self, output_dir='mike21_validation'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def validate_current_speed(self, observed_speed, simulated_speed):
        """Validate current speed against ADCP data."""
        rmse = np.sqrt(np.mean((observed_speed - simulated_speed) ** 2))
        correlation, p_value = stats.pearsonr(observed_speed, simulated_speed)

        return {
            'rmse': rmse,
            'correlation': correlation,
            'p_value': p_value,
        }

    def validate_current_direction(self, observed_direction, simulated_direction):
        """Validate current direction against ADCP data."""
        # Circular correlation for direction
        obs_rad = np.radians(observed_direction)
        sim_rad = np.radians(simulated_direction)

        correlation = np.mean(np.cos(obs_rad - sim_rad))

        return {
            'circular_correlation': correlation,
        }

    def validate_tidal_elevation(self, observed_elevation, simulated_elevation):
        """Validate tidal elevation against charts."""
        rmse = np.sqrt(np.mean((observed_elevation - simulated_elevation) ** 2))
        correlation, p_value = stats.pearsonr(observed_elevation, simulated_elevation)

        return {
            'rmse': rmse,
            'correlation': correlation,
            'p_value': p_value,
        }

    def plot_validation(self, observed, simulated, variable='Current Speed',
                        output_name='validation_plot'):
        """Plot validation comparison."""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Time series
        axes[0].plot(observed, 'b-', label='Observed', linewidth=2)
        axes[0].plot(simulated, 'r-', label='Simulated', linewidth=2)
        axes[0].set_xlabel('Time Step', fontsize=12)
        axes[0].set_ylabel(variable, fontsize=12)
        axes[0].set_title(f'{variable} - Time Series', fontsize=14, fontweight='bold')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)

        # Scatter plot
        axes[1].scatter(observed, simulated, alpha=0.5)
        axes[1].plot([min(observed), max(observed)],
                     [min(observed), max(observed)], 'r--', linewidth=2)
        axes[1].set_xlabel('Observed', fontsize=12)
        axes[1].set_ylabel('Simulated', fontsize=12)
        axes[1].set_title(f'{variable} - Scatter Plot', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'
