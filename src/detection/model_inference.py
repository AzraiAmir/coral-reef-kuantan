"""
Model Inference
Run inference on new images.
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from tqdm import tqdm
import json


class ModelInference:
    def __init__(self, model_path, class_names=None):
        self.model = YOLO(model_path)
        self.class_names = class_names or self.model.names

    def predict_single(self, image_path, conf=0.5, iou=0.45):
        """Run inference on a single image."""
        results = self.model.predict(
            source=str(image_path),
            conf=conf,
            iou=iou,
            verbose=False
        )

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()

                    detections.append({
                        'class': self.class_names.get(cls, f'class_{cls}'),
                        'class_id': cls,
                        'confidence': confidence,
                        'bbox': bbox,
                    })

        return detections

    def predict_batch(self, image_dir, output_json, conf=0.5):
        """Run inference on a batch of images."""
        image_dir = Path(image_dir)
        image_paths = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))

        all_results = {}

        for img_path in tqdm(image_paths, desc="Running inference"):
            detections = self.predict_single(img_path, conf=conf)
            all_results[img_path.name] = detections

        # Save results
        with open(output_json, 'w') as f:
            json.dump(all_results, f, indent=2)

        print(f"Results saved to {output_json}")
        return all_results

    def predict_with_visualization(self, image_path, output_dir, conf=0.5):
        """Run inference and save annotated image."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = self.model.predict(
            source=str(image_path),
            conf=conf,
            save=True,
            save_dir=str(output_dir),
            verbose=False
        )

        return results


if __name__ == "__main__":
    inference = ModelInference('models/trained/yolov8_coral_best.pt')
    results = inference.predict_single('test_images/coral_sample.jpg')
    print(f"Detections: {len(results)}")
