"""
Kuantan Bleaching Index (KBI) Calculator
Calculates KBI from colour distribution data.
"""

import numpy as np
import pandas as pd


class KBICalculator:
    def __init__(self):
        self.weights = {
            'C1': 1.0,
            'C2': 0.8,
            'C3': 0.6,
            'C4': 0.4,
            'C5': 0.2,
            'C6': 0.0,
        }

        self.thresholds = {
            'healthy': (0.0, 0.2),
            'mild_bleaching': (0.2, 0.4),
            'moderate_bleaching': (0.4, 0.6),
            'severe_bleaching': (0.6, 0.8),
            'critical_bleaching': (0.8, 1.0),
        }

    def calculate_kbi(self, colour_percentages):
        """Calculate KBI from colour percentages."""
        kbi = sum(
            self.weights.get(code, 0) * pct / 100
            for code, pct in colour_percentages.items()
        )
        return kbi

    def classify_health(self, kbi):
        """Classify health status based on KBI."""
        for status, (low, high) in self.thresholds.items():
            if low <= kbi < high:
                return status
        return 'unknown'

    def calibrate(self, automated_kbi, expert_scores):
        """Calibrate KBI against expert scores."""
        from scipy import stats

        correlation, p_value = stats.pearsonr(automated_kbi, expert_scores)
        r2 = correlation ** 2
        mae = np.mean(np.abs(np.array(automated_kbi) - np.array(expert_scores)))

        return {
            'correlation': correlation,
            'p_value': p_value,
            'r2': r2,
            'mae': mae,
        }
