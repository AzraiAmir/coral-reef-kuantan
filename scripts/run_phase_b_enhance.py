"""
Phase B.4 — Traditional Enhancement Runner
Applies RCC + Gray-World + CLAHE to all coral images.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
from tqdm import tqdm

from src.preprocessing.traditional_enhancement import TraditionalEnhancer


def main():
    enhancer = TraditionalEnhancer(clip_limit=2.5, tile_grid_size=(8, 8))

    image_dir = Path("data/raw/test_images")
    output_dir = Path("data/processed/enhanced")
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = sorted(image_dir.glob("*.jpg"))
    print(f"Enhancing {len(image_files)} images...")

    success = 0
    for img_path in tqdm(image_files):
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        enhanced = enhancer.enhance(img)
        out_path = output_dir / img_path.name.replace(".jpg", "_enhanced.jpg")
        cv2.imwrite(str(out_path), enhanced)
        success += 1

    print(f"\n=== Enhancement Summary ===")
    print(f"  Images enhanced: {success}/{len(image_files)}")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    main()