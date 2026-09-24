"""
Disease Detection
Detects band disease, white disease, tip necrosis, and predation scars.
"""

import cv2
import numpy as np
from ultralytics import YOLO


class DiseaseDetector:
    def __init__(self, model_path='disease_detection_model.pt'):
        self.model = YOLO(model_path)

        self.disease_classes = {
            0: 'Band_Disease',
            1: 'White_Disease',
            2: 'Tip_Necrosis',
            3: 'Predation_Scars',
        }

    def detect(self, image_path, conf=0.5):
        """Detect diseases in image."""
        results = self.model.predict(
            source=image_path,
            conf=conf,
            verbose=False
        )

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()

                    detections.append({
                        'disease': self.disease_classes.get(cls, 'Unknown'),
                        'confidence': conf,
                        'bbox': bbox,
                    })

        return detections

    def calculate_prevalence(self, detections, total_colonies):
        """Calculate disease prevalence."""
        prevalence = {}
        for disease in self.disease_classes.values():
            count = sum(1 for d in detections if d['disease'] == disease)
            prevalence[disease] = (count / total_colonies) * 100

        return prevalence
