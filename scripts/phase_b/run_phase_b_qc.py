"""
Phase B.2 — Quality Control Runner
Assesses sharpness + colour balance for all coral images.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.preprocessing.quality_control import ImageQualityControl


def main():
    qc = ImageQualityControl(
        sharpness_threshold=100,
        colour_balance_threshold=0.3,
    )

    image_dir = "data/raw/test_images"
    output_csv = "results/qc/qc_results.csv"

    print(f"Running QC on images in {image_dir}")
    df = qc.process_batch(image_dir, output_csv)

    print(f"\n=== QC Summary ===")
    print(f"  Total images: {len(df)}")
    print(f"  Pass rate: {df['pass'].mean() * 100:.1f}%")
    print(f"  Mean sharpness: {df['sharpness'].mean():.1f}")
    print(f"  Mean colour balance: {df['colour_balance'].mean():.3f}")
    print(f"  Output: {output_csv}")


if __name__ == "__main__":
    main()