"""
Statistical Analysis
Correlation and regression analyses for research findings.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm


class StatisticalAnalyzer:
    def __init__(self, data):
        self.data = data
        self.results = {}

    def correlation_analysis(self, var1, var2, method='pearson'):
        """Perform correlation analysis between two variables."""
        if method == 'pearson':
            corr, p_value = stats.pearsonr(self.data[var1], self.data[var2])
        elif method == 'spearman':
            corr, p_value = stats.spearmanr(self.data[var1], self.data[var2])

        self.results[f'{var1}_vs_{var2}'] = {
            'correlation': corr,
            'p_value': p_value,
            'method': method,
            'significant': p_value < 0.05,
        }

        return self.results[f'{var1}_vs_{var2}']

    def regression_analysis(self, dependent, independents):
        """Perform multiple regression analysis."""
        X = self.data[independents]
        X = sm.add_constant(X)
        y = self.data[dependent]

        model = sm.OLS(y, X).fit()

        self.results['regression'] = {
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'p_value': model.f_pvalue,
            'coefficients': model.params.to_dict(),
            'summary': model.summary(),
        }

        return self.results['regression']
