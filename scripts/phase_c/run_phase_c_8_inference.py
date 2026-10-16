import sys
from ultralytics import YOLO
from pathlib import Path
from collections import Counter

if len(sys.argv) < 2:
    print("Usage: python analyze.py <image_folder>")
    sys.exit(1)

src = sys.argv[1]
model = YOLO(r"C:\Users\mazra\OneDrive - International Islamic University Malaysia\coral-data\models\trained\yolov8s_coral\best.pt")

results = model.predict(source=src, conf=0.25, save=False, verbose=False)

total_boxes = 0
class_counts = Counter()
conf_sum = 0.0
per_image = []

for r in results:
    names = r.names
    boxes = r.boxes
    n = len(boxes)
    total_boxes += n
    confs = boxes.conf.tolist() if n else []
    for c, cf in zip(boxes.cls.tolist(), confs):
        class_counts[names[int(c)]] += 1
        conf_sum += cf
    per_image.append((Path(r.path).name, n, sum(confs)/len(confs) if confs else 0.0))

avg_conf = conf_sum / total_boxes if total_boxes else 0.0
images_with_detections = sum(1 for _, n, _ in per_image if n > 0)

print(f"Source: {src}")
print(f"=== OUTPUT 1: Total images processed === {len(results)}")
print(f"=== OUTPUT 2: Total detections (boxes) === {total_boxes}")
print("=== OUTPUT 3: Per-class detection counts ===")
for cls, cnt in class_counts.most_common():
    print(f"  {cls}: {cnt}")
print(f"=== OUTPUT 4: Average confidence === {avg_conf:.4f}")
print(f"[Extra] Images with >=1 detection: {images_with_detections} / {len(results)}")
print("[Extra] Top-5 densest images:")
for name, n, ac in sorted(per_image, key=lambda x: -x[1])[:5]:
    print(f"  {name}: {n} boxes, avg conf {ac:.3f}")