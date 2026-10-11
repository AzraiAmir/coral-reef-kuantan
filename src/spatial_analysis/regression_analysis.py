"""
Regression Analysis
Full regression analysis suite.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


class RegressionAnalysis:
    def __init__(self, data):
        self.data = data
        self.results = {}

    def simple_linear_regression(self, dependent, independent):
        """Perform simple linear regression."""
        X = self.data[independent].values.reshape(-1, 1)
        y = self.data[dependent].values

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)

        self.results[f'{dependent}_vs_{independent}'] = {
            'coefficient': model.coef_[0],
            'intercept': model.intercept_,
            'r_squared': r2_score(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred)),
        }

        return self.results[f'{dependent}_vs_{independent}']

    def multiple_regression(self, dependent, independents):
        """Perform multiple regression analysis."""
        X = self.data[independents]
        X = sm.add_constant(X)
        y = self.data[dependent]

        model = sm.OLS(y, X).fit()

        self.results['multiple_regression'] = {
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'p_value': model.f_pvalue,
            'coefficients': model.params.to_dict(),
            'summary': model.summary(),
        }

        return self.results['multiple_regression']

    def plot_regression(self, dependent, independent, output_name='regression_plot'):
        """Plot regression results."""
        import matplotlib.pyplot as plt

        X = self.data[independent]
        y = self.data[dependent]

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(X, y, alpha=0.5, label='Data')

        # Fit line
        z = np.polyfit(X, y, 1)
        p = np.poly1d(z)
        ax.plot(X, p(X), 'r-', label=f'Fit: y={z[0]:.2f}x+{z[1]:.2f}')

        ax.set_xlabel(independent, fontsize=12)
        ax.set_ylabel(dependent, fontsize=12)
        ax.set_title(f'{dependent} vs {independent}', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{output_name}.png'
