"""
Environmental Parameter Integration

Integrates coral health metrics with environmental parameters
for H3 and H4 hypothesis testing.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


class EnvironmentalIntegration:
    """Merges health metrics with environmental data and runs tests."""

    def __init__(self, output_dir="environmental_integration"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {}

    def merge_data(self, health_data, environmental_data):
        """Merge health and environmental data on site_id + campaign."""
        merged = pd.merge(
            health_data,
            environmental_data,
            on=["site_id", "campaign"],
            how="inner",
        )
        return merged

    def correlate_kbi_environment(self, merged):
        """Correlate KBI with each environmental parameter."""
        env_cols = [c for c in merged.columns
                    if c in ["temperature_c", "salinity_psu", "ph", "turbidity_ntu"]]
        correlations = {}
        for col in env_cols:
            r, p = stats.pearsonr(merged["kbi"], merged[col])
            correlations[col] = {
                "correlation": round(r, 3),
                "p_value": round(p, 4),
                "significant": p < 0.05,
            }
        self.results["correlations"] = correlations
        return correlations

    def regression_kbi_environment(self, merged):
        """Multiple regression: KBI ~ env parameters (H3)."""
        env_cols = [c for c in merged.columns
                    if c in ["temperature_c", "salinity_psu", "ph", "turbidity_ntu"]]
        X = sm.add_constant(merged[env_cols])
        y = merged["kbi"]
        model = sm.OLS(y, X).fit()
        self.results["regression"] = {
            "r_squared": round(model.rsquared, 3),
            "adj_r_squared": round(model.rsquared_adj, 3),
            "f_statistic": round(model.fvalue, 3),
            "p_value": round(model.f_pvalue, 4),
            "coefficients": model.params.to_dict(),
        }
        return self.results["regression"]

    def test_h3(self, merged):
        """Test H3: environmental parameters significantly influence KBI."""
        r = self.regression_kbi_environment(merged)
        self.results["H3"] = {
            "supported": r["p_value"] < 0.05,
            "r_squared": r["r_squared"],
            "p_value": r["p_value"],
        }
        return self.results["H3"]

    def test_h4(self, integrated_results, individual_results):
        """Test H4: integrated framework > individual components."""
        diffs = []
        for key in integrated_results:
            diffs.append(integrated_results[key] - individual_results[key])
        t_stat, p_value = stats.ttest_1samp(diffs, 0)
        self.results["H4"] = {
            "supported": (p_value < 0.05 and np.mean(diffs) > 0),
            "t_statistic": round(t_stat, 3),
            "p_value": round(p_value, 4),
            "mean_improvement": round(np.mean(diffs), 4),
        }
        return self.results["H4"]

    def plot_correlation_matrix(self, merged, output_name="correlation_matrix"):
        """Plot correlation matrix of KBI vs env parameters."""
        cols = ["kbi"] + [c for c in merged.columns
                          if c in ["temperature_c", "salinity_psu", "ph", "turbidity_ntu"]]
        corr = merged[cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(len(cols)))
        ax.set_yticks(range(len(cols)))
        ax.set_xticklabels(cols, rotation=45, ha="right")
        ax.set_yticklabels(cols)
        for i in range(len(cols)):
            for j in range(len(cols)):
                ax.text(j, i, f"{corr.values[i, j]:.2f}",
                        ha="center", va="center", fontsize=9)
        plt.colorbar(im, ax=ax)
        plt.tight_layout()
        path = self.output_dir / f"{output_name}.png"
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        return str(path)


if __name__ == "__main__":
    print("Environmental Integration ready.")