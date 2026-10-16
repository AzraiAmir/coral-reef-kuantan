"""
Phase B.5 — Enhancement Metrics Runner
Calculates UCIQE and UIQM for original vs enhanced images.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import pandas as pd
from tqdm import tqdm

from src.preprocessing.enhancement_metrics import EnhancementMetrics


def main():
    metrics = EnhancementMetrics()
    raw_dir = Path("data/raw/test_images")
    enh_dir = Path("data/processed/enhanced")
    output_csv = "results/enhancement/metrics.csv"

    image_files = sorted(raw_dir.glob("*.jpg"))
    print(f"Computing metrics for {len(image_files)} pairs...")

    rows = []
    for orig_path in tqdm(image_files):
        enh_path = enh_dir / orig_path.name.replace(".jpg", "_enhanced.jpg")
        if not enh_path.exists():
            continue

        orig = cv2.imread(str(orig_path))
        enh = cv2.imread(str(enh_path))

        rows.append({
            "filename": orig_path.name,
            "uciqe_original": round(metrics.calculate_uciqe(orig), 3),
            "uciqe_enhanced": round(metrics.calculate_uciqe(enh), 3),
            "uiqm_original": round(metrics.calculate_uiqm(orig), 3),
            "uiqm_enhanced": round(metrics.calculate_uiqm(enh), 3),
        })

    df = pd.DataFrame(rows)
    df["uciqe_improvement"] = df["uciqe_enhanced"] - df["uciqe_original"]
    df["uiqm_improvement"] = df["uiqm_enhanced"] - df["uiqm_original"]
    df.to_csv(output_csv, index=False)

    print(f"\n=== Enhancement Metrics Summary ===")
    print(f"  Pairs analysed: {len(df)}")
    print(f"  Mean UCIQE original: {df['uciqe_original'].mean():.3f}")
    print(f"  Mean UCIQE enhanced: {df['uciqe_enhanced'].mean():.3f}")
    print(f"  Mean UCIQE improvement: {df['uciqe_improvement'].mean():+.3f}")
    print(f"  Mean UIQM original: {df['uiqm_original'].mean():.3f}")
    print(f"  Mean UIQM enhanced: {df['uiqm_enhanced'].mean():.3f}")
    print(f"  Mean UIQM improvement: {df['uiqm_improvement'].mean():+.3f}")
    print(f"  Output: {output_csv}")


if __name__ == "__main__":
    main()