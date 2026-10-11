"""
Coral-CRCA Calibration
Calibrate KBI against expert-assessed bleaching scores.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class CoralCRCACalibration:
    def __init__(self, output_dir='kbi_calibration'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Initial weights
        self.weights = {
            'C1': 1.0,
            'C2': 0.8,
            'C3': 0.6,
            'C4': 0.4,
            'C5': 0.2,
            'C6': 0.0,
        }

    def calculate_kbi(self, colour_percentages, weights):
        """Calculate KBI with given weights."""
        kbi = sum(
            weights.get(code, 0) * pct / 100
            for code, pct in colour_percentages.items()
        )
        return kbi

    def objective(self, weights_array, colour_data, expert_scores):
        """Objective function for weight optimisation."""
        weights = dict(zip(['C1', 'C2', 'C3', 'C4', 'C5', 'C6'], weights_array))

        predicted = []
        for colour_percentages in colour_data:
            kbi = self.calculate_kbi(colour_percentages, weights)
            predicted.append(kbi)

        correlation = np.corrcoef(predicted, expert_scores)[0, 1]
        return -correlation  # Minimize negative correlation

    def calibrate(self, colour_data, expert_scores):
        """Calibrate weights against expert scores."""
        initial_weights = np.array(list(self.weights.values()))

        # Bounds: weights between 0 and 1
        bounds = [(0, 1) for _ in range(6)]

        result = minimize(
            self.objective,
            initial_weights,
            args=(colour_data, expert_scores),
            method='L-BFGS-B',
            bounds=bounds,
        )

        optimal_weights = dict(zip(['C1', 'C2', 'C3', 'C4', 'C5', 'C6'], result.x))
        self.weights = optimal_weights

        # Calculate validation metrics
        predicted = [
            self.calculate_kbi(cp, optimal_weights)
            for cp in colour_data
        ]

        correlation, p_value = stats.pearsonr(predicted, expert_scores)
        r2 = correlation ** 2
        mae = np.mean(np.abs(np.array(predicted) - np.array(expert_scores)))

        results = {
            'weights': optimal_weights,
            'correlation': correlation,
            'r_squared': r2,
            'p_value': p_value,
            'mae': mae,
            'passed': correlation > 0.80,
        }

        # Save results
        with open(f'{self.output_dir}/calibration_results.json', 'w') as f:
            import json
            json.dump(results, f, indent=2)

        # Plot correlation
        self.plot_calibration(predicted, expert_scores, correlation)

        return results

    def plot_calibration(self, predicted, expert_scores, correlation):
        """Plot calibration results."""
        fig, ax = plt.subplots(figsize=(8, 8))

        ax.scatter(expert_scores, predicted, alpha=0.6)

        # Fit line
        z = np.polyfit(expert_scores, predicted, 1)
        p = np.poly1d(z)
        x_range = np.linspace(min(expert_scores), max(expert_scores), 100)
        ax.plot(x_range, p(x_range), 'r-', linewidth=2,
                label=f'Fit (r={correlation:.3f})')

        # Perfect correlation line
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Perfect correlation')

        ax.set_xlabel('Expert Bleaching Score', fontsize=12)
        ax.set_ylabel('Automated KBI', fontsize=12)
        ax.set_title('KBI Calibration', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/calibration_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
