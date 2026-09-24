"""
Genetic Validation
Compares connectivity predictions with genetic data.
"""

import pandas as pd
import numpy as np
from scipy import stats


class GeneticValidation:
    def __init__(self):
        self.results = {}

    def compare_connectivity(self, model_connectivity, genetic_connectivity):
        """Compare model predictions with genetic data."""
        correlation, p_value = stats.pearsonr(model_connectivity, genetic_connectivity)

        self.results['comparison'] = {
            'correlation': correlation,
            'p_value': p_value,
            'alignment': correlation * 100,
        }

        return self.results['comparison']

    def calculate_alignment(self, model_connectivity, genetic_connectivity, threshold=0.7):
        """Calculate alignment percentage between model and genetic data."""
        aligned = 0
        total = 0

        for i in range(len(model_connectivity)):
            for j in range(len(model_connectivity[0])):
                total += 1
                if abs(model_connectivity[i][j] - genetic_connectivity[i][j]) < threshold:
                    aligned += 1

        alignment = (aligned / total) * 100

        self.results['alignment'] = {
            'alignment_percentage': alignment,
            'aligned_pairs': aligned,
            'total_pairs': total,
        }

        return self.results['alignment']

    def identify_discrepancies(self, model_connectivity, genetic_connectivity):
        """Identify discrepancies between model and genetic data."""
        discrepancies = []

        for i in range(len(model_connectivity)):
            for j in range(len(model_connectivity[0])):
                diff = abs(model_connectivity[i][j] - genetic_connectivity[i][j])
                if diff > 0.3:
                    discrepancies.append({
                        'source': i,
                        'sink': j,
                        'model': model_connectivity[i][j],
                        'genetic': genetic_connectivity[i][j],
                        'difference': diff,
                    })

        return discrepancies
