"""
Model Validation
Validates detection, health assessment, and connectivity models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, precision_score, recall_score, f1_score
from scipy import stats


class ModelValidator:
    def __init__(self):
        self.results = {}

    def validate_detection(self, y_true, y_pred):
        """Validate detection model predictions."""
        self.results['detection'] = {
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
        }
        return self.results['detection']

    def validate_health_assessment(self, automated_kbi, expert_kbi):
        """Validate health assessment against expert scores."""
        correlation, p_value = stats.pearsonr(automated_kbi, expert_kbi)
        r2 = r2_score(expert_kbi, automated_kbi)
        mae = mean_absolute_error(expert_kbi, automated_kbi)

        self.results['health_assessment'] = {
            'correlation': correlation,
            'p_value': p_value,
            'r2': r2,
            'mae': mae,
        }
        return self.results['health_assessment']

    def validate_connectivity(self, observed_current, simulated_current):
        """Validate connectivity model against ADCP data."""
        rmse = np.sqrt(np.mean((observed_current - simulated_current) ** 2))
        correlation, p_value = stats.pearsonr(observed_current, simulated_current)

        self.results['connectivity'] = {
            'rmse': rmse,
            'correlation': correlation,
            'p_value': p_value,
        }
        return self.results['connectivity']
