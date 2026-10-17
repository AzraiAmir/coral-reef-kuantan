"""
D.4B — Relative colour analysis (Flow B).
"""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
from azrai.common.logging import phase_logger

def analyse_colony(img, mask):
    coral_pixels = img[mask == 255]
    if len(coral_pixels) == 0: return None
    mean_bgr = coral_pixels.mean(axis=0).tolist()
    hsv_pixels = cv2.cvtColor(coral_pixels.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    mean_hsv = hsv_pixels.mean(axis=0).tolist()
    return {
        "mean_bgr": mean_bgr,
        "mean_hsv": mean_hsv,
        "paleness": round(float(mean_hsv[2] / 255.0), 4),
        "pixel_count": int(len(coral_pixels)),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="results/phase_d/detections_index.json")
    parser.add_argument("--masks", default="results/phase_d/masks")
    parser.add_argument("--output", default="results/phase_d/crca")
    args = parser.parse_args()

    log = phase_logger("phase_d_4_coral_crca")
    log.info("=== D.4B — Relative colour analysis ===")

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
            result = analyse_colony(img, mask)
            if result:
                result.update({"image": image_name, "colony_index": i, "class": entry["colonies"][i]["class"]})
                (out / f"{Path(image_name).stem}_colony{i}.json").write_text(json.dumps(result, indent=2))
                total += 1

    log.info(f"✅ Wrote {total} colour reports to {out}")

if __name__ == "__main__":
    main()