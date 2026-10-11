"""
Standard Monitoring Criteria

Develops and validates standard monitoring criteria for turbid
nearshore reef environments (Azr.AI Appendix P / K.4).
"""

from pathlib import Path
import json
import pandas as pd


class StandardMonitoringCriteria:
    """Defines and validates standard monitoring criteria."""

    def __init__(self, output_dir="standard_monitoring_criteria"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.criteria = {
            "Image Capture": [
                {"Parameter": "Resolution", "Standard": "≥ 20 MP", "Rationale": "Genera-level identification"},
                {"Parameter": "Altitude", "Standard": "1–2 m above substrate", "Rationale": "Consistent field of view"},
                {"Parameter": "Lighting", "Standard": "Dual strobes, 5000 lumen", "Rationale": "Reduce backscatter"},
                {"Parameter": "Colour Reference", "Standard": "CoralWatch chart", "Rationale": "Colour calibration"},
                {"Parameter": "Quadrat Area", "Standard": "50 m²", "Rationale": "Statistically significant"},
            ],
            "Video Capture": [
                {"Parameter": "Resolution", "Standard": "≥ 4K (3840×2160)", "Rationale": "Detection accuracy"},
                {"Parameter": "Frame Rate", "Standard": "≥ 30 fps", "Rationale": "Temporal resolution"},
                {"Parameter": "Duration", "Standard": "≥ 60 seconds per quadrat", "Rationale": "Adequate coverage"},
            ],
            "Environmental": [
                {"Parameter": "Temperature", "Standard": "30-min intervals", "Rationale": "Thermal stress detection"},
                {"Parameter": "Salinity", "Standard": "Per site visit", "Rationale": "Water mass characterisation"},
                {"Parameter": "pH", "Standard": "Per site visit", "Rationale": "Ocean acidification"},
                {"Parameter": "Turbidity", "Standard": "Per site visit", "Rationale": "Water clarity"},
            ],
            "Quality Control": [
                {"Parameter": "Sharpness", "Standard": "Laplacian variance > 100", "Rationale": "Image usability"},
                {"Parameter": "Colour Balance", "Standard": "Deviation < 0.3", "Rationale": "Colour calibration"},
                {"Parameter": "Visibility", "Standard": "> 3 m", "Rationale": "Coral detectability"},
                {"Parameter": "Murky Water", "Standard": "Score < 0.5", "Rationale": "Turbidity threshold"},
            ],
            "Detection": [
                {"Parameter": "mAP@50", "Standard": "> 85%", "Rationale": "Detection accuracy"},
                {"Parameter": "Precision", "Standard": "> 0.85", "Rationale": "Low false positives"},
                {"Parameter": "Recall", "Standard": "> 0.80", "Rationale": "Low false negatives"},
            ],
            "Health": [
                {"Parameter": "KBI Correlation", "Standard": "r > 0.80", "Rationale": "Health accuracy"},
                {"Parameter": "KBI MAE", "Standard": "< 0.10", "Rationale": "Low prediction error"},
            ],
            "Data Management": [
                {"Parameter": "Naming", "Standard": "{SiteID}_{Campaign}_{Quadrat}_{Number}", "Rationale": "Traceability"},
                {"Parameter": "Metadata", "Standard": "16 fields", "Rationale": "Context preservation"},
                {"Parameter": "Sharing", "Standard": "CC BY 4.0", "Rationale": "Open science"},
            ],
        }

    def generate_criteria_table(self):
        """Generate a combined criteria table."""
        rows = []
        for category, items in self.criteria.items():
            for item in items:
                rows.append({
                    "Category": category,
                    "Parameter": item["Parameter"],
                    "Standard": item["Standard"],
                    "Rationale": item["Rationale"],
                })
        return pd.DataFrame(rows)

    def validate_criteria(self, actual_data):
        """Validate criteria against actual data pass rates."""
        results = []
        if "image_resolution_mp" in actual_data.columns:
            passed = (actual_data["image_resolution_mp"] >= 20).mean() * 100
            results.append({"Criterion": "Resolution ≥ 20 MP", "Pass Rate": round(passed, 1)})
        if "sharpness" in actual_data.columns:
            passed = (actual_data["sharpness"] > 100).mean() * 100
            results.append({"Criterion": "Sharpness > 100", "Pass Rate": round(passed, 1)})
        if "murky_score" in actual_data.columns:
            passed = (actual_data["murky_score"] < 0.5).mean() * 100
            results.append({"Criterion": "Murky Water < 0.5", "Pass Rate": round(passed, 1)})
        return pd.DataFrame(results)

    def save_criteria(self, filename="criteria.json"):
        """Save criteria to JSON."""
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(self.criteria, f, indent=2)
        print(f"Criteria saved to {path}")
        return str(path)

    def generate_report(self, filename="criteria_table.csv"):
        """Generate full criteria report."""
        table = self.generate_criteria_table()
        path = self.output_dir / filename
        table.to_csv(path, index=False)
        print(f"Report saved to {path}")
        return str(path)


if __name__ == "__main__":
    criteria = StandardMonitoringCriteria()
    table = criteria.generate_criteria_table()
    print(table.to_string(index=False))
    criteria.save_criteria()
    criteria.generate_report()