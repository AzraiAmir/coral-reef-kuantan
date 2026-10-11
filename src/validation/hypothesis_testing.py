"""
Hypothesis Testing

Formal hypothesis testing for H1–H4 of the Azr.AI framework.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm


class HypothesisTesting:
    """Tests H1–H4 hypotheses for Azr.AI framework evaluation."""

    def __init__(self, output_dir="hypothesis_testing"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {}

    def test_h1_detection_performance(self, map_values, threshold=0.85):
        """H1: Detection model achieves mAP@50 > 0.85."""
        m = np.array(map_values)
        t_stat, p_value = stats.ttest_1samp(m, threshold, alternative="greater")
        self.results["H1"] = {
            "hypothesis": "Detection model achieves mAP@50 > 85%",
            "mean_map50": round(float(m.mean()), 4),
            "threshold": threshold,
            "t_statistic": round(float(t_stat), 4),
            "p_value": round(float(p_value), 4),
            "supported": bool(p_value < 0.05 and m.mean() > threshold),
        }
        return self.results["H1"]

    def test_h2_kbi_correlation(self, automated_kbi, expert_kbi, threshold=0.80):
        """H2: KBI correlates > 0.80 with expert assessment."""
        r, p_value = stats.pearsonr(automated_kbi, expert_kbi)
        self.results["H2"] = {
            "hypothesis": "KBI correlates with expert assessment (r > 0.80)",
            "correlation": round(float(r), 4),
            "p_value": round(float(p_value), 6),
            "threshold": threshold,
            "supported": bool(r > threshold and p_value < 0.05),
        }
        return self.results["H2"]

    def test_h3_environmental_correlation(self, kbi_values, env_data):
        """H3: Environmental parameters significantly influence KBI."""
        env_cols = env_data.columns.tolist()
        X = sm.add_constant(env_data)
        y = pd.Series(kbi_values)
        model = sm.OLS(y, X).fit()
        self.results["H3"] = {
            "hypothesis": "Environmental parameters influence KBI",
            "r_squared": round(float(model.rsquared), 4),
            "f_statistic": round(float(model.fvalue), 4),
            "p_value": round(float(model.f_pvalue), 6),
            "supported": bool(model.f_pvalue < 0.05),
        }
        return self.results["H3"]

    def test_h4_integrated_framework(self, integrated, individual):
        """H4: Integrated framework > individual components."""
        diffs = [integrated[k] - individual[k] for k in integrated]
        t_stat, p_value = stats.ttest_1samp(diffs, 0)
        self.results["H4"] = {
            "hypothesis": "Integrated framework provides better assessment",
            "mean_improvement": round(float(np.mean(diffs)), 4),
            "t_statistic": round(float(t_stat), 4),
            "p_value": round(float(p_value), 4),
            "supported": bool(p_value < 0.05 and np.mean(diffs) > 0),
        }
        return self.results["H4"]

    def generate_summary_table(self):
        """Generate summary of all hypothesis tests."""
        rows = []
        for key, res in self.results.items():
            rows.append({
                "Hypothesis": key,
                "Description": res["hypothesis"],
                "Supported": "Yes" if res["supported"] else "No",
                "p_value": res.get("p_value", "—"),
            })
        return pd.DataFrame(rows)

    def save_results(self, filename="hypothesis_results.json"):
        """Save all hypothesis results to JSON."""
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"Results saved to {path}")


if __name__ == "__main__":
    ht = HypothesisTesting()
    print("Hypothesis Testing module ready.")