"""
YOLOv8-Based Multi-Label Detection Model
For coral species, morphological growth forms, and anthropogenic debris.
"""

import torch
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import yaml
from datetime import datetime


class CoralDetectionModel:
    def __init__(self, model_size='m', num_classes=10, device='cuda'):
        self.model_size = model_size
        self.num_classes = num_classes
        self.device = device

        self.model = YOLO(f'yolov8{model_size}.pt')

        self.class_names = {
            0: 'Porites_massive',
            1: 'Porites_branching',
            2: 'Acropora_branching',
            3: 'Acropora_tabulate',
            4: 'Montipora_encrusting',
            5: 'Montipora_foliose',
            6: 'Bleached_coral',
            7: 'Dead_coral',
            8: 'Anthropogenic_debris',
            9: 'Disease_lesion'
        }

    def create_dataset_yaml(self, train_path, val_path, output_path='coral_dataset.yaml'):
        """Create YOLO dataset configuration file."""
        dataset_config = {
            'path': str(Path(train_path).parent),
            'train': str(train_path),
            'val': str(val_path),
            'nc': self.num_classes,
            'names': {i: name for i, name in self.class_names.items()}
        }

        with open(output_path, 'w') as f:
            yaml.dump(dataset_config, f, default_flow_style=False)

        print(f"Dataset configuration saved to {output_path}")
        return output_path

    def train(self, data_yaml, epochs=300, imgsz=640, batch=16,
              patience=100, project='coral_detection', name='yolov8_coral'):
        """Train the YOLOv8 model on coral dataset."""
        print(f"Starting training for {epochs} epochs...")

        results = self.model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=patience,
            project=project,
            name=name,
            device=self.device,
            optimizer='Adam',
            lr0=0.001,
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3,
            box=7.5,
            cls=0.5,
            dfl=1.5,
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=15.0,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.5,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0,
            copy_paste=0.0,
            save=True,
            save_period=10,
            val=True,
            verbose=True,
        )

        print("Training complete!")
        return results

    def validate(self, data_yaml, model_path=None):
        """Validate the trained model."""
        if model_path:
            self.model = YOLO(model_path)

        metrics = self.model.val(data=data_yaml)

        print("\nValidation Results:")
        print(f"  mAP@50: {metrics.box.map50:.4f}")
        print(f"  mAP@50-95: {metrics.box.map:.4f}")
        print(f"  Precision: {metrics.box.mp:.4f}")
        print(f"  Recall: {metrics.box.mr:.4f}")

        return metrics

    def predict(self, image_path, conf=0.5, iou=0.45, save=False, save_dir='predictions'):
        """Run inference on a single image or directory."""
        results = self.model.predict(
            source=image_path,
            conf=conf,
            iou=iou,
            save=save,
            save_dir=save_dir,
            device=self.device,
            verbose=False
        )
        return results
