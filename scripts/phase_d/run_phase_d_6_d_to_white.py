"""
D.6B — Relative D_to_White (Flow B).
"""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
from azrai.common.logging import phase_logger

def white_reference(img, mask):
    non_coral = img[mask == 0]
    if len(non_coral) == 0: return None
    gray = cv2.cvtColor(non_coral.reshape(-1, 1, 3), cv2.COLOR_BGR2GRAY).flatten()
    bright = non_coral[gray >= np.percentile(gray, 95)]
    return bright.mean(axis=0) if len(bright) > 0 else None

def compute_dwhite(img, mask, white_ref):
    coral_pixels = img[mask == 255]
    if len(coral_pixels) == 0: return None
    coral_lab = cv2.cvtColor(coral_pixels.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    white_lab = cv2.cvtColor(np.array([[white_ref]], dtype=np.uint8), cv2.COLOR_BGR2LAB)[0, 0]
    dists = np.linalg.norm(coral_lab.astype(float) - white_lab.astype(float), axis=1)
    return {"mean_d_to_white": float(dists.mean()), "std_d_to_white": float(dists.std())}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="results/phase_d/detections_index.json")
    parser.add_argument("--masks", default="results/phase_d/masks")
    parser.add_argument("--output", default="results/phase_d/dwhite")
    args = parser.parse_args()

    log = phase_logger("phase_d_6_d_to_white")
    log.info("=== D.6B — Relative D_to_White ===")

    index = json.loads(Path(args.index).read_text())
    masks_dir, out = Path(args.masks), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    total = 0
    for image_name, entry in index.items():
        img = cv2.imread(entry["path"])
        if img is None: continue
        for i in range(len(entry["colonies"])):
            mask_path = masks_dir / f"{Path(image_name).stem}_colony{i}.png"
            if not mask_path.exists(): continue
            mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            white_ref = white_reference(img, mask)
            if white_ref is None: continue
            result = compute_dwhite(img, mask, white_ref)
            if result:
                result.update({"image": image_name, "colony_index": i, "class": entry["colonies"][i]["class"]})
                (out / f"{Path(image_name).stem}_colony{i}.json").write_text(json.dumps(result, indent=2))
                total += 1

    log.info(f"✅ Wrote {total} D_to_White reports to {out}")

if __name__ == "__main__":
    main()