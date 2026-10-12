"""
Phase B.3 — Murky Water Handler Runner
Detects and classifies murky water for all coral images.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import pandas as pd
from tqdm import tqdm

from src.preprocessing.murky_water_handler import MurkyWaterHandler


def main():
    handler = MurkyWaterHandler()
    image_dir = Path("data/raw/test_images")
    output_csv = "results/murky/murky_scores.csv"

    image_files = sorted(image_dir.glob("*.jpg"))
    print(f"Processing {len(image_files)} images...")

    rows = []
    for img_path in tqdm(image_files):
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        score = handler.detect_murky_water(img)
        classification = handler.classify_murky_water(score)
        rows.append({
            "filename": img_path.name,
            "murky_score": round(score, 4),
            "classification": classification,
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)

    print(f"\n=== Murky Water Summary ===")
    print(f"  Total images: {len(df)}")
    print(f"  Mean murky score: {df['murky_score'].mean():.3f}")
    print(f"\n  Distribution:")
    print(df["classification"].value_counts())
    print(f"\n  Output: {output_csv}")


if __name__ == "__main__":
    main()