"""
D.3B — Segment coral colonies (Flow B: bounding-box masks).
"""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
from azrai.common.logging import phase_logger

def bbox_mask(shape, bbox):
    h, w = shape[:2]
    x1, y1, x2, y2 = [int(v) for v in bbox]
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[max(0, y1):min(h, y2), max(0, x1):min(w, x2)] = 255
    return mask

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="results/phase_d/detections_index.json")
    parser.add_argument("--output-dir", default="results/phase_d/masks")
    args = parser.parse_args()

    log = phase_logger("phase_d_3_segment_coral")
    log.info("=== D.3B — Segment coral (bbox masks) ===")

    index = json.loads(Path(args.index).read_text())
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    total = 0
    for image_name, entry in index.items():
        img = cv2.imread(entry["path"])
        if img is None: continue
        for i, colony in enumerate(entry["colonies"]):
            mask = bbox_mask(img.shape, colony["bbox"])
            cv2.imwrite(str(out / f"{Path(image_name).stem}_colony{i}.png"), mask)
            total += 1

    log.info(f"✅ Wrote {total} masks to {out}")

if __name__ == "__main__":
    main()