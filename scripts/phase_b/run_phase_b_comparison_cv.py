"""
Phase B.6 (v2) - Enhancement Comparison using pure OpenCV
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import numpy as np

print("Script started")

from src.preprocessing.enhancement_metrics import EnhancementMetrics

print("Imports OK")


def add_label(img, text):
    """Adds a text banner to the top of an image."""
    banner = np.zeros((40, img.shape[1], 3), dtype=np.uint8)
    cv2.putText(banner, text, (10, 28), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    return np.vstack([banner, img])


def resize_to_width(img, width=600):
    """Resize image to a fixed width preserving aspect ratio."""
    h, w = img.shape[:2]
    new_h = int(h * width / w)
    return cv2.resize(img, (width, new_h))


def main():
    raw_dir = Path("data/raw/test_images")
    enh_dir = Path("data/processed/enhanced")
    output_dir = Path("results/enhancement")
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = sorted(raw_dir.glob("*.jpg"))
    print(f"Found {len(image_files)} raw images")

    if not image_files:
        print("No images found.")
        return

    sample_names = [
        image_files[0].name,
        image_files[len(image_files) // 2].name,
        image_files[-1].name,
    ]
    print(f"Samples: {sample_names}")

    top_row = []
    bottom_row = []

    for sample_name in sample_names:
        orig = cv2.imread(str(raw_dir / sample_name))
        enh = cv2.imread(str(enh_dir / sample_name.replace(".jpg", "_enhanced.jpg")))

        if orig is None or enh is None:
            print(f"Skipping {sample_name}")
            continue

        orig = resize_to_width(orig, 600)
        enh = resize_to_width(enh, 600)

        top_row.append(add_label(orig, f"Original: {sample_name}"))
        bottom_row.append(add_label(enh, f"Enhanced: {sample_name}"))

    max_h = max(img.shape[0] for img in top_row + bottom_row)
    top_row = [cv2.copyMakeBorder(img, 0, max_h - img.shape[0], 0, 0,
                                   cv2.BORDER_CONSTANT, value=(30, 30, 30))
               for img in top_row]
    bottom_row = [cv2.copyMakeBorder(img, 0, max_h - img.shape[0], 0, 0,
                                      cv2.BORDER_CONSTANT, value=(30, 30, 30))
                  for img in bottom_row]

    top = np.hstack(top_row)
    bottom = np.hstack(bottom_row)
    comparison = np.vstack([top, bottom])

    output_path = output_dir / "comparison.png"
    cv2.imwrite(str(output_path), comparison)
    print(f"Comparison saved to {output_path}")
    print(f"Image shape: {comparison.shape}")


if __name__ == "__main__":
    main()