"""
D.1 — Load Phase C detections into a structured index.
"""
import argparse
import json
from pathlib import Path
from ultralytics import YOLO
from azrai.common.logging import phase_logger

DEFAULT_WEIGHTS = Path(r"C:\Users\mazra\OneDrive - International Islamic University Malaysia\coral-data\models\trained\yolov8s_coral\best.pt")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="runs/detect/predict")
    parser.add_argument("--weights", default=str(DEFAULT_WEIGHTS))
    parser.add_argument("--output", default="results/phase_d/detections_index.json")
    parser.add_argument("--conf", type=float, default=0.40)
    args = parser.parse_args()

    log = phase_logger("phase_d_1_load_detections")
    log.info("=== D.1 — Load Phase C detections ===")

    model = YOLO(str(args.weights))
    source = Path(args.source)
    image_files = sorted(source.glob("*.jpg")) + sorted(source.glob("*.png"))
    
    index = {}
    total_colonies = 0
    for i, img_path in enumerate(image_files, 1):
        results = model.predict(source=str(img_path), conf=args.conf, verbose=False)
        colonies = []
        for r in results:
            for box in r.boxes:
                colonies.append({
                    "bbox": [float(x) for x in box.xyxy[0].tolist()],
                    "class": r.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                })
        index[img_path.name] = {"path": str(img_path.resolve()), "colonies": colonies}
        total_colonies += len(colonies)
        if i % 20 == 0 or i == len(image_files):
            log.info(f"  processed {i}/{len(image_files)}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, indent=2))
    log.info(f"Indexed {total_colonies} colonies across {len(image_files)} images")
    log.info(f"✅ Written to {out}")

if __name__ == "__main__":
    main()