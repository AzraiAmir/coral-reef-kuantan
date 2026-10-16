"""
Data Loader Runner — Verify images load correctly and generate filename labels
"""

from pathlib import Path
import pandas as pd
from src.data_acquisition.data_loader import CoralDataLoader


def main():
    # Initialize loader
    loader = CoralDataLoader(data_dir="data")

    # Load images
    print("Loading images...")
    images, paths = loader.load_images("data/raw/test_images")
    print(f"Loaded {len(images)} images")

    # Check image dimensions
    if images:
        dims = [(img.shape[1], img.shape[0]) for img in images[:5]]
        print(f"Sample dimensions (first 5, WxH): {dims}")

    # Generate annotation CSV from filenames
    print("\nGenerating filename labels CSV...")
    rows = []
    for p in sorted(Path("data/raw/test_images").glob("*.jpg")):
        parts = p.stem.split("_")
        species = parts[2] if len(parts) > 2 else "UNK"
        rows.append({"filename": p.name, "label": species})

    df = pd.DataFrame(rows)
    out_path = Path("data/annotations/filename_labels.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")

    # Final verification
    print("\n=== Data Loader Verification ===")
    print(f"  Images loaded: {len(images)}")
    print(f"  Paths collected: {len(paths)}")
    print(f"  Status: {'OK' if len(images) == 131 else 'MISMATCH'}")


if __name__ == "__main__":
    main()